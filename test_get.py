import pytest
import requests
import json
import test_post

#получить питомца по ID
def test_get():
    url1 = "https://petstore.swagger.io/v2/pet/9223372036854600851"
    response = requests.get(url1)
    print("result_get=", response.json())
    assert response.json()['id'] == 9223372036854600851
    assert response.json()['name'] == "Marta"
    assert response.status_code == 200

def test_get_pet_id_negative ():
    url = "https://petstore.swagger.io/v2/pet/777777777"
    response_get = requests.get(url)
    print("result =", response_get.json ())
    assert response_get.json () ['message'] == "Pet not found"

#получить питомца по статусу
def test_get_by_status():
    url2 = "https://petstore.swagger.io/v2/pet"
    request = {}
    request["name"] = "Marta"
    request["status"] = "sold"
    request["category"] = {}
    request["category"]["name"] = "cats"
    request["photoUrls"] = ["photoMarta1"]
    print(request)
    response_post = requests.post(url2, json=request)
    print("result=", response_post.json())

    url1 = "https://petstore.swagger.io/v2/pet/findByStatus?status=sold"
    response = requests.get(url1)
    print("result_get=", response.json())
    assert response.status_code==200
    assert responce.json()[0]['status'] == "sold"
    assert str(response.json()).__contains__("Marta")

def test_get_negative_by_status():
    url1 = "https://petstore.swagger.io/v2/pet/findByStatus?status=test"
    response = requests.get(url1)
    print("result_get=", response.json())
    assert response.status_code == 200
    assert str(response.json()).__contains__("[]")

#*******************USER*****************

#получить пользователя по юренейму
def test_get_user():
    # подготавливаем пользователя
    test_post.test_post_user()
    # подготавливаем данные для запроса get
    username = "testuser"
    url_get_user = "https://petstore.swagger.io/v2/user/" + username
    print (url_get_user)
    response_user = requests.get(url_get_user)
    print (response_user)
    assert response_user.status_code ==200
    assert response_user.json()["username"] == username

def test_get_negative_user():
    test_post.test_post_user()
    username = "testuser"
    url_get_user1 = "https://petstore.swagger.io/v2/user/sombodynotknown"
    print(url_get_user1)
    response_user1 = requests.get(url_get_user1)
    print(response_user1)
    assert response_user1.status_code == 404

# pytest test_get.py::test_get -v -s
