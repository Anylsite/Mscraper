from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException
import chromedriver_binary
from bs4 import BeautifulSoup
from abc import abstractmethod
import platform
import os
import time
import smtplib
import ssl
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
import csv


def set_default_Chrome_options():

    chrome_options = Options()
    print("Running on ", platform.system())
    print("Release: ", platform.release())
    AM_I_IN_A_DOCKER_CONTAINER = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)
    print("AM_I_IN_A_DOCKER_CONTAINER? ", AM_I_IN_A_DOCKER_CONTAINER)
    if AM_I_IN_A_DOCKER_CONTAINER:
        print("Activating Headless option")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-dev-shm-usage')

    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("window-size=1400,2100")
    chrome_options.add_argument('--disable-gpu')
    return chrome_options


class Mscraper(object):

    def __init__(self, scraperInstance=None,
     driver_options=set_default_Chrome_options(),
     website='http://www.linkedin.com',
     scroll_pause=0.1, scroll_increment=300, timeout=15):

        if scraperInstance:
            self.driver = scraperInstance.driver
            self.scroll_increment = scraperInstance.scroll_increment
            self.timeout = scraperInstance.timeout
            self.scroll_pause = scraperInstance.scroll_pause
        else:
            self.driver = webdriver.Chrome(options=driver_options)
            self.scroll_pause = scroll_pause
            self.scroll_increment = scroll_increment
            self.timeout = timeout

        self.go_to_website(website)

    def get_this_html(self, use_soup=True):
        if use_soup:
            return BeautifulSoup(self.driver.page_source, 'html.parser')
        else:
            return self.driver.page_source

    @abstractmethod
    def login(self):
        raise Exception('This is an abstract method')

    def go_to_website(self, website):
        self.driver.get(website)

    def quit(self):
        self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.quit()

    def send_results_via_email(self, filename_to_attach,
     subject = "Scraper Results", body = "This is an email with attachment sent from Python",
     sender_email = "admin@gmail.com", receiver_email = "admin2@protonmail.com",
     password = "mypassword"):

        port = 465  # For SSL

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        # Open PDF file in binary mode
        with open(filename_to_attach, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename_to_attach}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)

    def scroll_to_bottom(self):

        expandable_button_selectors = [
            'button[aria-expanded="false"].pv-skills-section__additional-skills',
            'button[aria-expanded="false"].pv-profile-section__see-more-inline',
            'button[aria-expanded="false"].pv-top-card-section__summary-toggle-button',
            'button[data-control-name="contact_see_more"]'
        ]

        current_height = 0
        while True:
            for name in expandable_button_selectors:
                try:
                    self.driver.find_element_by_css_selector(name).click()
                except NoSuchElementException as err:
                    print(err.args)
                    print("ERROR, scroll_to_bottom (0)")
                    pass
                except ElementNotInteractableException as err:
                    print(err.args)
                    print("ERROR, scroll_to_bottom (1)")
                    pass
                except ElementClickInterceptedException as err:
                    print(err.args)
                    print("ERROR, scroll_to_bottom (2)")
                    pass

            # Use JQuery to click on invisible expandable 'see more...' elements
            self.driver.execute_script(
                'document.querySelectorAll(".lt-line-clamp__ellipsis:not(.lt-line-clamp__ellipsis--dummy) .lt-line-clamp__more").forEach(el => el.click())')

            # Scroll down to bottom
            new_height = self.driver.execute_script(
                "return Math.min({}, document.body.scrollHeight)".format(current_height + self.scroll_increment))
            if (new_height == current_height):
                break
            self.driver.execute_script(
                "window.scrollTo(0, Math.min({}, document.body.scrollHeight));".format(new_height))
            current_height = new_height
            # Wait to load page
            time.sleep(self.scroll_pause)
