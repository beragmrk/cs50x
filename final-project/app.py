from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from cs50 import SQL

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///tasks.db")

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")
    tasks = db.execute("SELECT * FROM tasks WHERE user_id = ?", session["user_id"])
    return render_template("index.html", tasks=tasks)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username or not password or password != confirmation:
            return render_template("apology.html", message="Invalid input")
        hash_pw = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_pw)
        except:
            return render_template("apology.html", message="Username taken")
        return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return render_template("apology.html", message="Must provide username and password")
        user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(user) != 1 or not check_password_hash(user[0]["hash"], password):
            return render_template("apology.html", message="Invalid username/password")
        session["user_id"] = user[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/add", methods=["POST"])
def add():
    if "user_id" not in session:
        return redirect("/login")
    title = request.form.get("title")
    description = request.form.get("description")
    due = request.form.get("due")
    if not title or not due:
        return render_template("apology.html", message="Missing title or due date")
    db.execute("INSERT INTO tasks (user_id, title, description, due) VALUES (?, ?, ?, ?)",
               session["user_id"], title, description, due)
    return redirect("/")

@app.route("/complete/<int:task_id>")
def complete(task_id):
    if "user_id" not in session:
        return redirect("/login")
    db.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", task_id, session["user_id"])
    return redirect("/")
