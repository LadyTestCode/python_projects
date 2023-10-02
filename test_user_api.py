import pytest
import requests
import json
import resources.urls as urls
import Steps.support_steps as support_steps

#************ Тестирование API для управления пользователями **************

#***** Запросы POST *****

#создать пользователя
def test_post_user(username):
    request={}
    request["id"]: 1
    if username == '':
        request["username"] = support_steps.generate_random_letter_strings(6)
    else:
        request["username"] =  username
    request["firstName"] = "Test"
    request["lastName"] = "LastTest"
    request["email"] = "test@test.ru"
    request["password"] = "123qwerty"
    request["phone"] = "1234567"
    request["userStatus"] = 0
    response_post_user = requests.post(urls.url_pet_user, json=request)
    print("response_post_user =", response_post_user.json())
    assert response_post_user.status_code ==200

#***** Запросы GET *****

#получить пользователя по юзеренейму
def test_get_user():
    # подготавливаем пользователя
    username = support_steps.generate_random_letter_strings(6)
    test_post_user(username)
    # подготавливаем данные для запроса get
    url_get_user = urls.url_pet_user + "/" + username
    response_user = requests.get(url_get_user)
    assert response_user.status_code ==200
    assert response_user.json()["username"] == username

def test_get_negative_user():
    username = support_steps.generate_random_letter_strings(6)
    test_post_user(username)
    url_get_user1 =  urls.url_pet_user + "/" + username
    print(url_get_user1)
    response_user1 = requests.get(url_get_user1)
    print(response_user1)
    assert response_user1.status_code == 404


#***** Запросы PUT *****

def test_put_user():
    #создаем пользователя
    username = support_steps.generate_random_letter_strings(6)
    request = {}
    request["id"] = 1
    request["username"] = username
    request["firstName"] = "Test"
    request["lastName"] = "LastTest"
    request["email"] = "test@test.ru"
    request["password"] = "123qwerty"
    request["phone"] = "1234567"
    request["userStatus"] = 0
    response_post_user = requests.post(urls.url_pet_user, json=request)
    print("response_post_user =", response_post_user.json())

    # готовим данные для обновления пользователя
    username1 = support_steps.generate_random_letter_strings(6)
    request_put = {}
    request_put["id"] = 1
    request_put["username"] = username1
    request_put["firstName"] = "Tester"
    request_put["lastName"] = "LastTestNew"
    request_put["email"] = "test1@test.ru"
    request_put["password"] = "1234qwerty"
    request_put["phone"] = "12345674"
    request_put["userStatus"] = 1
    url_put_user = urls.url_pet_user + "/" + username
    response_put_user = requests.put(url_put_user, json=request_put)
    print("response_put_user =", response_put_user.status_code)
    assert response_put_user.status_code==200

    #проверим, что по обновленому имени пользователя можно получить get
    url_get_user = urls.url_pet_user + "/" + username1
    response_get_user = requests.get(url_get_user)
    print("response_get_user =", response_get_user.status_code)
    assert response_get_user.status_code==200

def test_put_negative_user():
    username = support_steps.generate_random_letter_strings(6)
    request_put = {}
    request_put["id"] = 1
    request_put["username"] = support_steps.generate_random_letter_strings(6)
    request_put["firstName"] = "Tester"
    request_put["lastName"] = "LastTestNew"
    request_put["email"] = "test1@test.ru"
    request_put["password"] = "1234qwerty"
    request_put["phone"] = "12345674"
    request_put["userStatus"] = 1
    url_put_user = urls.url_pet_user + "/" + username
    response_put_user = requests.put(url_put_user, json=request_put)
    print("response_put_user =", response_put_user.status_code)
    assert response_put_user.status_code == 404


#***** Запросы DEL *****

def test_del_user():
    username = support_steps.generate_random_letter_strings(6)
    test_post_user(username)
    url_del_user = urls.url_pet_user + "/" + username
    print(url_del_user)
    response_user_del = requests.delete(url_del_user)
    print(response_user_del)
    assert response_user_del.status_code == 200
    # проверим далее, что удаленного пользователя теперь не получить запросом get
    response_user_get = requests.get(url_del_user)
    assert response_user_get.status_code == 404
    # pytest test_del.py::test_del -v -s

def test_del_negative_user():
    username = support_steps.generate_random_letter_strings(6)
    url_del_user = urls.url_pet_user + "/" + username
    response_user_del = requests.delete(url_del_user)
    print(response_user_del)
    assert response_user_del.status_code == 404




#pytest test_user_api.py::test_del_negative_user - v - s
