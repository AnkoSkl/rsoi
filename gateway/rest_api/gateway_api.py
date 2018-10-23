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

    def post(self):
        sess = requests.session()
        for cookie in flask.request.cookies:
            sess.cookies[cookie] = flask.request.cookies[cookie]
        response = sess.post("http://127.0.0.1:5003/tickets/create", data=flask.request.data)
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