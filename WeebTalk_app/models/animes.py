from WeebTalk_app.config.mysqlconnection import connectToMySQL
from flask import flash, get_flashed_messages


class Animes:
    DB = "weebtalk"
    def __init__( self , data ):
        self.id = data['id']
        self.mal_id = data['mal_id']
        self.title = data['title']
        self.thumbnail = data['thumbnail']
        self.synopsis = data['synopsis']

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO animes ( mal_id, title, thumbnail, synopsis, created_at, updated_at ) VALUES ( %(mal_id)s, %(title)s, %(thumbnail)s, %(synopsis)s, NOW() , NOW() );"
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def get_all_animes(cls):
        query = "SELECT * FROM animes;"
        results = connectToMySQL(cls.DB).query_db(query)
        animes = []
        for anime in results:
            animes.append( cls(anime) )
        return animes
    
    @classmethod
    def get_one_by_mal_id(cls, mal_id):
        query = "SELECT * FROM animes WHERE mal_id = %(mal_id)s"
        data = {'mal_id':mal_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_one_by_id(cls, id):
        query = "SELECT * FROM animes WHERE id = %(id)s"
        data = {'id': id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])