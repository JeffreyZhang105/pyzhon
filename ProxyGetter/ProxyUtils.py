# -*- coding: utf-8 -*-
"""
Proxy Utils
"""

import logging

import requests

import ProxyGetter


def check_proxy(target):
	""" Checks if a proxy is usable.

	:param target: set of proxy to check.
	:return: True(if usable) or False(if not)
	"""
	result = False
	try:
		logging.info(''.join(['Testing proxy: ', str(target), '...']))
		request = requests.get("https://www.google.com.hk", proxies=target, headers=ProxyGetter.HEADERS)
		try:
			if requests.codes.ok == request.status_code:
				result = True
		except Exception as ex:
			logging.info('Failed. ' + str(ex))
	finally:
		return result
