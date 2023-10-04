import random
import string
import Steps.support_steps as support_steps

#создать json для запроса создания пользователя с произвольным username
def generate_json_user_random():
    request = {}
    request["id"]= support_steps.generate_random_number_strings(6)
    request["username"] = support_steps.generate_random_letter_strings(6)
    request["firstName"] = support_steps.generate_random_letter_strings(6)
    request["lastName"] = support_steps.generate_random_letter_strings(6)
    request["email"] = support_steps.generate_random_email_strings()
    request["password"] = support_steps.generate_random_letter_strings(6)
    request["phone"] = support_steps.generate_random_phone_number_strings()
    request["userStatus"] = 0
    return request

#создать json для запроса создания пользователя с заданным username
def generate_json_user_username(username):
    request = {}
    request["id"]= support_steps.generate_random_number_strings(6)
    request["username"] = username
    request["firstName"] = support_steps.generate_random_letter_strings(6)
    request["lastName"] = support_steps.generate_random_letter_strings(6)
    request["email"] = support_steps.generate_random_email_strings()
    request["password"] = support_steps.generate_random_letter_strings(6)
    request["phone"] = support_steps.generate_random_phone_number_strings()
    request["userStatus"] = 0
    return request

#создать json для запроса создания питомца с произвольным именем заданной категории
def generate_json_pet(category):
    request = {}
    request["id"] = support_steps.generate_random_number_strings(6)
    request["name"] = support_steps.generate_random_letter_strings(6)
    request["category"] = {}
    request["category"]["name"] = category
    request["photoUrls"] = [support_steps.generate_random_number_strings(6)]
    request["status"] = 'sold'
    return request

#создать json для запроса обновления питомца
def generate_json_update_pet(id):
    request = {}
    request["id"] = id
    request["name"] = support_steps.generate_random_letter_strings(6)
    request["category"] = {}
    request["category"]["name"] = support_steps.generate_random_letter_strings(6)
    request["photoUrls"] = [support_steps.generate_random_number_strings(6)]
    request["status"] = 'sold'
    return request

#создать невалидный json для запроса создания питомца
def generate_json_pet_incorrect():
    request = {}
    request["id"] = support_steps.generate_random_number_strings(6)
    request["name"] = support_steps.generate_random_letter_strings(6)
    request["category"] = {}
    request["category"]["name"] = []
    request["photoUrls"] = [support_steps.generate_random_number_strings(6)]
    return request