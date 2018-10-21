from user import app
from flask_restful import Resource, abort, reqparse
from user.repository.user_repository import UserRepository
import jsonpickle
import flask


repo = UserRepository()


def abort_if_seance_doesnt_exist(user_id):
    if not repo.exists(user_id):
        abort(404, message="User {} doesn't exist".format(user_id))


class UserResource(Resource):
    def get(self, user_id):
        abort_if_seance_doesnt_exist(user_id)
        user = repo.get(user_id)
        response = app.make_response("")
        response.status_code = 200
        response.data = jsonpickle.encode(user)
        return response

    def delete(self, user_id):
        abort_if_seance_doesnt_exist(user_id)
        repo.delete(user_id)
        response = app.make_response("User %d deleted successfully" % user_id)
        response.status_code = 204
        return response


class UserCreateResource(Resource):
    def post(self):
        payload = jsonpickle.decode(flask.request.data)
        user_id = repo.create(payload["name"], payload["password"])
        seance = repo.get(user_id)
        response = app.make_response("")
        response.status_code = 201
        response.data = jsonpickle.encode(seance)
        return response