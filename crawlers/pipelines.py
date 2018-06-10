# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import requests

__USERAGENT = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0'
}


def check_proxy(proxy_item):
	ip_address = proxy_item["ip_address"][0]
	port_number = proxy_item["port_number"][0]
	is_https = proxy_item["is_https"][0]
	proxy = {
		"http": "" if is_https == "yes" else "".join(("http://", ip_address, ":", port_number)),
		"https": "".join(("https://", ip_address, ":", port_number)) if is_https == "yes" else ""
	}
	return requests.get("https://www.google.com", proxies=proxy, headers=__USERAGENT).status_code == requests.codes.ok


class ProxyPipline(object):
	def open_spider(self, spider):
		self.file = open("proxy_list.jl", "w")

	def close_spider(self, spider):
		self.file.close()

	def process_item(self, item, spider):
		if check_proxy(item):
			line = json.dumps(item) + "\n"
			self.file.write(line)
			return item
