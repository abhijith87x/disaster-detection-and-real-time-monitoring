from config import db_password
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = db_password,
    database = "disaster_db"
)
cursor = mydb.cursor()