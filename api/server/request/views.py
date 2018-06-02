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
from api.server.models import (
    save_request, all_user_requests, get_request_by_id, modify_user_request,
    delete_user_request)

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
                'message': 'Validation errors.',
                'errors': err.messages
            }
            return make_response(jsonify(response_object)), 422

        # If no validation errors
        current_user = get_jwt_identity()
        # Get input data as dictionary
        data = {
            "title": post_data.get('title'),
            "description": post_data.get('description'),
            "email": current_user
        }
        # save the data into a list
        save_request(data)
        # return response
        response_object = {
            "status": 'success',
            "message": "Request successfully sent to the admin."
        }
        return make_response(jsonify(response_object)), 201

    @jwt_required
    def get(self, request_id=None):  # pylint: disable=R0201
        """Send GET method to requests endpoint"""
        if not request_id:
            # get current email
            current_user = get_jwt_identity()
            if all_user_requests(current_user):
                get_data = all_user_requests(current_user)
                # return response
                response_object = {
                    "status": 'success',
                    "requests": get_data
                }
                return make_response(jsonify(response_object)), 200
            # if empty
            # return response
            response_object = {
                "status": 'fail',
                "message": "You have no requests."
            }
            return make_response(jsonify(response_object)), 400

        else:
            current_user = get_jwt_identity()
            specific_request = get_request_by_id(current_user, request_id)
            # If request id not found
            if not specific_request:
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
        current_user = get_jwt_identity()
        specific_request = get_request_by_id(current_user, request_id)
        # If request id not found
        if not specific_request:
            response_object = {
                "status": 'fail',
                "message": "Request ID not found."
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
                'message': 'Validation errors.',
                'errors': err.messages
            }
            return make_response(jsonify(response_object)), 422
        # Assign post data to variables
        title = post_data["title"]
        description = post_data["description"]
        modify_user_request(current_user, request_id, title, description)
        response_object = {
            "status": 'success',
            "message": "Your request has been updated."
        }
        return make_response(jsonify(response_object)), 201

    @jwt_required
    def delete(self, request_id=None):  # pylint: disable=R0201
        """Send DELETE method to requests endpoint"""
        current_user = get_jwt_identity()
        specific_request = get_request_by_id(current_user, request_id)
        # If request id not found
        if not specific_request:
            response_object = {
                "status": 'fail',
                "message": "Request ID not found."
            }
            return make_response(jsonify(response_object)), 404
        # If request ID exists
        delete_user_request(current_user, request_id)
        response_object = {
            "status": 'success',
            "message": "Request has been deleted."
        }
        return make_response(jsonify(response_object)), 200


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
