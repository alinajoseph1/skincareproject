from flask import render_template, session, flash
from flask_app import app
from flask_app.models.usermodel import User
from flask_app.models.concernmodel import Concern


@app.route("/")
def index2():
    if "user_id" in session:
        flash("Just a reminder, you're already logged in. Don't forget to logout! ")

    return render_template("index.html")


@app.route("/all")
def allproducts():
    return render_template("products.html")
