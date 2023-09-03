import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class web_scrapper(webdriver.Chrome):
    def __init__(self):
        options = self.config_options()
        service = Service()

        super().__init__(options=options, service=service)

    def config_options(self):
        x = os.getcwd()
        o = Options()
        o.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0')
        o.add_argument('--start-maximized')
        o.add_argument('--disable-web-security')
        o.add_argument('--disable-notifications')
        o.add_argument('--ignore-certificate-errors')
        o.add_argument('--no-sandbox')
        o.add_argument('--log-level=3')
        o.add_argument('--no-default-browser-check')
        o.add_argument('--no-first-run')
        o.add_argument('--no-proxy-server')
        o.add_argument('--disable-blink-features=AutomationControlled')

        exp_options = ['enable-automation',
                       'ignore-certificate-errors',
                       'enable-logging']

        prefs = {'profile.default_content_setting_values.notifications': 2,
                 'credentials_enable_service': False,
                 'download.default_directory': x}

        o.add_experimental_option('excludeSwitches', exp_options)
        o.add_experimental_option('prefs', prefs)

        return o

    def check_download(self):
        ANIMATION_CHARS = ['|', '/', '-', '\\']

        while True:
            for char in ANIMATION_CHARS:
                print(f'\rDownloading  ({char})  ', end='')
                time.sleep(0.15)

            for f in os.listdir():
                if 'crdownload' in f:
                    break

            else:
                print('Download completed')
                return
            
class Binance(web_scrapper):
    def __init__(self):
        super().__init__()
        