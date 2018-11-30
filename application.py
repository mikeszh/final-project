import os, csv

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///nutrition.db")

@app.route("/")
@login_required
def index():
    rows = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
    age = rows[0]["age"]
    gender = rows[0]["gender"]
    weight = rows[0]["weight"]
    height = rows[0]["height"]
    activity = rows[0]["activity"]
    if not age:
        return render_template("aboutme.html")
    else:
        if gender == 0:
            calories = round((9.99 * weight + 6.25 * height - 4.92 * age + 5) * activity)
            vitaminc = 90
            if age <= 18:
                iron = 11
            else:
                iron = 8
        else:
            calories = round((9.99 * weight + 6.25 * height - 4.92 * age - 161) * activity)
            vitaminc = 75
            if age <= 18:
                iron = 15
            else:
                iron = 18
        return render_template("index.html", vitaminc=vitaminc, iron=iron, calories=calories)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        age = rows[0]["age"]

        # Redirect user to home page
        if not age:
            return redirect("/aboutme")
        else:
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/aboutme", methods=["GET", "POST"])
def aboutme():
    if request.method == "POST":
        db.execute("UPDATE users SET age=:age, gender=:gender, height=:height, weight=:weight, activity=:activity WHERE id=:id",
                id=session["user_id"], age=request.form.get("age"), gender=request.form.get("gender"), height=request.form.get("height"), weight=request.form.get("weight"), activity=request.form.get("activity"))
        return redirect("/")

    else:
        return render_template("aboutme.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by clicking a link or via redirect)
    if request.method == "POST":
        # Check if username, password, and confirmed password are valid
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide password", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)
        # Hash the password and store it in users
        hashed_password = generate_password_hash(request.form.get("password"))
        new_user = db.execute("INSERT INTO users(username, hash) VALUES(:username, :hash)",
                              username=request.form.get("username"), hash=hashed_password)
        # Check if username is taken
        if not new_user:
            return apology("username taken", 400)
        session["user_id"] = new_user
        # Redirect to index
        return redirect("/aboutme")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/menu")
@login_required
def menu():
    file = open("index.csv", "a")
    writer = csv.writer(file)
    writer.writerow((request.form.get("name"), request.form.get("house"),
                     request.form.get("passion1"), request.form.get("passion2")))
    return render_template("menu.html")

@app.route("/lunch")
@login_required
def lunch():
    return render_template("lunch.html")

@app.route("/dinner")
@login_required
def dinner():
    return render_template("dinner.html")

@app.route("/history")
@login_required
def history():
    return render_template("history.html")

@app.route("/diet")
@login_required
def diet():
    return render_template("diet.html")

def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)