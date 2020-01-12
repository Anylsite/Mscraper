import unittest
import sys
sys.path.append('../mscraper/')
from google_scraper import Google
import pickle
import os


class TestGooglescraper(unittest.TestCase):

    def test_basic_setup(self):

        ls = Google()
        html = ls.get_this_html()
        self.assertIn("window.google", html.text)

        ls.look_for("karl", "schwarzschild")
        ls.google_it()
        html = ls.get_this_html()
        self.assertIn("physicist", html.text)

        ls.driver.quit()

    def test_advanced_search_functions(self):
        ls = Google()

        ls.look_for("cat", "dog")
        ls.exclude("mouse", "giraffe")
        ls.from_website("wikipedia.com")
        ls.must_include("race")
        self.assertEqual(
            ls.query_string, 'site:wikipedia.com  cat dog  -mouse -giraffe  "race" ')

        ls.google_it()

        links = ls.get_first_n_links(n=2)
        self.assertEqual(len(links), 2)

        links = ls.get_first_n_links(n=12)
        self.assertEqual(len(links), 12)
        self.assertEqual(len(set(links)), 12)

        ls.driver.quit()

    def test_save_and_read_links_from_file(self):

        links = ['https://de.linkedin.com/in/berlinjessica', 'https://de.linkedin.com/in/berlinjessica/zh-cn', 'https://de.linkedin.com/in/hessamlavi']
        the_filename = "links.txt"
        with open(the_filename, 'wb') as f:
            pickle.dump(links, f)

        with open(the_filename, 'rb') as f:
            restored_list = pickle.load(f)

        print(restored_list)
        self.assertTrue(restored_list.sort() == links.sort())
        os.remove(the_filename)
