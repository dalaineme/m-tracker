# ! /api/tests/test_admin.py
# -*- coding: utf-8 -*-
"""Tests for the admin endpoint"""
import json
import unittest
from flask_jwt_extended import (create_access_token)

from db_conn import DbConn
from api.tests.base import BaseTestCase, truncate_tables
from api.tests.test_requests import create_user, create_request

URL_PREFIX = "/api/v1/"


class TestAdminEndpoint(BaseTestCase):
    """Class that handles Request Endpoint test"""

    def test_successful_get(self):
        """Test for successful admin getting all requests"""
        # Create a request
        create_user()
        create_request(
            self,
            "This is the request title. Short and descriptive",
            ("The description. It has lengths that need to be adhered to. "
             "The description. It has lengths that need to be adhered to. "
             "The description. It has lengths that need to be adhered to. "
             "The description. It has lengths that need to be adhered to.")
        )
        user = {
            "user_id": "456",
            "user_level": "Admin"
        }
        access_token = create_access_token(identity=user)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = self.client.get(
            URL_PREFIX + 'requests', headers=headers)
        self.assertEqual(response.status_code, 200)
        truncate_tables()

    def test_no_requests(self):
        """Test for admin finding no requests"""
        # Create a request
        user = {
            "user_id": "456",
            "user_level": "Admin"
        }
        access_token = create_access_token(identity=user)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = self.client.get(
            URL_PREFIX + 'requests', headers=headers)
        self.assertEqual(response.status_code, 404)
        truncate_tables()

    def test_admin_only(self):
        """Test for user trying to access the get all requests route"""
        # Create a request
        user = {
            "user_id": "456",
            "user_level": "User"
        }
        access_token = create_access_token(identity=user)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = self.client.get(
            URL_PREFIX + 'requests', headers=headers)
        self.assertEqual(response.status_code, 403)
        truncate_tables()


if __name__ == "__main__":
    unittest.main()
