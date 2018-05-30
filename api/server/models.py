#! /api/server/models.py
# -*- coding: utf-8 -*-
"""Contains the schema for the auth endpoint

Use data structures for storage
"""

from werkzeug.security import generate_password_hash

# Users
USERS_LIST = []


class User(object):  # pylint: disable=too-few-public-methods
    """ User Model for storing user related details """

    def __init__(self, first_name, last_name, email, password):
        self.is_admin = 'False'
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def set_password(self, password):
        """Generate encrypted password"""
        self.password = generate_password_hash(password)

    def save(self):
        """User instance appending"""
        USERS_LIST.append(self)
