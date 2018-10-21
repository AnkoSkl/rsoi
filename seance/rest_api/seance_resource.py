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
        response = app.make_response("Seance %d deleted successfully" % seance_id)
        response.status_code = 204
        return response