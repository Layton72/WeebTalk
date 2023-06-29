from WeebTalk_app.config.mysqlconnection import connectToMySQL
from flask import flash, get_flashed_messages


class Likes:
    DB = "weebtalk"
    def __init__( self , data ):
        self.user_id = data['user_id']
        self.review_id = data['review_id']
        self.upvotes = data['upvote']


    @classmethod
    def upvote(cls, data ):
        query = "INSERT INTO likes ( user_id, review_id, upvote ) VALUES (%(user_id)s, %(review_id)s, 1 );"
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def downvote(cls, data ):
        query = "INSERT INTO likes ( user_id, review_id, upvote ) VALUES (%(user_id)s, %(review_id)s, -1 );"
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def delete(cls, data ):
        query = "DELETE FROM likes WHERE user_id=%(user_id)s AND review_id= %(review_id)s;"
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def get_all_upvotes(cls, review_id):
        query = """SELECT * FROM likes 
        JOIN reviews ON reviews.id=likes.review_id
        JOIN users ON users.id=likes.user_id
        WHERE reviews.id = %(id)s;"""
        data = {
            'id': review_id
        }
        results = connectToMySQL(cls.DB).query_db(query, data)
        likes = []
        for like in results:
            likes.append( cls(like) )
        return likes