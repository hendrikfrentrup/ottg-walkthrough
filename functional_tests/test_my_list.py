import os
from django.conf import settings
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

TEST_RECIPIENT=os.environ.get('TEST_RECIPIENT')

class MyListTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        # visit domain to set cookie (404 loads fastest)
        self.browser.get(self.live_server_url + '/404_no_such_url/')
        self.browser.add_cookie(
            dict(
                name = settings.SESSION_COOKIE_NAME,
                value = session_key,
                path='/'
            )
        )

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = TEST_RECIPIENT
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # test user logging in
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # user is logged in
        self.create_pre_authenticated_session('exists@site-user.com')

        # user navigates to homepage
        self.browser.get(self.live_server_url)
        self.add_list_item('multiuser list item')
        self.add_list_item('multiuser item')
        first_list_url = self.browser.current_url

        # user notices "my lists" link, for the first time
        self.browser.find_element_by_link_text('My lists').click()

        # user sees their lists there, named according to first list item
        self.wait_for(lambda: self.browser.find_element_by_link_text('multiuser list item'))
        self.browser.find_element_by_link_text('multiuser list item').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, first_list_url))

        # user starts another list out of curiosity
        self.browser.get(self.live_server_url)
        self.add_list_item('another item in new list')
        second_list_url = self.browser.current_url

        # new list appears under My lists
        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(lambda: self.browser.find_element_by_link_text('another item in new list'))
        self.browser.find_element_by_link_text('another item in new list').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, second_list_url))

        self.browser.find_element_by_link_text('Logout').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_link_text('My lists'), []
            ))