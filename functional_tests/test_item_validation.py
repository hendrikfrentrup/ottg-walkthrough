from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # visit homepage and submit empty list item
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # homepage refresh with error message
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        # another submission with text, success
        self.browser.find_element_by_id('id_new_item').send_keys("buy drill")
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: buy drill')

        # another empty submission, leading to error
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))
        
        # again another good submission with text, success
        inputbox = self.browser.find_element_by_id('id_new_item').send_keys("buy screen")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: buy drill')
        self.wait_for_row_in_list_table('2: buy screen')