from movie import app
from flask_restful import Api
from gateway.rest_api.gateway_api import *


api = Api(app)

api.add_resource(GatewayBuyTicket, "/gateway/api/tickets/buy")
api.add_resource(GatewayReturnTicket, "/gateway/api/tickets/return" + "/<ticket_id>")
api.add_resource(GatewayTicketResource, "/gateway/api/tickets" + "/<ticket_id>")
api.add_resource(GatewayTicketListResource, "/gateway/api/tickets")
api.add_resource(GatewaySeanceResource, "/gateway/api/seances" + "/<seance_id>")
api.add_resource(GatewaySeanceListResource, "/gateway/api/seances")
api.add_resource(GatewaySeanceCreateResource, "/gateway/api/seances/create")
api.add_resource(GatewayMovieResource, "/gateway/api/movies" + "/<movie_id>")
api.add_resource(GatewayMovieListResource, "/gateway/api/movies")
api.add_resource(GatewayMovieCreateResource, "/gateway/api/movies/create")
api.add_resource(GatewayUserResource, "/gateway/api/users" + "/<user_id>")
api.add_resource(GatewayUserListResource, "/gateway/api/users")
api.add_resource(GatewayAuthorization, "/gateway/api/users/auth/token")
api.add_resource(GatewayApiAuthorization, "/gateway/api/users/auth")


if __name__ == '__main__':
    app.run(debug=True)