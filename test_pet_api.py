import pytest
import requests
import json

#************** Тестирование API для управления питомцами **************

#***** Запросы POST *****

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

#***** Запросы PUT *****

def test_put_pet():
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

def test_negative_put_pet():
    url_get = "https://petstore.swagger.io/v2/pet/5555555555555"
    print("url_get", url_get)
    response_get = requests.get(url_get)
    assert response_get.status_code == 404

#***** Запросы GET *****

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

#***** Запросы DEL *****

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