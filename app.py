from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import sqlite3
import os

from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASk_SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash


# Example user (add more later or fetch from database)
user = User(id=1, username="admin", password_hash=generate_password_hash("password"))

@login_manager.user_loader
def load_user(user_id):
    if user_id == "1":
        return user
    return None

def get_db_connection():
    db_path = 'blog.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == user.username and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        
        return "Invalid credentials, please try againe.", 401
    
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    conn =get_db_connection()
    posts = conn.execute("SELECT * FROM blog_posts ORDER BY date DESC").fetchall()
    conn.close()
    return render_template("dashboard.html", posts=posts)

@app.route("/")
def index():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM blog_posts ORDER BY date DESC").fetchall()
    conn.close()
    return render_template("index.html", posts=posts)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        author = request.form["author"]
        date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        conn = get_db_connection()
        conn.execute("INSERT INTO blog_posts (title, author, date, content) VALUES (?, ?, ?, ?)",
                        (title, author, date, content))
        conn.commit()
        conn.close()

        return jsonify({"message": "Blog post added successfully!"}), 201

    
    return render_template("add_posts.html")

@app.route("/delete/<int:id>",methods=["GET"])
@login_required
def delete_post(id):
    
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM blog_posts WHERE id = ?", (id,)).fetchone()

    if post is None:
        return redirect("/")

    conn.execute("DELETE FROM blog_posts WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run()