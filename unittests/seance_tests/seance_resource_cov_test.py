import unittest
import jsonpickle
from seance.rest_api.seance_resource import SeanceResource, SeanceListResource, SeanceCreateResource


class TestSeanceCreateResource(unittest.TestCase):
    def test_post(self):
        sr = SeanceCreateResource()
        res = sr.post()
        self.assertEqual(res.status_code, 201)
        sr1 = SeanceResource()
        seance = jsonpickle.decode(res.data)
        sr1.delete(str(seance.id))


class TestSeanceResource(unittest.TestCase):
    def test_get_right(self):
        scr = SeanceCreateResource()
        sr = SeanceResource()
        res = scr.post()
        seance = jsonpickle.decode(res.data)
        res = sr.get(str(seance.id))
        self.assertEqual(res.status_code, 200)
        sr.delete(str(seance.id))

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

    def test_delete_right(self):
        sr = SeanceCreateResource()
        res = sr.post()
        sr1 = SeanceResource()
        seance = jsonpickle.decode(res.data)
        res = sr1.delete(str(seance.id))
        self.assertEqual(res.status_code, 204)


class TestSeanceListResource(unittest.TestCase):
    def test_get(self):
        sr = SeanceListResource()
        res = sr.get()
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
