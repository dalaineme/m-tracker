#! /api/server/helpers.py
# -*- coding: utf-8 -*-
"""This is the helpers module

This module contains functions that abstract the common DB usage
"""
import psycopg2
from db_conn import DbConn


def run_query(query, inputs):
    """Run queries"""
    try:
        db_instance = DbConn()
        db_instance.cur.execute(query, inputs)
        db_instance.conn.commit()
        db_instance.close()
        return True
    except psycopg2.Error:
        return False


def get_query(query, inputs):
    """Get results"""
    try:
        db_instance = DbConn()
        db_instance.cur.execute(query, (inputs,))
        result = db_instance.cur.fetchall()
        db_instance.close()
        return result
    except psycopg2.Error:
        return False
