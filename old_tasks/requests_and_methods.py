import requests

response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type")
print('кейс_1 текст:', response.text)

response_2 = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "HEAD"})
print('кейс_2 текст:', response_2.text)
print('кейс_2 код:', response_2.status_code)

response_3 = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "DELETE"})
print('кейс_3 текст:', response_3.text)


methods = ['get', 'post', 'put', 'delete']

for method in methods:
    if method == 'get':
        values = ["GET", "POST", "PUT", "DELETE"]
        for value in values:
            response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type",
                                         params={"method": f"{value}"})
            print(f"Метод: {method}, Параметр: {value} Ответ: {response.text}")
    else:
        values = ["GET", "POST", "PUT", "DELETE"]
        for value in values:
            response = requests.request(method, "https://playground.learnqa.ru/ajax/api/compare_query_type",
                                    data={"method": f"{value}"})
            print(f"Метод: {method}, Параметр: {value} Ответ: {response.text}")



