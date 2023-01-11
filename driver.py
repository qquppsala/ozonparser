from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent


# Simple function to create  webdriver
# Default UserAgent browser in header is "chrome", could be specified
# from following ["chrome", "edge", "internet explorer", "firefox", "safari", "opera"]
# for more information check https://github.com/fake-useragent/fake-useragent

# Also webdriver-manager is used
# for more information check https://github.com/SergeyPirogov/webdriver_manager
def make_driver(ua_browser="chrome"):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--disable-blink-features")  # required to avoid captcha
    options.add_argument("--disable-blink-features=AutomationControlled")  # required to avoid captcha
    options.add_argument(f'user-agent ={UserAgent(browsers=[ua_browser]).random}')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver
