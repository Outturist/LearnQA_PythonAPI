import requests
from time import sleep

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

# 1 Создание задачи
response = requests.get(url)
resp_json = response.json()

# 2 Запрос с token до того, как задача готова
empty_token = {"token": ''}
response_with_empty_token = requests.get(url, params=empty_token)
response_with_empty_token_json = response_with_empty_token.json()

assert response_with_empty_token_json["error"] == "No job linked to this token", "Response doesn't contains 'No job linked to this token'"


# 3 Старт таймера
sleep(resp_json["seconds"])

# 4 Запрос после готовности задачи
params = {"token": resp_json["token"]}
response_job_is_ready = requests.get(url, params=params)

response_job_is_ready_json = response_job_is_ready.json()

assert response_job_is_ready_json["result"] == "42", f"Expected result: '42', actual result:{response_job_is_ready_json['result']}"
assert 'result' in response_job_is_ready_json, f"Expected result: 'Job is ready' actual result:{response_job_is_ready_json['status']}"

