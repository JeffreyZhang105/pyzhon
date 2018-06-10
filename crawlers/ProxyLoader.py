# -*- coding: utf-8 -*-

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose


class ProxyLoader(ItemLoader):
	proxyOutput_out = MapCompose()
