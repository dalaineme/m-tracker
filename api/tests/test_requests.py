# ! /api/tests/test_test.py
# -*- coding: utf-8 -*-
"""Tests for the auth endpoint
Contains basic tests for registration, login and logout
"""

import json
import unittest
from flask_jwt_extended import (create_access_token)

from db_conn import DbConn
from api.tests.base import BaseTestCase, truncate_tables

URL_PREFIX = "/api/v1/users/"


def create_user():
    """Create a user in the DB"""
    db_instance = DbConn()
    query = (u"INSERT INTO tbl_users (user_id, first_name, last_name, "
             "email, user_level, password) VALUES (%s,%s,%s,%s,%s,%s);")
    inputs = '988', 'User', 'User', 'user@user.com', 'User', 'aaaAAA111'
    db_instance.cur.execute(query, inputs)
    db_instance.conn.commit()
    db_instance.close()


def create_request(self, title, description):
    """New request"""

    # Create a UserObject for tokens
    user = {
        "user_id": "988",
        "user_level": "User"
    }
    access_token = create_access_token(identity=user)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    return self.client.post(
        URL_PREFIX + 'requests',
        data=json.dumps(dict(
            title=title,
            description=description
        )),
        content_type='application/json',
        headers=headers
    )


class TestRequestEndpoint(BaseTestCase):
    """Class that handles Request Endpoint test"""

    def test_successful_request(self):
        """Test for successful request submission"""
        with self.client:
            response = create_request(
                self,
                "This is the request title. Short and descriptive",
                ("The description. It has lengths that need to be adhered to. "
                 "The description. It has lengths that need to be adhered to. "
                 "The description. It has lengths that need to be adhered to. "
                 "The description. It has lengths that need to be adhered to.")
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['msg'] ==
                            'Request successfully sent to the admin.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
            truncate_tables()

    def test_validation_errors(self):
        """Test for presence of validation error
        This case short body length
        """
        with self.client:
            response = create_request(
                self,
                "This is the request title. Short and descriptive",
                "Body goes here"
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['msg'] == 'Validation errors.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 422)
            truncate_tables()

    def test_successful_getall_requests(self):
        """Test for successful requests get all"""
        with self.client:
            create_user()
            create_request(
                self,
                "This is the request title. Short and descriptive",
                ("The description. It has lengths that need to be adhered to."
                 "The description. It has lengths that need to be adhered to."
                 "The description. It has lengths that need to be adhered to."
                 "The description. It has lengths that need to be adhered")

            )
            # Create a UserObject for tokens
            user = {
                "user_id": "988",
                "user_level": "User"
            }
            access_token = create_access_token(identity=user)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token)
            }
            response = self.client.get(
                URL_PREFIX + 'requests', headers=headers)
            self.assertEqual(response.status_code, 200)
            truncate_tables()

    def test_user_no_requests(self):
        """Test for user who has no requests"""
        with self.client:
            # Create a UserObject for tokens
            user = {
                "user_id": "26",
                "user_level": "User"
            }
            access_token = create_access_token(identity=user)
            headers = {
                'Authorization': 'Bearer {}'.format(access_token)
            }
            response = self.client.get(
                URL_PREFIX + 'requests', headers=headers)
            self.assertEqual(response.status_code, 404)
            truncate_tables()

    def test_request_exist(self):
        """Test for existing request by specific id"""
        create_request(
            self,
            "This is the request title. Short and descriptive",
            ("The description. It has lengths that need to be adhered to."
             "The description. It has lengths that need to be adhered to."
             "The description. It has lengths that need to be adhered to."
             "The description. It has lengths that need to be adhered")
        )
        user = {
            "user_id": "988",
            "user_level": "User"
        }
        access_token = create_access_token(identity=user)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = self.client.get(
            URL_PREFIX + 'requests/1', headers=headers)
        self.assertEqual(response.status_code, 404)
        truncate_tables()


if __name__ == "__main__":
    unittest.main()
