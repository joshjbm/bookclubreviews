#!/usr/bin/env python3

print("Content-Type: text/html\n")
print("""
<html>
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BookClubReviews – Home</title>
    <link rel="stylesheet" type="text/css" href="html/style.css">
  </head>
  <body>
    <h1>📚 Welcome to BookClubReviews</h1>
    <p>This is a community book club in New York!</p>

    <h2>Explore the Book Club</h2>
    <ul>
      <li><a href="submit_review.py">✍️ Submit a Book Review</a></li>
      <li><a href="view_reviews.py">🔍 View All Reviews</a></li>
    </ul>

    <p><em>Created by Josh Mackie</em></p>
  </body>
</html>
""")
