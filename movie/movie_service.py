from movie import app
from flask_restful import Api
from movie.rest_api.movie_resource import *
from movie.repository.movie_repository import Movies


api = Api(app)
service_namespace = "/movies"

api.add_resource(MovieListResource, "/movies")
api.add_resource(MovieResource, "/movies/<movie_id>")
api.add_resource(MovieCreateResource, "/movies/create")


if __name__ == '__main__':
    app.run(port=5001, debug=True)