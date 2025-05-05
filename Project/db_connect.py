# Project/db_connect.py

import mysql.connector
from mysql.connector import Error
from db_config import DB_CONFIG

def get_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print("Error connecting to MySQL database:", e)
        return None
