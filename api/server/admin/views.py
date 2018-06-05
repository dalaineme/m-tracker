#! /api/server/request/views.py
# -*- coding: utf-8 -*-
"""This is the users module

This module contains various routes for the users endpoint
"""

from flask import Blueprint
from flask.views import MethodView

# Create a blueprint
USERS_BLUEPRINT = Blueprint('request', __name__, url_prefix='/api/v1/users/')


class UsersAPI(MethodView):
    """Users resource"""

    def post(self):  # pylint: disable=R0201
        """Send POST method to requests endpoint"""
        pass

    def get(self, request_id=None):  # pylint: disable=R0201
        """Send GET method to requests endpoint"""
        pass

    def put(self, request_id=None):  # pylint: disable=R0201
        """Send PUT method to requests endpoint"""
        pass

    def delete(self, request_id=None):  # pylint: disable=R0201
        """Send DELETE method to requests endpoint"""
        pass


# define API resources
USERS_VIEW = UsersAPI.as_view('users_api')

# add rules for request enpoints
USERS_BLUEPRINT.add_url_rule(
    '/requests',
    view_func=USERS_VIEW,
    methods=['POST', 'GET']
)
USERS_BLUEPRINT.add_url_rule(
    '/requests/<int:request_id>',
    view_func=USERS_VIEW,
    methods=['GET', 'PUT', 'DELETE']
)
