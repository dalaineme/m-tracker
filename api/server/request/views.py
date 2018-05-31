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

from api.server.request.schema import RequestSchema
from api.server.models import save_request, all_user_requests

# Create a blueprint
REQUEST_BLUEPRINT = Blueprint('request', __name__, url_prefix='/api/v1/users/')

# Instanciate marshmallow shemas
REQUEST_SCHEMA = RequestSchema()


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
    def get(self):  # pylint: disable=R0201
        """Send GET method to requests endpoint"""
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


# define API resources
REQUESTS_VIEW = RequestsAPI.as_view('requests_api')

# add rules for auth enpoints
REQUEST_BLUEPRINT.add_url_rule(
    '/requests',
    view_func=REQUESTS_VIEW,
    methods=['POST', 'GET']
)
