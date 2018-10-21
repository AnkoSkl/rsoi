from flask_mongoalchemy import MongoAlchemy
from seance import app
from seance.domain.seance import Seance
import jsonpickle


db = MongoAlchemy(app)


class Seances(db.Document):
    movie_id = db.ObjectIdField()
    date_time = db.StringField()
    seats = db.StringField()


class SeanceRepository:
    def create(self, movie_id, date_time, number_of_seats):
        seats = []
        for i in range(number_of_seats):
            seats.append(True)
        seance = Seances(movie_id=movie_id, date_time=date_time, seats=jsonpickle.encode(seats))
        seance.save()
        return seance.mongo_id

    def get(self, seance_id):
        if self.exists(seance_id):
            seance = Seances.query.get(seance_id)
            seats = jsonpickle.decode(seance.seats)
            return Seance(seance_id=seance.mongo_id, movie_id=seance.movie_id, date_time=seance.date_time, seats=seats)
        else:
            return None

    def read_all(self):
        seances = []
        all_seances = Seances.query.all()
        for seance in all_seances:
            seats = jsonpickle.decode(seance.seats)
            seances.append(Seance(seance_id=seance.mongo_id, movie_id=seance.movie_id, date_time=seance.date_time,
                                  seats=seats))
        return seances

    def delete(self, seance_id):
        if self.exists(seance_id):
            seance = Seances.query.get(seance_id)
            seance.remove()

    def get_a_seat(self, seance_id, seat_number):
        if self.exists(seance_id):
            seance = Seances.query.get(seance_id)
            seats = jsonpickle.decode(seance.seats)
            if len(seats)>=seat_number & seat_number>0 & seats[seat_number]:
                seats[seat_number] = False
                seance.seats = jsonpickle.encode(seats)
                seance.save()
                return True
            else:
                return False
        else:
            return None


    def exists(self, seance_id):
        result = Seances.query.get(seance_id)
        return result is not None