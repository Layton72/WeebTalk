from WeebTalk_app.config.mysqlconnection import connectToMySQL
from flask import flash, get_flashed_messages


class Reviews:
    DB = "weebtalk"
    def __init__( self , data ):
        self.id = data['id']
        self.score = data['score']
        self.review = data['review']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.anime_id = data['anime_id']
        self.username = data['username']
        self.title = data['title']
        self.thumbnail = data['thumbnail']
        self.mal_id = data['mal_id']
        self.total_upvotes = 0


    @classmethod
    def save(cls, data ):
        query = "INSERT INTO reviews ( score, review, created_at, updated_at, user_id, anime_id ) VALUES ( %(score)s, %(review)s, NOW() , NOW(), %(user_id)s, %(anime_id)s );"
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def get_all_reviews(cls):
        query = """SELECT * FROM reviews 
        JOIN animes on reviews.anime_id=animes.id
        JOIN users ON reviews.user_id=users.id
        ORDER BY reviews.created_at DESC
        LIMIT 5;"""

        results = connectToMySQL(cls.DB).query_db(query)
        reviews = []
        for review in results:
            reviews.append( cls(review) )
        return reviews
    
    @classmethod
    def get_all_reviews_by_anime_id(cls, anime_id ):
        query = """SELECT * FROM reviews 
        JOIN animes on reviews.anime_id=animes.id
        JOIN users ON reviews.user_id=users.id 
        WHERE animes.id = %(id)s;"""
        data = {
            'id': anime_id
        }
        results = connectToMySQL(cls.DB).query_db(query, data)
        reviews = []
        for review in results:
            reviews.append( cls(review) )
        return reviews
    
    # @classmethod
    # def get_review_with_upvotes(cls, anime_id ):
    #     query = """SELECT * FROM reviews  
    #     LEFT JOIN likes on reviews.id=likes.review_id
    #     WHERE reviews.anime_id = %(id)s;"""
    #     data = {
    #         'id': anime_id
    #     }
    #     results = connectToMySQL(cls.DB).query_db(query, data)
    #     reviews = []
    #     for review in results:
    #         reviews.append( cls(review) )
    #     return reviews
    
    @classmethod
    def get_all_reviews_by_user_id(cls, user_id ):
        query = """SELECT * FROM reviews 
        JOIN animes on reviews.anime_id=animes.id
        JOIN users ON reviews.user_id=users.id 
        WHERE users.id = %(id)s;"""

        data = {
            'id': user_id
        }

        results = connectToMySQL(cls.DB).query_db(query, data)
        reviews = []
        for review in results:
            reviews.append( cls(review) )
        return reviews
    
    @classmethod
    def get_one(cls, data):
        query = """SELECT * FROM reviews 
        JOIN animes on reviews.anime_id=animes.id
        JOIN users ON reviews.user_id=users.id 
        WHERE reviews.id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = """UPDATE reviews
                SET score=%(score)s, review=%(review)s, updated_at=NOW()
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def delete(cls, data):
        query  = "DELETE FROM reviews WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validate_review(data):
        is_valid = True
        if "score" not in data or len(data["score"]) == 0:
            flash("Score is required!")
            is_valid = False
        elif int(data["score"]) < 1 or int(data["score"]) > 10:
            flash("Score must be between 1 and 10")
            is_valid = False

        if "review" not in data or len(data["review"]) == 0:
            flash("Review is required")
            is_valid = False
        elif len(data["review"]) < 10:
            flash("Review must be at least 10 characters.")
            is_valid = False
        
        return is_valid