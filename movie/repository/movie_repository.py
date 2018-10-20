from flask_mongoalchemy import MongoAlchemy
from movie import app

db = MongoAlchemy(app)


class Movies(db.Document):
    name = db.StringField()
    description = db.StringField()
    length = db.IntField()