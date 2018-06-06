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
        """Constructor method"""
        self.conn = connect(**CONNECT_CREDS)
        self.cur = self.conn.cursor()

    def query(self, query):
        """Query execution method"""
        self.cur.execute(query)

    def close(self):
        """Close Connection"""
        self.cur.close()
        self.conn.close()
