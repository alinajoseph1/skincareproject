from flask_app import app
from flask import render_template, redirect, request, session, flash, get_flashed_messages
from flask_app.models.usermodel import User
from flask_app.models.concernmodel import Concern

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/select-concerns")
def concerns():
    data = {
        "id": session["user_id"]
    }
    users = User.get_one(data)

    return render_template("select-concerns.html", user=users)


@app.route("/add/concerns", methods=["POST"])
def add():
    data = {
        "id": session["user_id"]
    }
    users = User.get_one(data)

    if Concern.validate(request.form):
        Concern.save(request.form)
        return redirect("/dashboard")
    else:
        return redirect("/select-concerns", user=users)


@app.route("/show")
def show_concerns():
    if "user_id" not in session:
        flash("Login or create a profile to choose a skin concern.")
        return redirect("/")
    
    data = {
        "id": session["user_id"]
    }
    logged_in_user = User.get_one(data)
    selected_concern = Concern.get_concern_with_user(data)

    return render_template("edit-concerns.html", selected=selected_concern, user=logged_in_user)


@app.route("/update/<concern_id>", methods=["POST"])
def update_concerns(concern_id):
    data = {
        "id": int(concern_id),
        "type": request.form["type"]
    }
    Concern.update(data)
    return redirect("/dashboard")

    
@app.route("/recommended")
def product_rec():
    if "user_id" not in session:
        return redirect("/")
    
    data = {
        "id": session["user_id"]
    }
    logged_in_user = User.get_one(data)
    selected_concern = Concern.get_concern_with_user(data)

    return render_template("recommended.html", selected=selected_concern, user=logged_in_user)

    
    
