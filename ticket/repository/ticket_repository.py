from flask_mongoalchemy import MongoAlchemy
from ticket import app
from ticket.domain.ticket import Ticket


db = MongoAlchemy(app)


class Tickets(db.Document):
    seance_id = db.StringField()
    seat_number = db.IntField()


class TicketRepository:
    def create(self, seance_id, seat_number):
        ticket = Tickets(seance_id=seance_id, seat_number=seat_number)
        ticket.save()
        return ticket.mongo_id

    def get(self, ticket_id):
        if self.exists(ticket_id):
            ticket = Tickets.query.get(ticket_id)
            return Ticket(ticket_id=ticket.mongo_id, seance_id=ticket.seance_id, seat_number=ticket.seat_number)
        else:
            return None

    def read_paginated(self, page_number, page_size):
        tickets = []
        tickets_paged = Tickets.query.paginate(page=page_number, per_page=page_size)
        for ticket in tickets_paged.items:
            tickets.append(Ticket(ticket_id=ticket.mongo_id, seance_id=ticket.seance_id,
                                  seat_number=ticket.seat_number))
        is_prev_num = (tickets_paged.prev_num > 0)
        is_next_num = (tickets_paged.next_num <= tickets_paged.pages)
        return tickets, is_prev_num, is_next_num

    def delete(self, ticket_id):
        if self.exists(ticket_id):
            ticket = Tickets.query.get(ticket_id)
            ticket.remove()

    def exists(self, ticket_id):
        result = Tickets.query.get(ticket_id)
        return result is not None