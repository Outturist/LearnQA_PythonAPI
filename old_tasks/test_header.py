import requests


class TestHeader:
    def test_header(self):
        url = 'https://playground.learnqa.ru/api/homework_header'

        response = requests.get(url)
        header_value = response.headers['x-secret-homework-header']

        assert 'x-secret-homework-header' in response.headers, f"There is no header 'x-secret-homework-header' in response"
        assert header_value == 'Some secret value', f"Header value is not equal to 'Some secret value'. The received value {header_value}"
