from flask import request
from flask_restx import fields, Resource, reqparse
from swagger_config import api
from service.MoviesService import MoviesService
from flask_jwt_extended import jwt_required
from common.customJwtDecorator import admin_jwt_required

movie_space = api.namespace('movies', description="This endpoint to perform all the operation related to movies.")


get_movie_details = reqparse.RequestParser()
get_movie_details.add_argument('type', type=str, required=True,help="type is nothing but director, movie name, genre, imdb_score, and popularity",location="args")
get_movie_details.add_argument('query', type=str, required=True,help="query you want to search",location="args")


new_movie = api.model("Add new movie record", {
    "movie_name": fields.String(required = True,description="Name of the movie",help="Enter the name of the string."),
    "imdb_score": fields.Float(required = True,description="Imdb score of the given movie name",help="It contains float value."),
    "genre": fields.List(fields.String,required = True,description="Genre list of the movie",help="Add the types in the list like (['Action','Comedie'].)"),
    "director": fields.String(required = True,description="Director name of the moview",help="String value of the director name."),
    "popularity": fields.Float(required = True,description="Popularity value of the movie",help="It contains the floating value.")
})


update_movie = api.model("Update the movie details", {
    "id": fields.Integer(required=True,description="Id of the movie you want to update details",help="It is integer value, make sure that id correct."),
    "movie_name": fields.String(description="Name of the movie",help="Enter the name of the string."),
    "imdb_score": fields.Float(required = True,description="Imdb score of the given movie name",help="It contains float value."),
    "genre": fields.List(fields.String,description="Genre list of the movie",help="Add the types in the list like (['Action','Comedie'].)"),
    "director": fields.String(description="Director name of the movie",help="String value of the director name."),
    "popularity": fields.Float(description="Popularity value of the movie",help="It contains the floating value.")
})

delete_movie = api.model("Delete movie details", {
    "id": fields.Integer(required=True,description="Id of the movie you want to delete details",help="It is integer value, make sure that id correct."),
})

@movie_space.route("/")
class Movies(Resource):
    @api.doc(responses={ 200: 'OK'})
    @api.expect(new_movie)
    @admin_jwt_required()
    def post(self):
        return MoviesService().store_new_record(request.json)

    @api.doc(responses={ 200: 'OK'})
    @api.expect(update_movie)
    @admin_jwt_required()
    def put(self):
        return MoviesService().update_records(request.json)

    @api.doc(responses={ 200: 'OK'})
    @api.expect(get_movie_details)
    @jwt_required()
    def get(self):
        return MoviesService().get_records(dict(request.args))
    
    @api.doc(responses={200: 'OK'})
    @api.expect(delete_movie)
    @admin_jwt_required()
    def delete(self):
        return MoviesService().delete_record(request.json)

