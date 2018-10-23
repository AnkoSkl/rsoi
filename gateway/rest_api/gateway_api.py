from flask_restful import Resource, reqparse
import flask
import jsonpickle
import requests


class GatewayTicketResource(Resource):
    def get(self, ticket_id):
        sess = requests.session()
        for cookie in flask.request.cookies:
            sess.cookies[cookie] = flask.request.cookies[cookie]
        response = requests.get("http://127.0.0.1:5003/tickets/%s" % ticket_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result

    def delete(self, ticket_id):
        sess = requests.session()
        for cookie in flask.request.cookies:
            sess.cookies[cookie] = flask.request.cookies[cookie]
        response = sess.delete("http://127.0.0.1:5003/tickets/%s" % ticket_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewayTicketCreateResource(Resource):
    def post(self):
        sess = requests.session()
        for cookie in flask.request.cookies:
            sess.cookies[cookie] = flask.request.cookies[cookie]
        response = sess.post("http://127.0.0.1:5003/tickets/create", data=flask.request.data)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewaySeanceResource(Resource):
    def get(self, seance_id):
        sess = requests.session()
        for cookie in flask.request.cookies:
            sess.cookies[cookie] = flask.request.cookies[cookie]
        response = requests.get("http://127.0.0.1:5002/seances/%s" % seance_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result

    def patch(self, seance_id):
        sess = requests.session()
        for cookie in flask.request.cookies:
            sess.cookies[cookie] = flask.request.cookies[cookie]
        response = sess.patch("http://127.0.0.1:5002/seances/%s" % seance_id, data=flask.request.data)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result

    def delete(self, seance_id):
        sess = requests.session()
        for cookie in flask.request.cookies:
            sess.cookies[cookie] = flask.request.cookies[cookie]
        response = sess.delete("http://127.0.0.1:5002/seances/%s" % seance_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewaySeanceCreateResource(Resource):
    def post(self):
        sess = requests.session()
        for cookie in flask.request.cookies:
            sess.cookies[cookie] = flask.request.cookies[cookie]
        response = sess.post("http://127.0.0.1:5002/seances/create", data=flask.request.data)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewaySeanceListResource(Resource):
    def get(self):
        sess = requests.session()
        for cookie in flask.request.cookies:
            sess.cookies[cookie] = flask.request.cookies[cookie]
        response = sess.delete("http://127.0.0.1:5002/seances")
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewayMovieResource(Resource):
    def get(self, movie_id):
        sess = requests.session()
        for cookie in flask.request.cookies:
            sess.cookies[cookie] = flask.request.cookies[cookie]
        response = requests.get("http://127.0.0.1:5001/movies/%s" % movie_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result

    def delete(self, movie_id):
        sess = requests.session()
        for cookie in flask.request.cookies:
            sess.cookies[cookie] = flask.request.cookies[cookie]
        response = sess.delete("http://127.0.0.1:5001/movies/%s" % movie_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewayMovieCreateResource(Resource):
    def post(self):
        sess = requests.session()
        for cookie in flask.request.cookies:
            sess.cookies[cookie] = flask.request.cookies[cookie]
        response = sess.post("http://127.0.0.1:5001/movies/create", data=flask.request.data)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewayUserResource(Resource):
    def get(self, user_id):
        sess = requests.session()
        for cookie in flask.request.cookies:
            sess.cookies[cookie] = flask.request.cookies[cookie]
        response = requests.get("http://127.0.0.1:5004/users/%s" % user_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result

    def delete(self, user_id):
        sess = requests.session()
        for cookie in flask.request.cookies:
            sess.cookies[cookie] = flask.request.cookies[cookie]
        response = sess.delete("http://127.0.0.1:5004/users/%s" % user_id)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result


class GatewayUserCreateResource(Resource):
    def post(self):
        sess = requests.session()
        for cookie in flask.request.cookies:
            sess.cookies[cookie] = flask.request.cookies[cookie]
        response = sess.post("http://127.0.0.1:5004/users/create", data=flask.request.data)
        result = flask.Response(status=response.status_code, headers=response.headers.items(),
                                response=response.content)
        return result