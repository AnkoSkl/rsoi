from flask_mongoalchemy import MongoAlchemy
from movie import app
from movie.domain.movie import Movie
import jsonpickle


db = MongoAlchemy(app)


class Movies(db.Document):
    id = db.StringField()
    name = db.StringField()
    description = db.StringField()
    length = db.IntField()

    def get_id(self):
        return self._id


class MovieRepository:
    def create(self, name, description, length):
        movie = Movies(name=name, description=description, length=length)
        movie.id = movie.get_id()
        movie.save()

        return movie.id

    def get(self, movie_id):
        if self.exists(movie_id):
            movie = Movies.query.filter_by(id=movie_id).first()
            return jsonpickle.encode(Movie(movie_id=movie.id, name=movie.name, description=movie.description,
                                           length=movie.length))
        else:
            return None

    def read_all(self):
        movies = []
        for movie in Movies.query.all():
            movies.append(Movie(movie_id=movie.id, name=movie.name, description=movie.description, length=movie.length))
        return movies

    def delete(self, movie_id):
        if self.exists(movie_id):
            movie = Movies.query.get(movie_id)
            Movies.delete(movie)
            Movies.commit()

    def exists(self, movie_id):
        return len(Movies.query.filter(Movies.id==movie_id)) > 0