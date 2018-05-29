# ! /api/tests/test_test.py
# -*- coding: utf-8 -*-
"""Tests for the auth endpoint

Contains basic tests for registration, login and logout
"""

import json
import unittest

from api.server import APP


class TestAuthEndpoint(unittest.TestCase):
    """Class that handles Auth Endpoint test"""

    def setUp(self):
        """code that is executed before each test"""
        APP.testing = True
        self.app = APP.test_client()
        self.data = {
            "first_name": "Random",
            "last_name": "Name",
            "email": "random@email.com",
            "password": "password"
        }

    def test_successful_registration(self):
        """Test for successful registration"""
        response = self.app.post('/api/v1/auth/register',
                                 data=json.dumps(self.data),
                                 content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["message"], "Success! New user registred.")
        self.assertEqual(response.status_code, 201)

    def test_existing_user_registration(self):
        """Test if an already existing user tries to register"""
        response = self.app.post('/api/v1/auth/register',
                                 data=json.dumps(self.data),
                                 content_type="application/json")
        data = {
            "first_name": "Random",
            "last_name": "Name",
            "email": "random@email.com",
            "password": "password"
        }
        response = self.app.post('/api/v1/auth/register',
                                 data=json.dumps(data),
                                 content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["message"],
                         "Fail! User already exists, Login instead.")
        self.assertEqual(response.status_code, 422)

    def test_empty_fields(self):
        """Test user has empty fields"""
        self.data = {
            "first_name": "",
            "last_name": "",
            "email": "",
            "password": ""
        }
        response = self.app.post('/api/v1/auth/register',
                                 data=json.dumps(self.data),
                                 content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["message"], "Fail! You have empty field(s).")
        self.assertEqual(response.status_code, 204)

    def test_invalid_email(self):
        """Test if user enters the wrong email"""
        data = {
            "first_name": "Random",
            "last_name": "Name",
            "email": "emailadddd",
            "password": "aaaAAA111"
        }
        response = self.app.post('/api/v1/auth/register',
                                 data=json.dumps(data),
                                 content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["message"], "Fail! Email is invalid.")
        self.assertEqual(response.status_code, 400)

    def test_password_strength(self):
        """Test if user enters strong password"""
        data = {
            "first_name": "Random",
            "last_name": "Name",
            "email": "email@add.com",
            "password": "asdfasdf"
        }
        response = self.app.post('/api/v1/auth/register',
                                 data=json.dumps(data),
                                 content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["message"], "Fail! Weak password.")
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
