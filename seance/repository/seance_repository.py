from flask_mongoalchemy import MongoAlchemy
from seance import app
from seance.domain.seance import Seance
import jsonpickle


db = MongoAlchemy(app)


class Seances(db.Document):
    movie_id = db.ObjectId()
    date_time = db.StringField()
    seats = db.StringField()