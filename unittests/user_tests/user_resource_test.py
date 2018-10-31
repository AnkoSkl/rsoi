import unittest
from gateway.config import current_config
import requests
import jsonpickle


class TestUserResource(unittest.TestCase):
    def test_get_right(self):
        res = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                           "/5bd0a351af13c713737dae92")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        res = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                           "/5bd0a351")
        self.assertEqual(res.status_code, 404)

    """
    def test_delete_right(self):
        res = requests.delete(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                           "/5bd9658daf13c767ca5524b9")
        self.assertEqual(res.status_code, 204)
    """

    def test_patch_buy(self):
        payload = {'ticket_id': '5bd8a49aaf13c7ea848cb9e2', 'status': 'buy'}
        res = requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                           "/5bd967f5af13c767ca5524bb", data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        payload['status'] = 'return'
        requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                           "/5bd967f5af13c767ca5524bb", data=jsonpickle.encode(payload))

    def test_patch_return(self):
        payload = {'ticket_id': '5bd8a49aaf13c7ea848cb9e2', 'status': 'buy'}
        requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                           "/5bd967f5af13c767ca5524bb", data=jsonpickle.encode(payload))
        payload['status'] = 'return'
        res = requests.patch(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                           "/5bd967f5af13c767ca5524bb", data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)

"""
class TestUserCreateResource(unittest.TestCase):
    def test_post(self):
        payload = {'name': 'test', 'password': 'test'}
        res = requests.post(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
"""


class TestSeanceListResource(unittest.TestCase):
    def test_get(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
