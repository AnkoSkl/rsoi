class Seance:
    def __init__(self, seance_id, movie_id, date_time, number_of_seats):
        self.id = seance_id
        self.movie_id = movie_id
        self.date_time = date_time
        self.seats = []
        for i in range(number_of_seats):
            self.seats.append(True)