import unittest
from gateway.config import current_config
import requests
import jsonpickle
from user.rest_api.user_resource import UserResource, UserListResource, UserCreateResource


class TestUserCreateResource(unittest.TestCase):
    def test_post(self):
        payload = {'name': 'test', 'password': 'test'}
        res = requests.post(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        self.assertEqual(res.status_code, 201)
        user = jsonpickle.decode(res.content)
        requests.delete(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH + "/%s" % str(user.id))


class TestUserCreateResource2(unittest.TestCase):
    def test_post(self):
        ur = UserCreateResource()
        res = ur.post()
        self.assertEqual(res.status_code, 201)
        ur1 = UserResource()
        movie = jsonpickle.decode(res.data)
        ur1.delete(str(movie.id))


class TestUserResource(unittest.TestCase):
    def test_get_right(self):
        res = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                           "/5bd0a351af13c713737dae92")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        res = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                           "/5bd0a351")
        self.assertEqual(res.status_code, 404)

    def test_delete_right(self):
        payload = {'name': 'test', 'password': 'test'}
        res = requests.post(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                            current_config.CREATE_PATH, data=jsonpickle.encode(payload))
        user = jsonpickle.decode(res.content)
        res = requests.delete(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH +
                              "/%s" % str(user.id))
        self.assertEqual(res.status_code, 204)

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


class TestUserResource2(unittest.TestCase):
    def test_get_right(self):
        ur = UserResource()
        res = ur.get("5bd0a351af13c713737dae92")
        self.assertEqual(res.status_code, 200)

    def test_get_error(self):
        ur = UserResource()
        try:
            res = ur.get("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_error(self):
        ur = UserResource()
        try:
            res = ur.delete("5bd0a351")
        except:
            self.assertTrue(True)

    def test_delete_right(self):
        ur = UserCreateResource()
        res = ur.post()
        ur1 = UserResource()
        movie = jsonpickle.decode(res.data)
        res = ur1.delete(str(movie.id))
        self.assertEqual(res.status_code, 204)


class TestSeanceListResource(unittest.TestCase):
    def test_get(self):
        payload = (('page', 1), ('page_size', 5))
        res = requests.get(current_config.USER_SERVICE_URL + current_config.USER_SERVICE_PATH, params=payload)
        self.assertEqual(res.status_code, 200)


class TestSeanceListResource2(unittest.TestCase):
    def test_get(self):
        ur = UserListResource()
        res = ur.get()
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
