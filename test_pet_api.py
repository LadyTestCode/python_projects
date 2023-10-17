import pytest
import requests
import json
import resources.urls as urls
import resources.constants as constants
import Steps.support_steps as support_steps
import Steps.create_request_json_steps as create_request_json
import Steps.request_steps as requests_steps
import Steps.assert_steps as assert_steps

#************** Тестирование API для управления питомцами **************

#***** Запросы POST *****

# проверка создания питомца
@pytest.mark.smoke_regression
@pytest.mark.full_regression
@pytest.mark.parametrize('type',
                         [
                             create_request_json.generate_json_pet_required_param(),
                             create_request_json.generate_json_pet()
                         ],
                         ids=["required_param", "all_param"]
                         )
def test_post_pet(type):
    # создаем данные json для запроса
    request = type
    print(request)
    # отправляем запрос
    response_post = requests_steps.request_post(urls.url_pet_post, request)
    print("result=", response_post.json())
    # проверяем, что вернулся непустой ID созданного питомца
    assert_steps.assert_not_none_id(response_post)
    # проверяем, что созданного питомца можно получить запросом get
    response_get = requests_steps.request_get(urls.url_pet_get_id(str(response_post.json()['id'])))
    print("result get =", response_get.json())
    # проверяем, что вернулся именно тот ID  питомца, с которым его создавали
    assert_steps.assert_equals_response_ids(response_get, response_post)

# проверка создания питомца с невалидными даннми
@pytest.mark.full_regression
def test_post_name_negative():
    # создаем json c для создания питомца
    request = create_request_json.generate_json_pet()
    # заменяем в нем имя категории на невалидное
    request["category"]["name"] = []
    # отправляем запрос
    response_post = requests_steps.request_post(urls.url_pet_post, request)
    print("result =", response_post.json())
    # проверяем ответ
    assert_steps.assert_equals_response_values(response_post.json()['message'],"something bad happened")

# проверка возможности загрузить файл для питомца
@pytest.mark.smoke_regression
@pytest.mark.full_regression
def test_post_pet_uploadImage():
    # создаем json для запроса
    request = create_request_json.generate_json_pet_required_param()
    # отправляем запрос и создаем питомца
    response_post = requests_steps.request_post(urls.url_pet_post, request)
    print("result=", response_post.json())
    assert_steps.assert_not_none_id (response_post)
    # работа с файлом (позже вынести файл куда - нибудь в resources)
    files = support_steps.open_file(constants.image_pet)
    # отправляем запрос на загрузку файла
    response_post_image = requests_steps.request_post_image(urls.url_pet_post_uploadimage(str(response_post.json()['id'])), files)
    print(response_post_image)
    # проверяем, что ответ содержит статус 200
    assert_steps.assert_response_has_status(response_post_image, 200)
    # закрываем чтение файла
    support_steps.close_file(files)

# проверка загрузки файла для несуществующего питомца
@pytest.mark.full_regression
def test_post_pet_negative_uploadImage():
    # работа с файлом (позже вынести файл куда - нибудь в resources)
    fp = open('/Users/20071554/Desktop/test.txt', 'rb')
    files = {'file': fp}
    # пробуем загрузить файл для несуществующего питомца
    response_post_image = requests_steps.request_post_image(urls.url_pet_post_uploadimage(support_steps.generate_random_letter_strings(6)), files)
    # проверяем, что ответ содержит статус 404
    assert_steps.assert_response_has_status (response_post_image, 404)
    # закрываем чтение файла
    fp.close()

#проверяем изменение данных о питомце запросом POST
@pytest.mark.smoke_regression
@pytest.mark.full_regression
def test_post_pet_id():
    # создаем json с данными о питомце
    request = create_request_json.generate_json_pet_required_param()
    # отправляем запрос на создание питомца
    response_post = requests_steps.request_post(urls.url_pet_post, request)
    print("result=", response_post.json())
    # убеждаемся, что питомец создан, вернулся непустой ID
    assert_steps.assert_not_none_id(response_post)
    # изменяем кличку питомца
    newname = support_steps.generate_random_letter_strings(6)
    datamy="name=" + newname +"&status=sold"
    # отправляем запрос на изменение питомца
    response_post_update = requests_steps.request_post_update(urls.url_pet_get_id(str(response_post.json()['id'])), datamy)
    print ("response_updated =" ,response_post_update.json() )
    # проверяем, что ответ содержит статус 200
    assert_steps.assert_response_has_status(response_post_update, 200)
    # отправляем запрос на получение данных питомца
    response_get = requests_steps.request_get(urls.url_pet_get_id(str(response_post.json()['id'])))
    print("result get =", response_get.json())
    # проверяем, что кличка действительно изменена
    assert_steps.assert_equals_response_valuesassert(response_get.json()['name'], newname)

#проверка, что нельзя измененить несуществующего питомца
@pytest.mark.full_regression
def test_post_negative_pet_id():
    # задаем произвольное имя питомцв
    newname = support_steps.generate_random_letter_strings(6)
    # готовим и выполняем запрос на обновление
    datamy = "name=" + newname +"&status=sold"
    response_post_update = requests_steps.request_post_update(urls.url_pet_get_id(support_steps.generate_random_number_strings(6)), datamy)
    print("response_updated =", response_post_update.json())
    # проверяем, что ответ содержит статус 404
    assert_steps.assert_response_has_status (response_post_update, 404)

#***** Запросы PUT *****
#проверка возможности изменить кличку питомца череp put
@pytest.mark.smoke_regression
@pytest.mark.full_regression
def test_put_pet():
    # создаем питомца
    request = create_request_json.generate_json_pet_required_param()
    response_post = requests_steps.request_post(urls.url_pet_post, request)
    print("result=", response_post.json())
    # формируем данные для обновления
    request_put = create_request_json.generate_json_update_pet(str(response_post.json()["id"]))
    # отправляем запрос на обновление
    response_put = requests_steps.request_put(urls.url_pet_post, request_put)
    print("result_put=", response_put.json())
    # отправляем запрос на получение
    response_get = requests_steps.request_get(urls.url_pet_get_id(str(response_post.json()['id'])))
    # убеждаемся, что имя изменено
    assert_steps.assert_equals_response_values(request_put["name"],response_get.json()["name"])
    assert_steps.assert_equals_response_values(response_put.json()["name"],response_get.json()["name"])

# Проверка, что нельзя обновить несуществующего питомца
@pytest.mark.full_regression
def test_negative_put_pet():
    # формируем json
    request_put = create_request_json.generate_json_update_pet(support_steps.generate_random_number_strings(9))
    print(request_put)
    # отправляем запросом на обновление питомца, которого не создавали:
    response_put_pet = requests_steps.request_put(urls.url_pet_post, request_put)
    print("response_put_pet =", response_put_pet.status_code)
    # проверяем, что ответ содержит статус 404
    assert_steps.assert_response_has_status (response_put_pet, 404)

#***** Запросы GET *****

# проверка получения питомца по ID
@pytest.mark.smoke_regression
@pytest.mark.full_regression
def test_get():
    # создаем json для питомца
    request = create_request_json.generate_json_pet()
    # отправляем запрос на создание питомца
    response_post = requests_steps.request_post(urls.url_pet_post, request)
    # отправляем запрос на получение питомца
    response = requests_steps.request_get(urls.url_pet_get_id(str(response_post.json()['id'])))
    # смотрим, что в статус ответа 200 и что в ответе получили данные питомца
    print("result =", response.json())
    assert_steps.assert_equals_response_ids(response,response_post)
    assert_steps.assert_equals_response_values(response.json()['status'], 'sold')
    assert_steps.assert_response_has_status (response, 200)

# проверка запроса на получение несуществующего питомца
@pytest.mark.full_regression
def test_get_pet_id_negative ():
    # отправляем запрос
    response_get = requests_steps.request_get(urls.url_pet_get_id(support_steps.generate_random_number_strings(6)))
    print("result =", response_get.json ())
    # убеждаемся, что питомец не найден
    assert_steps.assert_equals_response_values(response_get.json () ['message'], "Pet not found")

# проверка, получения питомца по статусу
@pytest.mark.smoke_regression
@pytest.mark.full_regression
@pytest.mark.parametrize('status',
                         [
                             "sold",
                             "available"
                         ],
                         ids=["sold", "available"]
                         )
def test_get_by_status(status):
    # создаем питомца с нужным статусом (параметр)
    print(status)
    request = create_request_json.generate_json_pet()
    # подменяем статус на нужный нам
    request['status'] = status
    # отправляем запрос
    response_post = requests_steps.request_post(urls.url_pet_post, request)
    print("result=", response_post.json())
    # отправляем запрос на получение питомцев со статусом sold
    response = requests_steps.request_get(urls.url_pet_get_findbystatus(status))
    print("result_get=", response.json())
    # выполняем проверки полученного результата
    assert_steps.assert_response_has_status (response, 200)
    assert_steps.assert_equals_response_values(response.json()[0]['status'],status)
    assert_steps.assert_response_contains_text(response.json(),(response_post.json()['name']))

# проверка поиска питомцев по заведомо не существующему статусу
@pytest.mark.smoke_regression
def test_get_negative_by_status():
    # отправляем запрос
    response = requests_steps.request_get(urls.url_pet_get_findbystatus(support_steps.generate_random_letter_strings(6)))
    print("result_get=", response.json())
    # проверяем, что ответ содержит статус 200 и список питомцев пуст
    assert_steps.assert_response_has_status (response, 200)
    assert_steps.assert_response_contains_text(response.json(), "[]")

#***** Запросы DEL *****

# проверка удаления питомца
@pytest.mark.smoke_regression
@pytest.mark.full_regression
def test_del():
    # создаем json для питомца
    request = create_request_json.generate_json_pet()
    # отправяем запрос на создание питомца
    response_post = requests_steps.request_post(urls.url_pet_post, request)
    print("result =", response_post.json())
    # теперь удаляем питомца, отправляем запрос
    response_del = requests_steps.request_del(urls.url_pet_get_id(str(response_post.json()["id"])))
    print("result delete =", response_del.json())
    # проверяем, что ответ содержит статус 200
    assert_steps.assert_response_has_status (response_del, 200)
    # пробуем получить удаленного питомца
    response_get = requests_steps.request_get(urls.url_pet_get_id(str(response_post.json()["id"])))
    assert_steps.assert_equals_response_values(response_get.json()['message'] , 'Pet not found')

# проверка удаления несуществующего питомца
@pytest.mark.full_regression
def test_del_negative_id():
    #отправляем запрос на удаление несуществующего питомца
    response_del = requests_steps.request_del(urls.url_pet_get_id(support_steps.generate_random_number_strings(6)))
    print("result delete =", response_del)
    # проверяем, что ответ содержит статус 404
    assert_steps.assert_response_has_status(response_del, 404)


# pytest test_get.py::test_get -v -s
# pytest -m smoke_regression