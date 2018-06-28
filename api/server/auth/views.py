#! /api/server/auth/views.py
# -*- coding: utf-8 -*-
"""This is the auth module
This module contains various routes for the auth endpoint
"""

from flask import Blueprint, make_response, jsonify, request, url_for
from flask.views import MethodView
from marshmallow import ValidationError
from flask_jwt_extended import (create_access_token)
from flasgger.utils import swag_from
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from api.server import MAIL
from api.server.auth.models import signup_user, login_user, email_exists, get_user_info
from api.server.auth.schema import UserSchema, LoginSchema

# Create a blueprint
AUTH_BLUEPRINT = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

# Instanciate marshmallow shemas
USER_SCHEMA = UserSchema()
LOGIN_SCHEMA = LoginSchema()

s = URLSafeTimedSerializer('Thisisasecret!')


class SignupAPI(MethodView):
    """User Signup resource"""
    @swag_from('documentation/register.yml', methods=['POST'])
    def post(self):  # pylint: disable=R0201
        """POST method"""
        # get the post data
        post_data = request.get_json()

        # check for no input i.e. {}
        if not post_data:
            response_object = {
                'status': 'fail',
                'msg': 'No input data provided.'
            }
            return make_response(jsonify(response_object)), 400

        try:
            USER_SCHEMA.load(post_data)

        # return error object case there is any
        except ValidationError as err:
            response_object = {
                'status': 'fail',
                'msg': 'Validation errors.',
                'errors': err.messages
            }
            return make_response(jsonify(response_object)), 422
        # Store user input in variables
        input_first_name = post_data.get('first_name')
        input_last_name = post_data.get('last_name')
        input_email = post_data.get('email')
        input_password = post_data.get('password')

        if email_exists(input_email):
            response_object = {
                "status": "fail",
                "msg": "Sorry! Email '{}' already exists.".format(
                    input_email)
            }
            return make_response(jsonify(response_object)), 422
        token = s.dumps(input_email, salt='email-confirm')
        msg = Message(
            'Confirm Email', sender='mcdalinoluoch@gmail.com',
            recipients=[input_email]
        )
        link = url_for('.confirm_email',
                       token=token, _external=True)
        msg.body = 'Your link is {}'.format(link)
        MAIL.send(msg)
        signup_user(input_first_name, input_last_name,
                    input_email, input_password, "User")
        # return response
        response_object = {
            "status": 'success',
            "msg": "Account for '{}' has been created.".format(
                input_email),
            "user": {
                "first_name": input_first_name,
                "last_name": input_last_name,
                "email": input_email
            }

        }
        return make_response(jsonify(response_object)), 201


class LoginAPI(MethodView):
    """User Login resource"""
    @swag_from('documentation/login.yml', methods=['POST'])
    def post(self):  # pylint: disable=R0201
        """post method"""
        # get the post data
        post_data = request.get_json()

        # load input to the marshmallow schema
        try:
            LOGIN_SCHEMA.load(post_data)

        # return error object case there is any
        except ValidationError as err:
            response_object = {
                'status': 'fail',
                'msg': 'Validation errors.',
                'errors': err.messages
            }
            return make_response(jsonify(response_object)), 422

        # Store input in variables
        input_email = post_data.get('email')
        input_password = post_data.get('password')
        # check if email exists
        if not email_exists(input_email):
            response_object = {
                'status': 'fail',
                'msg': "Sorry, email '{}' does not exist.".format(
                    input_email)
            }
            return make_response(jsonify(response_object)), 400

        # If no validation errors
        # If login is successful
        user_info = login_user(input_email, input_password)
        if not user_info:
            # Failed login - password
            response_object = {
                "status": "fail",
                "msg": "Invalid login credentials."
            }
            return make_response(jsonify(response_object)), 401
        # Create a UserObject for tokens422
        user = {
            "user_id": user_info["user_id"],
            "user_level": user_info["user_level"]
        }
        access_token = create_access_token(identity=user)
        response_object = {
            "status": 'success',
            "user_level": user_info["user_level"],
            "msg": "Successfully logged in.",
            "token": "Bearer {}".format(access_token)
        }
        return make_response(jsonify(response_object)), 200


class ConfirmEmail(MethodView):
    """Confirm email"""

    def get(self, token):  # pylint: disable=R0201
        """Get method"""
        try:
            s.loads(
                token, salt='email-confirm', max_age=3600)
        except SignatureExpired:
            return '<h1>The token is expired!</h1>'
        return '<h1>The token works!</h1>'


class UserAPI(MethodView):
    """User API"""
    @jwt_required
    @swag_from('documentation/user.yml', methods=['GET'])
    def get(self):  # pylint: disable=R0201
        """Get all user details"""
        user_id = get_jwt_identity()
        user_info = get_user_info(user_id)
        response_object = {
            "status": 'success',
            "result": user_info
        }
        return make_response(jsonify(response_object)), 200



# define API resources
SIGNUP_VIEW = SignupAPI.as_view('signup_api')
LOGIN_VIEW = LoginAPI.as_view('login_api')
CONFIRM_EMAIL_VIEW = ConfirmEmail.as_view('comfirm_email')
USER_VIEW = UserAPI.as_view('user_api')

# add rules for auth enpoints
AUTH_BLUEPRINT.add_url_rule(
    '/signup',
    view_func=SIGNUP_VIEW,
    methods=['POST']
)
AUTH_BLUEPRINT.add_url_rule(
    '/login',
    view_func=LOGIN_VIEW,
    methods=['POST']
)
AUTH_BLUEPRINT.add_url_rule(
    '/confirm_email/<token>',
    endpoint="confirm_email",
    view_func=CONFIRM_EMAIL_VIEW,
    methods=['GET']
)
AUTH_BLUEPRINT.add_url_rule(
    '/user',
    view_func=USER_VIEW,
    methods=['GET']
)
