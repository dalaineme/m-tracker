# ! /api/tests/auth_endpoint/test_auth.py
# -*- coding: utf-8 -*-
"""Tests for the auth endpoint

Contains basic tests for registration, login and logout
"""

import json
import unittest

from api.tests.base import BaseTestCase


def register_user(self, first_name, last_name, email, password):
    """Register user method"""
    return self.client.post(
        '/auth/v1/register',
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
        '/auth/v1/login',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json',
    )


class TestAuthEndpoint(BaseTestCase):
    """Class that handles Auth Endpoint test"""

    def test_successful_registration(self):
        """ Test for user registration """
        with self.client:
            response = register_user(
                self, 'Random', 'User', 'random@user.com', 'aaaAAA111')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_existing_user_registration(self):
        """Test if an already existing user tries to register"""
        register_user(self, 'Some', 'Name', 'another@gmail.com', 'aaaAAA111')
        with self.client:
            response = register_user(
                self, 'Dalin', 'Oluoch', 'another@gmail.com', 'aaaAAA111')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Email exists, login instead.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)

    def test_empty_fields(self):
        """Test user has empty fields"""
        with self.client:
            response = register_user(
                self, '', '', '', '')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] ==
                            'Sorry you have empty field(s).')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 204)

    def test_invalid_email(self):
        """Test if user enters the wrong email"""
        with self.client:
            response = register_user(
                self, 'Dalin', 'Oluoch', 'anothergmail.com', 'aaaAAA111')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Sorry your email is invalid.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

    def test_password_strength(self):
        """Test if user enters strong password"""
        with self.client:
            response = register_user(
                self, 'Dalin', 'Oluoch', 'anothergmail.com', 'asdfasdf')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Sorry your password is weak.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            response = login_user(self, 'joe@gmail.com', 'aaaAAA111')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_login_failure(self):
        with self.client:
            # registered user login
            response = login_user(self, 'joe@gmail.com', 'aaaAAA111')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(data['message'] == 'Wrong email and or password.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)


if __name__ == "__main__":
    unittest.main()
