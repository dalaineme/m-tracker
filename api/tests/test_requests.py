# ! /api/tests/test_test.py
# -*- coding: utf-8 -*-
"""Tests for the auth endpoint

Contains basic tests for registration, login and logout
"""

import json
import unittest
import pytest

from api.tests.conftest import BaseTestCase


def create_request(self, title, description):
    """New request"""
    return self.client.post(
        '/api/v1/request',
        data=json.dumps(dict(
            first_name=title,
            last_name=description
        )),
        content_type='application/json',
    )


class TestRequestEndpoint(BaseTestCase):
    """Class that handles Request Endpoint test"""

    @pytest.mark.skip("We'll execute this test later")
    def test_successful_request(self):
        """Test for successful request submission"""
        with self.client:
            response = create_request(
                self, 'The title', 'The description')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] ==
                            'Request successfully sent to the admin.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    @pytest.mark.skip("We'll execute this test later")
    def test_empty_fields(self):
        """Test request has empty fields"""
        with self.client:
            response = create_request(
                self, '', 'The description')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(data['message'] ==
                            'Sorry, you have empty field(s).')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 204)

    @pytest.mark.skip("We'll execute this test later")
    def test_get_all_requests(self):
        """Test if user can get all requests"""
        response = self.client.get('/api/v1/auth/requests')
        self.assertEqual(response.status_code, 200)

    @pytest.mark.skip("We'll execute this test later")
    def test_get_request_by_id(self):
        """Test if user can get request by id"""
        response = self.app.get('/api/v1/auth/requests/1')
        result = json.loads(response.data)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(response.status_code, 200)

    @pytest.mark.skip("We'll execute this test later")
    def test_update_request(self):
        """Test for successful request update"""
        with self.client:
            response = create_request(
                self, 'The New title', 'The description')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] ==
                            'Request successfully updated.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()
