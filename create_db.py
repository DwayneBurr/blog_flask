import sqlite3

conn = sqlite3.connect("blog.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS blog_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        date TEXT NOT NULL,
        content TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

print("Database and table created successfully!")