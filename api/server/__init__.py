#! /api/server/__init__.py
# -*- coding: utf-8 -*-
"""This is the core module

This module does imports flask framework, initializes it and passes the
initialized flask object to various modules and extensions.
"""

# the os module provides a portable way of using operating system dependent
# functionality
import os

# python microframework
from flask import Flask

# provides bcrypt hashing utilities for our application
from flask_bcrypt import Bcrypt
# Mail
from flask_mail import Mail, Message
# TOKEN
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)

# making cross-origin AJAX possible
from flask_cors import CORS
from flasgger import Swagger

# instanciate Flask
APP = Flask(__name__)

# initialize the Flask-Cors extension with default arguments in order
# to allow CORS for all domains on all routes
CORS(APP)

# os.getenv -> return the value of the environment variable
APP_SETTINGS = os.getenv(
    'APP_SETTINGS',
    'api.server.config.DevelopmentConfig'
)
# retreiving config stored in separate files (config.py)
APP.config.from_object(APP_SETTINGS)

# pass flask app object to Bcrypt
BCRYPT = Bcrypt(APP)
MAIL = Mail(APP)
JWT = JWTManager(APP)
SWAG = Swagger(
    APP,
    template={
        "swagger": "2.0",
        "uiversion": 2,
        "info": {
            "title": "M-Tracker - Docs",
            "version": "1.0",
        },
        "consumes": [
            "application/x-www-form-urlencoded",
        ],
        "produces": [
            "application/json",
        ],
    },
)


@JWT.user_claims_loader
def add_claims_to_access_token(user):
    """Function that will be called whenever create_access_token is used"""
    return {'role': user["user_level"]}


@JWT.user_identity_loader
def user_identity_lookup(user):
    """Define token identity"""
    return user["user_id"]


# import auth blueprints
from api.server.auth.views import AUTH_BLUEPRINT  # noqa  # pylint: disable=C0413
from api.server.request.views import REQUEST_BLUEPRINT  # noqa  # pylint: disable=C0413
from api.server.admin.views import ADMIN_BLUEPRINT  # noqa  # pylint: disable=C0413

# Register Blueprints
APP.register_blueprint(AUTH_BLUEPRINT)
APP.register_blueprint(REQUEST_BLUEPRINT)
APP.register_blueprint(ADMIN_BLUEPRINT)
