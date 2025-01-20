import sqlite3

# Connect to the database
conn = sqlite3.connect("blog.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS blog_posts")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS blog_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        date TEXT NOT NULL,
        content TEXT NOT NULL,
        image TEXT,
        video TEXT
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully!")
