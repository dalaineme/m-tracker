# ! /api/tests/auth_endpoint/test_auth.py
# -*- coding: utf-8 -*-
"""Tests for the auth endpoint
Contains basic tests for registration, login and logout
"""

import json
import unittest
from flask_jwt_extended import (create_access_token)
from api.tests.conftest import BaseTestCase


def register_user(self, first_name, last_name, email, password):
    """Register user method"""
    return self.client.post(
        '/api/v1/users/register',
        data=json.dumps(dict(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )),
        content_type='application/json',
    )


def login_user(self, email, password):
    """Login user method"""
    return self.client.post(
        '/api/v1/users/login',
        data=json.dumps(dict(
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
            self.assertTrue(data['message'] ==
                            "Account for 'random@user.com' has been created.")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_no_post_data_registration(self):
        """ Test empty dictionary """
        with self.client:
            input_data = {}
            response = self.client.post('/api/v1/users/register',
                                        data=json.dumps(input_data),
                                        content_type="application/json")
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'No input data provided.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

    def test_existing_user_registration(self):
        """Test if an already existing user tries to register"""
        register_user(self, 'Some', 'Name', 'another@gmail.com', 'aaaAAA111')
        with self.client:
            response = register_user(
                self, 'Dalin', 'Oluoch', 'another@gmail.com', 'aaaAAA111')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] ==
                "Sorry, email 'another@gmail.com' already exists.")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

    def test_empty_fields(self):
        """Test user has empty fields"""
        with self.client:
            response = register_user(
                self, '', '', '', '')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Validation errors.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 422)

    def test_invalid_email(self):
        """Test if user enters the wrong email"""
        with self.client:
            response = register_user(
                self, 'Dalin', 'Oluoch', 'anothergmail.com', 'aaaAAA111')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Validation errors.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 422)

    def test_password_strength(self):
        """Test if user enters strong password"""
        with self.client:
            response = register_user(
                self, 'Dalin', 'Oluoch', 'anothergmail.com', 'asdfasdf')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Validation errors.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 422)

    # Login Tests
    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        # register a user
        register_user(self, 'some', 'name', 'another@gmail.com', 'aaaAAA111')

        # test logging in registered user
        with self.client:
            response = login_user(self, 'another@gmail.com', 'aaaAAA111')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_unregistered_user_login(self):
        """ Test for login of a not registered-user"""
        with self.client:
            response = login_user(self, 'another@gmail.com', 'aaaAAA111')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] ==
                "Sorry, email 'another@gmail.com' does not exist.")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

    def test_login_failure(self):
        """Wrong login credentials

        Wrong password
        """
        # register a user
        register_user(self, 'some', 'name', 'the@user.com', 'aaaAAA111')

        # test logging in failure of a registered user - wrong password
        with self.client:
            response = login_user(self, 'the@user.com', 'Pa4s283dDI!')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == "Wrong login credentials.")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 422)

    def test_invalid_email_login(self):
        """ Test for invalid email while logging in"""
        with self.client:
            response = login_user(self, 'joegmail.com', 'aaaAAA111')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Validation errors.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 422)

    def test_short_password_login(self):
        """ Test for minimum length password"""
        with self.client:
            response = login_user(self, 'joe@gmail.com', 'aA111')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Validation errors.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 422)

    # Test logout
    def test_successful_logout(self):
        """ Test logout headers token """
        with self.client:
            access_token = create_access_token('test@user.com')
            headers = {
                'Authorization': 'Bearer {}'.format(access_token)
            }
            response = self.client.post(
                '/api/v1/users/logout', headers=headers)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] ==
                            'You have successfully logged out.')
            self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
