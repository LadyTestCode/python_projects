import pytest
import requests
import json

def test_put():
    url2 = "https://petstore.swagger.io/v2/pet"
    request = {}
    request["name"] = "Marta"
    request["category"] = {}
    request["category"]["name"] = "cats"
    request["photoUrls"] = ["photoMarta1"]
    response_post = requests.post(url2, json=request)
    print("result=", response_post.json())

    request_put = {}
    request_put["id"] = response_post.json()["id"]
    request_put["name"] = "Martin"
    response_put = requests.put(url2, json=request_put)
    print("result_put=", response_put.json())

    url_get = "https://petstore.swagger.io/v2/pet/" + str(response_post.json()['id'])
    print("url_get", url_get)
    response_get = requests.get(url_get)
    assert request_put["name"] == response_get.json()["name"]
    assert response_put.json()["name"] == response_get.json()["name"]

# *******************USER*****************
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

 # pytest test_put.py::test_put -v -s
