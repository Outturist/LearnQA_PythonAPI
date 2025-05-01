from lib.base_case import BaseCase
from lib.assertions import Assertions
import requests

class TestUserRegister(BaseCase):
    def test_create_user_successfully(self):
        data = self.generate_registration_data()

        url = "https://playground.learnqa.ru/api/user/"

        response = requests.post(url, data=data)


        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        url = url = "https://playground.learnqa.ru/api/user/"
        email = "vinkotov@example.com"

        data = self.generate_registration_data(email)

        response = requests.post(url, data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

