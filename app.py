from flask import Flask, render_template, request, jsonify

import json

from datetime import datetime

app = flask(__name__)

BLOG_POST_FILE = "blog_post.json"

def load_blog_posts():
    try:
        with open(BLOG_POST_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def save_blog_posts(posts):
    with open(BLOG_POST_FILE, "w") as file:
        json.dump(posts, file, indent= 4)


@app.route("/")
def index():
    posts = load_blog_posts()
    return render_template("index.html", posts=posts)

@app.route("/add", methods=["GET", "POST"])
def add_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        author = request.form["author"]
        date = datetime.now().strftime("%d-%m-%Y %H:%M")

        posts = load_blog_posts()

        new_post = {
            "title": title,
            "content": content,
            "author": author,
            "date": date
        }

        posts.append(new_post)

        save_blog_posts(posts)

        return jsonify({"message": "Blog post added successfully!"}), 201
    
    return render_template("add_post.html")

if __name__ == "__main__":
    app.run()