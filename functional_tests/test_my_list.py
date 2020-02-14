import os
from .base import FunctionalTest


class MyListTest(FunctionalTest):

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
            self.browser.find_elements_by_link_text('My lists'), []
            ))