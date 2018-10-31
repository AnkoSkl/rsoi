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