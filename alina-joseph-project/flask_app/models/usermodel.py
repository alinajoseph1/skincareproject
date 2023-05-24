from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import Bcrypt
from flask_app import app


bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    DB = 'skincare_db'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, age, email, password, created_at, updated_at ) 
        VALUES (%(first_name)s , %(last_name)s,%(age)s, %(email)s , %(password)s, NOW(), NOW() );"""
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_one(cls, data):
        query = " SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        return cls(result[0])

    @classmethod
    def update(cls, data):
        query = """
        UPDATE users 
        SET first_name = %(first_name)s, last_name= %(last_name)s, age = %(age)s, email=%(email)s, password=%(password)s
        WHERE id= %(user_id)s;"""
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM users WHERE email =%(email)s"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = " SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('skincare_db').query_db(query, user)
        if len(user["first_name"]) < 2:
            flash(
                "Invalid first name. First name must be at least 2 characters.", "register")
            is_valid = False
        if len(user["last_name"]) < 2:
            flash(
                "Invalid last name. Last name must be at least 2 characters. ", "register")
            is_valid = False
        if len(user["age"]) < 1:
            flash(
                "Invalid age. Age must be at least 2 characters. ", "register")
            is_valid = False
        if len(results) >= 1:
            flash("Email is already taken.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email.", "register")
            is_valid = False
        if len(user["password"]) < 8:
            flash("Invalid password. Password must be at least 8 characters.", "register")
            is_valid = False
        if user["password"] != user["confirm"]:
            flash("Passwords don't match.", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('skincare_db').query_db(query, user)

        return is_valid
