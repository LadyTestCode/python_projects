import random
import string
import json


#создание строки чисел 0-9 заданной длины
def generate_random_number_strings(length):
    result = ""
    for i in range(0, length):
        result += str(random.randint(0,9))
    return result

#создание текстовой строки заданной длины
def generate_random_letter_strings(length):
    result = ""
    for i in range(0, length):
        result += str(random.choice(string.ascii_letters[random.randint(0,5)]))
    return result

#создание текстово-цифровой строки заданной длины
def generate_random_letter_number_strings(length):
    result = ""
    for i in range(0, length):
        result += str(random.choice(string.ascii_letters[random.randint(0,5)]))
        result += str(random.randint(0,9))

    return result

#создание email
def generate_random_email_strings():
    result = ""
    for i in range(0, 8):
        result += str(random.choice(string.ascii_letters[random.randint(0,5)]))
    result +="@"
    for i in range(0, 4):
        result += str(random.choice(string.ascii_letters[random.randint(0,5)]))
    result += ".com"
    return result

#создание телефонного номера
def generate_random_phone_number_strings():
    result = "+"
    result += str(random.randint(0,99))
    for i in range(0, 10):
        result += str(random.randint(0,9))
    return result

#работа с файлом - открыть
def open_file(file):
    # Открываем файл на чтение
    fp = open(file, 'rb')
    files = {'file': fp}
    return files

#работа с файлом - закрыть
def close_file(file):
    # Закываем файл на чтение
    file['file'].close

#функция выводит json в удобном читаемом формате
def jprint(response):
    res = json.dumps(response.json(), indent=5, sort_keys=True, ensure_ascii=False).encode('utf8')
    print(res.decode())
    # indent регулирует размер отступа


#функция для парсинга json  - ищет значения по ключу
def find_values(json_str, target_key):
    """
    Парсит JSON и возвращает все значения для заданного ключа.
    json_str: строка с JSON для парсинга
    target_key: ключ, который нужно найти
    """
    def extract_values(obj, key):
        arr = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == key:
                    arr.append(v)
                arr += extract_values(v, key)
        elif isinstance(obj, list):
            for item in obj:
                arr += extract_values(item, key)
        return arr
    try:
        data = json.loads(json_str)
        return extract_values(data, target_key)
    except json.JSONDecodeError:
        return []