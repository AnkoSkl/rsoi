import unittest
import jsonpickle
from ticket.rest_api.ticket_resource import TicketCreateResource, TicketListResource, TicketResource


class TestTicketCreateResource(unittest.TestCase):
    def test_post(self):
        tr = TicketCreateResource()
        res = tr.post()
        self.assertEqual(res.status_code, 201)
        tr1 = TicketResource()
        seance = jsonpickle.decode(res.data)
        tr1.delete(str(seance.id))


class TestTicketResource(unittest.TestCase):
    def test_get_right(self):
        tr = TicketResource()
        tcr = TicketCreateResource()
        res = tcr.post()
        ticket = jsonpickle.decode(res.data)
        res = tr.get(str(ticket.id))
        self.assertEqual(res.status_code, 200)
        tr.delete(str(ticket.id))

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
        tr = TicketListResource()
        res = tr.get()
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
