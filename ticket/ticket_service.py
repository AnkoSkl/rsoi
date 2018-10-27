from ticket import app
from flask_restful import Api
from ticket.rest_api.ticket_resource import *
from ticket.repository.ticket_repository import Tickets


api = Api(app)
service_namespace = "/tickets"

api.add_resource(TicketListResource, "/tickets")
api.add_resource(TicketResource, "/tickets/<ticket_id>")
api.add_resource(TicketCreateResource, "/tickets/create")


if __name__ == '__main__':
    app.run(port=5003, debug=True)