#! /api/server/request/views.py
# -*- coding: utf-8 -*-
"""This is the request module

This module contains various routes for the request endpoint
"""

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from marshmallow import ValidationError
from api.server.request.schema import RequestSchema

# Create a blueprint
REQUEST_BLUEPRINT = Blueprint('request', __name__, url_prefix='/api/v1/users/')

# Instanciate marshmallow shemas
REQUEST_SCHEMA = RequestSchema()


class RequestsAPI(MethodView):
    """User Logout resource"""

    def post(self):  # pylint: disable=R0201
        """Send GET method to logout endpoint"""

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
