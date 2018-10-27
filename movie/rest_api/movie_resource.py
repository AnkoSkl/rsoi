from movie import app
from flask_restful import Resource, abort, reqparse
from movie.repository.movie_repository import MovieRepository
import jsonpickle
import flask


repo = MovieRepository()


def abort_if_movie_doesnt_exist(movie_id):
    if not repo.exists(movie_id):
        abort(404, message="Movie {} doesn't exist".format(movie_id))


class MovieResource(Resource):
    def get(self, movie_id):
        abort_if_movie_doesnt_exist(movie_id)
        movie = repo.get(movie_id)
        response = app.make_response("")
        response.status_code = 200
        response.data = jsonpickle.encode(movie)
        return response

    def delete(self, movie_id):
        abort_if_movie_doesnt_exist(movie_id)
        repo.delete(movie_id)
        response = app.make_response("Movie %s deleted successfully" % movie_id)
        response.status_code = 204
        return response


class MovieCreateResource(Resource):
    def post(self):
        payload = jsonpickle.decode(flask.request.data)
        movie_id = repo.create(payload["name"], payload["description"], payload["length"])
        movie = repo.get(movie_id)
        response = app.make_response("")
        response.status_code = 201
        response.data = jsonpickle.encode(movie)
        return response


class MovieListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int, default=1)
    parser.add_argument("page_size", type=int, default=5)

    def get(self):
        args = self.parser.parse_args(strict=True)
        #movies_list = repo.read_all()
        movies_list = repo.read_paginated(page_number=args['page'], page_size=args['page_size'])
        response = app.make_response("")
        response.status_code = 200
        response.data = jsonpickle.encode(movies_list)
        return response