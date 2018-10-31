class Ticket:
    def __init__(self, ticket_id, seance_id, seat_number):
        self.id = ticket_id
        self.seance_id = seance_id
        self.seat_number = seat_number

    def __eq__(self, other):
        if not isinstance(other, Ticket):
            return False
        else:
            return self.id == other.id and self.seance_id == other.seance_id and self.seat_number == other.seat_number
