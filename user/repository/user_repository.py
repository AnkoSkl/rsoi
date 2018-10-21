from flask_mongoalchemy import MongoAlchemy
from user import app
from user.domain.user import User


db = MongoAlchemy(app)


class Users(db.Document):
    name = db.StringField()
    password = db.StringField()

    