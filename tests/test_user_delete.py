import requests
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from lib.assertions import Assertions

class TestUserDelete(BaseCase):
    def test_negative_delete_default_user(self):
        url_login = '/user/login'
        data_login = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_login = MyRequests.post(url_login, data=data_login)

        auth_sid = self.get_cookie(response_login, 'auth_sid')
        token = self.get_header(response_login, 'x-csrf-token')
        user_id = self.get_json_value(response_login, "user_id")

        # DELETE
        url_delete = f'https://playground.learnqa.ru/api/user/{user_id}'

        response_delete = requests.delete(
            url_delete,
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
        )

        Assertions.assert_code_status(response_delete, 400)
        Assertions.assert_json_has_key(response_delete, "error")
        Assertions.assert_json_value_by_name(response_delete, "error",
                                             "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
                                             "Wasn't get error 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.'")


    def test_delete_just_created_user(self):
        # CREATE_USER (register)
        url_create = "/user/"
        data = self.generate_registration_data()

        response = MyRequests.post(url_create, data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        email = data["email"]
        first_name = data["firstName"]
        password = data["password"]
        user_id = self.get_json_value(response, "id")

        # LOGIN
        url_login = '/user/login'
        data_login = {
            'email': email,
            'password': password
        }

        response_login = MyRequests.post(url_login, data=data_login)

        auth_sid = self.get_cookie(response_login, 'auth_sid')
        token = self.get_header(response_login, 'x-csrf-token')

        # DELETE
        url_delete = f'https://playground.learnqa.ru/api/user/{user_id}'

        response_delete = requests.delete(
            url_delete,
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
        )

        Assertions.assert_code_status(response_delete, 200)
        Assertions.assert_json_has_key(response_delete, "success")
        Assertions.assert_json_value_by_name(response_delete, "success", "!", "Wasn't get success message '!'")

        # GET
        url_get = f'https://playground.learnqa.ru/api/user/{user_id}'
        response_get_deleted_user = requests.get(
            url_get,
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        Assertions.assert_code_status(response_get_deleted_user, 404)
        Assertions.assert_text(response_get_deleted_user, 'User not found', "Wasn't get error 'User not found'")
