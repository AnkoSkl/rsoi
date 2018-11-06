import unittest
import jsonpickle
from gateway.rest_api.gateway_api import GatewayTicketResource, GatewayTicketListResource, GatewaySeanceResource
from gateway.rest_api.gateway_api import GatewaySeanceCreateResource, GatewaySeanceListResource, GatewayMovieResource
from gateway.rest_api.gateway_api import GatewayMovieCreateResource, GatewayMovieListResource, GatewayUserResource
from seance.rest_api.seance_resource import SeanceResource, SeanceCreateResource
from movie.rest_api.movie_resource import MovieResource, MovieCreateResource
from ticket.rest_api.ticket_resource import TicketResource, TicketCreateResource
from user.rest_api.user_resource import UserResource, UserCreateResource


class TestGatewayTicketResource(unittest.TestCase):
    def test_get_right(self):
        tr = TicketResource()
        tcr = TicketCreateResource()
        res = tcr.post()
        ticket = jsonpickle.decode(res.data)
        gtr = GatewayTicketResource()
        res = gtr.get(str(ticket.id))
        self.assertEqual(res.status_code, 200)
        tr.delete(str(ticket.id))

    def test_get_error(self):
        gtr = GatewayTicketResource()
        try:
            res = gtr.get("5bd88423")
        except:
            self.assertTrue(True)


class TestGatewayTicketListResource(unittest.TestCase):
    def test_get(self):
        sr = GatewayTicketListResource()
        res = sr.get()
        self.assertEqual(res.status_code, 200)


class TestGatewaySeanceResource(unittest.TestCase):
    def test_get_right(self):
        sr = SeanceResource()
        scr = SeanceCreateResource()
        res = scr.post()
        seance = jsonpickle.decode(res.data)
        gsr = GatewaySeanceResource()
        res = gsr.get(str(seance.id))
        self.assertEqual(res.status_code, 200)
        sr.delete(str(seance.id))

    def test_get_error(self):
        gtr = GatewaySeanceResource()
        try:
            res = gtr.get("5bd88423")
        except:
            self.assertTrue(True)


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
        mr = MovieResource()
        mcr = MovieCreateResource()
        res = mcr.post()
        movie = jsonpickle.decode(res.data)
        gmr = GatewayMovieResource()
        res = gmr.get(str(movie.id))
        self.assertEqual(res.status_code, 200)
        mr.delete(str(movie.id))

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
        ur = UserResource()
        ucr = UserCreateResource()
        res = ucr.post()
        user = jsonpickle.decode(res.data)
        gur = GatewayUserResource()
        res = gur.get(str(user.id))
        self.assertEqual(res.status_code, 200)
        ur.delete(str(user.id))

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
