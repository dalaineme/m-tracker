# ! /api/tests/test_test.py
# -*- coding: utf-8 -*-
"""Tests for the auth endpoint

Contains basic tests for registration, login and logout
"""

import json
import unittest

from api.server import APP


class TestRequestEndpoint(unittest.TestCase):
    """Class that handles Request Endpoint test"""

    def setUp(self):
        """code that is executed before each test"""
        APP.testing = True
        self.app = APP.test_client()
        self.data = {
            "title": "Some title",
            "description": "Description of the request"
        }

    def test_successful_request(self):
        """Test for successful request submission"""
        response = self.app.post('/api/v1/auth/request',
                                 data=json.dumps(self.data),
                                 content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["message"], "Success! Request sent.")
        self.assertEqual(response.status_code, 201)

    def test_empty_fields(self):
        """Test request has empty fields"""
        self.data = {
            "title": "",
            "description": ""
        }
        response = self.app.post('/api/v1/auth/request',
                                 data=json.dumps(self.data),
                                 content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["message"], "Fail! You have empty field(s).")
        self.assertEqual(response.status_code, 204)

    def test_get_all_requests(self):
        """Test if user can get all requests"""
        response = self.app.get('/api/v1/auth/requests')
        result = json.loads(response.data)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(response.status_code, 400)

    def test_get_request_by_id(self):
        """Test if user can get request by id"""
        response = self.app.get('/api/v1/auth/requests/1')
        result = json.loads(response.data)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(response.status_code, 400)

    def test_update_request(self):
        """Test for successful request update"""
        data = {
            "title": "Change title",
            "description": "Change of the request"
        }
        response = self.app.put('/api/v1/auth/request/1',
                                data=json.dumps(data),
                                content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["message"], "Success! Request updated.")
        self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()
