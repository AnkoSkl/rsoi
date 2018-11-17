import json

class User:
    def __init__(self, user_id, ticket_ids, name, password):
        self.id = user_id
        self.ticket_ids = ticket_ids
        self.name = name
        self.password = password

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        else:
            return self.id == other.id and self.ticket_ids == other.ticket_ids and self.name == other.name and \
                   self.password == other.password

    def to_json(self):
        dictr = {'user_id': str(self.id), 'ticket_ids': self.ticket_ids, 'name': self.name, 'password': self.password}