import random
import string


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