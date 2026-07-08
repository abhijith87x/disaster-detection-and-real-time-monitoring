from config import db_password
import mysql.connector
import time

while True:
    try:
        mydb = mysql.connector.connect(
            host="mysql",
            port=3306,
            user="root",
            password="root87141",
            database="disaster_db"
        )
        break
    except mysql.connector.Error:
        time.sleep(2)
cursor = mydb.cursor()