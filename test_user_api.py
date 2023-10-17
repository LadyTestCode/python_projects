import pytest
import requests
import json
import resources.urls as urls
import Steps.support_steps as support_steps
import Steps.create_request_json_steps as create_request_json
import Steps.request_steps as requests_steps
import Steps.assert_steps as assert_steps

#************ Тестирование API для управления пользователями **************

#***** Запросы POST *****

#проверка создания пользователя с переданным username пользователя
@pytest.mark.smoke_regression
@pytest.mark.full_regression
@pytest.mark.parametrize('username',
                         [
                             support_steps.generate_random_letter_strings(6),
                             support_steps.generate_random_letter_strings(6)
                         ],
                         ids=["sold", "available"]
                         )
def test_post_user_username(username):
    # создать json для пользователя со всеми параметрами
    request = create_request_json.generate_json_user_random()
    # заменяем username на нужный нам
    request["username"] = username
    # отправить запрос
    response_post_user = requests_steps.request_post(urls.url_pet_user, request)
    print("response_post_user =", response_post_user.json())
    # проверить, что ответ содержит статус 200
    assert_steps.assert_response_has_status(response_post_user, 200)

# проверка создания пользователя со случайным username
@pytest.mark.smoke_regression
def test_post_user():
    # создать json для пользователя со случайным username
    request = create_request_json.generate_json_user_random()
    # отправить запрос
    response_post_user = requests_steps.request_post(urls.url_pet_user, request)
    print("response_post_user =", response_post_user.json())
    # проверить, что ответ содержит статус 200
    assert_steps.assert_response_has_status(response_post_user, 200)

#***** Запросы GET *****

# проверка получения пользователя по юзеренейму
@pytest.mark.smoke_regression
@pytest.mark.full_regression
def test_get_user():
    # подготавливаем юзеренейм пользователя
    username = support_steps.generate_random_letter_strings(6)
    # создать json для пользователя с определенным username
    test_post_user_username(username)
    # подготавливаем данные для запроса get
    url_get_user = urls.url_pet_user + "/" + username
    # отправить запрос
    response_user = requests_steps.request_get(url_get_user)
    # проверить, что ответ содержит статус 200
    assert_steps.assert_response_has_status(response_user, 200)
    # проверить, что ответ содержит заданный нами username
    assert_steps.assert_equals_response_values(response_user.json()["username"], username)

# проверка получения пользователя по несуществующему username
@pytest.mark.full_regression
def test_get_negative_user():
    # создаем username для запроса
    username = support_steps.generate_random_letter_strings(6)
    url_get_user1 =  urls.url_pet_user + "/" + username
    # пытаемся получить пользователя по несуществующему username
    response_user1 = requests_steps.request_get(url_get_user1)
    # проверить, что ответ содержит 404
    assert_steps.assert_response_has_status(response_user1, 404)

#***** Запросы PUT *****

# провека, что можно обновить данные пользователя метдом put
@pytest.mark.smoke_regression
@pytest.mark.full_regression
def test_put_user():
    # создаем username для запроса
    username = support_steps.generate_random_letter_strings(6)
    # создать json для пользователя с определенным username
    request = create_request_json.generate_json_user_random()
    # заменяем username на нужный нам
    request["username"] = username
    # отправляем запрос
    response_post_user = requests_steps.request_post(urls.url_pet_user, request)
    print("response_post_user =", response_post_user.json())
    # готовим данные для обновления пользователя
    username1 = support_steps.generate_random_letter_strings(6)
    # создать json для пользователя с новым username
    request_put = create_request_json.generate_json_user_random()
    # заменяем username на нужный нам
    request_put["username"] = username1
    # формируем url и отправляем запрос
    url_put_user = urls.url_pet_user + "/" + username
    response_put_user = requests_steps.request_put(url_put_user, request_put)
    # проверим, что ответ содержит 200
    print("response_put_user =", response_put_user.status_code)
    assert_steps.assert_response_has_status(response_put_user, 200)
    # проверим, что по обновленому имени пользователя можно получить данные методом get
    url_get_user = urls.url_pet_user + "/" + username1
    response_get_user = requests_steps.request_get(url_get_user)
    print("response_get_user =", response_get_user.status_code)
    # проверим, что ответ содержит 200
    assert_steps.assert_response_has_status(response_get_user, 200)

# проверка, что нельзя обновить данные несуществующего пользователя метдом put
@pytest.mark.full_regression
def test_put_negative_user():
    # создаем username для json запроса и для url (будем использовать разные username)
    username = support_steps.generate_random_letter_strings(6)
    username1 = support_steps.generate_random_letter_strings(6)
    # создать json для пользователя со всеми данными
    request = create_request_json.generate_json_user_random()
    # заменяем username на нужный нам
    request["username"] = username
    # обращаемся с запросом по имени пользователя, которого не создавали:
    url_put_user = urls.url_pet_user + "/" + username1
    response_put_user = requests_steps.request_put(url_put_user, request_put)
    print("response_put_user =", response_put_user.status_code)
    # проверим, что ответ содержит 404
    assert_steps.assert_response_has_status(response_put_user, 404)

#***** Запросы DEL *****

# проверка удаления пользователя
@pytest.mark.smoke_regression
@pytest.mark.full_regression
def test_del_user():
    username = support_steps.generate_random_letter_strings(6)
    #создаем пользователя
    test_post_user_username(username)
    # формируем url для запроса
    url_del_user = urls.url_pet_user + "/" + username
    print(url_del_user)
    # выполняем запрос и удаляем пользователя
    response_user_del = requests_steps.request_del(url_del_user)
    print(response_user_del)
    # проверим, что ответ содержит 200
    assert_steps.assert_response_has_status(response_user_del, 200)
    # проверим далее, что удаленного пользователя теперь не получить запросом get
    response_user_get = requests_steps.request_get(url_del_user)
    assert_steps.assert_response_has_status(response_user_get, 404)

# проверка, что нельзя удалить пользователя, которого нет
@pytest.mark.full_regression
def test_del_negative_user():
    # формируем произвольный username
    username = support_steps.generate_random_letter_strings(6)
    # формируем url запроса
    url_del_user = urls.url_pet_user + "/" + username
    # отправляем запрос
    response_user_del = requests_steps.request_del(url_del_user)
    print(response_user_del)
    # проверим, что ответ содержит 404
    assert_steps.assert_response_has_status(response_user_del, 404)

#pytest test_user_api.py::test_del_negative_user - v - s
#pytest -m smoke_regression
#pytest test_post -n3