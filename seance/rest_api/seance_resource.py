from seance import app
from flask_restful import Resource, abort, reqparse
from seance.repository.seance_repository import SeanceRepository
import jsonpickle
import flask


repo = SeanceRepository()


def abort_if_seance_doesnt_exist(seance_id):
    if not repo.exists(seance_id):
        abort(404, message="Seance {} doesn't exist".format(seance_id))


class SeanceResource(Resource):
    def get(self, seance_id):
        abort_if_seance_doesnt_exist(seance_id)
        seance = repo.get(seance_id)
        response = app.make_response("")
        response.status_code = 200
        response.data = jsonpickle.encode(seance)
        return response

    def delete(self, seance_id):
        abort_if_seance_doesnt_exist(seance_id)
        repo.delete(seance_id)
        response = app.make_response("Seance %s deleted successfully" % seance_id)
        response.status_code = 204
        return response

    def patch(self, seance_id):
        abort_if_seance_doesnt_exist(seance_id)
        payload = jsonpickle.decode(flask.request.data)
        if payload["status"] == "buy":
            res = repo.get_a_seat(seance_id, payload["seat_number"])
            if res == True:
                response = app.make_response("")
                response.status_code = 201
            else:
                response = app.make_response("This seat cannot be bought!")
                response.status_code = 301
        else:
            res = repo.free_a_seat(seance_id, payload["seat_number"])
            if res == True:
                response = app.make_response("")
                response.status_code = 201
            else:
                response = app.make_response("This seat cannot be released!")
                response.status_code = 301

        seance = repo.get(seance_id)
        response.data = jsonpickle.encode(seance)
        return response


class SeanceCreateResource(Resource):
    def post(self):
        payload = jsonpickle.decode(flask.request.data)
        seance_id = repo.create(payload["movie_id"], payload["datetime"], payload["number_of_seats"])
        seance = repo.get(seance_id)
        response = app.make_response("")
        response.status_code = 201
        response.data = jsonpickle.encode(seance)
        return response


class SeanceListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int, default=1)
    parser.add_argument("page_size", type=int, default=5)

    def get(self):
        args = self.parser.parse_args(strict=True)
        #seances_list = repo.read_all()
        seances_list = repo.read_paginated(page_number=args['page'], page_size=args['page_size'])
        response = app.make_response("")
        response.status_code = 200
        response.data = jsonpickle.encode(seances_list)
        return response