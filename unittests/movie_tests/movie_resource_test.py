import unittest
from movie.rest_api.movie_resource import MovieResource, MovieCreateResource, MovieListResource
from gateway.config import current_config
import requests
import jsonpickle


class TestMovieResource(unittest.TestCase):
    def test_get_right(self):
        res = requests.get(current_config.MOVIE_SERVICE_URL + current_config.MOVIE_SERVICE_PATH +
                           "/5bd0a513af13c7251f913dd9")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        res = requests.get(current_config.MOVIE_SERVICE_URL + current_config.MOVIE_SERVICE_PATH +
                           "/5bd0a513af")
        self.assertEqual(res.status_code, 404)

    """
    def test_delete_right(self):
        res = requests.delete(current_config.MOVIE_SERVICE_URL + current_config.MOVIE_SERVICE_PATH +
                           "/5bd8ad1daf13c7befde6ce41")
        self.assertEqual(res.status_code, 204)
    """

    def test_delete_error(self):
        res = requests.delete(current_config.MOVIE_SERVICE_URL + current_config.MOVIE_SERVICE_PATH +
                           "/5bd8ad1daf13c7")
        self.assertEqual(res.status_code, 404)


class TestMovieCreateResource(unittest.TestCase):
    def test_post(self):
        payload = {'name': 'test', 'description': 'test', 'length': 30}
        res = requests.post(current_config.MOVIE_SERVICE_URL + current_config.MOVIE_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)


class TestMovieListResource(unittest.TestCase):
    def test_get(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.MOVIE_SERVICE_URL + current_config.MOVIE_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
