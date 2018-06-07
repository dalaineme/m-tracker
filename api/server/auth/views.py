#! /api/server/auth/views.py
# -*- coding: utf-8 -*-
"""This is the auth module
This module contains various routes for the auth endpoint
"""

from flask import Blueprint, make_response, jsonify, request
from flask.views import MethodView

from api.server.auth.models import signup_user
from api.server.helpers import json_fetch_all

# Create a blueprint
AUTH_BLUEPRINT = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


class SignupAPI(MethodView):
    """User Signup resource"""

    def post(self):  # pylint: disable=R0201
        """post method"""
        # get the post data
        post_data = request.get_json()

        # check for no input i.e. {}
        if not post_data:
            response_object = {
                'status': 'fail',
                'msg': 'No input data provided.'
            }
            return make_response(jsonify(response_object)), 400
        # Store user input in variables
        input_first_name = post_data.get('first_name')
        input_last_name = post_data.get('last_name')
        input_email = post_data.get('email')
        input_password = post_data.get('password')

        signup_user(input_first_name, input_last_name,
                    input_email, input_password)
        # return response
        response_object = {
            "status": 'success',
            "msg": "Account for '{}' has been created.".format(
                input_email),
            "user": {
                "first_name": input_first_name,
                "last_name": input_last_name,
                "email": input_email
            }

        }
        return make_response(jsonify(response_object)), 201

    def get(self):
        """Test GET method"""
        result = json_fetch_all("SELECT * FROM tbl_users")
        return result


# define API resources
SIGNUP_VIEW = SignupAPI.as_view('signup_api')


# add rules for auth enpoints
AUTH_BLUEPRINT.add_url_rule(
    '/signup',
    view_func=SIGNUP_VIEW,
    methods=['POST', 'GET']
)
