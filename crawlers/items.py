# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProxyItem(scrapy.Item):
	ip_address = scrapy.Field()
	port_number = scrapy.Field()
	is_https = scrapy.Field()
