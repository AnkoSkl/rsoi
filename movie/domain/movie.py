import json


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

    def to_json(self):
        dictr = {'movie_id': str(self.id), 'name': self.name, 'length': self.length, 'description': self.description}
        return json.dumps(dictr)

    @staticmethod
    def from_json(json_object):
        decoded_object = json.loads(json_object)
        return Movie(movie_id=decoded_object["movie_id"], name=decoded_object["name"],
                     description=decoded_object["description"], length=decoded_object["length"])
