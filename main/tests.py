from django.test import TestCase
from rest_framework.test import APIClient
from .models import Item

class VendingMachineAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.base_link = '/api/v1'

        # Create test items
        self.item1 = Item.objects.create(name='Coca cola', price=2)
        self.item2 = Item.objects.create(name='Pepsi', price=3)

    def test_item_list(self):
        response = self.client.get(self.base_link + '/items/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)  # Assuming 2 items created in setUp()

    def test_item_purchase(self):
        # Send a purchase request
        data = {
            'item_id': self.item1.id,
            'amount_paid': 5,
        }
        response = self.client.post(self.base_link + '/items/purchase/', data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('change', response.data)
        self.assertIn('notes_to_return', response.data)
        self.assertEqual(response.data['change'], 3)  # Assuming item price is 2
        self.assertDictEqual(response.data['notes_to_return'], {1: 3})  # Assuming 3 RM1 notes to return

    def test_invalid_item_purchase(self):
        # Send a purchase request with an invalid item ID
        data = {
            'item_id': 999999,  # Invalid ID
            'amount_paid': 5,
        }
        response = self.client.post(self.base_link + '/items/purchase/', data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Invalid item ID.')

    def test_insufficient_amount_purchase(self):
        # Send a purchase request with insufficient amount paid
        data = {
            'item_id': self.item2.id,
            'amount_paid': 2.00,  # Insufficient amount for item price of 3
        }
        response = self.client.post(self.base_link + '/items/purchase/', data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Insufficient amount paid.')