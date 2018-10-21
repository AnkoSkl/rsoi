from flask_mongoalchemy import MongoAlchemy
from user import app
from user.domain.user import User


db = MongoAlchemy(app)


class Users(db.Document):
    ticket_ids = db.TupleField()
    name = db.StringField()
    password = db.StringField()


class UserRepository:
    def create(self, name, password):
        user = Users(ticket_ids=(), name=name, password=str(password))
        user.save()
        return user.mongo_id

    def get(self, user_id):
        if self.exists(user_id):
            user = Users.query.get(user_id)
            return User(user_id=user.mongo_id, ticket_ids=user.ticket_ids, name=user.name, password=user.password)
        else:
            return None

    def read_all(self):
        users = []
        all_users = Users.query.all()
        for user in all_users:
            users.append(User(user_id=user.mongo_id, ticket_ids=user.ticket_ids, name=user.name,
                              password=user.password))
        return users

    def delete(self, user_id):
        if self.exists(user_id):
            user = Users.query.get(user_id)
            user.remove()

    def assign_ticket(self, user_id, ticket_id):
        if self.exists(user_id):
            user = Users.query.get(user_id)
            ticket_ids = user.ticket_ids + tuple(ticket_id)
            user.ticket_ids = ticket_ids
            user.save()

    def exists(self, user_id):
        result = Users.query.get(user_id)
        return result is not None


