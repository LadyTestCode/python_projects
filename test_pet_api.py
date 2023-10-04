import pytest
import requests
import json
import resources.urls as urls
import Steps.support_steps as support_steps
import Steps.create_request_json as create_request_json

#************** Тестирование API для управления питомцами **************

#***** Запросы POST *****

@pytest.mark.smoke_regression
def test_post_pet():
    #создаем данные для запроса
    request = create_request_json.generate_json_pet("cats")
    response_post = requests.post(urls.url_pet_post, json=request)
    print("result=", response_post.json())
    #проверяем, что вернулся непустой ID созданного питомца
    assert response_post.json()['id'] is not None
    response_get = requests.get(urls.url_pet_get_id(str(response_post.json()['id'])))
    print("result get =", response_get.json())
    assert response_get.json () ['id'] == response_post.json() ['id']

@pytest.mark.full_regression
def test_post_name_negative():
    #создаем json c невалидным значением поля category.name
    request = create_request_json.generate_json_pet_incorrect()
    response_post = requests.post(urls.url_pet_post, json=request)
    print("result =", response_post.json())
    assert response_post.json()['message'] == "something bad happened"

@pytest.mark.smoke_regression
def test_post_pet_uploadImage():
    #проверка загрузки файла для питомца
    request = create_request_json.generate_json_pet("cats")
    response_post = requests.post(urls.url_pet_post, json=request)
    print("result=", response_post.json())
    assert response_post.json()['id'] is not None

    fp = open('/Users/20071554/Desktop/test.txt', 'rb')
    files = {'file': fp}
    response_post_image = requests.post(urls.url_pet_post_uploadimage(str(response_post.json()['id'])), files=files)
    print(response_post_image)
    assert response_post_image.status_code == 200
    fp.close()

@pytest.mark.full_regression
def test_post_pet_negative_uploadImage():
    # проверка загрузки файла для несуществующего питомца
    fp = open('/Users/20071554/Desktop/test.txt', 'rb')
    files = {'file': fp}
    response_post_image = requests.post(urls.url_pet_post_uploadimage(support_steps.generate_random_letter_strings(6)), files=files)
    assert response_post_image.status_code == 404
    fp.close()

#изменение данных о питомце запросом POST
@pytest.mark.smoke_regression
def test_post_pet_id():
    request = create_request_json.generate_json_pet("cats")
    response_post = requests.post(urls.url_pet_post, json=request)
    print("result=", response_post.json())
    assert response_post.json()['id'] is not None
    #изменяем кличку питомца
    newname = support_steps.generate_random_letter_strings(6)
    datamy="name=" + newname +"&status=sold"
    response_post_update = requests.post(urls.url_pet_get_id(str(response_post.json()['id'])), data=datamy)
    print ("response_updated =" ,response_post_update.json() )
    assert response_post_update.status_code ==200
    response_get = requests.get(urls.url_pet_get_id(str(response_post.json()['id'])))
    print("result get =", response_get.json())
    #проверяем, что кличка изменена
    assert response_get.json()['name']==newname

@pytest.mark.full_regression
def test_post_nagative_pet_id():
    #проверка изменения несуществующего питомца
    newname = support_steps.generate_random_letter_strings(6)
    datamy = "name=" + newname +"&status=sold"
    response_post_update = requests.post(urls.url_pet_get_id(support_steps.generate_random_number_strings(6)), data=datamy)
    print("response_updated =", response_post_update.json())
    assert response_post_update.status_code == 404

#***** Запросы PUT *****
@pytest.mark.smoke_regression
def test_put_pet():
    #проверка возможности изменить кличку питомца
    #создаем питомца
    request = create_request_json.generate_json_pet("cats")
    response_post = requests.post(urls.url_pet_post, json=request)
    print("result=", response_post.json())
    #формируем данные для обновления
    request_put = create_request_json.generate_json_update_pet(str(response_post.json()["id"]))
    response_put = requests.put(urls.url_pet_post, json=request_put)
    print("result_put=", response_put.json())
    response_get = requests.get(urls.url_pet_get_id(str(response_post.json()['id'])))
    #убеждаемся, что имя изменено
    assert request_put["name"] == response_get.json()["name"]
    assert response_put.json()["name"] == response_get.json()["name"]

@pytest.mark.full_regression
def test_negative_put_pet():
    request_put = create_request_json.generate_json_update_pet(support_steps.generate_random_number_strings(6))
    print(request_put)
    # обращаемся с запросом на обновление питомца, которого не создавали:
    url_put_pet = urls.url_pet_post
    response_put_pet = requests.put(url_put_pet, json=request_put)
    print("response_put_pet =", response_put_pet.status_code)
    assert response_put_pet.status_code == 404

#***** Запросы GET *****

#получить питомца по ID
@pytest.mark.smoke_regression
def test_get():
    #создаем питомца
    request = create_request_json.generate_json_pet("cats")
    response_post = requests.post(urls.url_pet_post, json=request)
    #получаем питомца
    response = requests.get(urls.url_pet_get_id(str(response_post.json()['id'])))
    #смотрим, что в ответе
    print("result =", response.json())
    assert response.json()['id'] == response_post.json()['id']
    assert response.json()['status'] == 'sold'
    assert response.status_code == 200

@pytest.mark.full_regression
def test_get_pet_id_negative ():
    #ищем несуществующего питомца
    response_get = requests.get(urls.url_pet_get_id(support_steps.generate_random_number_strings(6)))
    print("result =", response_get.json ())
    assert response_get.json () ['message'] == "Pet not found"

#получить питомца по статусу
@pytest.mark.smoke_regression
def test_get_by_status():
    #создаем питомца с нужным статусом  - sold
    request = create_request_json.generate_json_pet("dogs")
    response_post = requests.post(urls.url_pet_post, json=request)
    print("result=", response_post.json())
    #выбираем питомцев
    response = requests.get(urls.url_pet_get_findbystatus("sold"))
    print("result_get=", response.json())
    #выполняем проверки
    assert response.status_code==200
    assert response.json()[0]['status'] == "sold"
    assert str(response.json()).__contains__(response_post.json()['name'])

@pytest.mark.smoke_regression
def test_get_negative_by_status():
    #ищем питомцев по заведомо не существующему статусу
    response = requests.get(urls.url_pet_get_findbystatus(support_steps.generate_random_letter_strings(6)))
    print("result_get=", response.json())
    assert response.status_code == 200
    assert str(response.json()).__contains__("[]")

#***** Запросы DEL *****
@pytest.mark.smoke_regression
def test_del():
    #проверка удаления питомца
    #сначала создаем питомца
    request = create_request_json.generate_json_pet("dogs")
    response_post = requests.post(urls.url_pet_post, json=request)
    print("result =", response_post.json())
    #теперь удаляем питомца
    response_del = requests.delete(urls.url_pet_get_id(str(response_post.json()["id"])))
    print("result delete =", response_del.json())
    assert response_del.json()['code'] == 200
    #пробуем получить удаленного питомца
    response_get = requests.get(urls.url_pet_get_id(str(response_post.json()["id"])))
    assert response_get.json()['message'] == 'Pet not found'

@pytest.mark.full_regression
def test_del_negative_id():
    #проверка удаления несуществующего питомца
    response_del = requests.delete(urls.url_pet_get_id(support_steps.generate_random_number_strings(6)))
    print("result delete =", response_del)
    assert str(response_del).__contains__("404")


# pytest test_get.py::test_get -v -s