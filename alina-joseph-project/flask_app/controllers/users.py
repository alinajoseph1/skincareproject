from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.concernmodel import Concern
from flask_app.models.usermodel import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/register")
def register():
    return render_template("user-registration.html")


@app.route("/register-user", methods=["POST"])
def new_user():
    if not User.validate_register(request.form):
        return redirect("/register")

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "age": request.form["age"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"])

    }
    id = User.save(data)
    session["user_id"] = id
    return redirect("/select-concerns")


@app.route('/login', methods=['POST'])
def login_authenticate():
    data = {
        "email": request.form["email"]
    }
    user = User.get_email(data)

    if not user:
        flash("Invalid email", 'login')
        return redirect("/")

    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid password", 'login')
        return redirect("/")

    session["user_id"] = user.id

    return redirect("/dashboard")


@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        flash("Login or create a profile to view your profile.")
        return redirect("/")
    
    data = {
        "id": session["user_id"]
    }
    
    logged_in_user = User.get_one(data)
    concerns =Concern.get_concern_with_user(data)
    
    return render_template("dashboard.html", concern=concerns, user=logged_in_user)


@app.route('/logout')
def logout_user():
    session.clear()
    return redirect("/")
