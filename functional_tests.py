from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):

        # navigate to homepage
        self.browser.get('http://localhost:8000')

        # notice browser title
        self.assertIn( "To-Do" , self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn( "To-Do", header_text)

        # enter to-do
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute("placeholder"),
            "Enter a to-do item"
        )

        # type first item "buy surfboard"
        inputbox.send_keys("buy surfboard")
        # hit enter, page updates
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # page updates with item
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn("1: buy surfboard", [row.text for row in rows])

        # type another item "buy wax"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("buy wax")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # page updates with another item
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn("2: buy wax", [row.text for row in rows])
        self.fail("finish the test!")

if __name__ == '__main__':
    unittest.main()
    # (warnings='ignore')