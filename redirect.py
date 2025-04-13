import requests

response = requests.post("https://playground.learnqa.ru/api/long_redirect")
history = response.history

list_of_urls = list(map(lambda x: x.url, history))

num_of_redirects = len(list_of_urls)

print(f"Общее количество переходов: {num_of_redirects}")
print("Итоговый URL:", list_of_urls[len(list_of_urls) - 1])