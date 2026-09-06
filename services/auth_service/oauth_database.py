from config import db_password

import mysql.connector
import time

def get_db():
    while True:
        try:
            return mysql.connector.connect(
                host="mysql",
                port=3306,
                user="root",
                password=db_password,
                database="oauth_db"
            )
        except mysql.connector.Error:
            time.sleep(2)