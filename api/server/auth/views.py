#! /api/server/auth/views.py
# -*- coding: utf-8 -*-
"""This is the admin module

This module contains various routes for the admin endpoint
"""

from flask import Blueprint
from flask.views import MethodView

# Create a blueprint
ADMIN_BLUEPRINT = Blueprint('admin', __name__, url_prefix='/')


class RequestsAPI(MethodView):
    """Admin requests resource"""

    def get(self):  # pylint: disable=R0201
        """post method"""
        pass

    def put(self):  # pylint: disable=R0201
        """post method"""
        pass


# define API resources
REQUESTS_VIEW = RequestsAPI.as_view('requests_api')

# add rules for auth enpoints
ADMIN_BLUEPRINT.add_url_rule(
    '/requests',
    view_func=ADMIN_BLUEPRINT,
    methods=['GET', 'PUT']
)
