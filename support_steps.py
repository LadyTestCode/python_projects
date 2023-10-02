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