from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT=10


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:        
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):

        # navigate to homepage
        self.browser.get(self.live_server_url)

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

        # type first item "buy surfboard" & hit enter, page updates
        inputbox.send_keys("buy surfboard")
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: buy surfboard')

        # type another item "buy wax"  & hit enter, page updates again
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("buy wax")
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: buy surfboard')
        self.wait_for_row_in_list_table("2: buy wax")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # user 1 starts new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("buy a wetsuit")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: buy a wetsuit")

        # check for unique URL
        first_user_list_url = self.browser.current_url
        self.assertRegex(first_user_list_url, '/lists/.+')

        # switch session to new user starting another list
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # user 2 visits homepage, no sign of user 1 list items
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('buy surfboard', page_text)
        self.assertNotIn('buy a wetsuit', page_text)

        # user 2 start own list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("buy notebook")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: buy notebook")

        # check for unique URL
        second_user_list_url = self.browser.current_url
        self.assertRegex(second_user_list_url, '/lists/.+')
        self.assertNotEqual(second_user_list_url, first_user_list_url)

        # assert user 2 items in list, not user 1 items 
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('buy a wetsuit', page_text)
        self.assertIn('buy notebook', page_text)

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # test for centered input box
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + 0.5*inputbox.size['width'],
            512,
            delta=10 
        )

         # type first item "buy surfboard" & hit enter, page updates
        inputbox.send_keys("testing style")
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: testing style')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + 0.5*inputbox.size['width'],
            512,
            delta=10 
        )