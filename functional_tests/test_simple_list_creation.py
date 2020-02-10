from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_user_can_start_a_list_and_retrieve_it_later(self):

        # navigate to homepage
        self.browser.get(self.live_server_url)

        # notice browser title
        self.assertIn( "To-Do" , self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn( "To-Do", header_text)

        # enter to-do
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute("placeholder"),
            "Enter a to-do item"
        )

        # type first item "buy surfboard" & hit enter, page updates
        self.add_list_item('simple item')

        # type another item "buy wax"  & hit enter, page updates again
        self.add_list_item('another simple item')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # user 1 starts new to-do list
        self.browser.get(self.live_server_url)
        self.add_list_item('user 1 list')

        # check for unique URL
        first_user_list_url = self.browser.current_url
        self.assertRegex(first_user_list_url, '/lists/.+')

        # switch session to new user starting another list
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # user 2 visits homepage, no sign of user 1 list items
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('user 1 list', page_text)

        # user 2 start own list
        self.add_list_item('user 2 list')

        # check for unique URL
        second_user_list_url = self.browser.current_url
        self.assertRegex(second_user_list_url, '/lists/.+')
        self.assertNotEqual(second_user_list_url, first_user_list_url)

        # assert user 2 items in list, not user 1 items 
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('user 1 list', page_text)
        self.assertIn('user 2 list', page_text)
