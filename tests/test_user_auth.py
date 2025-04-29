# import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic('Authorization cases')
class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    exclude_fields = [
        ('no password'),
        ('no username'),
        ('no firstName'),
        ('no lastName'),
        ('no email')
    ]


    def setup_method(self):
        url = '/user/login'
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response = MyRequests.post(url, data=data)

        self.cookie = self.get_cookie(response, 'auth_sid')
        self.token = self.get_header(response, 'x-csrf-token')
        self.user_id = self.get_json_value(response, "user_id")

    @allure.description("This test successfully authorise user by email and password")
    def test_auth_user(self):
        url_check_auth_method = '/user/auth'
        response_check_auth_method = MyRequests.get(
            url_check_auth_method,
            headers={'x-csrf-token': self.token},
            cookies={'auth_sid': self.cookie}
        )

        Assertions.assert_json_value_by_name(
            response_check_auth_method,
            "user_id",
            self.user_id,
            "User id from auth method is not equal to user id from check method"
        )

    @allure.description("This test checks authorisation status without sending auth cookie or token")
    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookie":
            response_check_auth_method = MyRequests.get(
                '/user/auth',
                headers={'x-csrf-token': self.token}
            )
        else:
            response_check_auth_method = MyRequests.get(
                '/user/auth',
                cookies={'auth_sid': self.cookie}
            )

        # Проверяем если нам вернулся id пользователя это значит, что произошла авторизация. Но авторизации без куки
        # или токена происходить не должно и тогда мы выведим в ответе, при каком условии происходит авторизация.
        Assertions.assert_json_value_by_name(
            response_check_auth_method,
            'user_id',
            0,
            f"User is authorised with condition {condition}"
        )

    def test_negative_auth_without_at_sign(self):
        url = '/user/login'
        data_email_without_at_sign = {
            'email': 'vinkotovexample.com',
            'password': '1234'
        }
        response = MyRequests.post(url, data=data_email_without_at_sign)

        Assertions.assert_code_status(response, 400)

        expected_value = 'Invalid username/password supplied'

        assert response.text == expected_value, f"Response doesn't contain expected text 'Invalid username/password supplied'. Actual result is {response.text}"

    def test_create_user_with_existing_email(self):
        url = "/user/"
        email = "vinkotov@example.com"

        data = {
            'password': '123',
            'username': 'lernqa',
            'firstName': 'lernqa',
            'lastName': 'lernqa',
            'email': email

        }

        response = MyRequests.post(url, data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    @pytest.mark.parametrize("condition", exclude_fields)
    def test_negative_create_user(self, condition):
        url = "/user/"
        email = "vinkotov@example.com"

        if condition == 'no password':
            data = {
                'username': 'lernqa',
                'firstName': 'lernqa',
                'lastName': 'lernqa',
                'email': email
            }
            response = MyRequests.post(url, data=data)
            expected_result = 'The following required params are missed: password'
            assert response.text == expected_result, f"Response doesn't contain expected text 'The following required params are missed: password'. Actual result: {response.text}"
            Assertions.assert_code_status(response, 400)

        elif condition == 'no username':
            data = {
                'password': '123',
                'firstName': 'lernqa',
                'lastName': 'lernqa',
                'email': email
            }
            response = MyRequests.post(url, data=data)
            expected_result = 'The following required params are missed: username'
            assert response.text == expected_result, f"Response doesn't contain expected text 'The following required params are missed: username'. Actual result: {response.text}"
            Assertions.assert_code_status(response, 400)

        elif condition == 'no firstName':
            data = {
                'password': '123',
                'username': 'lernqa',
                'lastName': 'lernqa',
                'email': email
            }
            response = MyRequests.post(url, data=data)
            expected_result = 'The following required params are missed: firstName'
            assert response.text == expected_result, f"Response doesn't contain expected text 'The following required params are missed: firstName'. Actual result: {response.text}"
            Assertions.assert_code_status(response, 400)

        elif condition == 'no lastName':
            data = {
                'password': '123',
                'username': 'lernqa',
                'firstName': 'lernqa',
                'email': email
            }
            response = MyRequests.post(url, data=data)
            expected_result = 'The following required params are missed: lastName'
            assert response.text == expected_result, f"Response doesn't contain expected text 'The following required params are missed: lastName'. Actual result: {response.text}"
            Assertions.assert_code_status(response, 400)

        elif condition == 'no email':
            data = {
                'password': '123',
                'username': 'lernqa',
                'firstName': 'lernqa',
                'lastName': 'lernqa'
            }
            response = MyRequests.post(url, data=data)
            expected_result = 'The following required params are missed: email'
            assert response.text == expected_result, f"Response doesn't contain expected text 'The following required params are missed: email'. Actual result: {response.text}"
            Assertions.assert_code_status(response, 400)

    def test_negative_create_user_short_name(self):
        url = "/user/"
        email = "vinkotov@example.com"
        data = {
            'password': '123',
            'username': 'l',
            'firstName': 'lernqa',
            'lastName': 'lernqa',
            'email': email

        }

        response = MyRequests.post(url, data=data)
        expected_result = "The value of 'username' field is too short"
        assert response.text == expected_result, f"Response doesn't contain expected text 'The value of 'username' field is too short'. Actual result: {response.text}"
        Assertions.assert_code_status(response, 400)

    def test_negative_create_user_long_name(self):
        url = "/user/"
        email = "vinkotov@example.com"
        username = self.generate_random_string(251)
        data = {
            'password': '123',
            'username': username,
            'firstName': 'lernqa',
            'lastName': 'lernqa',
            'email': email

        }

        response = MyRequests.post(url, data=data)
        expected_result = "The value of 'username' field is too long"
        assert response.text == expected_result, f"Response doesn't contain expected text 'The value of 'username' field is too long'. Actual result: {response.text}"
        Assertions.assert_code_status(response, 400)