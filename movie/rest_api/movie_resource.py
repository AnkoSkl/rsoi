from movie import app
from flask_restful import Resource, abort, reqparse
from movie.repository.movie_repository import MovieRepository


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
        response.data = movie
        return response

    def delete(self, movie_id):
        abort_if_movie_doesnt_exist(movie_id)
        repo.delete(movie_id)
        response = app.make_response("Movie %d deleted successfully" % movie_id)
        response.status_code = 204
        return response


