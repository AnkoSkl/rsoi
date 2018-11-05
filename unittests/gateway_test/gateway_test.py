import unittest
import requests
from gateway.config import current_config
import jsonpickle
from gateway.rest_api.gateway_api import GatewayTicketResource, GatewayTicketListResource, GatewaySeanceResource
from gateway.rest_api.gateway_api import GatewaySeanceCreateResource, GatewaySeanceListResource, GatewayMovieResource
from gateway.rest_api.gateway_api import GatewayMovieCreateResource, GatewayMovieListResource, GatewayUserResource
from gateway.rest_api.gateway_api import GatewayUserListResource, GatewayBuyTicket, GatewayReturnTicket
from seance.rest_api.seance_resource import SeanceResource
from movie.rest_api.movie_resource import MovieResource


class TestGatewayTicketResource(unittest.TestCase):
    def test_get_right(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.TICKET_SERVICE_PATH
                           + "/5bd88423af13c7ea848cb9cf")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.TICKET_SERVICE_PATH
                           + "/5bd8842")
        self.assertEqual(res.status_code, 404)


class TestGatewayTicketResource2(unittest.TestCase):
    def test_get_right(self):
        gtr = GatewayTicketResource()
        res = gtr.get("5bd88423af13c7ea848cb9cf")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        gtr = GatewayTicketResource()
        res = gtr.get("5bd88423")
        self.assertEqual(res.status_code, 404)


class TestGatewayTicketListResource(unittest.TestCase):
    def test_get_right(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.TICKET_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        payload = (('page', 0), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.TICKET_SERVICE_PATH, params=payload)
        self.assertNotEqual(res.status_code, 200)


class TestGatewayTicketListResource2(unittest.TestCase):
    def test_get(self):
        sr = GatewayTicketListResource()
        res = sr.get()
        self.assertEqual(res.status_code, 200)


class TestGatewaySeanceResource(unittest.TestCase):
    def test_get_right(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.SEANCE_SERVICE_PATH
                           + "/5bd0aa41af13c72eb3d3963f")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.TICKET_SERVICE_PATH
                           + "/5bd0aa41af13")
        self.assertNotEqual(res.status_code, 200)


class TestGatewaySeanceResource2(unittest.TestCase):
    def test_get_right(self):
        gtr = GatewaySeanceResource()
        res = gtr.get("5bd0aa41af13c72eb3d3963f")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        gtr = GatewaySeanceResource()
        res = gtr.get("5bd88423")
        self.assertEqual(res.status_code, 404)


class TestGatewaySeanceCreateResource(unittest.TestCase):
    def test_post_right(self):
        payload = {'movie_id': '5bd0a513af13c7251f913dd9', 'datetime': '22.11.2018_10:15', 'number_of_seats':100}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                            current_config.SEANCE_SERVICE_PATH + current_config.CREATE_PATH,
                            data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        seance = jsonpickle.decode(res.content)
        requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.SEANCE_SERVICE_PATH +
                        "/%s" % str(seance.id))

    def test_post_error(self):
        payload = {'movie_id': '5bd0a513af13c7251f913dd9', 'datetime': '22.11.2018_10:15', 'number_of_seats':'100'}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                            current_config.TICKET_SERVICE_PATH + current_config.CREATE_PATH,
                            data=jsonpickle.encode(payload))
        self.assertNotEqual(res.status_code, 201)


class TestGatewaySeanceCreateResource2(unittest.TestCase):
    def test_post(self):
        gsr = GatewaySeanceCreateResource()
        res = gsr.post()
        self.assertEqual(res.status_code, 201)
        sr = SeanceResource()
        seance = jsonpickle.decode(res.data)
        sr.delete(str(seance.id))


class TestGatewaySeanceListResource(unittest.TestCase):
    def test_get_right(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.SEANCE_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        payload = (('page', 0), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.SEANCE_SERVICE_PATH, params=payload)
        self.assertNotEqual(res.status_code, 200)


class TestGatewaySeanceListResource2(unittest.TestCase):
    def test_get(self):
        gsr = GatewaySeanceListResource()
        res = gsr.get()
        self.assertEqual(res.status_code, 200)


class TestGatewayMovieResource(unittest.TestCase):
    def test_get_right(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.MOVIE_SERVICE_PATH
                           + "/5bd0a513af13c7251f913dd9")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.MOVIE_SERVICE_PATH
                           + "/5bd0a513")
        self.assertNotEqual(res.status_code, 200)

    def test_delete_right(self):
        payload = {'name': 'test', 'description': 'test', 'length': 30}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                            current_config.MOVIE_SERVICE_PATH + current_config.CREATE_PATH,
                            data=jsonpickle.encode(payload))
        movie = jsonpickle.decode(res.content)
        res = requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                              current_config.MOVIE_SERVICE_PATH + "/%s" % str(movie.id))
        self.assertEqual(res.status_code, 204)

    def test_delete_error(self):
        res = requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                              current_config.MOVIE_SERVICE_PATH + "/0")
        self.assertNotEqual(res.status_code, 204)


class TestGatewayMovieResource2(unittest.TestCase):
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
    def test_post_right(self):
        payload = {'name': 'test', 'description': 'test', 'length': 30}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                            current_config.MOVIE_SERVICE_PATH + current_config.CREATE_PATH,
                            data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        movie = jsonpickle.decode(res.content)
        requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.MOVIE_SERVICE_PATH +
                        "/%s" % str(movie.id))

    def test_post_error(self):
        payload = {'name': 'test', 'description': 'test', 'length': "0"}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                            current_config.MOVIE_SERVICE_PATH + current_config.CREATE_PATH,
                            data=jsonpickle.encode(payload))
        self.assertNotEqual(res.status_code, 201)


class TestGatewayMovieCreateResource2(unittest.TestCase):
    def test_post(self):
        gmr = GatewayMovieCreateResource()
        res = gmr.post()
        self.assertEqual(res.status_code, 201)
        mr = MovieResource()
        movie = jsonpickle.decode(res.data)
        mr.delete(str(movie.id))


class TestGatewayMovieListResource(unittest.TestCase):
    def test_get_right(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.MOVIE_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        payload = (('page', 0), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.MOVIE_SERVICE_PATH, params=payload)
        self.assertNotEqual(res.status_code, 200)


class TestGatewayMovieListResource2(unittest.TestCase):
    def test_get(self):
        gsr = GatewayMovieListResource()
        res = gsr.get()
        self.assertEqual(res.status_code, 200)


class TestGatewayUserResource(unittest.TestCase):
    def test_get_right(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.USER_SERVICE_PATH
                           + "/5bd0a351af13c713737dae92")
        self.assertEqual(res.status_code, 200)

    def test_get_with_error(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.USER_SERVICE_PATH
                           + "/5bd0")
        self.assertNotEqual(res.status_code, 200)


class TestGatewayUserResource2(unittest.TestCase):
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
    def test_get_right(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.USER_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        payload = (('page', 0), ('page_size', 5))
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                           current_config.USER_SERVICE_PATH, params=payload)
        self.assertNotEqual(res.status_code, 200)


class TestGatewayUserListResource2(unittest.TestCase):
    def test_get(self):
        gsr = GatewayMovieListResource()
        res = gsr.get()
        self.assertEqual(res.status_code, 200)


class TestGatewayBuyTicket(unittest.TestCase):
    def test_post_right(self):
        payload = {'seance_id': '5bd897f8af13c78fe908cb98', 'seat_number': 7}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + '/buy_ticket',
                            data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        ticket = jsonpickle.decode(res.content)
        requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                        '/return_ticket/%s' % str(ticket.id))

    def test_post_error(self):
        payload = {'seance_id': '5bd897f8', 'seat_number': 2}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + '/buy_ticket',
                            data=jsonpickle.encode(payload))
        self.assertNotEqual(res.status_code, 201)


class TestGatewayReturnTicket(unittest.TestCase):
    def test_delete_right(self):
        payload = {'seance_id': '5bd897f8af13c78fe908cb98', 'seat_number': 7}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + '/buy_ticket',
                            data=jsonpickle.encode(payload))
        ticket = jsonpickle.decode(res.content)
        res = requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                              '/return_ticket/%s' % str(ticket.id))
        self.assertEqual(res.status_code, 204)

    def test_delete_error(self):
        res = requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                              '/return_ticket/5bd8a540af13')
        self.assertNotEqual(res.status_code, 204)


class TestGatewayReturnTicket2(unittest.TestCase):
    def test_delete_right(self):
        payload = {'seance_id': '5bd897f8af13c78fe908cb98', 'seat_number': 7}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + '/buy_ticket',
                            data=jsonpickle.encode(payload))
        ticket = jsonpickle.decode(res.content)
        ret_ticket = GatewayReturnTicket()
        res = ret_ticket.delete(str(ticket.id))
        self.assertEqual(res.status_code, 204)

    def test_delete_error(self):
        ret_ticket = GatewayReturnTicket()
        res = ret_ticket.delete("5bd897f8")
        self.assertNotEqual(res.status_code, 204)


if __name__ == '__main__':
    unittest.main()
