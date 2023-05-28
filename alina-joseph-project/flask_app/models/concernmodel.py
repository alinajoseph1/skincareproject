from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.usermodel import User


class Concern:
    DB = "skincare_db"

    def __init__(self, data):
        self.id = data["id"]
        self.type = data["type"]
        
        if "user" in data:
            self.user = data["user"]
        else:
            self.user = None

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO concerns(type, user_id) 
        VALUES (%(type)s, %(user_id)s);"""
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def delete(cls, concern_id):
        data = {
            "id": concern_id
        }
        query = "DELETE FROM concerns WHERE id = %(id)s ;"
        connectToMySQL(cls.DB).query_db(query, data)
        return concern_id

    @classmethod
    def get_concern_with_user(cls, data):
        query = "SELECT * FROM concerns LEFT JOIN users ON concerns.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db( query,data )
        concern = cls( results[0] )
        
        user_data = {
            "id" : results[0]["users.id"],
            "first_name" : results[0]["first_name"],
            "last_name" : results[0]["last_name"],
            "age" : results[0]["age"],
            "email" : results[0]["email"],
            "password": results[0]["password"],
            "created_at" : results[0]["users.created_at"],
            "updated_at" : results[0]["users.updated_at"]
        }
        concern.user = User(user_data)
        print(results)
        return concern

    @classmethod
    def get_one(cls, concern_id):
        data = {
            "id": concern_id
        }
        query = " SELECT * FROM concerns WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        return cls(result[0])

    @classmethod
    def update(cls, data):
        query = """
        UPDATE concerns SET type = %(type)s
        WHERE id = %(id)s """
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validate(data):
        is_valid = True
        if "type" not in data:
            flash("Please select at least one concern.")
            is_valid = False
            
        return is_valid
