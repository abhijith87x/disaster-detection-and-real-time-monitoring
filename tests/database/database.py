from config import db_password
import mysql.connector

def get_disaster_db():
    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password=db_password,
        database="disaster_db",
        connection_timeout=10
    )

def get_oauth_db():
    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password=db_password,
        database="oauth_db",
        connection_timeout=10
    )