import string
import random
from requests import Response
import json.decoder


class BaseCase:
    # метод для получения значений cookie из ответов сервера по имени.
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Can not find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    # метод для получения значений header из ответов сервера по имени.
    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Can not find header with name {headers_name} in the last response"
        return response.headers[headers_name]

    # метод парсинга ответа от сервера. Если ответ сервера в формате JSON проверяем наличие ключа (name) в response.
    # иначе возвращается ошибка с str
    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key {name}"

        return response_as_dict[name]

    def generate_random_string(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

