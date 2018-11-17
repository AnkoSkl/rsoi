import unittest
from movie.rest_api.movie_resource import MovieResource, MovieCreateResource, MovieListResource
from movie.domain.movie import Movie


class TestMovieCreateResource(unittest.TestCase):
    def test_post(self):
        mr = MovieCreateResource()
        res = mr.post()
        self.assertEqual(res.status_code, 201)
        movie = Movie.from_json(res.data)
        mr1 = MovieResource()
        mr1.delete(str(movie.id))


class TestMovieResource(unittest.TestCase):
    def test_get_right(self):
        mr1 = MovieResource()
        mr2 = MovieCreateResource()
        res = mr2.post()
        movie = Movie.from_json(res.data)
        res = mr1.get(str(movie.id))
        self.assertEqual(res.status_code, 200)
        mr1.delete(str(movie.id))

    def test_get_error(self):
        mr = MovieResource()
        try:
            res = mr.get("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_error(self):
        mr = MovieResource()
        try:
            res = mr.delete("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_right(self):
        mr = MovieCreateResource()
        res = mr.post()
        movie = Movie.from_json(res.data)
        mr1 = MovieResource()
        res = mr1.delete(str(movie.id))
        self.assertEqual(res.status_code, 204)


class TestMovieListResource(unittest.TestCase):
    def test_get(self):
        mr = MovieListResource()
        res = mr.get()
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
