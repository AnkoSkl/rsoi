class User:
    def __init__(self, user_id, ticket_ids, name, password):
        self.id = user_id
        self.ticket_ids = ticket_ids
        self.name = name
        self.password = password
