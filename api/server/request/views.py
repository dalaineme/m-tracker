#! /api/server/request/views.py
# -*- coding: utf-8 -*-
"""This is the request module

This module contains various routes for the request endpoint
"""

from flask import Blueprint, make_response, jsonify
from flask.views import MethodView

# Create a blueprint
REQUEST_BLUEPRINT = Blueprint('request', __name__, url_prefix='/api/v1/users/')


class RequestsAPI(MethodView):
    """User Logout resource"""

    def post(self):  # pylint: disable=R0201
        """Send GET method to logout endpoint"""
        response_object = {
            "status": 'success',
            "message": "Request successfully sent to the admin."
        }
        return make_response(jsonify(response_object)), 201


# define API resources
REQUESTS_VIEW = RequestsAPI.as_view('requests_api')

# add rules for auth enpoints
REQUEST_BLUEPRINT.add_url_rule(
    '/requests',
    view_func=REQUESTS_VIEW,
    methods=['POST']
)
