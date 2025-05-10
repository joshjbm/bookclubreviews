#!/usr/bin/env python3
"""
BookClubReviews - Database Connection
========================
Provides the database connection for the BookClubReviews application.
This module handles the connection to the MySQL database using pymysql.
"""

import pymysql
from db_config import DB_CONFIG

def get_connection():
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception as e:
        print(f"<p>❌ Error connecting to MySQL database: {e}</p>")
        return None