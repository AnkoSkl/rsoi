import flask
import jsonpickle
import requests
from flask_restful import Resource, reqparse
from seance.domain.seance import Seance
from movie.domain.movie import Movie
from ticket.domain.ticket import Ticket
from user.domain.user import User
from config import current_config
from gateway import app
import json


class GatewayTicketResource(Resource):
    def get(self, ticket_id):
        app.logger.info('Получен запрос на получение информации о билете с идентификатором %s' % ticket_id)
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
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
        try:
            args = self.parser.parse_args(strict=True)
            req = requests.session()
            for cookie in flask.request.cookies:
                req.cookies[cookie] = flask.request.cookies[cookie]
            cookies = req.cookies
            token = cookies['token']

            response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                    "/token", data=jsonpickle.encode({'token':token}))
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            if result.status_code != 200:
                return result
        except:
            args = {'page': 1, 'page_size': 5}
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
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
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

        seance = Seance.from_json(response_seance.content) #jsonpickle.decode(response_seance.content)
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
        movie = Movie.from_json(response_movie.content)
        response = seance.to_json() + '\n' + movie.to_json()
        result = flask.Response(status=response_seance.status_code, headers=response_seance.headers.items(),
                                response=response)
        app.logger.info('Запрос на получение подробной информации о сеансе с идентификатором %s успешно обработан'
                        % seance_id)
        return result


class GatewaySeanceCreateResource(Resource):
    def post(self):
        app.logger.info('Получен запрос на создание сеанса')
        try:
            response = requests.post(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH +
                                     current_config.CREATE_PATH, data=flask.request.data)
            req = requests.session()
            for cookie in flask.request.cookies:
                req.cookies[cookie] = flask.request.cookies[cookie]
            cookies = req.cookies
            token = cookies['token']

            response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                    "/token", data=jsonpickle.encode({'token':token}))
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            if result.status_code != 200:
                return result
        except:
            payload = {'movie_id': '5bd89b59af13c757e1b7f3fd', 'datetime': '12.11.2018_20:00', 'number_of_seats': 50}
            response = requests.post(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH +
                                     current_config.CREATE_PATH, data = jsonpickle.encode(payload))
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
        try:
            req = requests.session()
            for cookie in flask.request.cookies:
                req.cookies[cookie] = flask.request.cookies[cookie]
            cookies = req.cookies
            token = cookies['token']

            response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                    "/token", data=jsonpickle.encode({'token':token}))
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            if result.status_code != 200:
                return result
            args = self.parser.parse_args(strict=True)
        except:
            args = {'page': 1, 'page_size': 5}
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
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
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
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
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
        try:
            req = requests.session()
            for cookie in flask.request.cookies:
                req.cookies[cookie] = flask.request.cookies[cookie]
            cookies = req.cookies
            token = cookies['token']

            response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                    "/token", data=jsonpickle.encode({'token':token}))
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            if result.status_code != 200:
                return result
            response = requests.post(current_config.MOVIE_SERVICE_URL + current_config.MOVIE_SERVICE_PATH +
                                     current_config.CREATE_PATH, data=flask.request.data)
        except:
            payload = {'name': 'test', 'description': 'test', 'length': 30}
            response = requests.post(current_config.MOVIE_SERVICE_URL + current_config.MOVIE_SERVICE_PATH +
                                     current_config.CREATE_PATH, data=jsonpickle.encode(payload))
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
        try:
            args = self.parser.parse_args(strict=True)
            req = requests.session()
            for cookie in flask.request.cookies:
                req.cookies[cookie] = flask.request.cookies[cookie]
            cookies = req.cookies
            token = cookies['token']

            response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                    "/token", data=jsonpickle.encode({'token':token}))
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            if result.status_code != 200:
                return result
        except:
            args = {'page': 1, 'page_size': 5}
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
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
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
        try:
            args = self.parser.parse_args(strict=True)
            req = requests.session()
            for cookie in flask.request.cookies:
                req.cookies[cookie] = flask.request.cookies[cookie]
            cookies = req.cookies
            token = cookies['token']

            response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                    "/token", data=jsonpickle.encode({'token':token}))
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            if result.status_code != 200:
                return result
        except:
            args = {'page': 1, 'page_size': 5}
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


class GatewayAuthorization(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str)
    parser.add_argument("password", type=str)

    def get(self):
        app.logger.info('Получен запрос на аутентификацию')
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        args = self.parser.parse_args(strict=True)
        login = args['name']
        password = args['password']
        payload = {'name': login, 'password': password}
        response = req.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                           current_config.GET_TOKEN_URL_PATH, params=payload)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if response.status_code == 200:
            app.logger.info('Запрос на авторизацию успешно обработан')
        else:
            app.logger.warning('Авторизация не может быть произведена')
        return result


class GatewayBuyTicket(Resource):
    #user_id = "5bd0a351af13c713737dae92"

    def post(self):
        app.logger.info('Получен запрос на покупку билета')
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']

        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        user = User.from_json(response.content)
        user_id = user.id
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
                            % (payload["seance_id"], user_id))

        response = requests.post(current_config.TICKET_SERVICE_URL + current_config.TICKET_SERVICE_PATH +
                                 current_config.CREATE_PATH, jsonpickle.encode(payload))
        ticket = Ticket.from_json(response.content) #jsonpickle.decode(response.content)
        if response.status_code == 201:
            app.logger.info('Билет с идентификатором %s успешно создан' % str(ticket.id))
        else:
            payload1['status'] = 'return'
            requests.patch(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH + "/" +
                           payload["seance_id"], jsonpickle.encode(payload1))
            app.logger.warning('Билет не может быть создан')
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            return result

        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)

        payload3 = {'ticket_id': str(ticket.id), 'status': 'buy'}
        response = requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                  "/%s" % user_id, jsonpickle.encode(payload3))
        if response.status_code == 201:
            app.logger.info('Покупка билета для пользователя успешно произведена')
        else:
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            payload1['status'] = 'return'
            requests.patch(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH + "/" +
                           payload["seance_id"], jsonpickle.encode(payload1))
            requests.delete(current_config.TICKET_SERVICE_URL + current_config.TICKET_SERVICE_PATH + "/" +
                            payload3['ticket_id'])
            app.logger.warning('Покупка билета не может быть завершена')
        return result


class GatewayReturnTicket(Resource):
    #user_id = "5bd0a351af13c713737dae92"

    def delete(self, ticket_id):
        app.logger.info('Получен запрос на возврат билета')
        req = requests.session()
        for cookie in flask.request.cookies:
            req.cookies[cookie] = flask.request.cookies[cookie]
        cookies = req.cookies
        token = cookies['token']
        response = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                "/token", data=jsonpickle.encode({'token':token}))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 200:
            return result
        user = User.from_json(response.content)
        user_id = user.id

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

        ticket = Ticket.from_json(response.content) #jsonpickle.decode(response.content)
        payload1 = {'seat_number': ticket.seat_number, 'status': 'return'}
        response = requests.patch(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH +
                                  "/%s" % ticket.seance_id, jsonpickle.encode(payload1))
        if response.status_code == 201:
            app.logger.info('Освобождение места на сеансе успешно завершен')
        else:
            app.logger.warning('Освобождение места на сеансе не может быть завершено')
            result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                    response=response.content)
            return result

        payload3 = {'ticket_id': ticket_id, 'status': 'return'}
        response = requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                                  "/%s" % user_id, jsonpickle.encode(payload3))
        if response.status_code == 201:
            app.logger.info('Возврат билета для пользователя %s успешно произведен' % user_id)
        else:
            payload1['status'] = 'buy'
            requests.patch(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH +
                           "/%s" % ticket.seance_id, jsonpickle.encode(payload1))
            app.logger.warning('Возврат билета для пользователя %s не может быть произведен' % user_id)
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
            payload1['status'] = 'buy'
            requests.patch(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH +
                           "/%s" % ticket.seance_id, jsonpickle.encode(payload1))
            payload3['status'] = 'buy'
            requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                           "/%s" % user_id, jsonpickle.encode(payload3))
            app.logger.warning('Билет с идентификатором %s не может быть удален' % ticket_id)
        return result