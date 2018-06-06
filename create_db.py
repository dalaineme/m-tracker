"""This module allows db creation and schema installation"""

import os
import sys

import psycopg2
from psycopg2 import connect


def main():
    """Main method

    Creates main and test databases
    """
    db_name = os.environ["PGDATABASE"]
    test_db_name = os.environ["PGDATABASE"] + "_test"
    default_db = "postgres"
    connection_parameters = {
        "host": "localhost",
        "database": default_db,
        "user": os.environ["PGUSER"],
        "password": os.environ["PGPASSWORD"]
    }
    drop_statement = "DROP DATABASE IF EXISTS {};".format(db_name)
    test_drop_statement = "DROP DATABASE IF EXISTS {};".format(test_db_name)
    ddl_statement = "CREATE DATABASE {};".format(db_name)
    test_ddl_statement = "CREATE DATABASE {};".format(test_db_name)
    conn = connect(**connection_parameters)
    conn.autocommit = True

    try:
        with conn.cursor() as cursor:
            # execute ddls
            cursor.execute(drop_statement)
            cursor.execute(test_drop_statement)
            cursor.execute(ddl_statement)
            cursor.execute(test_ddl_statement)
        conn.close()
        sys.stdout.write("Created database environment successfully.\n")
    except psycopg2.Error:
        raise SystemExit(
            "Failed to setup Postgres environment.\n{0}".format(sys.exc_info())
        )

    # # Populate Main DB
    # try:
    #     main_connection_parameters = {
    #         "host": "localhost",
    #         "database": db_name,
    #         "user": os.environ["PGUSER"],
    #         "password": os.environ["PGPASSWORD"]
    #     }
    #     main_conn = connect(**main_connection_parameters)
    #     main_conn.autocommit = True
    #     with main_conn.cursor() as cursor:
    #         cursor.execute(open("schema.sql", "r").read())
    #     main_conn.close()
    #     sys.stdout.write("Populated main db successfully.\n")
    # except psycopg2.Error:
    #     raise SystemExit(
    #         "Failed to setup nment.\n{0}".format(sys.exc_info())


if __name__ == "__main__":
    main()
