# db_con.py
"""This module connects to the database"""

import sys
import psycopg2
from psycopg2 import connect

from api.server import APP

CONNECT_CREDS = {
    "host": APP.config.get('DATABASE_HOST'),
    "database": APP.config.get('PGDATABASE'),
    "user": APP.config.get('DATABASE_USER'),
    "password": APP.config.get('DATABASE_PASS')
}


class DbConn(object):
    """Database Creation Class"""

    def __init__(self):
        self.conn = ""
        self.cursor = ""

    def connect(self):
        """Connect to db"""
        self.conn = connect(**CONNECT_CREDS)
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        return self.cursor

    def close_conn(self):
        """Close connections"""
        self.cursor.close()
        self.conn.close()
