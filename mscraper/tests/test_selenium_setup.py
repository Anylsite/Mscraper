# pytest tests/test_selenium_setup.py -s
# pytest -k test_Chrome_version -s

import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import pkg_resources


class TestSeleniumSetup(unittest.TestCase):


    def test_Chrome_version(self):

        chromedriver_binary_version = pkg_resources.get_distribution("chromedriver_binary").version

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options = chrome_options)

        cap = driver.capabilities
        print("driver.capabilities", cap)

        self.assertEqual(chromedriver_binary_version,"79.0.3945.36.0")
        self.assertEqual(cap["chrome"]["chromedriverVersion"][:12],"79.0.3945.36")
        self.assertEqual(cap["browserVersion"],"79.0.3945.88")
        self.assertEqual(cap["browserName"], 'chrome')

    def test_basic_setup(self):

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("window-size=1400,2100")
        chrome_options.add_argument('--disable-gpu')

        driver = webdriver.Chrome(options = chrome_options)
        driver.get('https://duckduckgo.com')


        search_box = driver.find_element_by_xpath("//input[@name='q']")
        search_box.send_keys('wikipedia')
        search_box.submit()

        results = driver.find_elements_by_class_name('result')
        print(results[0].text)
        self.assertIn("en.wikipedia.org", results[0].text)
        driver.quit()
