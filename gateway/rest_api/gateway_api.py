from flask_restful import Resource, reqparse
from gateway import app
from gateway.config import current_config
import flask
import jsonpickle
import requests
from ticket.domain.ticket import Ticket
from seance.domain.seance import Seance


class GatewayTicketResource(Resource):
    def get(self, ticket_id):
        app.logger.info('Получен запрос на получение информации о билете с идентификатором %s' % ticket_id)
        response = requests.get(current_config.TICKET_SERVICE_URL + current_config.TICKET_SERVICE_PATH +
                                "/%s" % ticket_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Информация о билете с идентификатором %s успещно получена' % ticket_id)
        else:
            app.logger.warning('Информация о билете с идентификатором %s не может быть получена' % ticket_id)
        return result


class GatewayTicketListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int)
    parser.add_argument("page_size", type=int)

    def get(self):
        app.logger.info('Получен запрос на получение списка билетов')
        args = self.parser.parse_args(strict=True)
        app.logger.info('Номер страницы: %d; количество билетов на странице: %d' % (args['page'], args['page_size']))
        page = args['page']
        page_size = args['page_size']
        payload = (('page', page), ('page_size', page_size))
        response = requests.get(current_config.TICKET_SERVICE_URL + current_config.TICKET_SERVICE_PATH, params=payload)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение списка билетов успешно обработан')
        else:
            app.logger.warning('Список билетов не может быть получен')
        return result


class GatewaySeanceResource(Resource):
    def get(self, seance_id):
        app.logger.info('Получен запрос на получение подробной информации о сеансе с идентификатором %s' % seance_id)
        response_seance = requests.get(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH +
                                       "/%s" % seance_id)
        if response_seance.status_code == 200:
            app.logger.info('Запрос на получение информации о сеансе с идентификатором %s успешно обработан'
                            % seance_id)
        else:
            app.logger.warning('Информация о сеансе с идентификатором %s не модет быть получена' % seance_id)
            result = flask.Response(status=response_seance.status_code, headers=response_seance.headers.items(),
                                    response=response_seance.content)
            return result

        seance = jsonpickle.decode(response_seance.content)
        movie_id = str(seance.movie_id)

        response_movie = requests.get(current_config.MOVIE_SERVICE_URL + current_config.MOVIE_SERVICE_PATH +
                                      "/%s" % movie_id)
        if response_movie.status_code == 200:
            app.logger.info('Запрос на получение информации о фильме с идентификатором %s успешно обработан'
                            % movie_id)
        else:
            app.logger.warning('Информация о фильме с идентификатором %s не модет быть получена' % movie_id)
            result = flask.Response(status=response_movie.status_code, headers=response_movie.headers.items(),
                                    response=response_movie.content)
            return result
        movie = jsonpickle.decode(response_movie.content)
        response = {"seance":seance, "movie":movie}
        result = flask.Response(status=response_seance.status_code, headers=response_seance.headers.items(),
                                response=jsonpickle.encode(response))
        app.logger.info('Запрос на получение подробной информации о сеансе с идентификатором %s успешно обработан'
                        % seance_id)
        return result


class GatewaySeanceCreateResource(Resource):
    def post(self):
        app.logger.info('Получен запрос на создание сеанса')
        response = requests.post(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH +
                                 current_config.CREATE_PATH, data=flask.request.data)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 201:
            app.logger.info('Сеанс успешно создан')
        else:
            app.logger.warning('Сеанс не может быть создан')
        return result


class GatewaySeanceListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int)
    parser.add_argument("page_size", type=int)

    def get(self):
        app.logger.info('Получен запрос на получение списка сеансов')
        args = self.parser.parse_args(strict=True)
        app.logger.info('Номер страницы: %d; количество сеансов на странице: %d' % (args['page'], args['page_size']))
        page = args['page']
        page_size = args['page_size']
        payload = (('page', page), ('page_size', page_size))
        response = requests.get(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH, params=payload)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение списка сеансов успешно обработан')
        else:
            app.logger.warning('Список сеансов не может быть получен')
        return result


class GatewayMovieResource(Resource):
    def get(self, movie_id):
        app.logger.info('Получен запрос на получение информации о фильме с идентификатором %s' % movie_id)
        response = requests.get(current_config.MOVIE_SERVICE_URL + current_config.MOVIE_SERVICE_PATH +
                                "/%s" % movie_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение информации о фильме с идентификатором %s успешно обработан' % movie_id)
        else:
            app.logger.warning('Информация о фильме с идентификатором %s не может быть получена' % movie_id)
        return result

    def delete(self, movie_id):
        app.logger.info('Получен запрос на удаление фильма с идентификатором %s' % movie_id)
        response = requests.delete(current_config.MOVIE_SERVICE_URL + current_config.MOVIE_SERVICE_PATH +
                                   "/%s" % movie_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 204:
            app.logger.info('Фильм с идентификатором %s успешно удален' % movie_id)
        else:
            app.logger.warning('Фильм с идентификатором %s не может быть удален' % movie_id)
        return result


class GatewayMovieCreateResource(Resource):
    def post(self):
        app.logger.info('Получен запрос на создание фильма')
        response = requests.post(current_config.MOVIE_SERVICE_URL + current_config.MOVIE_SERVICE_PATH +
                                 current_config.CREATE_PATH, data=flask.request.data)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 201:
            app.logger.info('Фильм успешно создан')
        else:
            app.logger.warning('Фильм не может быть создан')
        return result


class GatewayMovieListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int)
    parser.add_argument("page_size", type=int)

    def get(self):
        app.logger.info('Получен запрос на получение списка фильмов')
        args = self.parser.parse_args(strict=True)
        page = args['page']
        page_size = args['page_size']
        app.logger.info('Номер страницы: %d; количество фильмов на странице: %d' % (args['page'], args['page_size']))
        payload = (('page', page), ('page_size', page_size))
        response = requests.get(current_config.MOVIE_SERVICE_URL + current_config.MOVIE_SERVICE_PATH, params=payload)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение списка фильмов успешно обработан')
        else:
            app.logger.warning('Список фильмов не может быть получен')
        return result


class GatewayUserResource(Resource):
    def get(self, user_id):
        app.logger.info('Получен запрос на получение информации о пользователе с идентификатором %s' % user_id)
        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/%s" % user_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение информации о пользователе с идентификатором %s успешно обработан'
                            % user_id)
        else:
            app.logger.warning('Информация о пользователе с идентификатором %s не может быть получена' % user_id)
        return result


class GatewayUserListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int)
    parser.add_argument("page_size", type=int)

    def get(self):
        app.logger.info('Получен запрос на получение списка пользователей')
        args = self.parser.parse_args(strict=True)
        app.logger.info('Номер страницы: %d; количество пользователей на странице: %d'
                        % (args['page'], args['page_size']))
        page = args['page']
        page_size = args['page_size']
        payload = (('page', page), ('page_size', page_size))
        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH, params=payload)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на получение списка пользователей успешно обработан')
        else:
            app.logger.warning('Список пользователей не может быть получен')
        return result


class GatewayBuyTicket(Resource):
    user_id = "5bd0a351af13c713737dae92"

    def post(self):
        app.logger.info('Получен запрос на покупку билета')
        payload = jsonpickle.decode(flask.request.data)
        payload1 = {'seat_number': payload["seat_number"], 'status': 'buy'}
        response = requests.patch(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH +
                                  "/%s" % payload["seance_id"], jsonpickle.encode(payload1))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 201:
            app.logger.error('Покупка билета на сеанс с идентификатором %s не может быть выполнена'
                             % payload["seance_id"])
            return result
        else:
            app.logger.info('Место на сеанс с идентификатором %s для пользователя с идентификатором %s успешно занято'
                            % (payload["seance_id"], self.user_id))

        response = requests.post(current_config.TICKET_SERVICE_URL + current_config.TICKET_SERVICE_PATH +
                                 current_config.CREATE_PATH, jsonpickle.encode(payload))
        ticket = jsonpickle.decode(response.content)
        if response.status_code == 201:
            app.logger.info('Билет с идентификатором %s успешно создан' % str(ticket.id))
        else:
            app.logger.warning('Билет не может быть создан')
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            return result

        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)

        payload3 = {'ticket_id': str(ticket.id), 'status': 'buy'}
        response = requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                  "/%s" % self.user_id, jsonpickle.encode(payload3))
        if response.status_code == 201:
            app.logger.info('Покупка билета для пользователя успешно произведена')
        else:
            app.logger.warning('Покупка билета не может быть завершена')
        return result


class GatewayReturnTicket(Resource):
    user_id = "5bd0a351af13c713737dae92"

    def delete(self, ticket_id):
        app.logger.info('Получен запрос на возврат билета')
        response = requests.get(current_config.TICKET_SERVICE_URL + current_config.TICKET_SERVICE_PATH +
                                "/%s" % ticket_id)
        if response.status_code == 200:
            app.logger.info('Запрос на получение информации о билете с идентификатором %s успешно обработан'
                            % ticket_id)
        else:
            app.logger.warning('Информация о билете с идентификатором %s не может быть получена' % ticket_id)
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            return result

        ticket = jsonpickle.decode(response.content)
        payload1 = {'seat_number': ticket.seat_number, 'status': 'release'}
        response = requests.patch(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH +
                                  "/%s" % ticket.seance_id, jsonpickle.encode(payload1))
        if response.status_code == 201:
            app.logger.info('Освобождение места на сеансе успешно завершен')
        else:
            app.logger.warning('Освобождение места на сеансе не может быть завершено')
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            return result

        payload3 = {'ticket_id': ticket_id, 'status': 'release'}
        response = requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                  "/%s" % self.user_id, jsonpickle.encode(payload3))
        if response.status_code == 201:
            app.logger.info('Возврат билета для пользователя %s успешно произведен' % self.user_id)
        else:
            app.logger.warning('Возврат билета для пользователя %s не может быть произведен' % self.user_id)
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            return result

        response = requests.delete(current_config.TICKET_SERVICE_URL + current_config.TICKET_SERVICE_PATH +
                                   "/%s" % ticket_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 204:
            app.logger.info('Билет с идентификатором %s успешно удален' % ticket_id)
        else:
            app.logger.warning('Билет с идентификатором %s не может быть удален' % ticket_id)
        return result