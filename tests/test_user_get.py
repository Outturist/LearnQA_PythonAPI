import requests

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response = requests.get("https://playground.learnqa.ru/api/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, 'email')
        Assertions.assert_json_has_not_key(response, 'firstName')
        Assertions.assert_json_has_not_key(response, 'lastName')

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': "vinkotov@example.com",
            'password': '1234',
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)


        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}",
                                 headers={'x-csrf-token': token},
                                 cookies={'auth_sid': auth_sid})

        # Вместо assert_json_has_key для проверки каждого ключа можно использовать метод assert_json_has_keys
        # Assertions.assert_json_has_key(response2, 'username')
        # Assertions.assert_json_has_key(response2, 'email')
        # Assertions.assert_json_has_key(response2, 'firstName')
        # Assertions.assert_json_has_key(response2, 'lastName')

        expected_fields = ['username', 'email', 'firstName', 'lastName']
        Assertions.assert_json_has_keys(response2, expected_fields)

    def test_get_user_details_auth_as_different_user(self):
        data = {
            'email': "vinkotov@example.com",
            'password': '1234',
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')

        user_id_not_authorised_user = 121855

        response2 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_not_authorised_user}",
                                 headers={'x-csrf-token': token},
                                 cookies={'auth_sid': auth_sid})

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_key(response2, 'email')
        Assertions.assert_json_has_not_key(response2, 'firstName')
        Assertions.assert_json_has_not_key(response2, 'lastName')
        Assertions.assert_json_value_by_name(response2, "username", "test_user", f"Expected value: 'test_user'. Actual value: '{response2.json()['username']}'")



