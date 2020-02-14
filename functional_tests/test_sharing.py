from selenium import webdriver
from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListPage

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
        list_page = ListPage(self).add_list_item('user1 item')

        # share list option is present on site
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'), 
            'your-friends@email.com'
        )

        # user1 shares list with user2
        list_page.share_list_with('also-exists@site-user.com')

        # user2 goes to their lists page
        self.browser = user2_browser
        MyListPage(self).go_to_my_lists_page()

        # user2 notices user1's list
        self.browser.find_element_by_link_text('user1 item').click()

        # user2 can see the list's owner is user 1
        self.wait_for(lambda: self.assertEqual(
            list_page.get_list_owner(),
            'exists@site-user.com'
        ))
        # user 2 adds an item
        list_page.add_list_item('hi user 1')
        # user 1 notices added item upon refresh
        self.browser = user1_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('hi user 1', 2)