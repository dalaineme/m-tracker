#! /api/server/models.py
# -*- coding: utf-8 -*-
"""Contains the schema for the auth endpoint

Marshmallow validation with wtforms
"""


class User(object):  # pylint: disable=too-few-public-methods
    """ User Model for storing user related details """

    def __init__(self, first_name, last_name, email, password):
        self.is_admin = 'False'
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
