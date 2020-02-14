from selenium import webdriver
from .base import FunctionalTest

def quit_if_possible(browser):
    try: browser.quit()
    except: pass

class SharingTest(FunctionalTest):

    def test_can_share_a_list_with_another_user(self):
        # user1 is logged in
        self.create_pre_authenticated_session('exists@site-user.com')
        user1_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(user1_browser))

        # user2 is logged in
        user2_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(user2_browser))
        self.browser = user2_browser
        self.create_pre_authenticated_session('also-exists@site-user.com')

        # user1 starts a list on the homepage
        self.browser = user1_browser
        self.browser.get(self.live_server_url)
        self.add_list_item('user1 item')

        # share list option is present on site
        share_box = self.browser.find_element_by_css_selector(
            'input[name="sharee"]'
        )
        self.assertEqual(
            share_box.get_attribute('placeholder'), 'your-friends@email.com'
        )