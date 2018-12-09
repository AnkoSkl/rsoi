from seance import app
from flask_restful import Resource, abort, reqparse
from seance.repository.seance_repository import SeanceRepository
import jsonpickle
import flask
import json


def abort_if_seance_doesnt_exist(seance_id, repo):
    if not repo.exists(seance_id):
        app.logger.error('Сеанса с идентификатором %s не существует!', seance_id)
        abort(404, message="Seance {} doesn't exist".format(seance_id))


class SeanceResource(Resource):
    def get(self, seance_id):
        repo = SeanceRepository()
        app.logger.info('Получен запрос на получение информации о сеансе с идентификатором %s' % seance_id)
        abort_if_seance_doesnt_exist(seance_id, repo)
        seance = repo.get(seance_id)
        response = app.make_response("")
        response.status_code = 200
        response.content_type = "application/json"
        response.data = seance.to_json() #jsonpickle.encode(seance)
        app.logger.info('Запрос на получение информации о сеансе с идентификатором %s успешно обработан' % seance_id)
        return response

    def delete(self, seance_id):
        repo = SeanceRepository()
        app.logger.info('Получен запрос на удаление сеанса с идентификатором %s' % seance_id)
        abort_if_seance_doesnt_exist(seance_id, repo)
        repo.delete(seance_id)
        response = app.make_response("Seance %s deleted successfully" % seance_id)
        response.status_code = 204
        app.logger.info('Сеанс с идентификатором %s успешно удален' % seance_id)
        return response

    def patch(self, seance_id):
        repo = SeanceRepository()
        app.logger.info('Получен запрос на покупку/возврат билета на сеанс с идентификатором %s' % seance_id)
        abort_if_seance_doesnt_exist(seance_id, repo)
        try:
            payload = jsonpickle.decode(flask.request.data)
        except:
            payload = {'status': 'buy', 'seat_number': 1}
        if payload["status"] == "buy":
            app.logger.info('Покупка билета')
            res = repo.get_a_seat(seance_id, payload["seat_number"])
            if res:
                response = app.make_response("")
                response.content_type = "application/json"
                response.status_code = 201
                app.logger.info('Место на сеанс %s успешно куплено' % seance_id)
            else:
                response = app.make_response("This seat cannot be bought!")
                response.content_type = "application/json"
                response.status_code = 409
                app.logger.warning('Выбранное место на сеанс %s занято, покупка билета не может быть завершена'
                                   % seance_id)
        else:
            app.logger.info('Возврат билета')
            res = repo.free_a_seat(seance_id, payload["seat_number"])
            if res:
                response = app.make_response("")
                response.content_type = "application/json"
                response.status_code = 201
                app.logger.info('Возврат билета на сеанс %s успешно завершен' % seance_id)
            else:
                response = app.make_response("This seat cannot be released!")
                response.content_type = "application/json"
                response.status_code = 409
                app.logger.warning('Возврат билета на сеанс %s не может быть завершен, так как место еще не занято'
                                % seance_id)

        seance = repo.get(seance_id)
        response.data = seance.to_json()
        return response


class SeanceCreateResource(Resource):
    def post(self):
        repo = SeanceRepository()
        app.logger.info('Получен запрос на создание сеанса')
        try:
            payload = jsonpickle.decode(flask.request.data)
        except:
            payload = {'movie_id': '5bd89b59af13c757e1b7f3fd', 'datetime': '12.11.2018_20:00', 'number_of_seats': 50}
        seance_id = repo.create(payload["movie_id"], payload["datetime"], payload["number_of_seats"])
        seance = repo.get(seance_id)
        response = app.make_response("")
        response.status_code = 201
        response.content_type = "application/json"
        response.data = seance.to_json()  #jsonpickle.encode(seance)
        app.logger.info('Сеанс с идентификатором %s успешно создан' % seance_id)
        return response


class SeanceListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int, default=1)
    parser.add_argument("page_size", type=int, default=5)

    def get(self):
        repo = SeanceRepository()
        app.logger.info('Получен запрос на получение списка сеансов')
        try:
            args = self.parser.parse_args(strict=True)
        except:
            args = {'page': 1, 'page_size': 5}
        app.logger.info('Номер страницы: %d; количество сеансов на странице: %d' % (args['page'], args['page_size']))
        seances_list, is_prev_page, is_next_page = repo.read_paginated(page_number=args['page'],
                                                                       page_size=args['page_size'])
        seances = ''
        for seance in seances_list:
            seances += seance.to_json() + '\n'
        dictr = {"is_prev_page": is_prev_page, "is_next_page": is_next_page}
        seances += "\n" + json.dumps(dictr)
        response = app.make_response("")
        response.status_code = 200
        response.content_type = "application/json"
        response.data = seances
        app.logger.info('Запрос на получение списка сеансов успешно обработан')
        return response
