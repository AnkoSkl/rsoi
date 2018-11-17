import json


class Seance:
    def __init__(self, seance_id, movie_id, date_time, seats):
        self.id = seance_id
        self.movie_id = movie_id
        self.date_time = date_time
        self.seats = seats

    def __eq__(self, other):
        if not isinstance(other, Seance):
            return False
        else:
            return self.id == other.id and self.movie_id == other.movie_id and self.date_time == other.date_time and \
                   self.seats == other.seats

    def to_json(self):
        dictr = {'seance_id': str(self.id), 'movie_id': str(self.movie_id), 'datetime': self.date_time,
                 'seats': self.seats}
        return json.dumps(dictr)

    @staticmethod
    def from_json(json_object):
        decoded_object = json.loads(json_object)
        return Seance(seance_id=decoded_object["seance_id"], movie_id=decoded_object["movie_id"],
                      date_time=decoded_object["datetime"], seats=decoded_object["seats"])