#! /api/server/auth/views.py
# -*- coding: utf-8 -*-
"""This is the auth module

This module contains various routes for the auth endpoint
"""

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from marshmallow import ValidationError
from flask_jwt_extended import (create_access_token)

from api.server.auth.schema import UserSchema, LoginSchema
from api.server.models import save, check_email, login

# Create a blueprint
AUTH_BLUEPRINT = Blueprint('auth', __name__, url_prefix='/api/v1/users')

# Instanciate marshmallow
USER_SCHEMA = UserSchema()
LOGIN_SCHEMA = LoginSchema()


class RegisterAPI(MethodView):
    """User Registration resource"""

    def post(self):  # pylint: disable=R0201
        """post method"""
        # get the post data
        post_data = request.get_json()

        # check for no input i.e. {}
        if not post_data:
            response_object = {
                'status': 'fail',
                'message': 'No input data provided.'
            }
            return make_response(jsonify(response_object)), 400
        # load input to the marshmallow schema
        try:
            USER_SCHEMA.load(post_data)

        # return error object case there is any
        except ValidationError as err:
            response_object = {
                'status': 'fail',
                'message': 'Validation errors.',
                'errors': err.messages
            }
            return make_response(jsonify(response_object)), 422

        input_email = post_data.get('email')
        # check if email exists
        if check_email(input_email):
            response_object = {
                'status': 'fail',
                'message': "Sorry, email '{}' already exists.".format(
                    input_email)
            }
            return make_response(jsonify(response_object)), 400
        # if no validation errors
        # Get input data as dictionary
        data = {
            "first_name": post_data.get('first_name'),
            "last_name": post_data.get('last_name'),
            "email": post_data.get('email'),
            "password": post_data.get('password')
        }
        # save the data into a list
        save(data)
        # return response
        response_object = {
            "status": 'success',
            "message": "Account for '{}' has been created.".format(
                data["email"])
        }
        return make_response(jsonify(response_object)), 201


class LoginAPI(MethodView):
    """User Login resource"""

    def post(self):  # pylint: disable=R0201
        """post method"""
        # get the post data
        post_data = request.get_json()

        # load input to the marshmallow schema
        try:
            LOGIN_SCHEMA.load(post_data)

        # return error object case there is any
        except ValidationError as err:
            response_object = {
                'status': 'fail',
                'message': 'Validation errors.',
                'errors': err.messages
            }
            return make_response(jsonify(response_object)), 422

        # Get email
        input_email = post_data.get('email')
        # check if email exists
        if not check_email(input_email):
            response_object = {
                'status': 'fail',
                'message': "Sorry, email '{}' does not exist.".format(
                    input_email)
            }
            return make_response(jsonify(response_object)), 400

        # If no validation errors
        # Get input data as dictionary
        data = {
            "email": post_data.get('email'),
            "password": post_data.get('password')
        }
        # If login is successful
        if login(data):
            access_token = create_access_token(identity=data["email"])
            response_object = {
                "status": 'success',
                "message": "Successfully logged in.",
                "token": access_token
            }
            return make_response(jsonify(response_object)), 200
        # Failed login - password
        response_object = {
            "status": 'fail',
            "message": "Wrong login credentials."
        }
        return make_response(jsonify(response_object)), 422


# define API resources
REGISTRATION_VIEW = RegisterAPI.as_view('register_api')
LOGIN_VIEW = LoginAPI.as_view('login_api')

# add rules for auth enpoints
AUTH_BLUEPRINT.add_url_rule(
    '/register',
    view_func=REGISTRATION_VIEW,
    methods=['POST']
)
AUTH_BLUEPRINT.add_url_rule(
    '/login',
    view_func=LOGIN_VIEW,
    methods=['POST']
)
