from flask_mongoalchemy import MongoAlchemy
from movie import app
from movie.domain.movie import Movie


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

    def read_paginated(self, page_number, page_size):
        movies = []
        movies_paginated = Movies.query.paginate(page=page_number, per_page=page_size)
        for movie in movies_paginated.items:
            movies.append(Movie(movie_id=movie.mongo_id, name=movie.name, description=movie.description,
                                length=movie.length))
        is_prev_num = (movies_paginated.prev_num > 0)
        is_next_num = (movies_paginated.next_num <= movies_paginated.pages)
        return movies, is_prev_num, is_next_num

    def delete(self, movie_id):
        if self.exists(movie_id):
            movie = Movies.query.get(movie_id)
            movie.remove()

    def exists(self, movie_id):
        result = Movies.query.get(movie_id)
        return result is not None