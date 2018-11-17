import json


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

    def to_json(self):
        dictr = {'ticket_id': str(self.id), 'seance_id': self.seance_id, 'seat_number': self.seat_number}
        return json.dumps(dictr)

    @staticmethod
    def from_json(json_object):
        decoded_object = json.loads(json_object)
        return Ticket(ticket_id=decoded_object["ticket_id"], seance_id=decoded_object["seance_id"],
                      seat_number=decoded_object["seat_number"])