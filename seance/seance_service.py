from movie import app
from flask_restful import Api
from seance.rest_api.seance_resource import *
from movie.repository.movie_repository import Movies


api = Api(app)
service_namespace = "/seances"

api.add_resource(SeanceListResource, "/seances")
api.add_resource(SeanceResource, "/seances/<seance_id>")
api.add_resource(SeanceCreateResource, "/seances/create")


if __name__ == '__main__':
    app.run(port=5002, debug=True)