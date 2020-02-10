from django.core import mail
from selenium.webdriver.common.keys import Keys
import re
import os
import poplib
import time

from .base import FunctionalTest

# TEST_RECIPIENT=os.environ.get('TEST_RECIPIENT')
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):

    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.gmx.net')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['GMX_PASSWORD'])
            while time.time() - start < 60:
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count-10), count+1)):
                    print('getting msg', i, flush=True)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    # print(lines)
                    if f'Subject: {subject}' in lines:
                        email_id =i
                        body = '\n'.join(lines)
                        return body
                    time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
                inbox.quit

    def test_can_get_email_link_to_log_in(self):
        # user enters email address upon first visit
        if self.staging_server:
            TEST_RECIPIENT = os.environ.get('TEST_RECIPIENT')
        else:
            TEST_RECIPIENT = 'user@site-user.co'

        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_RECIPIENT)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # message confirms email sent
        self.wait_for(lambda: self.assertIn(
            "Check your email", self.browser.find_element_by_tag_name('body').text
        ))

        # email found in mailbox
        body = self.wait_for_email(TEST_RECIPIENT, SUBJECT)

        # email has a url link in it
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find link in email body:\n {body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # user navigates to sent url
        self.browser.get(url)
        self.wait_to_be_logged_in(email=TEST_RECIPIENT)
        
        # user logs out
        self.browser.find_element_by_link_text('Logout').click()
        self.wait_to_be_logged_out(email=TEST_RECIPIENT)
