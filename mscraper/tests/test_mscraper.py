# pytest tests/test_mscraper.py -s
import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import sys
sys.path.append('../mscraper/')
from mscraper import Mscraper


class TestMscraper(unittest.TestCase):

    def test_basic_setup(self):

        ls = Mscraper(website='https://duckduckgo.com')

        html = ls.get_this_html()
        self.assertIn("DuckDuckGo — Privacy, simplified", html.text)
        ls.driver.quit()

    def test_instances_move(self):

        ls = Mscraper(website='https://google.com')
        ls2 = Mscraper(scraperInstance = ls, website='https://duckduckgo.com')
        ls3 = Mscraper(website='https://duckduckgo.com')

        self.assertEqual(ls.driver.session_id, ls2.driver.session_id)
        self.assertNotEqual(ls.driver.session_id, ls3.driver.session_id)

        ls.driver.quit()
        ls2.driver.quit()
        ls3.driver.quit()

    def test_enter_quit(self):

        with Mscraper() as ms:
            print("OK")
