# ! /api/tests/auth_endpoint/test_auth.py
# -*- coding: utf-8 -*-
"""Tests for the auth endpoint
Contains basic tests for signup, login and logout
"""

import json
from api.tests.base import BaseTestCase, truncate_tables

# abstract the common url for auth endpoint
URL_PREFIX = "/api/v1/auth/"


def register_user(self, first_name, last_name, email, password):
    """Register user method"""
    return self.client.post(
        URL_PREFIX + "signup",
        data=json.dumps(dict(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )),
        content_type='application/json',
    )


class TestAuthEndpoint(BaseTestCase):
    """Class that handles Auth Endpoint test"""

    # Registration tests
    def test_successful_registration(self):
        """ Test for user registration """
        with self.client:
            response = register_user(
                self, 'Random', 'User', 'random@user.com', 'aaaAAA111')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['msg'] ==
                            "Account for 'random@user.com' has been created.")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
            truncate_tables()

    def test_no_post_data_registration(self):
        """ Test empty dictionary """
        with self.client:
            input_data = {}
            response = self.client.post(URL_PREFIX + "signup",
                                        data=json.dumps(input_data),
                                        content_type="application/json")
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['msg'] == 'No input data provided.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)
            truncate_tables()

    def test_existing_user_registration(self):
        """Test if an already existing user tries to register"""
        register_user(self, 'Some', 'Name', 'another@gmail.com', 'aaaAAA111')
        with self.client:
            response = register_user(
                self, 'Dalin', 'Oluoch', 'another@gmail.com', 'aaaAAA111')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['msg'] ==
                "Sorry! Email 'another@gmail.com' already exists.")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)
            truncate_tables()

    def test_empty_fields(self):
        """Test user has empty fields"""
        with self.client:
            response = register_user(
                self, '', '', '', '')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['msg'] == 'Validation errors.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 422)
            truncate_tables()

    def test_invalid_email(self):
        """Test if user enters the wrong email"""
        with self.client:
            response = register_user(
                self, 'Dalin', 'Oluoch', 'anothergmail.com', 'aaaAAA111')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['msg'] == 'Validation errors.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 422)
            truncate_tables()

    def test_password_strength(self):
        """Test if user enters strong password"""
        with self.client:
            response = register_user(
                self, 'Dalin', 'Oluoch', 'anothergmail.com', 'asdfasdf')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['msg'] == 'Validation errors.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 422)
            truncate_tables()
