import unittest
import time
import sys
sys.path.append('../mscraper/')
from linkedin_scraper import LinkedinScraper
from google_scraper import Google
import random
import pickle
import platform

def find_linkedin_links(n):

    with Google() as gs:
        gs.look_for("paris", "blockchain", "developer")
        gs.from_website("linkedin.com/in")
        gs.exclude("marketing", "fashion", "medical")
        gs.google_it()
        links = gs.get_first_n_links(n=n, save_to_file=True, the_filename="mainlinks.txt")
        print(links)

def scrape_linkedin():

    with open("mainlinks.txt", 'rb') as f:
        links = pickle.load(f)

    with LinkedinScraper() as ls:
        ls.login()

        for link in links:
            time.sleep(random.uniform(0.5, 1))
            profile = ls.scrape(url=link)
            if profile is not None:
                profile_info = profile.to_dict()
                csv_dict = ls.filter_profile(ls.order_dict(profile_info))
                ls.save_to_csv(csv_dict)

        body = "Message sent from " + str(platform.system()) + " version " + str(platform.release())
        ls.send_results_via_email(ls.csv_name + '.csv', body=body)


if __name__ == "__main__":

    n = int(input("Enter a number of links to scrape: "))
    find_linkedin_links(n)
    scrape_linkedin()
