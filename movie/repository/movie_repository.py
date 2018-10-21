from flask_mongoalchemy import MongoAlchemy
from movie import app
from movie.domain.movie import Movie
import jsonpickle


db = MongoAlchemy(app)


class Movies(db.Document):
    name = db.StringField()
    description = db.StringField()
    length = db.IntField()


class MovieRepository:
    def create(self, name, description, length):
        movie = Movies(name=name, description=description, length=length)
        movie.save()

        return movie.mongo_id

    def get(self, movie_id):
        if self.exists(movie_id):
            movie = Movies.query.get(movie_id)
            return Movie(movie_id=movie.mongo_id, name=movie.name, description=movie.description,
                                           length=movie.length)
        else:
            return None

    def read_all(self):
        movies = []
        all_movies = Movies.query.all()
        for movie in all_movies:
            movies.append(Movie(movie_id=movie.mongo_id, name=movie.name, description=movie.description, length=movie.length))
        return movies

    def delete(self, movie_id):
        if self.exists(movie_id):
            movie = Movies.query.get(movie_id)
            Movies.delete(movie)
            Movies.commit()

    def exists(self, movie_id):
        result = Movies.query.get(movie_id)
        return result is not None