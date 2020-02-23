import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from lists.models import List, Item
from lists.forms import DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR


class ListAPITest(TestCase):

    base_url = '/api/lists/{}/'

    def test_get_returns_json_200(self):
        list_ = List.objects.create()
        response = self.client.get(self.base_url.format(list_.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_get_returns_not_found(self):
        response = self.client.get(self.base_url.format(404))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response['content-type'], 'application/json')

    def test_get_returns_items_for_correct_list(self):
        other_list = List.objects.create()
        Item.objects.create(list=other_list, text='item1')
        our_list = List.objects.create()
        item1 = Item.objects.create(list=our_list, text='item1')
        item2 = Item.objects.create(list=our_list, text='item2')
        response = self.client.get(self.base_url.format(our_list.id))
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'id': our_list.id, 'items': [
                {'id': item1.id, 'list': our_list.id, 'text': item1.text},
                {'id': item2.id, 'list': our_list.id, 'text': item2.text}
            ]}
        )


class ItemsAPITest(TestCase):
    base_url = reverse('item-list')

    def test_POSTing_a_new_item(self):
        list_ = List.objects.create()
        response = self.client.post(
            self.base_url,
            {'list': list_.id, 'text': 'new item'}
        )
        self.assertEqual(response.status_code, 201)
        new_item = list_.item_set.get()
        self.assertEqual(new_item.text, 'new item')

    def post_empty_input(self):
        list_ = List.objects.create()
        return self.client.post(
            self.base_url.format(list_.id),
            data={'text': ''}
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_empty_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_returns_error_code(self):
        response = self.post_empty_input()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'text': [EMPTY_ITEM_ERROR]}
        )

    def test_duplicate_item_errors(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text="item input")
        response = self.client.post(
            self.base_url,
            data={'list': list_.id, 'text': 'item input'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {'non_field_errors': [DUPLICATE_ITEM_ERROR]}
        )
