from config import db_password
import mysql.connector

mydb = mysql.connector.connect(
    host="mysql",
    port=3306,
    user="root",
    password="root87141",
    database="disaster_db"
)
cursor = mydb.cursor()