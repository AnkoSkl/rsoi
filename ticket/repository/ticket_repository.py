from flask_mongoalchemy import MongoAlchemy
from ticket import app
from ticket.domain.ticket import Ticket


db = MongoAlchemy(app)


class Tickets(db.Document):
    seance_id = db.StringField()
    seat_number = db.IntField()