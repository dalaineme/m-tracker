# db_con.py
"""This module connects to the database"""

from psycopg2 import connect
from psycopg2.extras import RealDictCursor


class DbConn(object):
    """Database Creation Class"""

    def __init__(self):
        """Constructor method"""
        self.conn = connect(**CONNECT_CREDS)
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def query(self, query):
        """Query execution method"""
        self.cur.execute(query)

    def close(self):
        """Close Connection"""
        self.cur.close()
        self.conn.close()


# Placed at the bottom to avoid cirtular importation
from api.server import APP

CONNECT_CREDS = {
    "host": APP.config.get('DATABASE_HOST'),
    "database": APP.config.get('DATABASE_NAME'),
    "user": APP.config.get('DATABASE_USER'),
    "password": APP.config.get('DATABASE_PASS')
}
