from flask_restful import Resource, reqparse
import flask
import jsonpickle
import requests
from ticket.domain.ticket import Ticket


class GatewayTicketResource(Resource):
    def get(self, ticket_id):
        sess = requests.session()
        response = requests.get("http://127.0.0.1:5003/tickets/%s" % ticket_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result

    def delete(self, ticket_id):
        sess = requests.session()
        response = sess.delete("http://127.0.0.1:5003/tickets/%s" % ticket_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewayTicketCreateResource(Resource):
    def post(self):
        sess = requests.session()
        response = sess.post("http://127.0.0.1:5003/tickets/create", data=flask.request.data)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewaySeanceResource(Resource):
    def get(self, seance_id):
        sess = requests.session()
        response = requests.get("http://127.0.0.1:5002/seances/%s" % seance_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result

    def patch(self, seance_id):
        sess = requests.session()
        response = sess.patch("http://127.0.0.1:5002/seances/%s" % seance_id, data=flask.request.data)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result

    def delete(self, seance_id):
        sess = requests.session()
        response = sess.delete("http://127.0.0.1:5002/seances/%s" % seance_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewaySeanceCreateResource(Resource):
    def post(self):
        sess = requests.session()
        response = sess.post("http://127.0.0.1:5002/seances/create", data=flask.request.data)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewaySeanceListResource(Resource):
    def get(self):
        sess = requests.session()
        response = sess.delete("http://127.0.0.1:5002/seances")
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewayMovieResource(Resource):
    def get(self, movie_id):
        sess = requests.session()
        response = requests.get("http://127.0.0.1:5001/movies/%s" % movie_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result

    def delete(self, movie_id):
        sess = requests.session()
        response = sess.delete("http://127.0.0.1:5001/movies/%s" % movie_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewayMovieCreateResource(Resource):
    def post(self):
        sess = requests.session()
        response = sess.post("http://127.0.0.1:5001/movies/create", data=flask.request.data)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewayUserResource(Resource):
    def get(self, user_id):
        sess = requests.session()
        response = requests.get("http://127.0.0.1:5004/users/%s" % user_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result

    def delete(self, user_id):
        sess = requests.session()
        response = sess.delete("http://127.0.0.1:5004/users/%s" % user_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewayUserCreateResource(Resource):
    def post(self):
        sess = requests.session()
        response = sess.post("http://127.0.0.1:5004/users/create", data=flask.request.data)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewayBuyTicket(Resource):
    user_id = "5bd0a351af13c713737dae92"

    def post(self):
        payload = jsonpickle.decode(flask.request.data)
        sess = requests.session()
        payload1 = {'seat_number': payload["seat_number"], 'status': 'buy'}
        response = sess.patch("http://127.0.0.1:5002/seances/%s" % payload["seance_id"], jsonpickle.encode(payload1))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 201:
            return result

        response = sess.post("http://127.0.0.1:5003/tickets/create", jsonpickle.encode(payload))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)

        ticket = jsonpickle.decode(response.content)
        payload3 = {'ticket_id': str(ticket.id), 'status': 'buy'}
        sess.patch("http://127.0.0.1:5004/users/%s" % self.user_id, jsonpickle.encode(payload3))
        return result


class GatewayReturnTicket(Resource):
    user_id = "5bd0a351af13c713737dae92"

    def post(self, ticket_id):
        sess = requests.session()
        response = sess.get("http://127.0.0.1:5003/tickets/%s" % ticket_id)

        ticket = jsonpickle.decode(response.content)
        payload1 = {'seat_number': ticket.seat_number, 'status': 'release'}
        sess.patch("http://127.0.0.1:5002/seances/%s" % ticket.seance_id, jsonpickle.encode(payload1))

        payload3 = {'ticket_id': ticket_id, 'status': 'release'}
        sess.patch("http://127.0.0.1:5004/users/%s" % self.user_id, jsonpickle.encode(payload3))

        response = sess.delete("http://127.0.0.1:5003/tickets/%s" % ticket_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result