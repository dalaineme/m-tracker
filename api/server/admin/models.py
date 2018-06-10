#! /api/admin/models.py
# -*- coding: utf-8 -*-
"""This is the admin modules
This module contains functions that are used in the admin endpoint
"""
from api.server.helpers import get_query
from db_conn import DbConn


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


def get_request_by_id(request_id):
    """Retreive a request by it's ID"""
    query = ("SELECT * FROM tbl_requests "
             "WHERE request_id=%s;")
    user_reqeust = get_query(query, request_id)
    if user_reqeust:
        return user_reqeust
    return False


def approve_request(request_id):
    """Approve a request method"""
    # Get the specific request
    requests = get_request_by_id(request_id)
    if not requests:
        return "no_id"
    # Check if it's pending first of all
    for request in requests:
        if request["current_status"] == "Pending":
            db_instance = DbConn()
            query = (u"UPDATE tbl_requests SET current_status = %s "
                     "WHERE request_id = %s")
            inputs = "Approved", request_id
            db_instance.cur.execute(query, inputs)
            db_instance.conn.commit()
            query2 = (u"INSERT INTO tbl_status_logs (request_status, request) "
                      "VALUES(%s,%s);")
            inputs2 = "Approved", request_id
            db_instance.cur.execute(query2, inputs2)
            db_instance.conn.commit()
            return request
        return False


def dissaprove_request(request_id):
    """Disapprove a request method"""
    # Get the specific request
    requests = get_request_by_id(request_id)
    if not requests:
        return "no_id"
    # Check if it's pending first of all
    for request in requests:
        if ((request["current_status"] == "Approved") or
                (request["current_status"] == "Pending")):
            db_instance = DbConn()
            query = (u"UPDATE tbl_requests SET current_status = %s "
                     "WHERE request_id = %s")
            inputs = "Dissaproved", request_id
            db_instance.cur.execute(query, inputs)
            db_instance.conn.commit()
            query2 = (u"INSERT INTO tbl_status_logs (request_status, request) "
                      "VALUES(%s,%s);")
            inputs2 = "Dissaproved", request_id
            db_instance.cur.execute(query2, inputs2)
            db_instance.conn.commit()
            return request
        if request["current_status"] == "Dissaproved":
            return "already_dissaproved"
        return False


def resolve_request(request_id):
    """Resolve a request method"""
    # Get the specific request
    requests = get_request_by_id(request_id)
    if not requests:
        return "no_id"
    # Check if it's pending first of all
    for request in requests:
        if request["current_status"] == "Approved":
            db_instance = DbConn()
            query = (u"UPDATE tbl_requests SET current_status = %s "
                     "WHERE request_id = %s")
            inputs = "Resolved", request_id
            db_instance.cur.execute(query, inputs)
            db_instance.conn.commit()
            query2 = (u"INSERT INTO tbl_status_logs (request_status, request) "
                      "VALUES(%s,%s);")
            inputs2 = "Resolved", request_id
            db_instance.cur.execute(query2, inputs2)
            db_instance.conn.commit()
            return request
        if request["current_status"] == "Resolved":
            return "already_resolved"
        return False
