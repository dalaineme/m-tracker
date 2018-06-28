#! /api/server/models.py
# -*- coding: utf-8 -*-
"""This is the auth modules
This module contains functions that are used in the auth endpoint
"""
from api.server import APP, BCRYPT
from api.server.helpers import run_query, get_query


def signup_user(first_name, last_name, email, password, level):
    """Create a new user account"""
    # encrypt the password
    hash_password = BCRYPT.generate_password_hash(
        password, APP.config.get('BCRYPT_LOG_ROUNDS')
    ).decode()
    # capitalize first letter
    first_name = first_name.title()
    last_name = last_name.title()
    # query and the user inputs
    query = (u"INSERT INTO tbl_users (first_name, last_name, email, password, "
             "user_level) VALUES (%s, %s, %s, %s, %s);")
    inputs = first_name, last_name, email, hash_password, level
    # run query
    return run_query(query, inputs)


def email_exists(input_email):
    """Chek if the user email exists"""
    # SQL query
    query = u"SELECT * FROM tbl_users WHERE email = %s;"
    inputs = input_email
    all_users = get_query(query, inputs)

    for find_email in all_users:
        if find_email['email'] == inputs:
            return True
    return False


def check_email_for_login(input_email):
    """Return user email"""
    # SQL query
    query = u"SELECT * FROM tbl_users WHERE email = %s;"
    inputs = input_email
    all_users = get_query(query, inputs)

    for find_email in all_users:
        if find_email['email'] == input_email:
            return find_email


def login_user(input_email, input_password):
    """Log in user function"""
    logging_user_details = check_email_for_login(input_email)
    if BCRYPT.check_password_hash(logging_user_details['password'],
                                  input_password):
        # compare password input to saved password
        return logging_user_details
    return False


def get_user_info(user_id):
    """Retreive user info"""
    query = ("SELECT * FROM tbl_users "
             "WHERE user_id=%s;")
    user_reqeust = get_query(query, user_id)
    for result in user_reqeust:
        response_dict = {
            "first_name": result["first_name"],
            "last_name": result["last_name"],
            "email": result["email"]
        }
        return response_dict
