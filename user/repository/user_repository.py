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
                     admin=str(admin), token=str(token))
        user.save()
        return user.mongo_id

    def hash_password(self, password):
        tmp1 = str(password).encode('utf8')
        tmp = hashlib.sha256(tmp1).hexdigest()
        return tmp

    def get(self, user_id):
        if self.exists(user_id):
            user = Users.query.get(user_id)
            ticket_ids = jsonpickle.decode(user.ticket_ids)
            return User(user_id=user.mongo_id, ticket_ids=ticket_ids, name=user.name, admin=user.admin)
        else:
            return None

    def get_real_user_by_token(self, token):
        user = self.get_by_token(token)
        if user is None:
            return user
        ticket_ids = jsonpickle.decode(user.ticket_ids)
        return User(user_id=user.mongo_id, ticket_ids=ticket_ids, name=user.name, admin=user.admin)


    def get_by_token(self, token):
        if not Token.is_expired(token):
            login = Token.get_value(token)
            user = self.get_user_by_login(login)
            return user
        return None

    def check_password(self, hash_password, password):
        p1 = self.hash_password(password)
        p2 = hash_password
        return p1 == p2

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
                user.token = str(t)
                user.save()
                return t
        return None

    def get_code(self, client_id):
        if self.exists(client_id):
            return 'edaf13c7'
        return None

    def get_token_for_auth(self, client_id, client_secret, code):
        if self.exists(client_id):
            if code == 'edaf13c7':
                user = Users.query.get(client_id)
                t = Token.generate(user.name).serialize()
                user.token = str(t)
                user.save()
                return t
        return None

    def check_password_for_user(self, login, password):
        if self.login_exists(login):
            user = self.get_user_by_login(login)
            return self.check_password(user.password, password)

    def login_exists(self, login):
        result = Users.query.filter(Users.name == login)
        return result is not None

    def get_user_by_login(self, login):
        return Users.query.filter(Users.name == login).first()

    def exists(self, user_id):
        result = Users.query.get(user_id)
        return result is not None


