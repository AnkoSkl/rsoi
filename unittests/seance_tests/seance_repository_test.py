import unittest
from seance.repository.seance_repository import SeanceRepository
from seance.domain.seance import Seance
from flask_mongoalchemy import fields


class TestSeanceRepository(unittest.TestCase):
    def test_create(self):
        rep = SeanceRepository()
        id1 = rep.create('5bd89b59af13c757e1b7f3fd', '01.01.2018_12:00', 50)
        id2 = rep.create('5bd89b59af13c757e1b7f3fd', '01.01.2018_12:00', 50)
        self.assertNotEqual(id1, id2)
        rep.delete(id1)
        rep.delete(id2)

    def test_get_exists(self):
        rep = SeanceRepository()
        seance_id = rep.create('5bd89b59af13c757e1b7f3fd', '01.01.2018_12:00', 5)
        seance1 = rep.get(seance_id)
        seance2 = Seance(seance_id=fields.ObjectId(seance_id), movie_id=fields.ObjectId('5bd89b59af13c757e1b7f3fd'),
                         date_time='01.01.2018_12:00', seats=[True, True, True, True, True])
        self.assertEqual(seance1, seance2)
        rep.delete(seance_id)

    def test_get_false(self):
        rep = SeanceRepository()
        seance = rep.get('5bd89b59af1')
        self.assertIsNone(seance)

    def test_read_paginated(self):
        rep = SeanceRepository()
        seances = rep.read_paginated(1, 5)
        self.assertLessEqual(len(seances), 5)

    def test_delete(self):
        rep = SeanceRepository()
        seance_id = rep.create('5bd89b59af13c757e1b7f3fd', '01.01.2018_12:00', 50)
        rep.delete(seance_id)
        self.assertFalse(rep.exists(seance_id))

    def test_get_a_seat_true(self):
        rep = SeanceRepository()
        seance_id = rep.create('5bd89b59af13c757e1b7f3fd', '01.01.2018_12:00', 50)
        boolean = rep.get_a_seat(seance_id, 2)
        self.assertTrue(boolean)
        rep.delete(seance_id)

    def test_get_a_seat_false(self):
        rep = SeanceRepository()
        seance_id = rep.create('5bd89b59af13c757e1b7f3fd', '01.01.2018_12:00', 50)
        rep.get_a_seat(seance_id, 2)
        boolean = rep.get_a_seat(seance_id, 2)
        self.assertFalse(boolean)
        rep.delete(seance_id)

    def test_get_a_seat_none(self):
        rep = SeanceRepository()
        boolean = rep.get_a_seat('5bd897f8af', 1)
        self.assertIsNone(boolean)

    def test_free_a_seat_true(self):
        rep = SeanceRepository()
        seance_id = rep.create('5bd89b59af13c757e1b7f3fd', '01.01.2018_12:00', 50)
        rep.get_a_seat(seance_id, 1)
        boolean = rep.free_a_seat(seance_id, 1)
        self.assertTrue(boolean)
        rep.delete(seance_id)

    def test_free_a_seat_false(self):
        rep = SeanceRepository()
        seance_id = rep.create('5bd89b59af13c757e1b7f3fd', '01.01.2018_12:00', 50)
        boolean = rep.free_a_seat(seance_id, 2)
        self.assertFalse(boolean)
        rep.delete(seance_id)

    def test_free_a_seat_none(self):
        rep = SeanceRepository()
        boolean = rep.free_a_seat('5bd897f8af', 2)
        self.assertIsNone(boolean)

    def test_exists(self):
        rep = SeanceRepository()
        seance_id = rep.create('5bd89b59af13c757e1b7f3fd', '01.01.2018_12:00', 50)
        boolean = rep.exists(seance_id)
        self.assertTrue(boolean)
        rep.delete(seance_id)


if __name__ == '__main__':
    unittest.main()
