from ticket import app
from flask_restful import Resource, abort, reqparse
from ticket.repository.ticket_repository import TicketRepository
import jsonpickle
import flask


repo = TicketRepository()


def abort_if_seance_doesnt_exist(ticket_id):
    if not repo.exists(ticket_id):
        abort(404, message="Ticket {} doesn't exist".format(ticket_id))


class TicketResource(Resource):
    def get(self, ticket_id):
        abort_if_seance_doesnt_exist(ticket_id)
        ticket = repo.get(ticket_id)
        response = app.make_response("")
        response.status_code = 200
        response.data = jsonpickle.encode(ticket)
        return response

    def delete(self, ticket_id):
        abort_if_seance_doesnt_exist(ticket_id)
        repo.delete(ticket_id)
        response = app.make_response("Ticket %d deleted successfully" % ticket_id)
        response.status_code = 204
        return response


class TicketCreateResource(Resource):
    def post(self):
        payload = jsonpickle.decode(flask.request.data)
        ticket_id = repo.create(payload["seance_id"], payload["seat_number"])
        ticket = repo.get(ticket_id)
        response = app.make_response("")
        response.status_code = 201
        response.data = jsonpickle.encode(ticket)
        return response


class TicketListResource(Resource):
    def get(self):
        ticket_list = repo.read_all()
        response = app.make_response("")
        response.status_code = 200
        response.data = jsonpickle.encode(ticket_list)
        return response