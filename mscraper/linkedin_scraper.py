from mscraper import Mscraper
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from os import environ
from linkedin_profile import LinkedinProfile
from utils import AnyEC
from pandas.io.json._normalize import nested_to_record
import pandas as pd
from datetime import datetime

class LinkedinScraper(Mscraper):

    def __init__(self, linkedin_email='', linkedin_password='', li_at=''):
        super().__init__(website="https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
        self.linkedin_email = linkedin_email
        self.linkedin_password = linkedin_password
        self.li_at = li_at
        self.last_url_visited = ''
        self.df = None

        self.driver.add_cookie({
                'name': 'li_at',
                'value': li_at,
                'domain': '.linkedin.com'
            })

        if 'LINKEDIN_EMAIL' in environ and 'LINKEDIN_PASS' in environ:
            self.linkedin_email = environ['LINKEDIN_EMAIL']
            self.linkedin_password = environ['LINKEDIN_PASS']
            self.li_at = environ['LI_AT']

        # UNCOMMENT AND PUT HERE YOUR DATA, or pass the data as environment variables
        # self.li_at = ""
        # self.linkedin_email = ""
        # self.linkedin_password = ""


    def login(self):
        email_input = self.driver.find_element_by_name("session_key")
        password_input = self.driver.find_element_by_name("session_password")
        email_input.send_keys(self.linkedin_email)
        password_input.send_keys(self.linkedin_password)
        password_input.send_keys(Keys.ENTER)

    def save_to_csv(self, dict, csv_name="out", use_current_time=True):

        if use_current_time:
            csv_name = csv_name + str(datetime.now().strftime('%Y-%m-%d_%H:%M:%S')).strip()

        if self.df is None:
            # create a new dataframe
            self.df = pd.DataFrame(dict, index=[0])
            self.df.to_csv(csv_name + '.csv')
            self.csv_name = csv_name
        else:
            # append to existing dataframe
            self.df = self.df.append(dict, ignore_index=True)
            # append to existing csv
            new_row = pd.DataFrame(dict, index=[len(self.df.index)-1])
            new_row.to_csv(self.csv_name + '.csv', mode='a', header=False)

    # implement your custom filter logic
    def filter_profile(self, dict):
        filtered_dict = {}

        filtered_dict = dict
        return filtered_dict

    def order_dict(self, dict):
        dict = nested_to_record(dict, sep='_')
        print("dict", dict)
        ordered_dict = {}
        ordered_dict["last_url_visited"] = self.last_url_visited

        same_fields = ['personal_info_headline',
          'personal_info_summary']

        self.same_field_in_dict(ordered_dict, dict, same_fields)

        self.unpack_experiences(ordered_dict, dict["experiences_jobs"], "job")
        self.unpack_experiences(ordered_dict, dict["experiences_education"], "edu")

        same_fields = ['personal_info_name',
         'personal_info_location', 'personal_info_company',
          'personal_info_school',
          'accomplishments_publications', 'accomplishments_certifications',
           'accomplishments_patents', 'accomplishments_courses',
            'accomplishments_projects', 'accomplishments_honors',
             'accomplishments_test_scores', 'accomplishments_languages',
              'accomplishments_organizations'
          ]

        self.same_field_in_dict(ordered_dict, dict, same_fields)
        print("ordered_dict", ordered_dict)

        if dict["skills"]:
            ordered_dict["skills"] = ' '.join(dict["skills"])

        if dict["interests"]:
            ordered_dict["interests"] = ' '.join(dict["interests"])

        return ordered_dict

    def same_field_in_dict(self, new_dict, old_dict, fields):
        for field in fields:
            try:
                if isinstance(old_dict[field], str):
                    new_dict[field] = old_dict[field]
                    continue
                if isinstance(old_dict[field], list):
                    new_dict[field] = ' '.join(old_dict[field])
                    continue
                else:
                    raise ValueError("Not supported type for old_dict[field] = " +
                    str(old_dict[field]) + " of type " + str(type(old_dict[field])))
            except ValueError as err:
                print(err.args)
                print("ERROR, same_field_in_dict")
                new_dict[field] = ""

    def unpack_experiences(self, new_dict, old_dict, prefix):
        i = 1
        if old_dict:
            for d in old_dict:
                new_dict[prefix + "_" + str(i)] = ' '.join(str(x) for x in d.values())
                i = i + 1

    MAIN_SELECTOR = '.core-rail'
    ERROR_SELECTOR = '.profile-unavailable'

    def scrape(self, url='', user=None):
        try:
            self.load_profile_page(url, user)
            return self.get_profile()
        except ValueError as err:
            print(err.args)
            print("ERROR, scrape")
            return None
        except NoSuchElementException as err:
            print(err.args)
            print("ERROR, scrape")
            return None


    def load_profile_page(self, url='', user=None):
        if user:
            url = 'http://www.linkedin.com/in/' + user
        if 'com/in/' not in url and 'sales/gmail/profile/proxy/' not in url:
            raise ValueError(
                "Url must look like... .com/in/NAME or... '.com/sales/gmail/profile/proxy/EMAIL")

        self.driver.get(url)
        self.last_url_visited = url

        # Wait for page to load dynamically via javascript
        try:
            myElem = WebDriverWait(self.driver, self.timeout).until(AnyEC(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.MAIN_SELECTOR)),
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.ERROR_SELECTOR))
            ))
        except TimeoutException as e:
            print("Took too long to load profile")

        self.driver.find_element_by_css_selector(self.MAIN_SELECTOR)

        self.scroll_to_bottom()

    def get_profile(self):
        profile = self.driver.find_element_by_css_selector(
            self.MAIN_SELECTOR).get_attribute("outerHTML")

        print('profile ', profile)
        return LinkedinProfile(profile)
