import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup_method(self):
        url = 'https://playground.learnqa.ru/ajax/api/user/login'
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response = requests.post(url, data=data)

        self.cookie = self.get_cookie(response, 'auth_sid')
        self.token = self.get_header(response, 'x-csrf-token')
        self.user_id = self.get_json_value(response, "user_id")


    def test_auth_user(self):
        url_check_auth_method = 'https://playground.learnqa.ru/ajax/api/user/auth'
        response_check_auth_method = requests.get(
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

    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookie":
            response_check_auth_method = requests.get(
                'https://playground.learnqa.ru/ajax/api/user/auth',
                headers={'x-csrf-token': self.token}
            )
        else:
            response_check_auth_method = requests.get(
                'https://playground.learnqa.ru/ajax/api/user/auth',
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
