# pytest tests/test_linkedin_scraper.py -s
import unittest
import time
import random
from pandas.io.json._normalize import nested_to_record
import copy
import sys
sys.path.append('../mscraper/')
from linkedin_scraper import LinkedinScraper


class TestLinkedinScraper(unittest.TestCase):

    def test_linkedin_login(self):

        ls = LinkedinScraper()

        ls.login()
        time.sleep(random.uniform(0.5, 1))

        ls.driver.get("https://www.linkedin.com/feed/")

        ls.go_to_website("https://www.linkedin.com/in/amantonopoulos/")
        ls.scroll_to_bottom()
        ls.driver.quit()

    def test_linkedin_profile_scraper(self):

        with LinkedinScraper() as ls:
            ls.login()
            # Insert your user, for instance amantonopoulos if your link is https://www.linkedin.com/in/amantonopoulos/
            myuser = ""
            profile = ls.scrape(user=myuser)

        profile_info = profile.to_dict()
        print("profile_info ", profile_info)

        for a in profile.attributes:
            assert profile_info[a]

        # Personal Info
        personal_info = profile_info['personal_info']
        print("personal_info ", personal_info)

        skills = profile_info['skills']
        print("skills", skills)

        accomplishments = profile_info['accomplishments']
        print("accomplishments ", profile_info['accomplishments'])
        assert profile_info['accomplishments']

        print("Interests ", profile_info['interests'])
        interests = profile_info['interests']
        assert interests

        # Experiences
        experiences = profile_info['experiences']
        print("experiences ", experiences)

        jobs = experiences['jobs']
        assert jobs

        education = experiences['education']
        assert education


        profile_info_original = copy.deepcopy(profile_info)
        # add some dummy fields, to see how the csv handle different dicts
        profile_info["experiences"]["jobs"].append({'title': 'DUMMY', 'company': 'DUMMY', 'date_range': 'DUMMY', 'location': "DUMMY", 'description': 'DUMMY', 'li_company_url': ''})
        profile_info["experiences"]["jobs"].append({'title': 'DUMMY', 'company': 'DUMMY', 'date_range': 'DUMMY', 'location': "DUMMY", 'description': 'DUMMY', 'li_company_url': ''})
        profile_info["experiences"]["jobs"].append({'title': 'DUMMY', 'company': 'DUMMY', 'date_range': 'DUMMY', 'location': "DUMMY", 'description': 'DUMMY', 'li_company_url': ''})
        profile_info["experiences"]["education"].append({'name': 'DUMMY', 'degree': "DUMMY", 'grades': "DUMMY", 'field_of_study': 'DUMMY', 'date_range': 'DUMMY', 'activities': "DUMMY", 'description': 'DUMMY'})

        csv_dict = ls.filter_profile(ls.order_dict(profile_info))
        ls.save_to_csv(csv_dict)

        csv_dict = ls.filter_profile(ls.order_dict(profile_info_original))
        ls.save_to_csv(csv_dict)
