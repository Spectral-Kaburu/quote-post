from flask import Blueprint, request, session, flash, redirect, render_template
from db import get_db
from utils import hash_password, check_password

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    
    with get_db() as cx:
        cursor = cx.cursor()
        first = request.form.get("first_name")
        last = request.form.get("last_name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        required_fields = ["first", "last", "username", "email", "password"]
        for field in required_fields:
            if not locals().get(field):
                msg = f"Did not input a {field.replace('_', ' ')}"
                return render_template("error.html", msg=msg)

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        if cursor.fetchone():
            msg = f"Username ({username}) already in use!"
            return render_template("error.html", msg=msg)

        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users(first_name, last_name, username, email) VALUES (?, ?, ?, ?)", (first, last, username, email))
        cursor.execute("INSERT INTO hashed_passwords(username, password) VALUES (?, ?)", (username, hashed_password))
        cx.commit()
        
        session["username"] = username
        flash(f"{username} added successfully!")
        return redirect("/blog")

@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    with get_db() as cx:
        cursor = cx.cursor()
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            msg = "Username and password are required."
            return render_template("error.html", msg=msg)

        cursor.execute("SELECT password FROM hashed_passwords WHERE username = ?", (username,))
        result = cursor.fetchone()

        if result and check_password(result[0], password):
            session["username"] = username
            return redirect("/blog")
        
        msg = "Invalid username or password."
        return render_template("error.html", msg=msg)
