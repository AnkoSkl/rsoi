from movie import app
from flask_restful import Resource, abort, reqparse
from movie.repository.movie_repository import MovieRepository
import jsonpickle
import flask


repo = MovieRepository()


def abort_if_movie_doesnt_exist(movie_id):
    if not repo.exists(movie_id):
        app.logger.error('Фильма с идентификатором %s не существует!', movie_id)
        abort(404, message="Movie {} doesn't exist".format(movie_id))


class MovieResource(Resource):
    def get(self, movie_id):
        app.logger.info('Получен запрос на получение информации о фильме с идентификатором %s' % movie_id)
        abort_if_movie_doesnt_exist(movie_id)
        movie = repo.get(movie_id)
        response = app.make_response("")
        response.status_code = 200
        response.content_type = "application/json"
        response.data = movie.to_json()
        app.logger.info('Запрос на получение информации о фильме с идентификатором %s успешно обработан' % movie_id)
        return response

    def delete(self, movie_id):
        app.logger.info('Получен запрос на удаление фильма с идентификатором %s' % movie_id)
        abort_if_movie_doesnt_exist(movie_id)
        repo.delete(movie_id)
        response = app.make_response("Movie %s deleted successfully" % movie_id)
        response.status_code = 204
        app.logger.info('Фильм с идентификатором %s успешно удален' % movie_id)
        return response


class MovieCreateResource(Resource):
    def post(self):
        app.logger.info('Получен запрос на создание фильма')
        try:
            payload = jsonpickle.decode(flask.request.data)
        except:
            payload = {'name': 'test', 'description': 'test', 'length': 60}
        movie_id = repo.create(payload["name"], payload["description"], payload["length"])
        movie = repo.get(movie_id)
        response = app.make_response("")
        response.status_code = 201
        response.content_type = "application/json"
        response.data = jsonpickle.encode(movie)
        app.logger.info('Фильм с идентификатором %s успешно создан' % movie_id)
        return response


class MovieListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int, default=1)
    parser.add_argument("page_size", type=int, default=5)

    def get(self):
        app.logger.info('Получен запрос на получение списка фильмов')
        try:
            args = self.parser.parse_args(strict=True)
        except:
            args = {'page': 1, 'page_size': 5}
        app.logger.info('Номер страницы: %d; количество фильмов на странице: %d' % (args['page'], args['page_size']))
        movies_list = repo.read_paginated(page_number=args['page'], page_size=args['page_size'])
        movies = ''
        for movie in movies_list:
            movies += "\n" + movie.to_json()
        response = app.make_response("")
        response.status_code = 200
        response.content_type = "application/json"
        response.data = movies
        app.logger.info('Запрос на получение списка фильмов успешно обработан')
        return response
