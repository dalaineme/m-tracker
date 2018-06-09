#! /api/admin/models.py
# -*- coding: utf-8 -*-
"""This is the admin modules
This module contains functions that are used in the admin endpoint
"""
from api.server.helpers import get_query


def all_user_requests():
    """Method to gett all user requests"""
    # SQL query
    query = ("SELECT tbl_users.email, "
             "tbl_requests.request_id, "
             "tbl_requests.request_title, "
             "tbl_requests.request_description, "
             "tbl_requests.current_status "
             "FROM tbl_users, tbl_requests "
             "WHERE tbl_users.user_id = tbl_requests.created_by "
             "AND tbl_users.user_level = %s;")
    user_level = "User"
    all_requests = get_query(query, user_level)
    return all_requests
