class Movie:
    def __init__(self, movie_id, name, description, length):
        self.id = movie_id
        self.name = name
        self.description = description
        self.length = length

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        else:
            return self.id == other.id and self.name == other.name and self.length == other.length and \
                   self.description == other.description