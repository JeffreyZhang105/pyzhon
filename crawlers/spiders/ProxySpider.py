# -*- coding: utf-8 -*-

import scrapy

from crawlers.ProxyLoader import ProxyLoader
from crawlers.items import ProxyItem


class ProxySpider(scrapy.Spider):
	name = "ProxySpider"

	start_urls = ["https://www.us-proxy.org/", ]

	def parse(self, response):
		for row in response.selector.xpath("//table/tbody/tr"):
			loader = ProxyLoader(ProxyItem(), row)
			loader.add_xpath("ip_address", "./td[1]/text()")
			loader.add_xpath("port_number", "./td[2]/text()")
			loader.add_xpath("is_https", "./td[7]/text()")
			yield loader.load_item()
