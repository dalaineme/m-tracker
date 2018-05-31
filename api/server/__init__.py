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

# TOKEN
from flask_jwt_extended import JWTManager

# making cross-origin AJAX possible
from flask_cors import CORS

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
JWT = JWTManager(APP)

# import auth blueprint and register it
from api.server.auth.views import AUTH_BLUEPRINT
APP.register_blueprint(AUTH_BLUEPRINT)
