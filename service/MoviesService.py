from flask import jsonify
from dbconnect import dbsession
from modules.movies import Movies
from sqlalchemy import text
from common.StatusCode import Done, StatusCode
from common.Validatefunction import validateParamsFromCheckList
import json

class MoviesService():
    def __init__(self):
        pass
        
    def store_new_record(self,request_body):
        try:
            request_body = validateParamsFromCheckList(request_body,{"movie_name":(str),"imdb_score":(int,float),"genre":(list),"director":(str),"popularity":(int,float)})
            new_movie = Movies(request_body.get("movie_name"),request_body.get("imdb_score"),json.dumps(request_body.get("genre")),request_body.get("director"),request_body.get("popularity"))

            dbsession.add(new_movie)
            dbsession.commit()
            return Done(jsonify(new_movie).get_json())
        except Exception as e:
            dbsession.rollback()
            return StatusCode(({False:str(e),True:e.args[0]})[len(e.args)>0]) 
        finally:
            dbsession.close()

    def update_records(self,request_body):
        try:
            request_body = validateParamsFromCheckList(request_body,{"id":(int),"movie_name":(str),"imdb_score":(int,float),"genre":(list),"director":(str),"popularity":(int,float)})

            update_movie  = dbsession.query(Movies).filter(Movies.id == request_body.get("id")).update({"movie_name":request_body.get("movie_name"),"imdb_score":request_body.get("imdb_score"),"genre":json.dumps(request_body.get("genre")),"director":request_body.get("director"),"popularity":request_body.get("popularity")})

            dbsession.commit()
            if update_movie == 1:
                return Done(None, "Updated")
            else:
                return StatusCode("not_found","Movie not found")
        except Exception as e:
            dbsession.rollback()
            return StatusCode(({False:str(e),True:e.args[0]})[len(e.args)>0])
        finally:
            dbsession.close()

    def get_records(self,request_params):
        obj = {
            "name": "movie_name",
            "imdbscore": "imdb_score",
            "genre": "genre",
            "director": "director",
            "popularity": "popularity"
        }
        try:
            request_params = validateParamsFromCheckList(request_params,{"type":(str),"query":(str)})
            if obj.get(request_params.get("type")) is None:
                raise Exception("type_is_not_exist")
            
            if obj.get(request_params.get("type")) == "genre":
                filter_str = self.genreCreate(request_params.get("query"))
            elif obj.get(request_params.get("type")) in ("imdb_score","popularity"):
                filter_str = "{}>={}".format(obj.get(request_params.get("type")),request_params.get("query"))
            else:
                filter_str = "{}='{}'".format(obj.get(request_params.get("type")),request_params.get("query"))

            movie_list = dbsession.query(Movies).filter(text(filter_str)).all()

            return Done(jsonify(movie_list).get_json())
        except Exception as e:
            return StatusCode(({False:str(e),True:e.args[0]})[len(e.args)>0])
        finally:
            dbsession.close()

    def genreCreate(self,list_genre):
        list_genre = list_genre.split(",")
        genre_str = "("
        for genre in list_genre:
            genre_str += "json_contains(genre,'\"{}\"',\"$\") or ".format(genre)
        genre_str = genre_str.rstrip(" or ")+")"
        return genre_str

    def delete_record(self,request_params):
        try:
            request_params = validateParamsFromCheckList(request_params,{"id":(int)})

            delete_movie = dbsession.query(Movies).filter(Movies.id == request_params.get("id")).delete()

            dbsession.commit()
            if delete_movie == 1:
                return Done(None, "Deleted")
            else:
                return StatusCode("not_found","Movie not found")
        except Exception as e:
            dbsession.rollback()
            return StatusCode(({False:str(e),True:e.args[0]})[len(e.args)>0])
        finally:
            dbsession.close()