import pytest
import requests
import json
import test_post

def test_del():
    url2 = "https://petstore.swagger.io/v2/pet"
    request = {}
    request["name"] = "Marta"
    request["category"] = {}
    request["category"]["name"] = "cats"
    request["photoUrls"] = ["photoMarta1"]
    print(request)

    response_post = requests.post(url2, json=request)
    print("result =", response_post.json())
    url_delete = "https://petstore.swagger.io/v2/pet/" + str(response_post.json()['id'])
    response_del = requests.delete(url_delete)
    print("result delete =", response_del.json())
    assert response_del.json()['code'] == 200
    response_get = requests.get(url_delete)
    assert response_get.json()['message'] == 'Pet not found'

def test_del_negative_id():
    url_delete = "https://petstore.swagger.io/v2/pet/77777777777777"
    response_del = requests.delete(url_delete)
    print("result delete =", response_del)
    assert str(response_del).__contains__("404")

# *******************USER*****************
def test_del_user():
    test_post.test_post_user()
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