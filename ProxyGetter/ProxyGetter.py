# -*- coding: utf-8 -*-
"""
Proxy Getter
"""

import json
import logging
import random
import re
import threading

import requests

import ProxyGetter
from ProxyGetter import ProxyUtils

__PROXY_SITES = [
	'https://www.us-proxy.org/',
	'https://free-proxy-list.net/'
]

__PROXIES_CHECK_THREAD_COUNT = 5;

__RG_TR = re.compile(r'<tr[^>]*>(?:.|\n)*?</tr>')
__RG_IP = re.compile(r'(<td[^>]*>)((\d{2,3}\.){3}\d{2,3})')
__RG_PORT = re.compile(r'(<td[^>]*>)(\d+)</td>')
__RG_HEAD = re.compile(r'(<thead[^>]*>)(<tr[^>]*>.*?</tr>)')
__RG_TH = re.compile(r'<th[^>]*>.*?</th>')
__RG_TD = re.compile(r'(<td[^>]*>)(.*?)</td>')

__CACHE = {}
__POOL_LOCKER = threading.Lock()
__EVENT_FIRST_PROXY_FOUND = threading.Event()
__EVENT_PROXY_CHECK_FINISHED = threading.Event()


def __check_proxies_and_update_pool(targets):
	"""Updates POOL.
	When finds a usable proxy for the first time, sets the event for other method(if any) to get value.
	"""
	for proxy in targets:
		if ProxyUtils.check_proxy(proxy):
			try:
				__POOL_LOCKER.acquire()
				if proxy not in __CACHE:
					__CACHE.append(proxy)
					logging.info('Fond usable proxy: %s, appending to POOL.' % proxy)

					if len(__CACHE) == 1 and not __EVENT_FIRST_PROXY_FOUND.isSet():
						__EVENT_FIRST_PROXY_FOUND.set()
			finally:
				__POOL_LOCKER.release()


def __get_proxies(from_url):
	"""Gets proxies from indicated url .
	"""
	try:
		response = requests.get(from_url, proxies=random.sample(__CACHE, 1)[0] if __CACHE else None, headers=ProxyGetter.HEADERS)
	except Exception as ex:
		logging.error(''.join(['ERROR attempting get proxy from: ', from_url, '\r\nmessage: ', str(ex)]))
		return
	text = re.sub(r'\s', '', response.text)
	thread = __RG_HEAD.findall(text)[0][1]
	ths = __RG_TH.findall(thread)
	protocol_index = -1
	for th in ths:
		if th.lower().find('https') >= 0:
			protocol_index = ths.index(th)
			break

	trs = __RG_TR.findall(text)
	proxies_found = []
	for tr in trs:
		is_https = False
		if __RG_PORT.findall(tr) and __RG_IP.findall(tr):
			if protocol_index > -1 and __RG_TD.findall(tr)[protocol_index][1] == 'yes':
				is_https = True

			ip_port = ''.join((__RG_IP.findall(tr)[0][1], ':', __RG_PORT.findall(tr)[0][1]))
			proxies_found.append({
				'http': '' if is_https else ''.join(('http://', ip_port)),
				'https': ''.join(('https://', ip_port)) if is_https else ''
			})
	return proxies_found


def __update_pool(raw_proxies):
	threadCount = __PROXIES_CHECK_THREAD_COUNT
	perthread = int(len(raw_proxies) / threadCount)
	for proxy_page in [raw_proxies[threadNum * perthread::(threadNum + 1) * perthread - 1] for threadNum in range(threadCount)]:
		threading.Thread(target=__check_proxies_and_update_pool, args=(proxy_page,)).start()

	if not __EVENT_PROXY_CHECK_FINISHED.isSet():
		__EVENT_PROXY_CHECK_FINISHED.set()


def __write_pool_after_check_finish():
	__EVENT_PROXY_CHECK_FINISHED.wait()
	if __CACHE:
		with open(ProxyGetter.Pool_FileName, "w") as pool_file:
			json.dump(__CACHE, pool_file)


def get_proxy():
	""" Gets a set of proxies.
	:return: a set of proxies, e.g. {'http':'http://xxxxxx','https':"https://xxxxxx'}
	"""
	result = None

	with open(ProxyGetter.Pool_FileName, "r") as pool_file:
		__CACHE = json.load(pool_file)

	while __CACHE and not result:
		temp = random.sample(__CACHE, 1)[0]
		if ProxyUtils.check_proxy(temp):
			result = temp
			break
		else:
			__CACHE.remove(temp)

	# No usable proxy in POOL, start threads to get proxies and wait for the first result.
	if not result and not __CACHE:
		for url in __PROXY_SITES:
			proxies = __get_proxies(url)
			threading.Thread(target=__update_pool, args=(proxies,)).start()
			threading.Thread(target=__write_pool_after_check_finish).start()

	__EVENT_FIRST_PROXY_FOUND.wait()
	result = __CACHE[0]
	return result
