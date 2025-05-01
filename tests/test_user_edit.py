import requests
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
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

        # EDIT
        new_name = 'Changed Name'
        url_edit = f'https://playground.learnqa.ru/api/user/{user_id}'
        response_edit = requests.put(
            url_edit,
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'firstName': new_name}
        )

        Assertions.assert_code_status(response_edit, 200)

        # GET
        url_get = f'https://playground.learnqa.ru/api/user/{user_id}'
        response_get_changed_user = requests.get(
            url_get,
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response_get_changed_user,
            "firstName",
            new_name,
            'Wrong name of the user after edit'
        )

    def test_negative_edit_user_without_login(self):
        new_name = 'Changed Name'
        existed_user_id = 121887
        expired_token = '3a1f368b5b1e90527f1608319d6f136f7bf5596ef7494cf0fa365afac9a5314e'
        expired_cookie = '041d47bae4a48ea4dfd3af00b921e52636ba94cf7bf5596ef7494cf0fa365afac9a5314e'
        url_edit = f'https://playground.learnqa.ru/api/user/{existed_user_id}'

        response_edit = requests.put(
            url_edit,
            data={'firstName': new_name},
            headers={'x-csrf-token': expired_token},
            cookies={'auth_sid': expired_cookie}
        )

        Assertions.assert_code_status(response_edit, 400)
        Assertions.assert_json_value_by_name(response_edit, "error", "Auth token not supplied", "Wasn't get error 'Auth token not supplied'")

    def test_negative_edit_user_with_authorization_from_another_one(self):
        # LOGIN
        url_login = '/user/login'
        data_login = {
            'email': 'test_user@example.com',
            'password': '123'
        }

        response_login = MyRequests.post(url_login, data=data_login)

        auth_sid = self.get_cookie(response_login, 'auth_sid')
        token = self.get_header(response_login, 'x-csrf-token')

        # EDIT
        new_name = 'Changed Name'
        existed_user_id = 121887
        url_edit = f'https://playground.learnqa.ru/api/user/{existed_user_id}'
        response_edit = requests.put(
            url_edit,
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'firstName': new_name}
        )

        Assertions.assert_code_status(response_edit, 400)
        Assertions.assert_json_value_by_name(response_edit, "error", "This user can only edit their own data.", "Wasn't get error 'This user can only edit their own data.'")

    def test_negative_edit_user_with_email_without_at_sign(self):
        # LOGIN
        url_login = '/user/login'
        data_login = {
            'email': 'test_user@example.com',
            'password': '123'
        }

        response_login = MyRequests.post(url_login, data=data_login)

        auth_sid = self.get_cookie(response_login, 'auth_sid')
        token = self.get_header(response_login, 'x-csrf-token')
        user = self.get_json_value(response_login, "user_id")

        # EDIT
        new_email_without_at_sign = 'test_userexample.com'
        url_edit = f'https://playground.learnqa.ru/api/user/{user}'
        response_edit = requests.put(
            url_edit,
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'email': new_email_without_at_sign}
        )

        Assertions.assert_code_status(response_edit, 400)
        Assertions.assert_json_value_by_name(response_edit, "error", "Invalid email format",
                                             "Wasn't get error 'Invalid email format'")

    def test_negative_edit_user_with_short_first_name(self):
        # LOGIN
        url_login = '/user/login'
        data_login = {
            'email': 'test_user@example.com',
            'password': '123'
        }

        response_login = MyRequests.post(url_login, data=data_login)

        auth_sid = self.get_cookie(response_login, 'auth_sid')
        token = self.get_header(response_login, 'x-csrf-token')
        user = self.get_json_value(response_login, "user_id")

        # EDIT
        new_short_first_name = self.generate_random_string(1)
        url_edit = f'https://playground.learnqa.ru/api/user/{user}'
        response_edit = requests.put(
            url_edit,
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'firstName': new_short_first_name}
        )

        Assertions.assert_code_status(response_edit, 400)
        Assertions.assert_json_value_by_name(response_edit, "error", "The value for field `firstName` is too short",
                                             "Wasn't get error 'The value for field `firstName` is too short'")
