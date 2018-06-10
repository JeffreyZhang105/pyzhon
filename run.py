# -*- coding: utf-8 -*-

from ProxyGetter import ProxyGetter
from scrapy import cmdline

if __name__ == "__main__":
	#ProxyGetter.get_proxy()

	cmdline.execute("scrapy crawl WeiboSpider".split())