#! /api/server/models.py
# -*- coding: utf-8 -*-
"""This is the auth modules

This module contains functions that are used in the auth endpoint
"""
from api.server import APP, BCRYPT
from api.server.helpers import run_query


def signup_user(first_name, last_name, email, password):
    """Create a new user account"""
    # encrypt the password
    hash_password = BCRYPT.generate_password_hash(
        password, APP.config.get('BCRYPT_LOG_ROUNDS')
    ).decode()
    # capitalize first letter
    first_name = first_name.title()
    last_name = last_name.title()
    # query and the user inputs
    query = u"INSERT INTO tbl_users (first_name, last_name, email, password, user_level) VALUES (%s, %s, %s, %s, %s);"
    inputs = first_name, last_name, email, hash_password, "User"
    # run query
    run_query(query, inputs)
