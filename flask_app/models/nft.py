from flask_app.config.mysqlconnection import connectToMySQL

db_name = 'token_records'

class Nft:
    def __init__( self , data ):
        self.id = data['id']
        self.image_name = data['image_name']
        self.collection_name = data['collection_name']
        self.token_number = data['token_number']
        self.purchase_price = data['purchase_price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        # example_list = []

    @classmethod
    def create(cls, data):
        query = "INSERT INTO nfts ( image_name, collection_name , token_number , purchase_price, user_id) VALUES (%(image_name)s, %(collection_name)s, %(token_number)s, %(purchase_price)s, %(user_id)s)"
        return connectToMySQL(db_name).query_db(query, data)

    # @classmethod
    # def enter_image_name(cls, data):
    #     query = "INSERT INTO nfts ( image_name, user_id) VALUES (%(image_name)s, %(user_id)s)"
    #     return connectToMySQL(db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM nfts JOIN users ON users.id = nfts.user_id;"
        results = connectToMySQL(db_name).query_db(query)
        collections = []
        for collection in results:
            collections.append( cls(collection) )
        # favorites.sort(reverse=True)
        return collections

    # @classmethod
    # def get_by_id(cls, data):
    #     query = "SELECT * FROM nfts WHERE id = %(id)s";
    #     result = connectToMySQL(db_name).query_db(query, data)
    #     return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM nfts JOIN users ON users.id = nfts.user_id WHERE nfts.id = %(id)s";
        result = connectToMySQL(db_name).query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_image_name(cls, data):
        query = "SELECT image_name FROM nfts JOIN users ON users.id = nfts.user_id WHERE nfts.id = %(id)s";
        result = connectToMySQL(db_name).query_db(query, data)
        return cls(result[0])

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM nfts WHERE id = %(id)s;"
        return connectToMySQL(db_name).query_db(query,data)

    # @classmethod
    # def update(cls, data):
    #     query = "UPDATE table_name(s) SET name=%(name)s, last_name=%(last_name)s, updated_at=NOW() WHERE id = %(id)s;"
    #     return connectToMySQL('database_file(sometimes a schema)').query_db(query, data)

    # @staticmethod
    # def validate_new_user(x):
    #     is_valid = True
    #     query = "SELECT * FROM users WHERE email = %(email)s;"
    #     results = connectToMySQL(db_name).query_db(query, x)
    #     if len(results) >= 1:
    #         flash("Email already taken." , "register")
    #         is_valid=False
    #     if not EMAIL_REGEX.match(x['email']):
    #         flash("Invalid email address." , "register")
    #         is_valid=False
    #     if len(x['first_name']) < 2:
    #         flash("First name must be at least 2 characters." , "register")
    #         is_valid=False
    #     if len(x['last_name']) < 2:
    #         flash("Last name must be at least 2 characters." , "register")
    #         is_valid = False
    #     if len(x['password']) < 8:
    #         flash("Password must be at least 8 characters." , "register")
    #         is_valid = False
    #     if x['password'] != x['confirm_password']:
    #         flash("Passwords do not match!" , "register")
    #         is_valid = False
    #     return is_valid
