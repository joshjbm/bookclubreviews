#!/usr/bin/env python3

import cgitb
from db_connect import get_connection

cgitb.enable()

print("Content-Type: text/html\n")
print("<html><body>")

conn = get_connection()
if conn:
    print("<p>✅ Connection successful!</p>")
    conn.close()
else:
    print("<p>❌ Failed to connect to database.</p>")

print("</body></html>")