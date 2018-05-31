#! /api/server/models.py
# -*- coding: utf-8 -*-
"""Contains the schema for the auth endpoint

Use data structures for storage
"""
from api.server import APP, BCRYPT

# Users
USERS_LIST = []
# Blacklist Tokens
BLACKLIST = set()


class User(object):  # pylint: disable=too-few-public-methods
    """ User Model for storing user related details """

    def __init__(self, first_name, last_name, email, password):
        self.is_admin = 'False'
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password


def save(data):
    """User instance appending"""
    data['user_id'] = len(USERS_LIST) + 1
    data['password'] = BCRYPT.generate_password_hash(
        data['password'], APP.config.get('BCRYPT_LOG_ROUNDS')
    ).decode()
    data['first_name'] = data['first_name'].title()
    data['last_name'] = data['last_name'].title()
    # save to list
    USERS_LIST.append(data)


def check_email(search_email):
    """Check if email exists in USERS_LIST"""
    for find_email in USERS_LIST:
        if find_email['email'] == search_email:
            return True
    return False


def check_email_for_login(search_email):
    """Return user email"""
    for find_email in USERS_LIST:
        if find_email['email'] == search_email:
            return find_email


def login(data):
    """Login method"""
    # Get user dictionary, assign it to variable
    logging_user_details = check_email_for_login(data['email'])
    if BCRYPT.check_password_hash(logging_user_details['password'],
                                  data['password']):
        # compare password input to saved password
        return True
    return False
