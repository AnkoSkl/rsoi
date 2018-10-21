from movie import app
from flask_restful import  Resource, abort, reqparse
from movie.repository.movie_repository import Movies


repo = Movies()


