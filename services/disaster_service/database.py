from ..config import db_password
import mysql.connector
import time
import sys

def get_db():

    while True:
        try:
            print("Trying MySQL connection...", file=sys.stderr, flush=True)

            connection = mysql.connector.connect(
                host="mysql",
                port=3306,
                user="root",
                password=db_password,
                database="disaster_db"
            )

            print("MySQL connection successful!", file=sys.stderr, flush=True)

            return connection

        except mysql.connector.Error as e:
            print(
                f"MySQL connection failed: {e}",
                file=sys.stderr,
                flush=True
            )

            time.sleep(2)