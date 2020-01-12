from mscraper import Mscraper
from selenium.webdriver.common.keys import Keys
from os import environ
import time
import random
import pickle

class Google(Mscraper):

    def __init__(self):
        super().__init__(website='https://www.google.com')

        self.query_string = ''

    def google_it(self):
        search_box = self.driver.find_element_by_name('q')
        search_box.clear()
        search_box.send_keys(self.query_string)
        search_box.submit()
        self.query_string = ''

    def look_for(self, *keywords):
        self.query_string += ' '
        for keyword in keywords:
            self.query_string += keyword
            self.query_string += ' '

    def exclude(self, *keywords):
        self.query_string += ' '
        for keyword in keywords:
            self.query_string += '-' + keyword
            self.query_string += ' '

    def from_website(self, website):
        self.query_string = "site:" + website + " " +  self.query_string

    def must_include(self, *keywords):
        self.query_string += ' '
        for keyword in keywords:
            self.query_string += '"' + keyword + '"'
            self.query_string += ' '

    def go_to_next_page(self):
        self.driver.find_element_by_id("pnnext").click()

    def go_back(self):
        self.driver.back()

    def get_first_n_links(self, n=1, save_to_file=False, the_filename="links.txt"):
        assert(isinstance(n, int))
        n_links_per_page = 10
        links = []

        while n > 0:
            web_els = self.driver.find_elements_by_css_selector('div.g')

            if (n < n_links_per_page):
                web_els = web_els[:n]

            for el in web_els:
                links.append(el.find_element_by_tag_name("a").get_attribute("href"))
            n = n - n_links_per_page
            self.go_to_next_page()
            print("n", n)
            print("links", links)
            time.sleep(random.uniform(0.5, 1))

        if save_to_file:
            with open(the_filename, 'wb') as f: # erasing existing text
                pickle.dump(links, f)

        return links
