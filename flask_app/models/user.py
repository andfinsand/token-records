from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
db_name = 'token_records'

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.email = data['email']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # example_list = []

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users ( email , first_name , last_name , password) VALUES (%(email)s, %(first_name)s, %(last_name)s, %(password)s)"
        return connectToMySQL(db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(db_name).query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db_name).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s";
        result = connectToMySQL(db_name).query_db(query, data)
        return cls(result[0])

    # @classmethod
    # def update(cls, data):
    #     query = "UPDATE table_name(s) SET name=%(name)s, last_name=%(last_name)s, updated_at=NOW() WHERE id = %(id)s;"
    #     return connectToMySQL('database_file(sometimes a schema)').query_db(query, data)

    @staticmethod
    def validate_new_user(x):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db_name).query_db(query, x)
        if len(results) >= 1:
            flash("Email already taken." , "register")
            is_valid=False
        if not EMAIL_REGEX.match(x['email']):
            flash("Invalid email address." , "register")
            is_valid=False
        if len(x['first_name']) < 2:
            flash("First name must be at least 2 characters." , "register")
            is_valid=False
        if len(x['last_name']) < 2:
            flash("Last name must be at least 2 characters." , "register")
            is_valid = False
        if len(x['password']) < 8:
            flash("Password must be at least 8 characters." , "register")
            is_valid = False
        if x['password'] != x['confirm_password']:
            flash("Passwords do not match!" , "register")
            is_valid = False
        return is_valid
