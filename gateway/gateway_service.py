from movie import app
from flask_restful import Api
from movie.rest_api.movie_resource import MovieResource, MovieCreateResource
from seance.rest_api.seance_resource import SeanceResource, SeanceListResource, SeanceCreateResource
from user.rest_api.user_resource import UserResource, UserListResource, UserCreateResource
from ticket.rest_api.ticket_resource import TicketResource, TicketListResource, TicketCreateResource
from gateway.rest_api.gateway_api import *


api = Api(app)

api.add_resource(GatewayTicketResource, "/gateway/api/tickets" + "/<ticket_id>")
api.add_resource(GatewayTicketCreateResource, "/gateway/api/tickets/create")
api.add_resource(GatewaySeanceResource, "/gateway/api/seances" + "/<seance_id>")
api.add_resource(GatewaySeanceListResource, "/gateway/api/seances")
api.add_resource(GatewaySeanceCreateResource, "/gateway/api/seances/create")
api.add_resource(GatewayMovieResource, "/gateway/api/movies" + "/<movie_id>")
api.add_resource(GatewayMovieCreateResource, "/gateway/api/movies/create")
api.add_resource(GatewayUserResource, "/gateway/api/users" + "/<user_id>")
api.add_resource(GatewayUserCreateResource, "/gateway/api/users/create")


if __name__ == '__main__':
    app.run()