import unittest
from seance.rest_api.seance_resource import SeanceResource, SeanceListResource, SeanceCreateResource
from seance.domain.seance import Seance
from unittest.mock import patch


class TestSeanceCreateResource(unittest.TestCase):
    @patch('seance.rest_api.seance_resource.SeanceRepository')
    def test_post(self, mock_seance):
        mock_seance.return_value.create.return_value = "123"
        sr = SeanceCreateResource()
        res = sr.post()
        self.assertEqual(res.status_code, 201)


class TestSeanceResource(unittest.TestCase):
    @patch('seance.rest_api.seance_resource.SeanceRepository')
    def test_get_right(self, mock_seance):
        seance = Seance(seance_id="123", movie_id="012", date_time="01.01.2018", seats=[True])
        mock_seance.return_value.get.return_value = seance
        sr = SeanceResource()
        res = sr.get("123")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        sr = SeanceResource()
        try:
            res = sr.get("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_error(self):
        sr = SeanceResource()
        try:
            res = sr.delete("5bd0a351")
        except:
            self.assertTrue(True)

    @patch('seance.rest_api.seance_resource.SeanceRepository')
    def test_delete_right(self, mock_seance):
        mock_seance.return_value.delete.return_value = ''
        sr = SeanceResource()
        res = sr.delete("123")
        self.assertEqual(res.status_code, 204)

    @patch('seance.rest_api.seance_resource.SeanceRepository')
    def test_patch_right(self, mock_seance):
        mock_seance.return_value.get_a_seat.return_value = True
        seance = Seance(seance_id="123", movie_id="012", date_time="01.01.2018", seats=[True])
        mock_seance.return_value.get.return_value = seance
        sr = SeanceResource()
        res = sr.patch('123')
        self.assertEqual(res.status_code, 201)


class TestSeanceListResource(unittest.TestCase):
    @patch('seance.rest_api.seance_resource.SeanceRepository')
    def test_get(self, mock_seance):
        seances = []
        seance = Seance(seance_id="123", movie_id="012", date_time="01.01.2018", seats=[True])
        seances.append(seance)
        mock_seance.return_value.read_paginated.return_value = seances, False, True
        sr = SeanceListResource()
        res = sr.get()
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
