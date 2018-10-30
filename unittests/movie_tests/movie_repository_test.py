import unittest
from movie.repository.movie_repository import MovieRepository
from movie.domain.movie import Movie
from flask_mongoalchemy import fields

class TestMovieRepository(unittest.TestCase):
    """
    def test_create(self):
        rep = MovieRepository()
        id1 = rep.create('a', 'a', 10)
        id2 = rep.create('a', 'a', 10)
        self.assertNotEqual(id1, id2)
    """

    def test_get_right(self):
        rep = MovieRepository()
        movie1 = rep.get('5bd8ad1daf13c7befde6ce42')
        movie2 = Movie(movie_id=fields.ObjectId('5bd8ad1daf13c7befde6ce42'), name='a', description='a', length=10)
        self.assertEqual(movie1, movie2)

    def test_exists_true(self):
        rep = MovieRepository()
        boolean = rep.exists('5bd8ad1daf13c7befde6ce42')
        self.assertTrue(boolean)

    def test_exists_false(self):
        rep = MovieRepository()
        boolean = rep.exists('5bd8ad1daf')
        self.assertFalse(boolean)

    def test_read_paginated(self):
        rep = MovieRepository()
        movies = rep.read_paginated(1, 5)
        self.assertLessEqual(len(movies), 5)

    def test_delete_existed(self):
        rep = MovieRepository()
        id1 = rep.create('a', 'a', 10)
        rep.delete(id1)
        self.assertFalse(rep.exists(id1))


if __name__ == '__main__':
    unittest.main()
