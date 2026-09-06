from config import db_password
import mysql.connector

def get_disaster_db():
    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="root87141",
        database="disaster_db",
        connection_timeout=10
    )

def get_oauth_db():
    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="root87141",
        database="oauth_db",
        connection_timeout=10
    )