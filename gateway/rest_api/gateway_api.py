from flask_restful import Resource, reqparse
import flask
import jsonpickle
import requests
from ticket.domain.ticket import Ticket
from seance.domain.seance import Seance


class GatewayTicketResource(Resource):
    def get(self, ticket_id):
        response = requests.get("http://127.0.0.1:5003/tickets/%s" % ticket_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result

    def delete(self, ticket_id):
        response = requests.delete("http://127.0.0.1:5003/tickets/%s" % ticket_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewayTicketCreateResource(Resource):
    def post(self):
        response = requests.post("http://127.0.0.1:5003/tickets/create", data=flask.request.data)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewaySeanceResource(Resource):
    def get(self, seance_id):
        response_seance = requests.get("http://127.0.0.1:5002/seances/%s" % seance_id)

        seance = jsonpickle.decode(response_seance.content)
        movie_id = str(seance.movie_id)

        response_movie = requests.get("http://127.0.0.1:5001/movies/%s" % movie_id)
        movie = jsonpickle.decode(response_movie.content)
        response = {"seance":seance, "movie":movie}
        result = flask.Response(status=response_seance.status_code, headers=response_seance.headers.items(),
                                response=jsonpickle.encode(response))
        return result

    def patch(self, seance_id):
        response = requests.patch("http://127.0.0.1:5002/seances/%s" % seance_id, data=flask.request.data)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result

    def delete(self, seance_id):
        response = requests.delete("http://127.0.0.1:5002/seances/%s" % seance_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewaySeanceCreateResource(Resource):
    def post(self):
        response = requests.post("http://127.0.0.1:5002/seances/create", data=flask.request.data)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewaySeanceListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("page", type=int)
    parser.add_argument("page_size", type=int)

    def get(self):
        args = self.parser.parse_args(strict=True)
        page = args['page']
        page_size = args['page_size']
        payload = (('page', page), ('page_size', page_size))
        response = requests.get("http://127.0.0.1:5002/seances", params=payload)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewayMovieResource(Resource):
    def get(self, movie_id):
        response = requests.get("http://127.0.0.1:5001/movies/%s" % movie_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result

    def delete(self, movie_id):
        response = requests.delete("http://127.0.0.1:5001/movies/%s" % movie_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewayMovieCreateResource(Resource):
    def post(self):
        response = requests.post("http://127.0.0.1:5001/movies/create", data=flask.request.data)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewayUserResource(Resource):
    def get(self, user_id):
        response = requests.get("http://127.0.0.1:5004/users/%s" % user_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result

    def delete(self, user_id):
        response = requests.delete("http://127.0.0.1:5004/users/%s" % user_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewayUserCreateResource(Resource):
    def post(self):
        response = requests.post("http://127.0.0.1:5004/users/create", data=flask.request.data)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewayBuyTicket(Resource):
    user_id = "5bd0a351af13c713737dae92"

    def post(self):
        payload = jsonpickle.decode(flask.request.data)
        payload1 = {'seat_number': payload["seat_number"], 'status': 'buy'}
        response = requests.patch("http://127.0.0.1:5002/seances/%s" % payload["seance_id"], jsonpickle.encode(payload1))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        if result.status_code != 201:
            return result

        response = requests.post("http://127.0.0.1:5003/tickets/create", jsonpickle.encode(payload))
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)

        ticket = jsonpickle.decode(response.content)
        payload3 = {'ticket_id': str(ticket.id), 'status': 'buy'}
        requests.patch("http://127.0.0.1:5004/users/%s" % self.user_id, jsonpickle.encode(payload3))
        return result


class GatewayReturnTicket(Resource):
    user_id = "5bd0a351af13c713737dae92"

    def post(self, ticket_id):
        response = requests.get("http://127.0.0.1:5003/tickets/%s" % ticket_id)

        ticket = jsonpickle.decode(response.content)
        payload1 = {'seat_number': ticket.seat_number, 'status': 'release'}
        requests.patch("http://127.0.0.1:5002/seances/%s" % ticket.seance_id, jsonpickle.encode(payload1))

        payload3 = {'ticket_id': ticket_id, 'status': 'release'}
        requests.patch("http://127.0.0.1:5004/users/%s" % self.user_id, jsonpickle.encode(payload3))

        response = requests.delete("http://127.0.0.1:5003/tickets/%s" % ticket_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result