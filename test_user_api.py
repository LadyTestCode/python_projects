import pytest
import requests
import json

#************ Тестирование API для управления пользователями **************

#***** Запросы POST *****

#создать пользователя
def test_post_user():
    url_post_user = "https://petstore.swagger.io/v2/user"
    request={}
    request["id"]: 1
    request["username"]: "testuser"
    request["firstName"]: "Test"
    request["lastName"]: "LastTest"
    request["email"]: "test@test.ru"
    request["password"]: "123qwerty"
    request["phone"]: "1234567"
    request["userStatus"]: 0
    response_post_user = requests.post(url_post_user, json=request)
    print("response_post_user =", response_post_user.json())
    assert response_post_user.status_code ==200

#***** Запросы GET *****

#получить пользователя по юзеренейму
def test_get_user():
    # подготавливаем пользователя
    test_post_user()
    # подготавливаем данные для запроса get
    username = "testuser"
    url_get_user = "https://petstore.swagger.io/v2/user/" + username
    print (url_get_user)
    response_user = requests.get(url_get_user)
    print (response_user)
    assert response_user.status_code ==200
    assert response_user.json()["username"] == username

def test_get_negative_user():
    test_post_user()
    username = "testuser"
    url_get_user1 = "https://petstore.swagger.io/v2/user/sombodynotknown"
    print(url_get_user1)
    response_user1 = requests.get(url_get_user1)
    print(response_user1)
    assert response_user1.status_code == 404


#***** Запросы PUT *****

def test_put_user():
    #создаем пользователя
    url_post_user = "https://petstore.swagger.io/v2/user"
    request = {}
    request["id"]: 1
    request["username"]: "testuser"
    request["firstName"]: "Test"
    request["lastName"]: "LastTest"
    request["email"]: "test@test.ru"
    request["password"]: "123qwerty"
    request["phone"]: "1234567"
    request["userStatus"]: 0
    response_post_user = requests.post(url_post_user, json=request)
    print("response_post_user =", response_post_user.json())
    # готовим данные для обновления пользователя
    username="testuser"

    request_put = {}
    request_put["id"]: 1
    request_put["username"]: "testuser123"
    request_put["firstName"]: "Tester"
    request_put["lastName"]: "LastTestNew"
    request_put["email"]: "test1@test.ru"
    request_put["password"]: "1234qwerty"
    request_put["phone"]: "12345674"
    request_put["userStatus"]: 1
    url_put_user = "https://petstore.swagger.io/v2/user" + username
    response_put_user = requests.put(url_put_user, json=request_put)
    print("response_put_user =", response_put_user.status_code)
    assert response_put_user.status_code==200

    #проверим, что по обновленому имени пользователя можно получить get
    username1 = "testuser123"
    url_get_user = "https://petstore.swagger.io/v2/user" + username1
    response_get_user = requests.get(url_get_user)
    print("response_get_user =", response_get_user.status_code)
    assert response_get_user.status_code==200

def test_put_negative_user():
    username ="iamnotexist"
    request_put = {}
    request_put["id"]: 1
    request_put["username"]: "testuser123"
    request_put["firstName"]: "Tester"
    request_put["lastName"]: "LastTestNew"
    request_put["email"]: "test1@test.ru"
    request_put["password"]: "1234qwerty"
    request_put["phone"]: "12345674"
    request_put["userStatus"]: 1
    url_put_user = "https://petstore.swagger.io/v2/user" + username
    response_put_user = requests.put(url_put_user, json=request_put)
    print("response_put_user =", response_put_user.status_code)
    assert response_put_user.status_code == 404


#***** Запросы DEL *****

def test_del_user():
    test_post_user()
    username = "testuser"
    url_del_user = "https://petstore.swagger.io/v2/user/" + username
    print(url_del_user)
    response_user_del = requests.delete(url_del_user)
    print(response_user_del)
    assert response_user_del.status_code == 200
    # проверим далее, что удаленного пользователя теперь не получить запросом get
    response_user_get = requests.get(url_del_user)
    assert response_user_get.status_code == 404
    # pytest test_del.py::test_del -v -s

def test_del_negative_user():
    username = "iamnotexist"
    url_del_user = "https://petstore.swagger.io/v2/user/" + username
    response_user_del = requests.delete(url_del_user)
    print(response_user_del)
    assert response_user_del.status_code == 404




#pytest test_user_api.py::test_del_negative_user - v - s
