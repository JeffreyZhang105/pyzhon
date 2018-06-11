from crawlers import settings

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_path = 'bin\chromedriver.exe'


def create_chrome_driver():
	chrome_options = Options()
	for setting in settings.DEFAULT_REQUEST_HEADERS:
		chrome_options.add_argument(''.join((setting, '="', settings.DEFAULT_REQUEST_HEADERS[setting], '"')))

	chrome = webdriver.Chrome(executable_path=chrome_path, chrome_options=chrome_options)
	chrome.fullscreen_window()
	return chrome
