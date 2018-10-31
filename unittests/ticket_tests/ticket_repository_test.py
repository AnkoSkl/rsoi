import unittest
from ticket.repository.ticket_repository import TicketRepository
from ticket.domain.ticket import Ticket
from flask_mongoalchemy import fields


class TestTicketRepository(unittest.TestCase):
    def test_create(self):
        rep = TicketRepository()
        id1 = rep.create('5bd897f8af13c78fe908cb98', 2)
        id2 = rep.create('5bd897f8af13c78fe908cb98', 2)
        self.assertNotEqual(id1, id2)
        rep.delete(id1)
        rep.delete(id2)

    def test_get_right(self):
        rep = TicketRepository()
        ticket1 = rep.get('5bd89fd9af13c7ea848cb9dc')
        ticket2 = Ticket(ticket_id=fields.ObjectId('5bd89fd9af13c7ea848cb9dc'),
                        seance_id='5bd897f8af13c78fe908cb98', seat_number=1)
        self.assertEqual(ticket1, ticket2)

    def test_get_error(self):
        rep = TicketRepository()
        ticket = rep.get('5bd89fd9')
        self.assertIsNone(ticket)

    def test_read_paginated(self):
        rep = TicketRepository()
        tickets = rep.read_paginated(1, 5)
        self.assertLessEqual(len(tickets), 5)

    def test_delete_existed(self):
        rep = TicketRepository()
        id1 = rep.create('5bd897f8af13c78fe908cb98', 2)
        rep.delete(id1)
        self.assertFalse(rep.exists(id1))

    def test_exists_true(self):
        rep = TicketRepository()
        boolean = rep.exists('5bd89fd9af13c7ea848cb9dc')
        self.assertTrue(boolean)

    def test_exists_false(self):
        rep = TicketRepository()
        boolean = rep.exists('5bd8ad1daf')
        self.assertFalse(boolean)


if __name__ == '__main__':
    unittest.main()
