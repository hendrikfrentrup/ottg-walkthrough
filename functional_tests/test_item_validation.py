from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip

class ItemValidationTest(FunctionalTest):

    @skip("while writing test")
    def test_cannot_add_empty_list_items(self):
        self.fail('write me!')
        # visit homepage and submit empty list item
        # homepage refresh with error message
        # another submission with text, success
        # another empty submission, leading to error
        # 