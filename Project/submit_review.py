#!/usr/bin/env python3
"""
BookClubReviews - Submit Review
========================
CGI script for submitting new book reviews via a HTML form. 
Validates input and inserts review data into the MySQL database.
"""

import cgi
import cgitb
import pymysql
import os
from db_connect import get_connection

cgitb.enable()

print("Content-Type: text/html\n")
print("""
<html>
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Submit Review</title>
    <link rel="stylesheet" type="text/css" href="html/style.css">
  </head>
  <body>
    <h1>Submit a Book Review</h1>
""")

form = cgi.FieldStorage()
is_post = os.environ.get("REQUEST_METHOD", "") == "POST"

book_id = form.getvalue("book_id", "").strip()
review_title = form.getvalue("review_title", "").strip()
review_text = form.getvalue("review_text", "").strip()
rating = form.getvalue("rating", "").strip()

validation_messages = []

if is_post:
    # Validation
    if not book_id:
        validation_messages.append("⚠️ Please select a book.")
    if not review_title:
        validation_messages.append("⚠️ Please enter a review title.")
    if not review_text:
        validation_messages.append("⚠️ Please enter your review.")
    if not rating:
        validation_messages.append("⚠️ Please provide a rating between 1 and 5.")
    else:
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                validation_messages.append("⚠️ Rating must be between 1 and 5.")
        except ValueError:
            validation_messages.append("⚠️ Rating must be a number between 1 and 5.")

if not is_post or validation_messages:
    if is_post and validation_messages:
        print("<ul style='color:red;'>")
        for msg in validation_messages:
            print(f"<li>{msg}</li>")
        print("</ul>")

    conn = get_connection()
    if not conn:
        print("<p style='color:red;'>❌ Failed to connect to the database.</p>")
    else:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM books ORDER BY title")
        books = cursor.fetchall()
        cursor.close()
        conn.close()

        print('<form method="post" action="submit_review.py">')

        # Book dropdown
        print('<label for="book_id">Choose a book: <span style="color:red;">*</span></label><br>')
        print('<select name="book_id">')
        if not book_id:
            print('<option value="" selected disabled>-- Choose a book --</option>')
        for b_id, title in books:
            selected = 'selected' if str(b_id) == book_id else ''
            print(f'<option value="{b_id}" {selected}>{title}</option>')
        print('</select><br><br>')

        # Review title
        print('<label for="review_title">Review Title: <span style="color:red;">*</span></label><br>')
        print(f'<input type="text" name="review_title" value="{review_title}" size="60"><br><br>')

        # Review text
        print('<label for="review_text">Your Review: <span style="color:red;">*</span></label><br>')
        print(f'<textarea name="review_text" rows="5" cols="60">{review_text}</textarea><br><br>')

        # Rating
        print('<label for="rating">Rating (1-5): <span style="color:red;">*</span></label><br>')

        print('<select name="rating">')
        print(f'<option value="" {"selected" if not rating else ""} disabled>-- Select a Rating --</option>')

        for i in range(1, 6):
            selected = 'selected' if str(i) == rating else ''
            print(f'<option value="{i}" {selected}>{i}</option>')

        print('</select><br><br>')

        print('<input type="submit" value="Submit Review">')
        print('</form>')

else:
    # All inputs valid, proceed to insert
    conn = get_connection()
    if not conn:
        print("<p style='color:red;'>❌ Failed to connect to the database.</p>")
    else:
        try:
            cursor = conn.cursor()

            # Step 1: Count existing reviews by this user for this book
            cursor.execute(
                "SELECT COUNT(*) FROM reviews WHERE user_id = %s AND book_id = %s",
                (1, book_id)  # This is hardcoded logic for user_id; replace in future
            )
            count = cursor.fetchone()[0]
            review_number = count + 1

            # Step 2: Insert new review with calculated review_number enhancement
            cursor.execute("""
                INSERT INTO reviews (book_id, user_id, review_title, review_text, rating, review_date, review_number)
                VALUES (%s, %s, %s, %s, %s, NOW(), %s)
            """, (book_id, 1, review_title, review_text, rating, review_number)) # This is hardcoded logic for user_id; replace in future

            conn.commit()
            cursor.close()
            print("<p style='color:green;'>✅ Review submitted successfully.</p>")
        except Exception as e:
            print(f"<p style='color:red;'>Error inserting review: {e}</p>")
        finally:
            conn.close()

try:
    with open("html/footer.html", "r") as f:
        print(f.read())
except Exception as e:
    print(f"<!-- Footer load failed: {e} -->")

print("</body></html>")