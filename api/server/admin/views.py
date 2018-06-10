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
from flasgger.utils import swag_from
from api.server.admin.models import (
    all_user_requests, approve_request, dissaprove_request, resolve_request)

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


@ADMIN_BLUEPRINT.route('requests/<int:request_id>/approve', methods=['PUT'])
@jwt_required
@admin_only
@swag_from('documentation/approve_request.yml', methods=['PUT'])
def admin_approve_request(request_id=None):
    """Approve request method"""
    result = approve_request(request_id)
    if result == "no_id":
        # return response
        response_object = {
            "status": 'fail',
            "msg": "Request ID not found."
        }
        return make_response(jsonify(response_object)), 404
    if result:
        # return response
        response_object = {
            "status": 'success',
            "msg": "Request has been successfully Approved.",
            "request": result
        }
        return make_response(jsonify(response_object)), 201
    # If not approve
    response_object = {
        "status": 'fail',
        "msg": "You can only approve a pending request"
    }
    return make_response(jsonify(response_object)), 401


@ADMIN_BLUEPRINT.route('requests/<int:request_id>/disapprove', methods=['PUT'])
@jwt_required
@admin_only
@swag_from('documentation/disapprove_request.yml', methods=['PUT'])
def admin_disapprove_request(request_id=None):
    """Approve request method"""
    result = dissaprove_request(request_id)
    if result == "no_id":
        # return response
        response_object = {
            "status": 'fail',
            "msg": "Request ID not found."
        }
        return make_response(jsonify(response_object)), 404
    if result == "already_dissaproved":
        # return response
        response_object = {
            "status": 'fail',
            "msg": "Request has already been Dissaproved."
        }
        return make_response(jsonify(response_object)), 403
    if result:
        # return response
        response_object = {
            "status": 'success',
            "msg": "Request has been successfully Dissaproved.",
            "request": result
        }
        return make_response(jsonify(response_object)), 201
    # If not approve
    response_object = {
        "status": 'fail',
        "msg": "You can not dissaprove a Resolved request"
    }
    return make_response(jsonify(response_object)), 403


@ADMIN_BLUEPRINT.route('requests/<int:request_id>/resolve', methods=['PUT'])
@jwt_required
@admin_only
@swag_from('documentation/resolve_request.yml', methods=['PUT'])
def admin_resolve_request(request_id=None):
    """Resolve request method"""
    result = resolve_request(request_id)
    if result == "no_id":
        # return response
        response_object = {
            "status": 'fail',
            "msg": "Request ID not found."
        }
        return make_response(jsonify(response_object)), 404
    if result == "already_resolved":
        # return response
        response_object = {
            "status": 'fail',
            "msg": "Request has already been Resolved."
        }
        return make_response(jsonify(response_object)), 403
    if result:
        # return response
        response_object = {
            "status": 'success',
            "msg": "Request has been successfully Resolved.",
            "request": result
        }
        return make_response(jsonify(response_object)), 201
    # If not approve
    response_object = {
        "status": 'fail',
        "msg": "You can only Resolve an Approved request"
    }
    return make_response(jsonify(response_object)), 403


class AdminAPI(MethodView):
    """User Signup resource"""
    @jwt_required
    @admin_only
    @swag_from('documentation/get_requests.yml', methods=['GET'])
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
    methods=['GET']
)
