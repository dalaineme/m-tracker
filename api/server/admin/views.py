#! /api/server/admin/views.py
# -*- coding: utf-8 -*-
"""This is the admin module
This module contains various routes for the admin endpoint
"""
from functools import wraps
from flask import Blueprint, jsonify, make_response
from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required, get_jwt_claims
)
from api.server.admin.models import all_user_requests

# Create a blueprint
ADMIN_BLUEPRINT = Blueprint('admin', __name__, url_prefix='/api/v1/')


def admin_only(admin):
    """Admin only decorator function"""
    @wraps(admin)
    def wrapped(*args, **kwargs):
        """wrapped method"""
        user_level = get_jwt_claims()["role"]
        if user_level != "Admin":
            # return response
            response_object = {
                "msg": "Insufficient access rights"
            }
            return make_response(jsonify(response_object)), 403
        return admin(*args, **kwargs)
    return wrapped


class AdminAPI(MethodView):
    """User Signup resource"""
    @jwt_required
    @admin_only
    def get(self):  # pylint: disable=R0201
        """post method"""

        # Get the requests
        get_data = all_user_requests()
        if get_data:
            # return response
            response_object = {
                "status": 'success',
                "all_requests": get_data
            }
            return make_response(jsonify(response_object)), 200
        response_object = {
            "status": 'fail',
            "msg": 'No requests found.'
        }
        return make_response(jsonify(response_object)), 404


# define API resources
ADMIN_VIEW = AdminAPI.as_view('admin_view')

# add rules for auth enpoints
ADMIN_BLUEPRINT.add_url_rule(
    '/requests',
    view_func=ADMIN_VIEW,
    methods=['POST', 'GET', 'PUT']
)
