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


def update_request(self, title, description):
    """New request"""
    access_token = create_access_token('test@user.com')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    return self.client.put(
        '/api/v1/users/requests/1',
        data=json.dumps(dict(
            title=title,
            description=description
        )),
        content_type='application/json',
        headers=headers
    )


class TestRequestEndpoint(BaseTestCase):
    """Class that handles Request Endpoint test"""

    def test_fail_get_all_requests(self):
        """Test if user can not all requests. User has no requests"""
        access_token = create_access_token('randossms@user.com')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = self.client.get('/api/v1/users/requests', headers=headers)

        self.assertEqual(response.status_code, 400)

    def test_successful_update(self):
        """Test for successful request update"""
        description = ("The description. This is the description. "
                       "The description. This is the description. "
                       "The description. This is the description. ")
        create_request(
            self,
            "This is the request title. Short and descriptive",
            description,
            "test@user.com"
        )
        with self.client:
            description = ("Update description. This is the description. "
                           "Update description. This is the description. "
                           "Update description. This is the description. ")
            response = update_request(
                self,
                "This is the request title. Short and descriptive",
                description
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_error_update(self):
        """Test for validation errors when updating request"""
        # Create a request
        description = ("The description. This is the description. "
                       "The description. This is the description. "
                       "The description. This is the description. ")
        create_request(
            self,
            "This is the request title. Short and descriptive",
            description,
            "test@user.com"
        )
        with self.client:
            description = ("Update description. This is the description.")
            response = update_request(
                self,
                "This is the request title. Short and descriptive",
                description
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 422)

    def test_update_id_notexist(self):
        """Test if request id is not present"""
        access_token = create_access_token('anotherone@user.com')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = self.client.put(
            '/api/v1/users/requests/23383837', headers=headers)

        self.assertEqual(response.status_code, 404)

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

    def test_successful_getall_requests(self):
        """Test for successful request submission"""
        with self.client:
            create_request(
                self,
                "This is the request title. Short and descriptive",
                "The description. It has lengths that need to be adhered to. The description. It has lengths that need to be adhered to. The description. It has lengths that need to be adhered to. The description. It has lengths that need to be adhered to.",
                "user@mail.co"
            )
            access_token = create_access_token('test@user.com')
            headers = {
                'Authorization': 'Bearer {}'.format(access_token)
            }
            response = self.client.get(
                '/api/v1/users/requests', headers=headers)
            self.assertEqual(response.status_code, 200)

    def test_get_no_id(self):
        """Test for getting request which id donesn't exist"""

        access_token = create_access_token('anotheruser@user.com')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = self.client.get(
            '/api/v1/users/requests/2334', headers=headers)

        self.assertEqual(response.status_code, 404)

    def test_request_exist(self):
        """Test for existing request by specific id"""

        access_token = create_access_token('test@user.com')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = self.client.get(
            '/api/v1/users/requests/1', headers=headers)

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
