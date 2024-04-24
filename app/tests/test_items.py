import os
import sys
import unittest

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_dir)

from app import app
from app.utils import get_db_connection


class TestItemsRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.connection = get_db_connection()

    def tearDown(self):
        self.app_context.pop()
        self.connection.close()

    def test_list_items_route(self):
        response = self.client.get('/items/')
        self.assertEqual(response.status_code, 200)

    def test_create_item_route(self):
        data = {
            'item_group': 'Test Item',
            'unit_of_measurement': 'Each',
            'quantity': 10,
            'price_without_vat': 100.00,
            'status': 'New',
            'storage_location': 'A1',
            'contact_person': 'John Doe',
            'photo_file_path': '/path/to/photo.jpg'
        }
        response = self.client.post('/items/create/', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_edit_item_route(self):
        item_id = 1  # Assuming the ID of the item to be edited is 1
        data = {
            'item_group': 'Updated Item',
            'unit_of_measurement': 'Dozen',
            'quantity': 20,
            'price_without_vat': 200.00,
            'status': 'New',
            'storage_location': 'B2',
            'contact_person': 'Jane Doe',
            'photo_file_path': '/path/to/updated_photo.jpg'
        }
        response = self.client.post(f'/items/edit/{item_id}/', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_item_route(self):
        item_id = 1  # Assuming the ID of the item to be deleted is 1
        response = self.client.post(f'/items/delete/{item_id}/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
