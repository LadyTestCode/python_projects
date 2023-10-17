import random
import string
import Steps.support_steps as support_steps
import allure

#создать json для запроса создания пользователя с произвольным username
def generate_json_user_random():
    #with allure.step("Создаем JSON для метода POST/user c произвольным username, генерируем ID"):
    request = {}
    request["id"]= support_steps.generate_random_number_strings(6)
    request["username"] = support_steps.generate_random_letter_strings(6)
    request["firstName"] = support_steps.generate_random_letter_strings(6)
    request["lastName"] = support_steps.generate_random_letter_strings(6)
    request["email"] = support_steps.generate_random_email_strings()
    request["password"] = support_steps.generate_random_letter_strings(6)
    request["phone"] = support_steps.generate_random_phone_number_strings()
    request["userStatus"] = 0
    print("request =", request)
    return request

#создать json для запроса создания питомца с произвольным именем  - все поля
def generate_json_pet():
    #with allure.step("Создаем JSON для метода POST/pet со всеми параметрами, генерируем ID"):
        request = {}
        request['id'] = support_steps.generate_random_number_strings(7)
        request['category'] = {}
        request['category']['id'] = support_steps.generate_random_number_strings(7)
        request['category']['name'] = support_steps.generate_random_letter_strings(7)
        request['name'] = support_steps.generate_random_letter_strings(7)
        request['photoUrls'] = [support_steps.generate_random_letter_strings(7)]
        request['tags'] = [{}]
        request['tags'][0]['id'] = support_steps.generate_random_number_strings(7)
        request['tags'][0]['name'] = support_steps.generate_random_letter_strings(7)
        request['status'] = "sold"
        print("request =", request)
        return request

#создать json для запроса создания питомца с произвольным именем  - только обязательные поля
def generate_json_pet_required_param():
    #with allure.step("Создаем JSON для метода POST/pet только с обязательными параметрами"):
        request = {}
        request['name'] = support_steps.generate_random_letter_strings(6)
        request['category'] = {}
        request['category']['name'] = support_steps.generate_random_letter_strings(6)
        request['photoUrls'] = [support_steps.generate_random_letter_strings(6)]
        print("request =", request)
        return request

#создать json для запроса обновления питомца
def generate_json_update_pet(id):
    #with allure.step("Создаем JSON для обновления питомца "):
        request = {}
        request["id"] = id
        request["name"] = support_steps.generate_random_letter_strings(6)
        request["category"] = {}
        request["category"]["name"] = support_steps.generate_random_letter_strings(6)
        request["photoUrls"] = [support_steps.generate_random_number_strings(6)]
        request["status"] = 'sold'
        print("request =", request)
        return request
