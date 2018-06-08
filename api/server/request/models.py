#! /api/server/request/models.py
# -*- coding: utf-8 -*-
"""This is the request modules
This module contains functions that are used in the auth endpoint
"""

from api.server.helpers import run_query


def create_request(input_title, input_description, user_id):
    """Create a new user request"""
    query = (u"INSERT INTO tbl_requests (request_title, request_description, "
             "created_by) VALUES (%s, %s, %s);")
    inputs = input_title, input_description, user_id
    # run query
    run_query(query, inputs)
