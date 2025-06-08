import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd

app = Flask(__name__)
app.jinja_env.filters["usd"] = usd

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    holdings = db.execute("""
        SELECT symbol, SUM(shares) as total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """, user_id)
    total = 0
    for holding in holdings:
        stock = lookup(holding["symbol"])
        holding["name"] = stock["name"]
        holding["price"] = stock["price"]
        holding["total"] = holding["total_shares"] * stock["price"]
        total += holding["total"]
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
    grand_total = total + cash
    return render_template("index.html", holdings=holdings, cash=cash, grand_total=grand_total)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username or not password or password != confirmation:
            return apology("invalid input", 400)
        hash_pw = generate_password_hash(password)
        try:
            new_id = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_pw)
        except:
            return apology("username already exists", 400)
        session["user_id"] = new_id
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return apology("must provide username and password", 400)
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 400)
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        if not stock:
            return apology("invalid symbol", 400)
        return render_template("quoted.html", stock=stock)
    else:
        return render_template("quote.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol or not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("invalid input", 400)
        stock = lookup(symbol)
        if not stock:
            return apology("invalid symbol", 400)
        price = stock["price"]
        total_cost = price * int(shares)
        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        if cash < total_cost:
            return apology("insufficient funds", 400)
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user_id, stock["symbol"], int(shares), price)
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    user_id = session["user_id"]
    symbols = db.execute(
        "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol or not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("invalid input", 400)
        shares_owned = db.execute(
            "SELECT SUM(shares) FROM transactions WHERE user_id = ? AND symbol = ?", user_id, symbol)[0]["SUM(shares)"]
        if shares_owned < int(shares):
            return apology("not enough shares", 400)
        stock = lookup(symbol)
        proceeds = stock["price"] * int(shares)
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", proceeds, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user_id, symbol, -int(shares), stock["price"])
        return redirect("/")
    else:
        return render_template("sell.html", symbols=symbols)


@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    history = db.execute(
        "SELECT symbol, shares, price, timestamp FROM transactions WHERE user_id = ? ORDER BY timestamp DESC", user_id)
    return render_template("history.html", history=history)
