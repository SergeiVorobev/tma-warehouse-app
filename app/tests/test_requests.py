from flask import url_for
import os
import sys
import unittest

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_dir)

from app import app
from app.utils import get_db_connection


class TestRequests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.connection = get_db_connection()

    def tearDown(self):
        self.app_context.pop()
        self.connection.close()
    # Test list orders route
    def test_list_orders(self):
        with self.app as client:
            response = client.get(url_for('list_orders'))
            self.assertEqual(response.status_code, 200)

    # Test create order route
    def test_create_order(self):
        with self.app as client:
            response = client.post('/orders/create/1', data={'quantity': 5, 'comment': 'Test comment'})
            self.assertEqual(response.status_code, 302)  # Check if redirected after successful request creation

    # Test view purchase request route
    def test_view_purchase_request(self):
        with self.app as client:
            response = client.get(url_for('view_purchase_request', request_id=1))
            self.assertEqual(response.status_code, 200)

    # Test confirm purchase request route
    def test_confirm_purchase_request(self):
        with self.app as client:
            response = client.post(url_for('confirm_purchase_request', request_id=1))
            self.assertEqual(response.status_code, 302)

    # Test reject purchase request route
    def test_reject_purchase_request(self):
        with self.app as client:
            response = client.post(url_for('reject_purchase_request', request_id=1), data={'comment': 'Test comment'})
            self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
