#!/usr/bin/env python3

import cgi
import cgitb 
import os
from db_connect import get_connection

cgitb.enable()
form = cgi.FieldStorage()

# Collect query parameters
order_input = form.getvalue("order", "desc").lower()
limit_input = form.getvalue("limit", "10")
book_search = form.getvalue("book", "").strip()
author_search = form.getvalue("author", "").strip()
rating_filter = form.getvalue("rating", "").strip()
reviewer_filter = form.getvalue("reviewer", "").strip()

# Validate order and limit
order = "ASC" if order_input == "asc" else "DESC"
try:
    limit = int(limit_input)
except ValueError:
    limit = 10

# Start HTML
print("Content-Type: text/html\n")
print(f"""
<html>
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Book Reviews</title>
    <link rel="stylesheet" type="text/css" href="html/style.css">
  </head>
  <body>
    <h1>Book Reviews</h1>

    <form method="get" action="view_reviews.py">
      <label for="book">Search by Title:</label>
      <input type="text" name="book" value="{book_search}">
      
      <label for="author">Author:</label>
      <input type="text" name="author" value="{author_search}">

      <label for="rating">Rating:</label>
      <select name="rating">
        <option value="">All</option>
        {''.join([f'<option value="{i}" {"selected" if rating_filter == str(i) else ""}>{i}</option>' for i in range(1,6)])}
      </select>

      <label for="reviewer">Reviewer:</label>
      <input type="text" name="reviewer" value="{reviewer_filter}">

      <label for="order">Sort by Date:</label>
      <select name="order">
        <option value="desc" {"selected" if order == "DESC" else ""}>Newest first</option>
        <option value="asc" {"selected" if order == "ASC" else ""}>Oldest first</option>
      </select>

      <label for="limit">Limit:</label>
      <input type="number" name="limit" value="{limit}" min="1" max="100">

      <input type="submit" value="Apply Filters">
    </form>
    <hr>
""")

# Connect to DB
conn = get_connection()
if not conn:
    print("<p style='color:red;'>❌ Failed to connect to the database.</p>")
    print("</body></html>")
    exit()

cursor = conn.cursor()

# Build query
query = """
SELECT books.title, books.author, users.username, reviews.review_title, 
       reviews.review_text, reviews.review_date, reviews.rating
FROM reviews
JOIN books ON reviews.book_id = books.id
LEFT JOIN users ON reviews.user_id = users.id
"""
conditions = []
params = []

if book_search:
    conditions.append("books.title LIKE %s")
    params.append(f"%{book_search}%")

if author_search:
    conditions.append("books.author LIKE %s")
    params.append(f"%{author_search}%")

if rating_filter:
    conditions.append("reviews.rating = %s")
    params.append(rating_filter)

if reviewer_filter:
    conditions.append("users.username LIKE %s")
    params.append(f"%{reviewer_filter}%")

if conditions:
    query += " WHERE " + " AND ".join(conditions)

query += f" ORDER BY reviews.review_date {order} LIMIT %s"
params.append(limit)

# Execute query
cursor.execute(query, params)
rows = cursor.fetchall()

# Display results
if not rows:
    print("<p>No reviews found for these filters.</p>")
else:
    print('<div class="table-container">')
    print("<table border='1' cellpadding='5'>")
    print("<thead><tr><th>Book</th><th>Author</th><th>Reviewer</th><th>Review Title</th><th>Review</th><th>Rating</th><th>Date</th></tr></thead>")
    print("<tbody>")
    for title, author, username, review_title, review, date, rating in rows:
        reviewer = username if username else "Anonymous"
        print(f"<tr><td>{title}</td><td>{author}</td><td>{reviewer}</td><td>{review_title}</td><td>{review}</td><td>{rating}</td><td>{date}</td></tr>")
    print("</tbody></table></div>")

cursor.close()
conn.close()

print("""
    <ul>
      <li><a href="project.py">🏠 Back to Home</a></li>
      <li><a href="submit_review.py">✍️ Submit a Book Review</a></li>
    </ul>
      """)
print("</body></html>")
