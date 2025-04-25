import requests

payload = {"login": "secret_login", "password": "secret_pass"}
response_get_cookie = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload)

cookie_value = response_get_cookie.cookies.get('auth_cookie')

cookies = {}
if cookie_value is not None:
    cookies.update({'auth_cookie': cookie_value})

response_check_cookie = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)

print(response_check_cookie.text)




