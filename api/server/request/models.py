#! /api/server/request/models.py
# -*- coding: utf-8 -*-
"""This is the request modules
This module contains functions that are used in the auth endpoint
"""

from api.server.helpers import run_query, get_query


def create_request(input_title, input_description, user_id):
    """Create a new user request"""
    query = (u"INSERT INTO tbl_requests (request_title, request_description, "
             "created_by) VALUES (%s, %s, %s);")
    inputs = input_title, input_description, user_id
    # run query
    run_query(query, inputs)


def all_user_requests(user_id):
    """Method to gett all user request based on their email"""
    # SQL query
    query = u"SELECT * FROM tbl_requests WHERE created_by = %s;"
    inputs = user_id
    user_reqeusts = get_query(query, inputs)
    return user_reqeusts
