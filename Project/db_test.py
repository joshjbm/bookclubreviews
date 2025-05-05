# Project/db_test.py

from db_connect import get_connection

print("Content-Type: text/html\n")
print("<html><body>")

conn = get_connection()
if conn:
    print("<p>✅ Connection successful!</p>")
    conn.close()
else:
    print("<p>❌ Failed to connect to database.</p>")

print("</body></html>")