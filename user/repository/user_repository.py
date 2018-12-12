from flask_mongoalchemy import MongoAlchemy
from user import app
from user.token import Token
from user.domain.user import User
import jsonpickle
import hashlib


db = MongoAlchemy(app)


class Users(db.Document):
    ticket_ids = db.StringField()
    name = db.StringField()
    password = db.StringField()
    admin = db.StringField()
    token = db.StringField()


class UserRepository:
    def create(self, name, password, admin):
        ticket_ids = []
        token = Token.generate(name).serialize()
        user = Users(ticket_ids=jsonpickle.encode(ticket_ids), name=name, password=self.hash_password(password),
                     admin = admin, token=token)
        user.save()
        return user.mongo_id

    def hash_password(self, password):
        return hashlib.sha256(str(password))

    def get(self, user_id):
        if self.exists(user_id):
            user = Users.query.get(user_id)
            ticket_ids = jsonpickle.decode(user.ticket_ids)
            return User(user_id=user.mongo_id, ticket_ids=ticket_ids, name=user.name, admin=user.admin)
        else:
            return None

    def get_by_token(self, token):
        if not Token.is_expired(token):
            user_id = Token.get_value(token)
            user = self.get(user_id)
            return user
        return None

    def check_password(self, user_id, password):
        if self.exists(user_id):
            user = self.get(user_id)
            return hash(password) == user.password
        return False

    def refresh_token(self, token):
        user_id = Token.get_value(token)
        if self.exists(user_id):
            t = Token.refresh(token)
            user = self.get(user_id)
            user.token = t
            user.save()
            return t
        return None

    def read_paginated(self, page_number, page_size):
        users = []
        users_paged = Users.query.paginate(page=page_number, per_page=page_size)

        for user in users_paged.items:
            ticket_ids = jsonpickle.decode(user.ticket_ids)
            users.append(User(user_id=user.mongo_id, ticket_ids=ticket_ids, name=user.name,
                              admin=user.admin))
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

    def get_token(self, login, password):
        if self.login_exists(login):
            if self.check_password_for_user(login, password):
                user = self.get_user_by_login(login)
                t = Token.generate(login).serialize()
                user.token = t
                user.save()
                return t
        return None

    def check_password_for_user(self, login, password):
        if self.login_exists(login):
            user = self.get_user_by_login(login)
            return self.check_password(user.mongo_id, password)

    def login_exists(self, login):
        result = Users.query.filter(Users.name == login)
        return result is not None

    def get_user_by_login(self, login):
        return Users.query.filter(Users.name == login)

    def exists(self, user_id):
        result = Users.query.get(user_id)
        return result is not None


