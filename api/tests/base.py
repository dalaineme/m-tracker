# api/tests/base.py
"""This is the base test module"""

import sys
from flask_testing import TestCase
import psycopg2
from api.server import APP
from db_conn import DbConn


def truncate_tables():
    """Truncate all the tables"""
    db_instance = DbConn()
    db_instance.conn.autocommit = True
    try:
        with db_instance.conn.cursor() as cursor:
            cursor.execute("TRUNCATE tbl_users CASCADE;")
            cursor.execute("TRUNCATE tbl_requests CASCADE;")
            db_instance.conn.close()
    except psycopg2.Error:
        raise SystemExit(
            "Failed to load schema.\n{0}".format(sys.exc_info())
        )


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        APP.config.from_object('api.server.config.TestingConfig')
        return APP

    def setUp(self):
        pass

    def tearDown(self):
        """Code that is executed after each test"""
        pass
