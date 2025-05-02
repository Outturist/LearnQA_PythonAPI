import requests
class TestHomeworkCookie:
    def test_homework_cookie(self):
        url = 'https://playground.learnqa.ru/api/homework_cookie'

        response = requests.get(url)
        print(response.text)
        cookie_value = dict(response.cookies)['HomeWork']

        assert 'HomeWork' in dict(response.cookies), f"There is no 'HomeWork' in response"
        assert cookie_value == 'hw_value', f"Cookie value is not equal to 'hw_value'. The received value {cookie_value}"


