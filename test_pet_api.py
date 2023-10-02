import pytest
import requests
import json
import resources.urls as urls
import Steps.support_steps as support_steps

#************** Тестирование API для управления питомцами **************

#***** Запросы POST *****

def test_post_pet():

    request = {}
    request["id"] = 9223372036854600851
    request["name"] = support_steps.generate_random_letter_strings(6)
    request["category"] = {}
    request["category"]["name"] = "cats"
    request["photoUrls"] = ["photoMarta1"]
    print(request)
    response_post = requests.post(urls.url_pet_post, json=request)
    print("result=", response_post.json())
    assert response_post.json()['id'] is not None
    response_get = requests.get(urls.url_pet_get_id(str(response_post.json()['id'])))
    print("result get =", response_get.json())
    assert response_get.json () ['id'] == response_post.json() ['id']


def test_post_name_negative():
    request = {}
    request['name'] = support_steps.generate_random_letter_strings(6)
    request['category'] = {}
    request['category']['name'] = []
    request['photoUrls'] = ["photoSberCat1"]
    print(request)
    response_post = requests.post(urls.url_pet_post, json=request)
    print("result =", response_post.json())
    assert response_post.json()['message'] == "something bad happened"


def test_post_pet_uploadImage():
    request = {}
    request["name"] = support_steps.generate_random_letter_strings(6)
    request["category"] = {}
    request["category"]["name"] = "cats"
    request["photoUrls"] = ["photoMarta1"]
    print(request)
    response_post = requests.post(urls.url_pet_post, json=request)
    print("result=", response_post.json())
    assert response_post.json()['id'] is not None

    fp = open('/Users/20071554/Desktop/test.txt', 'rb')
    files = {'file': fp}
    response_post_image = requests.post(urls.url_pet_post_uploadimage(str(response_post.json()['id'])), files=files)
    print(response_post_image)
    assert response_post_image.status_code == 200
    fp.close()

def test_post_pet_negative_uploadImage():
    fp = open('/Users/20071554/Desktop/test.txt', 'rb')
    files = {'file': fp}
    response_post_image = requests.post(urls.url_pet_post_uploadimage(support_steps.generate_random_letter_strings(6)), files=files)
    assert response_post_image.status_code == 404
    fp.close()

#изменение данных о питомце запросом POST
def test_post_pet_id():
    request = {}
    request["name"] = support_steps.generate_random_letter_strings(6)
    request["category"] = {}
    request["category"]["name"] = "cats"
    request["photoUrls"] = ["photoNavy1"]
    print(request)
    response_post = requests.post(urls.url_pet_post, json=request)
    print("result=", response_post.json())
    assert response_post.json()['id'] is not None

    newname = support_steps.generate_random_letter_strings(6)
    datamy="name=" + newname +"&status=sold"
    response_post_update = requests.post(urls.url_pet_get_id(str(response_post.json()['id'])), data=datamy)
    print ("response_updated =" ,response_post_update.json() )
    assert response_post_update.status_code ==200
    response_get = requests.get(urls.url_pet_get_id(str(response_post.json()['id'])))
    print("result get =", response_get.json())
    assert response_get.json()['name']==newname

def test_post_nagative_pet_id():
    newname = support_steps.generate_random_letter_strings(6)
    datamy = "name=" + newname +"&status=sold"
    response_post_update = requests.post(urls.url_pet_get_id(support_steps.generate_random_number_strings(6)), data=datamy)
    print("response_updated =", response_post_update.json())
    assert response_post_update.status_code == 404

#***** Запросы PUT *****

def test_put_pet():
    request = {}
    request["name"] = support_steps.generate_random_letter_strings(6)
    request["category"] = {}
    request["category"]["name"] = "cats"
    request["photoUrls"] = ["photoMarta1"]
    response_post = requests.post(urls.url_pet_post, json=request)
    print("result=", response_post.json())

    request_put = {}
    request_put["id"] = response_post.json()["id"]
    request_put["name"] = support_steps.generate_random_letter_strings(6)
    response_put = requests.put(urls.url_pet_post, json=request_put)
    print("result_put=", response_put.json())
    response_get = requests.get(urls.url_pet_get_id(str(response_post.json()['id'])))
    assert request_put["name"] == response_get.json()["name"]
    assert response_put.json()["name"] == response_get.json()["name"]

def test_negative_put_pet():
    response_get = requests.get(urls.url_pet_get_id(support_steps.generate_random_number_strings(6)))
    assert response_get.status_code == 404

#***** Запросы GET *****

#получить питомца по ID
def test_get():
    idtmp = support_steps.generate_random_number_strings(6)
    nametmp = support_steps.generate_random_letter_strings(6)
    request = {}
    request["id"] = idtmp
    request["name"] = nametmp
    request["category"] = {}
    request["category"]["name"] = "cats"
    request["photoUrls"] = ["photoMarta1"]
    response_post = requests.post(urls.url_pet_post, json=request)

    response = requests.get(urls.url_pet_get_id(idtmp))
    print("result_get=", response)
    assert response.json()['id'] == int(idtmp)
    assert response.json()['name'] == nametmp
    assert response.status_code == 200

def test_get_pet_id_negative ():
    response_get = requests.get(urls.url_pet_get_id(support_steps.generate_random_number_strings(6)))
    print("result =", response_get.json ())
    assert response_get.json () ['message'] == "Pet not found"

#получить питомца по статусу
def test_get_by_status():
    nametmp = support_steps.generate_random_letter_strings(6)
    request = {}
    request["name"] = nametmp
    request["status"] = "sold"
    request["category"] = {}
    request["category"]["name"] = "cats"
    request["photoUrls"] = ["photoMarta1"]
    print(request)
    response_post = requests.post(urls.url_pet_post, json=request)
    print("result=", response_post.json())

    response = requests.get(urls.url_pet_get_findbystatus("sold"))
    print("result_get=", response.json())
    assert response.status_code==200
    assert response.json()[0]['status'] == "sold"
    assert str(response.json()).__contains__(nametmp)

def test_get_negative_by_status():
    response = requests.get(urls.url_pet_get_findbystatus("test"))
    print("result_get=", response.json())
    assert response.status_code == 200
    assert str(response.json()).__contains__("[]")

#***** Запросы DEL *****

def test_del():
    request = {}
    request["name"] = "Marta"
    request["category"] = {}
    request["category"]["name"] = "cats"
    request["photoUrls"] = ["photoMarta1"]
    print(request)

    response_post = requests.post(urls.url_pet_post, json=request)
    print("result =", response_post.json())
    response_del = requests.delete(urls.url_pet_get_id(str(response_post.json()["id"])))
    print("result delete =", response_del.json())
    assert response_del.json()['code'] == 200
    response_get = requests.get(urls.url_pet_get_id(str(response_post.json()["id"])))
    assert response_get.json()['message'] == 'Pet not found'

def test_del_negative_id():
    response_del = requests.delete(urls.url_pet_get_id(support_steps.generate_random_number_strings(6)))
    print("result delete =", response_del)
    assert str(response_del).__contains__("404")


# pytest test_get.py::test_get -v -s