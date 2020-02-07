from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from lists.forms import DUPLICATE_ITEM_ERROR


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # visit homepage and submit empty list item
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # browser intercepts request and does not reload
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

        # with inputs, field validates, submission with text, success
        self.get_item_input_box().send_keys("buy drill")
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: buy drill')

        # another empty submission, leading to error
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))
        
        # again with inputs field validates and yields another good submission with text, success
        inputbox = self.get_item_input_box()
        inputbox.send_keys("buy screen")
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:valid'))
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: buy drill')
        self.wait_for_row_in_list_table('2: buy screen')

    def test_cannot_add_duplicate_items(self):
        # visit homepage and submit list item
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("buy duplicate")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: buy duplicate')

        self.get_item_input_box().send_keys("buy duplicate")
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            DUPLICATE_ITEM_ERROR
            ))

    def test_error_messages_are_cleared_on_input(self):
        # start list and cause validation error
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('keypress')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: keypress')
        self.get_item_input_box().send_keys('keypress')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        # user input clears the error
        self.get_item_input_box().send_keys('n')
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))

    def test_error_messages_are_cleared_on_click(self):
        # start list and cause validation error
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('click')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: click')
        self.get_item_input_box().send_keys('click')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        # user selecting input box clears the error
        self.get_item_input_box().click()
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))