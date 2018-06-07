#! /api/server/helpers.py
# -*- coding: utf-8 -*-
"""This is the helpers module

This module contains functions that abstract the common DB usage
"""
import sys
import json
import psycopg2
from db_conn import DbConn


def json_fetch_all(query):
    """Retrieve all data as JSON"""
    try:
        db_conn = DbConn()
        db_conn.cur.execute(query)
        result = json.dumps(db_conn.cur.fetchall(), indent=2)
        db_conn.close()
        return result
    except psycopg2.Error:
        return False


def run_query(query, inputs):
    """Run queries"""
    try:
        db_conn = DbConn()
        db_conn.cur.execute(query, inputs)
        db_conn.conn.commit()
        db_conn.close()
        return True
    except psycopg2.Error:
        return False


def truncate_tables():
    """Truncate all the tables"""
    db_instance = DbConn()
    db_instance.query("TRUNCATE tbl_users;")
    db_instance.close()
