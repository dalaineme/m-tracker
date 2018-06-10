# ! /api/tests/test_admin.py
# -*- coding: utf-8 -*-
"""Tests for the admin endpoint"""
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
        # Test approve ID Not found
        response2 = self.client.put(
            URL_PREFIX + 'requests/93837/approve', headers=headers)
        self.assertEqual(response2.status_code, 404)
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
        # test in approve route
        response2 = self.client.put(
            URL_PREFIX + 'requests/1/approve', headers=headers)
        self.assertEqual(response2.status_code, 403)
        truncate_tables()

    def test_successful_approve(self):
        """Test for successful admin approving a requests"""
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
        response = self.client.put(
            URL_PREFIX + 'requests/1/approve', headers=headers)
        self.assertEqual(response.status_code, 201)
        truncate_tables()

    def test_pending_update(self):
        """Test for failed update due to pending status"""
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
        # Update set to Approved
        db_instance = DbConn()
        query = (u"UPDATE tbl_requests SET current_status = %s"
                 "WHERE request_id=%s;")
        inputs = 'Approved', '1'
        db_instance.cur.execute(query, inputs)
        db_instance.conn.commit()
        db_instance.close()
        user = {
            "user_id": "456",
            "user_level": "Admin"
        }
        access_token = create_access_token(identity=user)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = self.client.put(
            URL_PREFIX + 'requests/1/approve', headers=headers)
        self.assertEqual(response.status_code, 401)
        truncate_tables()


if __name__ == "__main__":
    unittest.main()
