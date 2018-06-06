#! /api/server/auth/views.py
# -*- coding: utf-8 -*-
"""This is the auth module
This module contains various routes for the auth endpoint
"""

from flask import Blueprint
from flask.views import MethodView


# Create a blueprint
AUTH_BLUEPRINT = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


class SignupAPI(MethodView):
    """User Signup resource"""

    def get(self):  # pylint: disable=R0201
        """post method"""
        return 'working', 200


# define API resources
SIGNUP_VIEW = SignupAPI.as_view('signup_api')


# add rules for auth enpoints
AUTH_BLUEPRINT.add_url_rule(
    '/signup',
    view_func=SIGNUP_VIEW,
    methods=['GET']
)
