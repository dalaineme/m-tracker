#! /api/server/helpers.py
# -*- coding: utf-8 -*-
"""This is the helpers module

This module contains functions that abstract the common DB usage
"""
import json
import psycopg2
from db_conn import DbConn


def json_fetch_all(query):
    """Retrieve all data as JSON"""
    try:
        DB_CONN = DbConn()
        DB_CONN.cur.execute(query)
        result = json.dumps(DB_CONN.cur.fetchall(), indent=2)
        DB_CONN.close()
        return result
    except psycopg2.Error:
        return False


def run_query(query):
    """Run queries"""
    try:
        DB_CONN = DbConn()
        DB_CONN.cur.execute(query)
        return True
    except psycopg2.Error:
        return False


def truncate_tables():
    """Truncate all the tables"""
    db_instance = DbConn()
    db_instance.query("TRUNCATE tbl_users;")
    db_instance.close()
