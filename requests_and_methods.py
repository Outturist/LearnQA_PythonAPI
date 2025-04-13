import requests

response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)

response_2 = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "HEAD"})
print(response_2.text)
print(response_2.status_code)

response_3 = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method": "DELETE"})
print(response_3.text)


methods = ['get', 'post', 'put', 'delete']

for method in methods:
    if method == 'get':
        response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type",
                                     params={"method": "GET"})
        print(response.text)
    else:
        values = ["POST", "PUT", "DELETE"]
        for value in values:
            response = requests.request(method, "https://playground.learnqa.ru/ajax/api/compare_query_type",
                                    data={"method": f"{value}"})
            print(f"Метод: {method}, Параметр: {value} Ответ: {response.text}")



