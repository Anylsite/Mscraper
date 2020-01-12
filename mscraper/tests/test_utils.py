# pytest tests/test_linkedin_scraper.py -s
import sys
sys.path.append('../mscraper/')
from os import path
from bs4 import BeautifulSoup as BS
import bs4
import utils as u
import unittest


class TestUtils(unittest.TestCase):

    def test_utils_basics(self):

        file_path = path.abspath(__file__)
        DIR = path.dirname(file_path)

        with open(path.join(DIR, 'html_files/profile.html'), 'r') as f1, open(path.join(DIR, 'test.html'), 'r') as f2:
            profile_soup = BS(f1.read(), 'html.parser')
            basic_soup = BS(f2.read(), 'html.parser')

        def test_split_lists():
            lst = [1, 2, 3, 4, 5, 6]
            assert(u.split_lists(lst, 3) == [[1, 2], [3, 4], [5, 6]])
            assert(u.split_lists(lst, 4) == [[1, 2], [3, 4], [5], [6]])

        def test_all_or_default():
            assert u.all_or_default(
                profile_soup, '.asjdksjaldjsklajdksaldas') == []
            assert u.all_or_default(
                profile_soup, '.fjdskalfjdsalfs', default=None) == None
            assert len(u.all_or_default(basic_soup, '.test1')) == 2
            assert u.all_or_default(None, '.test1') == []

        def test_get_first_element():
            el = u.get_first_element(basic_soup, '.test1')
            assert isinstance(el, bs4.element.Tag)
            el = u.get_first_element(basic_soup, '.asdfgh', default='')
            assert el == ''

        def test_get_info():
            mapping = {
                'name': '.test1',
                'value': '.asdfg'
            }
            default = None
            output = u.get_info(basic_soup, mapping)
            expected_output = {}
            for key, selector in mapping.items():
                expected_output[key] = u.get_first_element(
                    basic_soup, selector, default=default)
            assert output == expected_output
