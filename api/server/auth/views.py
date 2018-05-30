#! /api/server/auth/views.py
# -*- coding: utf-8 -*-
"""This is the auth module

This module contains various routes for the auth endpoint
"""
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

# create a blueprint for /auth route
AUTH_BLUEPRINT = Blueprint('auth', __name__, url_prefix='/auth/v1')


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def post(self):
        """POST method for registration route"""
        # get the post data
        post_data = request.get_json(force=True)
        data = {
            'first_name': post_data['first_name'],
            'last_name': post_data['last_name'],
            'email': post_data['email'],
            'password': post_data['password']
        }

        responseObject = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return make_response(jsonify(responseObject)), 201


# define the API resources
REGISTRATION_VIEW = RegisterAPI.as_view('register_api')


# add Rules for API Endpoints
AUTH_BLUEPRINT.add_url_rule(
    '/register',
    view_func=REGISTRATION_VIEW,
    methods=['POST']
)
