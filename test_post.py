import pytest
import requests
import json

def test_post_pet():
    url2 = "https://petstore.swagger.io/v2/pet"
    request = {}
    request["name"] = "Marta"
    request["category"] = {}
    request["category"]["name"] = "cats"
    request["photoUrls"] = ["photoMarta1"]
    print(request)

    response_post = requests.post(url2, json=request)
    print("result=", response_post.json())
    assert response_post.json()['id'] is not None

    url_get = "https://petstore.swagger.io/v2/pet/"+ str(response_post.json()['id'])
    print("url_get", url_get)
    response_get = requests.get(url_get)
    print("result get =", response_get.json())
    assert response_get.json () ['id'] == response_post.json() ['id']



def test_post_name_negative():
    url = "https://petstore.swagger.io/v2/pet"
    request = {}
    request['name'] = "sberCat"
    request['category'] = {}
    request['category']['name'] = []
    request['photoUrls'] = ["photoSberCat1"]
    print(request)
    response_post = requests.post(url, json=request)
    print("result =", response_post.json())
    assert response_post.json()['message'] == "something bad happened"

def test_post_pet_uploadImage():
    url3 = "https://petstore.swagger.io/v2/pet"
    request = {}
    request["name"] = "Marta"
    request["category"] = {}
    request["category"]["name"] = "cats"
    request["photoUrls"] = ["photoMarta1"]
    print(request)
    response_post = requests.post(url3, json=request)
    print("result=", response_post.json())
    assert response_post.json()['id'] is not None

    url_image = "https://petstore.swagger.io/v2/pet/" + str(response_post.json()['id']) + "/uploadImage"
    print ("urlImage=", url_image)
    fp = open('/Users/20071554/Desktop/test.txt', 'rb')
    files = {'file': fp}
    response_post_image = requests.post(url_image, files=files)
    print(response_post_image)
    assert response_post_image.status_code == 200
    fp.close()

def test_post_pet_negative_uploadImage():
    url_image = "https://petstore.swagger.io/v2/pet/ttttt/uploadImage"
    fp = open('/Users/20071554/Desktop/test.txt', 'rb')
    files = {'file': fp}
    response_post_image = requests.post(url_image, files=files)
    assert response_post_image.status_code == 404
    fp.close()

#изменение данных о питомце запросом POST
def test_post_pet_id():
    url = "https://petstore.swagger.io/v2/pet"
    request = {}
    request["name"] = "Navy"
    request["category"] = {}
    request["category"]["name"] = "cats"
    request["photoUrls"] = ["photoNavy1"]
    print(request)
    response_post = requests.post(url, json=request)
    print("result=", response_post.json())
    assert response_post.json()['id'] is not None

    url_post = "https://petstore.swagger.io/v2/pet/" + str(response_post.json()['id'])
    print("url_post", url_post)
    datamy="name=NavySolo&status=sold"
    response_post_update = requests.post(url_post, data=datamy)
    print ("response_updated =" ,response_post_update.json() )
    assert response_post_update.status_code ==200
    url_get = "https://petstore.swagger.io/v2/pet/" + str(response_post.json()['id'])
    print("url_get", url_get)
    response_get = requests.get(url_get)
    print("result get =", response_get.json())
    assert response_get.json()['name']=="NavySolo"

def test_post_nagative_pet_id():
    url_post = "https://petstore.swagger.io/v2/pet/2222222222222"
    print("url_post", url_post)
    datamy = "name=NavySolo&status=sold"
    response_post_update = requests.post(url_post, data=datamy)
    print("response_updated =", response_post_update.json())
    assert response_post_update.status_code == 404

#***************USER*******************

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


# pytest test_post.py::test_post_pet -v -s
