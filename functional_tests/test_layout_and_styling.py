from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # test for centered input box
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + 0.5*inputbox.size['width'],
            512,
            delta=10 
        )

         # type first item "buy surfboard" & hit enter, page updates
        self.add_list_item('testing style')
        
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + 0.5*inputbox.size['width'],
            512,
            delta=10 
        )
