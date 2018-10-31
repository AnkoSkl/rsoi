import unittest
from gateway.config import current_config
import requests
import jsonpickle


class TestSeanceCreateResource(unittest.TestCase):
    def test_post(self):
        payload = {'movie_id': '5bd89b59af13c757e1b7f3fd', 'datetime': '10.10.2010', 'number_of_seats': 30}
        res = requests.post(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        seance = jsonpickle.decode(res.content)
        requests.delete(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH + "/%s" % str(seance.id))


class TestSeanceResource(unittest.TestCase):
    def test_get_right(self):
        res = requests.get(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH +
                           "/5bd897f8af13c78fe908cb98")
        self.assertEqual(res.status_code, 200)

    def test_get_false(self):
        res = requests.get(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH +
                           "/5bd897f8af")
        self.assertEqual(res.status_code, 404)

    def test_delete_right(self):
        payload = {'movie_id': '5bd89b59af13c757e1b7f3fd', 'datetime': '10.10.2010', 'number_of_seats': 30}
        res = requests.post(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        seance = jsonpickle.decode(res.content)
        res = requests.delete(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH +
                              "/%s" % str(seance.id))
        self.assertEqual(res.status_code, 204)

    def test_patch_buy_right(self):
        seance_id = '5bd897f8af13c78fe908cb98'
        payload = {'seat_number': 10, 'status': 'buy'}
        res = requests.patch(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH +
                             "/5bd897f8af13c78fe908cb98", data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        payload['status'] = 'return'
        requests.patch(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH +
                       "/5bd897f8af13c78fe908cb98", data=jsonpickle.encode(payload))

    def test_patch_buy_error(self):
        seance_id = '5bd897f8af13c78fe908cb98'
        payload = {'seat_number': 1, 'status': 'buy'}
        res = requests.patch(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH +
                             "/5bd897f8af13c78fe908cb98", data=jsonpickle.encode(payload))
        self.assertNotEqual(res.status_code, 201)

    def test_patch_return_right(self):
        seance_id = '5bd897f8af13c78fe908cb98'
        payload = {'seat_number': 1, 'status': 'return'}
        res = requests.patch(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH +
                             "/5bd897f8af13c78fe908cb98", data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        payload['status'] = 'buy'
        requests.patch(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH +
                       "/5bd897f8af13c78fe908cb98", data=jsonpickle.encode(payload))

    def test_patch_return_error(self):
        seance_id = '5bd897f8af13c78fe908cb98'
        payload = {'seat_number': 10, 'status': 'return'}
        res = requests.patch(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH +
                             "/5bd897f8af13c78fe908cb98", data=jsonpickle.encode(payload))
        self.assertNotEqual(res.status_code, 201)


class TestSeanceListResource(unittest.TestCase):
    def test_get(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.SEANCE_SERVICE_URL + current_config.SEANCE_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
