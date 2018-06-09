#! /api/server/request/models.py
# -*- coding: utf-8 -*-
"""This is the request modules
This module contains functions that are used in the auth endpoint
"""
import sys
import psycopg2
from db_conn import DbConn
from api.server.helpers import get_query


# def create_request(input_title, input_description, user_id):
#     """Create a new user request"""
#     query = (u"INSERT INTO tbl_requests (request_title, request_description, "
#              "created_by) VALUES (%s, %s, %s);")
#     inputs = input_title, input_description, user_id
#     # run query
#     run_query(query, inputs)

def create_request(input_title, input_description, user_id):
    """Create a new user request"""
    try:
        db_instance = DbConn()
        query = (u"INSERT INTO tbl_requests (request_title, "
                 "request_description, created_by) VALUES (%s,%s,%s) "
                 "RETURNING request_id;")
        inputs = input_title, input_description, user_id
        db_instance.cur.execute(query, inputs)
        db_instance.conn.commit()
        last_insert_id = db_instance.cur.fetchone()["request_id"]
        print(last_insert_id)
        query2 = (u"INSERT INTO tbl_status_logs (request_status, request) "
                  "VALUES(%s,%s);")
        inputs2 = "Sent", last_insert_id
        db_instance.cur.execute(query2, inputs2)
        db_instance.conn.commit()
    except psycopg2.Error:
        print('error')
        print(sys.exc_info())


def all_user_requests(user_id):
    """Method to gett all user request based on their email"""
    # SQL query
    query = ("SELECT tbl_users.email, "
             "tbl_requests.request_id, "
             "tbl_requests.request_title, "
             "tbl_requests.request_description, "
             "tbl_requests.current_status "
             "FROM tbl_users, tbl_requests "
             "WHERE tbl_users.user_id = tbl_requests.created_by "
             "AND tbl_requests.created_by = %s;")
    user_reqeusts = get_query(query, user_id)
    return user_reqeusts


def get_request_by_id(user_id, request_id):
    """Method to update a previous request"""
    # call the all requests method
    dicts = all_user_requests(user_id)
    result = next(
        (item for item in dicts if item["request_id"] == request_id), False)
    query = ("SELECT tbl_status_logs.request_status,tbl_status_logs.date_updated, tbl_status_logs.request, tbl_requests.request_id FROM tbl_requests, tbl_status_logs WHERE tbl_status_logs.request=tbl_requests.request_id AND tbl_requests.request_id=%s;")
    if result:
        request_logs = get_query(query, result["request_id"])
        response_dict = {
            "request_id": result["request_id"],
            "request_title": result["request_title"],
            "request_description": result["request_description"],
            "my_email": result["email"],
            "status_logs": request_logs
        }
        return response_dict
    return "fail"
