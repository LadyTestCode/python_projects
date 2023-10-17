import requests
import allure
import json

# Отправка запросов и получение ответа для метода POST
# URL - эндпоинт
# request - JSON
def request_post(url, request):
    #with allure.step("Отправка запросов и получение ответа для метода POST"):
    response = requests.post(url, json=request)
    return response

# Отправка запросов и получение ответа для метода POST для обновления данных
# URL - эндпоинт
# request - JSON
def request_post_update(url, dataup):
    #with allure.step("Отправка запросов и получение ответа для метода POST для обновления данных"):
    response = requests.post(url, data=dataup)
    return response

# Отправка запросов и получение ответа для метода PUT
# URL - эндпоинт
# request - JSON
def request_put(url, request):
    #with allure.step("Отправка запросов и получение ответа для метода POST"):
    response = requests.put(url, json=request)
    return response

# Отправка запросов и получение ответа для метода POST для отправки файла
# URL - эндпоинт
# files - files
def request_post_image(url, files):
    #with allure.step("Отправка запросов и получение ответа для метода POST для отправки файлов"):
    response = requests.post(url, files=files)
    return response

# Отправка запроса и получение ответа для метода GET
# url - эндопойнт
def request_get(url):
    #with allure.step("Отправка запросов и получение ответа для метода GET"):
        response = requests.get(url)
        return response

# Отправка запроса и поличение ответа для метода DEL
# URL - эндпоинт
def request_del(url):
    #with allure.step("Отправка запросов и получение ответа для метода DEL"):
        response = requests.delete(url)
        return response