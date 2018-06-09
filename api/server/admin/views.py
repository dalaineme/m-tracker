#! /api/server/admin/views.py
# -*- coding: utf-8 -*-
"""This is the admin module
This module contains various routes for the admin endpoint
"""

from flask import Blueprint
from flask.views import MethodView

# Create a blueprint
ADMIN_BLUEPRINT = Blueprint('admin', __name__, url_prefix='/api/v1/')


class AdminAPI(MethodView):
    """User Signup resource"""

    def get(self):  # pylint: disable=R0201
        """post method"""
        return "working", 200


# define API resources
ADMIN_VIEW = AdminAPI.as_view('admin_view')

# add rules for auth enpoints
ADMIN_BLUEPRINT.add_url_rule(
    '/requests',
    view_func=ADMIN_VIEW,
    methods=['POST', 'GET', 'PUT']
)
