import os
from contextlib import contextmanager

import mysql.connector
from dotenv import load_dotenv

from utils.variables import MYSQL_DATABASE

load_dotenv()


class MySQLConnection:
    _connection = None

    def __init__(self):
        self._host = os.getenv("MYSQL_DB_HOST", "localhost")
        self._user = os.getenv("MYSQL_DB_USER", "root")
        self._password = os.getenv("MYSQL_DB_PASSWORD")
        self._database = MYSQL_DATABASE

    def _get_conection(self):
        if self._connection is None or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(
                    host=self._host,
                    user=self._user,
                    password=self._password,
                    database=self._database,
                )
            except mysql.connector.Error as err:
                print(err)
                return None

        return self._connection

    @contextmanager
    def managed_cursor(self):
        connection = self._get_conection()
        if connection is None:
            raise IOError("Could not connect to the database.")

        cursor = connection.cursor()
        try:
            yield cursor
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            connection.rollback()
            raise
        finally:
            cursor.close()


db_connection = MySQLConnection()
