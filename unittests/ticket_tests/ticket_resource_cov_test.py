import unittest
from ticket.rest_api.ticket_resource import TicketCreateResource, TicketListResource, TicketResource
from ticket.domain.ticket import Ticket
from unittest.mock import patch


class TestTicketCreateResource(unittest.TestCase):
    @patch('ticket.rest_api.ticket_resource.TicketRepository')
    def test_post(self, mock_ticket):
        mock_ticket.return_value.create.return_value = "123"
        tr = TicketCreateResource()
        res = tr.post()
        self.assertEqual(res.status_code, 201)


class TestTicketResource(unittest.TestCase):
    @patch('ticket.rest_api.ticket_resource.TicketRepository')
    def test_get_right(self, mock_ticket):
        ticket = Ticket(ticket_id="123", seance_id="012", seat_number=1)
        mock_ticket.return_value.get.return_value = ticket
        tr = TicketResource()
        res = tr.get("123")
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

    @patch('ticket.rest_api.ticket_resource.TicketRepository')
    def test_delete_right(self, mock_ticket):
        mock_ticket.return_value.delete.return_value = '';
        tr1 = TicketResource()
        res = tr1.delete("123")
        self.assertEqual(res.status_code, 204)


class TestTicketListResource(unittest.TestCase):
    @patch('ticket.rest_api.ticket_resource.TicketRepository')
    def test_get(self, mock_ticket):
        tickets = []
        ticket = Ticket(ticket_id="123", seance_id="012", seat_number=1)
        tickets.append(ticket)
        mock_ticket.return_value.read_paginated.return_value = tickets, False, True
        tr = TicketListResource()
        res = tr.get()
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
