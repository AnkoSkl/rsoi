import unittest
from gateway.config import current_config
import requests
import jsonpickle
from ticket.rest_api.ticket_resource import TicketCreateResource, TicketListResource, TicketResource


class TestTicketCreateResource(unittest.TestCase):
    def test_post(self):
        payload = {'seance_id': '5bd897f8af13c78fe908cb98', 'seat_number': 2}
        res = requests.post(current_config.TICKET_SERVICE_URL + current_config.TICKET_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        ticket = jsonpickle.decode(res.content)
        requests.delete(current_config.TICKET_SERVICE_URL + current_config.TICKET_SERVICE_PATH +
                        "/%s" % str(ticket.id))


class TestTicketCreateResource2(unittest.TestCase):
    def test_post(self):
        tr = TicketCreateResource()
        res = tr.post()
        self.assertEqual(res.status_code, 201)
        tr1 = TicketResource()
        seance = jsonpickle.decode(res.data)
        tr1.delete(str(seance.id))


class TestTicketResource(unittest.TestCase):
    def test_get_right(self):
        res = requests.get(current_config.TICKET_SERVICE_URL + current_config.TICKET_SERVICE_PATH +
                           "/5bd89fd9af13c7ea848cb9dc")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        res = requests.get(current_config.TICKET_SERVICE_URL + current_config.TICKET_SERVICE_PATH +
                           "/5bd0a351")
        self.assertEqual(res.status_code, 404)

    def test_delete_right(self):
        payload = {'seance_id': '5bd897f8af13c78fe908cb98', 'seat_number': 2}
        res = requests.post(current_config.TICKET_SERVICE_URL + current_config.TICKET_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        ticket = jsonpickle.decode(res.content)
        res = requests.delete(current_config.TICKET_SERVICE_URL + current_config.TICKET_SERVICE_PATH +
                              "/%s" % ticket.id)
        self.assertEqual(res.status_code, 204)


class TestTicketResource2(unittest.TestCase):
    def test_get_right(self):
        tr = TicketResource()
        res = tr.get("5bd89fd9af13c7ea848cb9dc")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        tr = TicketResource()
        try:
            res = tr.get("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_error(self):
        tr = TicketResource()
        try:
            res = tr.delete("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_right(self):
        tr = TicketCreateResource()
        res = tr.post()
        tr1 = TicketResource()
        seance = jsonpickle.decode(res.data)
        res = tr1.delete(str(seance.id))
        self.assertEqual(res.status_code, 204)


class TestTicketListResource(unittest.TestCase):
    def test_get(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.TICKET_SERVICE_URL + current_config.TICKET_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)


class TestTicketListResource2(unittest.TestCase):
    def test_get(self):
        tr = TicketListResource()
        res = tr.get()
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
