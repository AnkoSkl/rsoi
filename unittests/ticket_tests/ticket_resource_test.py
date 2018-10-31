import unittest
from gateway.config import current_config
import requests
import jsonpickle


class TestTicketResource(unittest.TestCase):
    def test_get_right(self):
        res = requests.get(current_config.TICKET_SERVICE_URL + current_config.TICKET_SERVICE_PATH +
                           "/5bd89fd9af13c7ea848cb9dc")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        res = requests.get(current_config.TICKET_SERVICE_URL + current_config.TICKET_SERVICE_PATH +
                           "/5bd0a351")
        self.assertEqual(res.status_code, 404)

    """
    def test_delete_right(self):
        res = requests.delete(current_config.TICKET_SERVICE_URL + current_config.TICKET_SERVICE_PATH +
                           "/5bd9d92faf13c78bda291896")
        self.assertEqual(res.status_code, 204)
    """


"""
class TestTicketCreateResource(unittest.TestCase):
    def test_post(self):
        payload = {'seance_id': '5bd897f8af13c78fe908cb98', 'seat_number': 2}
        res = requests.post(current_config.TICKET_SERVICE_URL + current_config.TICKET_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
"""


class TestSeanceListResource(unittest.TestCase):
    def test_get(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.TICKET_SERVICE_URL + current_config.TICKET_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
