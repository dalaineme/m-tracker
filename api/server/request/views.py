#! /api/server/request/views.py
# -*- coding: utf-8 -*-
"""This is the request module
This module contains various routes for the request endpoint
"""

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from marshmallow import ValidationError
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from api.server.request.schema import RequestSchema, ModifyRequestSchema
from api.server.request.models import (
    create_request, all_user_requests, get_request_by_id, modify_user_request,
    delete_request)

# Create a blueprint
REQUEST_BLUEPRINT = Blueprint('request', __name__, url_prefix='/api/v1/users/')

# Instanciate marshmallow shemas
REQUEST_SCHEMA = RequestSchema()
MODIFY_REQUEST_SCHEMA = ModifyRequestSchema()


class RequestsAPI(MethodView):
    """User Logout resource"""
    @jwt_required
    def post(self):  # pylint: disable=R0201
        """Send POST method to requests endpoint"""

        # get the post data
        post_data = request.get_json()

        # load input to the marshmallow schema
        try:
            REQUEST_SCHEMA.load(post_data)

        # return error object case there is any
        except ValidationError as err:
            response_object = {
                'status': 'fail',
                'msg': 'Validation errors.',
                'errors': err.messages
            }
            return make_response(jsonify(response_object)), 422

        # If no validation errors
        current_user = get_jwt_identity()
        # Get input data as dictionary

        input_title = post_data.get('title')
        input_desc = post_data.get('description')
        user_id = current_user

        # save the data into a list
        create_request(input_title, input_desc, user_id)

        response_object = {
            "status": 'success',
            "msg": "Request successfully sent to the admin."
        }
        return make_response(jsonify(response_object)), 201

    @jwt_required
    def get(self, request_id=None):  # pylint: disable=R0201
        """Send GET method to requests endpoint"""
        if not request_id:
            # get current user id
            user_id = get_jwt_identity()
            # Get the requests
            get_data = all_user_requests(user_id)
            if get_data:
                # return response
                response_object = {
                    "status": 'success',
                    "my_requests": get_data
                }
                return make_response(jsonify(response_object)), 200
            response_object = {
                "status": 'fail',
                "msg": 'You have no requests.'
            }
            return make_response(jsonify(response_object)), 404
        else:
            user_id = get_jwt_identity()
            specific_request = get_request_by_id(user_id, request_id)
            # If request id not found
            if specific_request == "fail":
                response_object = {
                    "status": 'fail',
                    "message": "Request ID not found."
                }
                return make_response(jsonify(response_object)), 404
            # If request ID exists
            response_object = {
                "status": 'success',
                "request": specific_request
            }
            return make_response(jsonify(response_object)), 200

    @jwt_required
    def put(self, request_id=None):  # pylint: disable=R0201
        """Send PUT method to requests endpoint"""
        user_id = get_jwt_identity()
        specific_request = get_request_by_id(user_id, request_id)
        # If request id not found
        if specific_request == "fail":
            response_object = {
                "status": 'fail',
                "msg": "Request ID not found."
            }
            return make_response(jsonify(response_object)), 404
        # If request ID exists
        # get the post data
        post_data = request.get_json()

        # load input to the marshmallow schema
        try:
            MODIFY_REQUEST_SCHEMA.load(post_data)

        # return error object case there is any
        except ValidationError as err:
            response_object = {
                'status': 'fail',
                'msg': 'Validation errors.',
                'errors': err.messages
            }
            return make_response(jsonify(response_object)), 422
        # Assign post data to variables
        title = post_data["title"]
        description = post_data["description"]
        result = modify_user_request(user_id, request_id, title, description)
        if result == "fail":
            response_object = {
                "status": 'fail',
                "msg": "You can only modify a sent request."
            }
            return make_response(jsonify(response_object)), 401

        response_object = {
            "status": 'success',
            "msg": "Your request has been updated."
        }
        return make_response(jsonify(response_object)), 201

    @jwt_required
    def delete(self, request_id=None):  # pylint: disable=R0201
        """Send DELETE method to requests endpoint"""
        user_id = get_jwt_identity()
        specific_request = get_request_by_id(user_id, request_id)
        # If request id not found
        if specific_request == "fail":
            response_object = {
                "status": 'fail',
                "msg": "Request ID not found."
            }
            return make_response(jsonify(response_object)), 404
        result = delete_request(user_id, request_id)
        if result == "fail":
            response_object = {
                "status": 'fail',
                "msg": "You can not delete an Approved request."
            }
            return make_response(jsonify(response_object)), 403
        # Successful deletion
        response_object = {
            "status": 'success',
            "msg": "Your request has been deleted."
        }
        return make_response(jsonify(response_object)), 201


# define API resources
REQUESTS_VIEW = RequestsAPI.as_view('requests_api')

# add rules for request enpoints
REQUEST_BLUEPRINT.add_url_rule(
    '/requests',
    view_func=REQUESTS_VIEW,
    methods=['POST', 'GET']
)
REQUEST_BLUEPRINT.add_url_rule(
    '/requests/<int:request_id>',
    view_func=REQUESTS_VIEW,
    methods=['GET', 'PUT', 'DELETE']
)
