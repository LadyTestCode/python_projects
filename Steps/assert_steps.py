# Функция проверяет утверждение, что іd is not None
def assert_not_none_id(response):
    print (response)
    assert response.json()['id'] is not None
    print ("PASSED")

# Функция проверяет утверждение, іd в запросах равны
def assert_equals_response_ids(first, second):
    print("first =", first.json())
    print("second =", second.json ())
    assert first.json()['id'] == second.json()['id']
    print ("PASSED")

# Функция проверяет, что ответ содержит определенный текст
def assert_response_contains_text(response, text):
    assert str(response).__contains__(text)
    print("PASSED")

# Функция проверяет, что два переданных значения равны
def assert_equals_response_values(value1, value2):
    assert value1 == value2
    print("PASSED")

# Функция проверяет, что ответ содержит определенный статус
def assert_response_has_status(response, status):
    assert response.status_code == status
    print("PASSED")
