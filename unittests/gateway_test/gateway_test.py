import unittest
import requests
from ticket.domain.ticket import Ticket
from gateway.config import current_config
import jsonpickle


class TestGatewayTicketResource(unittest.TestCase):
    def test_get_right(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.TICKET_SERVICE_PATH
                           + "/5bd88423af13c7ea848cb9cf")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.TICKET_SERVICE_PATH
                            + "/5bd8842")
        self.assertNotEqual(res.status_code, 200)


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


class TestGatewaySeanceResource(unittest.TestCase):
    def test_get_right(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.SEANCE_SERVICE_PATH
                           + "/5bd0aa41af13c72eb3d3963f")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.TICKET_SERVICE_PATH
                            + "/5bd0aa41af13")
        self.assertNotEqual(res.status_code, 200)

"""
class TestGatewaySeanceCreateResource(unittest.TestCase):
    def test_post_right(self):
        payload = {'movie_id': '5bd0a513af13c7251f913dd9', 'datetime': '22.11.2018_10:15', 'number_of_seats':100}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                            current_config.SEANCE_SERVICE_PATH + current_config.CREATE_PATH,
                            data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)

    def test_post_error(self):
        payload = {'movie_id': '5bd0a513af13c7251f913dd9', 'datetime': '22.11.2018_10:15', 'number_of_seats':'100'}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                            current_config.TICKET_SERVICE_PATH + current_config.CREATE_PATH,
                            data=jsonpickle.encode(payload))
        self.assertNotEqual(res.status_code, 201)
"""

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


class TestGatewayMovieResource(unittest.TestCase):
    def test_get_right(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.MOVIE_SERVICE_PATH
                           + "/5bd0a513af13c7251f913dd9")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.MOVIE_SERVICE_PATH
                           + "/5bd0a513")
        self.assertNotEqual(res.status_code, 200)

"""
    def test_delete_right(self):
        res = requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                              current_config.MOVIE_SERVICE_PATH+ "/5bd89b13af13c757e1b7f3fc")
        self.assertEqual(res.status_code, 204)

    def test_delete_error(self):
        res = requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                              current_config.MOVIE_SERVICE_PATH+ "/0")
        self.assertNotEqual(res.status_code, 204)


class TestGatewayMovieCreateResource(unittest.TestCase):
    def test_post_right(self):
        payload = {'name': 'test', 'description': 'test', 'length': 30}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                            current_config.MOVIE_SERVICE_PATH + current_config.CREATE_PATH,
                            data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)

    def test_post_error(self):
        payload = {'name': 'test', 'description': 'test', 'length': "0"}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                            current_config.MOVIE_SERVICE_PATH + current_config.CREATE_PATH,
                            data=jsonpickle.encode(payload))
        self.assertNotEqual(res.status_code, 201)
"""


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


class TestGatewayUserResource(unittest.TestCase):
    def test_get_right(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.USER_SERVICE_PATH
                           + "/5bd0a351af13c713737dae92")
        self.assertEqual(res.status_code, 200)

    def test_get_with_error(self):
        res = requests.get(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + current_config.USER_SERVICE_PATH
            + "/5bd0")
        self.assertNotEqual(res.status_code, 200)


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

"""
class TestGatewayBuyTicket(unittest.TestCase):
    def test_post_right(self):
        payload = {'seance_id': '5bd897f8af13c78fe908cb98', 'seat_number': 7}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + '/buy_ticket',
                            data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)

    def test_post_error(self):
        payload = {'seance_id': '5bd897f8af13c78fe908cb98', 'seat_number': 2}
        res = requests.post(current_config.GATEWAY_URL + current_config.GATEWAY_PATH + '/buy_ticket',
                            data=jsonpickle.encode(payload))
        self.assertNotEqual(res.status_code, 201)
"""


class TestGatewayReturnTicket(unittest.TestCase):
    def test_post_right(self):
        res = requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                            '/return_ticket/5bd8a022af13c7ea848cb9de')
        self.assertEqual(res.status_code, 204)

    def test_post_error(self):
        res = requests.delete(current_config.GATEWAY_URL + current_config.GATEWAY_PATH +
                            '/return_ticket/5bd8a540af13')
        self.assertNotEqual(res.status_code, 204)


if __name__ == '__main__':
    unittest.main()
