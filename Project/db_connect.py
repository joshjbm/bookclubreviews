#!/usr/bin/env python3

import pymysql
from db_config import DB_CONFIG

def get_connection():
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception as e:
        print(f"<p>Error connecting to MySQL database: {e}</p>")
        return None
