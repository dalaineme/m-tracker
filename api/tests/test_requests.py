# ! /api/tests/test_test.py
# -*- coding: utf-8 -*-
"""Tests for the auth endpoint

Contains basic tests for registration, login and logout
"""

import json
import unittest
import pytest
from flask_jwt_extended import (create_access_token)

from api.tests.conftest import BaseTestCase


def create_request(self, title, description, user_email):
    """New request"""
    access_token = create_access_token('test@user.com')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    return self.client.post(
        '/api/v1/users/requests',
        data=json.dumps(dict(
            title=title,
            description=description,
            user_email=user_email
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
                "The description. It has lengths that need to be adhered to. The description. It has lengths that need to be adhered to. The description. It has lengths that need to be adhered to. The description. It has lengths that need to be adhered to.",
                "user@mail.co"
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] ==
                            'Request successfully sent to the admin.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_validation_errors(self):
        """Test for presence of validation error

        This case short body length
        """
        with self.client:
            response = create_request(
                self,
                "This is the request title. Short and descriptive",
                "Body goes here",
                "user@mail.co"
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Validation errors.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 422)

    @pytest.mark.skip("We'll execute this test later")
    def test_empty_fields(self):
        """Test request has empty fields"""
        with self.client:
            response = create_request(
                self, '', 'The description', '')
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
                self, 'The New title', 'The description', 'email@mail.com')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] ==
                            'Request successfully updated.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()
