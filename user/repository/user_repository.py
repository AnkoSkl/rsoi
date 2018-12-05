from flask_mongoalchemy import MongoAlchemy
from user import app
from user.domain.user import User
import jsonpickle


db = MongoAlchemy(app)


class Users(db.Document):
    ticket_ids = db.StringField()
    name = db.StringField()
    password = db.StringField()


class UserRepository:
    def create(self, name, password):
        ticket_ids = []
        user = Users(ticket_ids=jsonpickle.encode(ticket_ids), name=name, password=str(password))
        user.save()
        return user.mongo_id

    def get(self, user_id):
        if self.exists(user_id):
            user = Users.query.get(user_id)
            ticket_ids = jsonpickle.decode(user.ticket_ids)
            return User(user_id=user.mongo_id, ticket_ids=ticket_ids, name=user.name, password=user.password)
        else:
            return None

    def read_paginated(self, page_number, page_size):
        users = []
        users_paged = Users.query.paginate(page=page_number, per_page=page_size)

        for user in users_paged.items:
            ticket_ids = jsonpickle.decode(user.ticket_ids)
            users.append(User(user_id=user.mongo_id, ticket_ids=ticket_ids, name=user.name,
                              password=user.password))
        is_prev_num = (users_paged.prev_num > 0)
        is_next_num = (users_paged.next_num <= users_paged.pages)
        return users, is_prev_num, is_next_num

    def delete(self, user_id):
        if self.exists(user_id):
            user = Users.query.get(user_id)
            user.remove()

    def assign_ticket(self, user_id, ticket_id):
        if self.exists(user_id):
            user = Users.query.get(user_id)
            ticket_ids = jsonpickle.decode(user.ticket_ids)
            ticket_ids.append(ticket_id)
            user.ticket_ids = jsonpickle.encode(ticket_ids)
            user.save()
            return True
        return False

    def remove_ticket(self, user_id, ticket_id):
        if self.exists(user_id):
            user = Users.query.get(user_id)
            ticket_ids = jsonpickle.decode(user.ticket_ids)
            ticket_ids.remove(ticket_id)
            user.ticket_ids = jsonpickle.encode(ticket_ids)
            user.save()
            return True
        return False

    def exists(self, user_id):
        result = Users.query.get(user_id)
        return result is not None


