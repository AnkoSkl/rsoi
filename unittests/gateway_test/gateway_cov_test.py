import unittest
import jsonpickle
from gateway.rest_api.gateway_api import GatewayTicketResource, GatewayTicketListResource, GatewaySeanceResource
from gateway.rest_api.gateway_api import GatewaySeanceCreateResource, GatewaySeanceListResource, GatewayMovieResource
from gateway.rest_api.gateway_api import GatewayMovieCreateResource, GatewayMovieListResource, GatewayUserResource
from seance.rest_api.seance_resource import SeanceResource
from movie.rest_api.movie_resource import MovieResource


class TestGatewayTicketResource(unittest.TestCase):
    def test_get_right(self):
        gtr = GatewayTicketResource()
        res = gtr.get("5bd88423af13c7ea848cb9cf")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        gtr = GatewayTicketResource()
        res = gtr.get("5bd88423")
        self.assertEqual(res.status_code, 404)


class TestGatewayTicketListResource(unittest.TestCase):
    def test_get(self):
        sr = GatewayTicketListResource()
        res = sr.get()
        self.assertEqual(res.status_code, 200)


class TestGatewaySeanceResource(unittest.TestCase):
    def test_get_right(self):
        gtr = GatewaySeanceResource()
        res = gtr.get("5bd0aa41af13c72eb3d3963f")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        gtr = GatewaySeanceResource()
        res = gtr.get("5bd88423")
        self.assertEqual(res.status_code, 404)


class TestGatewaySeanceCreateResource(unittest.TestCase):
    def test_post(self):
        gsr = GatewaySeanceCreateResource()
        res = gsr.post()
        self.assertEqual(res.status_code, 201)
        sr = SeanceResource()
        seance = jsonpickle.decode(res.data)
        sr.delete(str(seance.id))


class TestGatewaySeanceListResource(unittest.TestCase):
    def test_get(self):
        gsr = GatewaySeanceListResource()
        res = gsr.get()
        self.assertEqual(res.status_code, 200)


class TestGatewayMovieResource(unittest.TestCase):
    def test_get_right(self):
        gmr = GatewayMovieResource()
        res = gmr.get("5bd89b59af13c757e1b7f3fd")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        gmr = GatewayMovieResource()
        try:
            res = gmr.get("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_error(self):
        gmr = GatewayMovieResource()
        try:
            res = gmr.delete("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_right(self):
        gmr = GatewayMovieCreateResource()
        res = gmr.post()
        movie = jsonpickle.decode(res.data)
        gmr1 = GatewayMovieResource()
        res = gmr1.delete(str(movie.id))
        self.assertEqual(res.status_code, 204)


class TestGatewayMovieCreateResource(unittest.TestCase):
    def test_post(self):
        gmr = GatewayMovieCreateResource()
        res = gmr.post()
        self.assertEqual(res.status_code, 201)
        mr = MovieResource()
        movie = jsonpickle.decode(res.data)
        mr.delete(str(movie.id))


class TestGatewayMovieListResource(unittest.TestCase):
    def test_get(self):
        gsr = GatewayMovieListResource()
        res = gsr.get()
        self.assertEqual(res.status_code, 200)


class TestGatewayUserResource(unittest.TestCase):
    def test_get_right(self):
        gur = GatewayUserResource()
        res = gur.get("5bd0a351af13c713737dae92")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        gur = GatewayUserResource()
        try:
            res = gur.get("5bd0a351")
        except:
            self.assertTrue(True)


class TestGatewayUserListResource(unittest.TestCase):
    def test_get(self):
        gsr = GatewayMovieListResource()
        res = gsr.get()
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
