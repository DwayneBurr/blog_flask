from flask import Flask, render_template, request, jsonify

import sqlite3

from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("blog.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM blog_posts ORDER BY date DESC").fetchall()
    conn.close()
    return render_template("index.html", posts=posts)

@app.route("/add", methods=["GET", "POST"])
def add_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        author = request.form["author"]
        date = datetime.now().strftime("%d-%m-%Y %H:%M")

        conn = get_db_connection()
        conn.execute("INSERT INTO blog_posts (title, author, date, content) VALUES (?, ?, ?, ?)",
                        (title, author, date, content))
        conn.commit()
        conn.close()

        return jsonify({"message": "Blog post added successfully!"}), 201

    
    return render_template("add_posts.html")

if __name__ == "__main__":
    app.run()