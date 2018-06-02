#! /api/server/models.py
# -*- coding: utf-8 -*-
"""Contains the schema for the auth endpoint

Use data structures for storage
"""
import datetime
from api.server import APP, BCRYPT

# Users
USERS_LIST = []

# Reqeusts
REQUESTS_LIST = []

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


class Request(object):  # pylint: disable=too-few-public-methods
    """Request model for storing user requests"""

    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.email = ''


# Helper methods
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


def save_request(data):
    """Add request to list"""
    data['request_id'] = len(REQUESTS_LIST) + 1
    data['date_created'] = datetime.datetime.now()
    # save to list
    REQUESTS_LIST.append(data)


def all_user_requests(user_email):
    """Method to gett all user request based on their email"""
    request = [
        request for request in REQUESTS_LIST if request["email"] == user_email]
    return request


def get_request_by_id(user_email, request_id):
    """Method to update a previous request"""
    # call the all requests method
    dicts = all_user_requests(user_email)
    result = next(
        (item for item in dicts if item["request_id"] == request_id), False)
    return result


def modify_user_request(user_email, request_id, title, description):
    """Method that modifies a request"""
    result = get_request_by_id(user_email, request_id)
    result['title'] = title
    result['description'] = description
    result['date_updated'] = datetime.datetime.now()


def delete_user_request(user_email, request_id):
    """Method that deletes a user request by id"""
    result = get_request_by_id(user_email, request_id)
    # remove from list
    REQUESTS_LIST.remove(result)


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
