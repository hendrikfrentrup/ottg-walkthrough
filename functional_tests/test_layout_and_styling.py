from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class LayoutAndStylingTest(FunctionalTest):

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
