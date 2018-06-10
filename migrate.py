# migrate.py
"""This is the migrations moduls

This module handles populating the database
"""
import sys
import psycopg2

from db_conn import DbConn
from api.server.auth.models import signup_user

CONN = DbConn()


def main():
    """Main method"""
    CONN.conn.autocommit = True
    try:
        with CONN.conn.cursor() as cursor:
            cursor.execute(open("schema.sql", "r").read())
            CONN.conn.close()
            print("Schema uploaded")
    except psycopg2.Error:
        raise SystemExit(
            "Failed to load schema.\n{0}".format(sys.exc_info())
        )

    # Create default Admin
    signup_user("Dalin", "Oluoch", "mcdalinoluoch@gmail.com",
                "aaaAAA111", "Admin")


if __name__ == "__main__":
    main()
