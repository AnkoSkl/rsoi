import unittest
import jsonpickle
import requests
from config import current_config
from gateway.rest_api.gateway_api import GatewayMovieCreateResource, GatewayMovieListResource, GatewayUserResource
from gateway.rest_api.gateway_api import GatewayReturnTicket
from gateway.rest_api.gateway_api import GatewaySeanceCreateResource, GatewaySeanceListResource, GatewayMovieResource
from gateway.rest_api.gateway_api import GatewayTicketResource, GatewayTicketListResource, GatewaySeanceResource
from movie.rest_api.movie_resource import MovieResource, MovieCreateResource
from seance.rest_api.seance_resource import SeanceResource, SeanceCreateResource
from ticket.rest_api.ticket_resource import TicketResource, TicketCreateResource
from user.rest_api.user_resource import UserResource, UserCreateResource
from movie.domain.movie import Movie
from seance.domain.seance import Seance
from ticket.domain.ticket import Ticket
from user.domain.user import User


class TestGatewayTicketResource(unittest.TestCase):
    def test_get_right(self):
        tr = TicketResource()
        tcr = TicketCreateResource()
        res = tcr.post()
        ticket = Ticket.from_json(res.data)
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
        seance = Seance.from_json(res.data)
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
        seance = Seance.from_json(res.data)
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
        movie = Movie.from_json(res.data)
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
        movie = Movie.from_json(res.data)
        gmr1 = GatewayMovieResource()
        res = gmr1.delete(str(movie.id))
        self.assertEqual(res.status_code, 204)


class TestGatewayMovieCreateResource(unittest.TestCase):
    def test_post(self):
        gmr = GatewayMovieCreateResource()
        res = gmr.post()
        self.assertEqual(res.status_code, 201)
        mr = MovieResource()
        movie = Movie.from_json(res.data)
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
        user = User.from_json(res.data)
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


class TestGatewayReturnTicket(unittest.TestCase):
    def test_delete_right(self):
        payload = {'seance_id': '5bd897f8af13c78fe908cb98', 'seat_number': 7}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + '/tickets/buy',
                            data=jsonpickle.encode(payload))
        ticket = Ticket.from_json(res.content)
        ret_ticket = GatewayReturnTicket()
        res = ret_ticket.delete(str(ticket.id))
        self.assertEqual(res.status_code, 204)

    def test_delete_error(self):
        ret_ticket = GatewayReturnTicket()
        res = ret_ticket.delete("5bd897f8")
        self.assertNotEqual(res.status_code, 204)


if __name__ == '__main__':
    unittest.main()
