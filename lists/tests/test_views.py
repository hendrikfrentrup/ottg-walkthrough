import unittest
from django.test import TestCase
from unittest.mock import patch, Mock
from django.http import HttpRequest
from lists.views import new_list
from lists.models import Item, List
from lists.forms import (
    EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR,
    ItemForm, ExistingListItemForm
)
from django.utils.html import escape
from django.contrib.auth import get_user_model
User = get_user_model()

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_anonymous_user_get_your_todo_list_header(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertContains(response, "Your")

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_exisiting_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for a an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for a an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for a an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_displays_existing_list_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            f'/lists/{list_.id}/', 
            data={'text': ''}
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)   

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()        
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='texty')
        response = self.client.post(
            f'/lists/{list1.id}/',
            data={'text': 'texty'}
        )
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)

class NewListViewIntegratedTest(TestCase):

    URL='/lists/new'

    def test_can_save_POST_request(self):
        self.client.post(self.URL, data={'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post(self.URL, data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        user = User.objects.create(email='a@b.com')
        self.client.force_login(user)
        self.client.post(self.URL, data={'text': 'new_item'})
        list_ = List.objects.first()
        self.assertEqual(list_.owner, user)

@patch('lists.views.NewListForm')
class NewListViewUnitTest(unittest.TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['text'] = 'new list item'
        self.request.user = Mock()

    def test_passes_POST_data_to_NewListForm(self, mockNewListForm):
        new_list(self.request)
        mockNewListForm.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_valid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        new_list(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch('lists.views.redirect')
    def test_redirects_to_form_return_object_if_form_valid(
        self, mock_redirect, mockNewListForm
    ):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        response = new_list(self.request)

        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(mock_form.save.return_value)

    @patch('lists.views.render')
    def test_redirects_to_form_return_object_if_form_invalid(
        self, mock_render, mockNewListForm
    ):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        response = new_list(self.request)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request, 'home.html', {'form': mock_form}
        )

    def test_does_not_save_if_form_invalid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        new_list(self.request)
        self.assertFalse(mock_form.save.called)

class MyListsTest(TestCase):

    def test_my_lists_url_render_my_lists_template(self):
        User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertTemplateUsed(response, 'my_lists.html')

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email='wrong@owner.com')
        correct_user = User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        owner = response.context['owner']
        self.assertEqual(owner, correct_user)

class ShareListTest(TestCase):

    def test_post_redirects_to_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(f'/lists/{list_.id}/share', data={
            "sharee": "anonymous@site-user.com"
        })
        self.assertRedirects(response, f'/lists/{list_.id}/')

    def test_post_with_anonymous_user_shows_error(self):
        list_ = List.objects.create()
        response = self.client.post(f'/lists/{list_.id}/share', data={
            "sharee": "anonymous@site-user.com"
        }, follow=True)
        message = list(response.context['messages'])[0]
        self.assertEqual(message.tags, 'error')
        self.assertIn('not found', message.message)

    def test_share_list_renders_list_template(self):
        user = User.objects.create(email='a@b.com')
        list_ = List.objects.create()
        response = self.client.post(f'/lists/{list_.id}/share', data={
            "sharee": "a@b.com"
        })
        print(response.context)
        self.assertIn(user, list_.shared_with.all())