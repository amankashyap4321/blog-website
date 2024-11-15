import sqlite3
import os

# Ensure the 'db' folder exists
if not os.path.exists('db'):
    os.makedirs('db')

# Path to the database file
database_path = 'db/blog.db'

# Connect to the SQLite database (creates the file if it does not exist)
conn = sqlite3.connect(database_path)

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create the 'posts' table if it does not exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL
)
''')

# Commit the changes
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

print("Database and table created successfully.")
