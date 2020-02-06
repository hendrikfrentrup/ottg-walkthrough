from django.core import mail
from selenium.webdriver.common.keys import Keys
import re
import os

from .base import FunctionalTest

TEST_RECIPIENT=os.environ.get('TEST_RECIPIENT')
SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # user enters email address upon first visit
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_RECIPIENT)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # message confirms email sent
        self.wait_for(lambda: self.assertIn(
            "Check your email", self.browser.find_element_by_tag_name('body').text
        ))

        # email found in mailbox
        email = mail.outbox[0]
        self.assertIn(TEST_RECIPIENT, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # email has a url link in it
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find link in email body:\n {email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # user navigates to sent url
        self.browser.get(url)
        self.wait_for(lambda: self.browser.find_elements_by_link_text('Log out'))
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_RECIPIENT, navbar.text)