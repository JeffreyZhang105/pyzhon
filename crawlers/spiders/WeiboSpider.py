# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import FormRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import config
from utils import crawler_util


class WeiboSpider(scrapy.Spider):
	name = 'WeiboSpider'
	allowed_domains = ['weibo.com', ]

	weibo_url = 'https://weibo.com'

	def login(self, url):
		"""Log in and get cookies.
		"""
		chrome = crawler_util.create_chrome_driver()
		chrome.get(self.weibo_url)
		login_name_xpath = '//input[@id="loginname"]'
		WebDriverWait(chrome, 10).until(expected_conditions.presence_of_element_located((By.XPATH, '//input[@id="loginname"]')))

		chrome.find_element_by_xpath(login_name_xpath).send_keys(config.weibo_user_name)
		chrome.find_element_by_name('password').send_keys(config.weibo_password)
		chrome.find_element_by_xpath('//input[@id="loginname"]').click()

		return chrome.get_cookies()

	def start_requests(self):
		cookies = self.login(self.weibo_url)

		return [FormRequest(
			self.weibo_url,
			method='GET',
			cookies=cookies,
			callback=self.logged_in
		)]

	def parse(self, response):
		pass

	def logged_in(self, response):
		print(response.body)
