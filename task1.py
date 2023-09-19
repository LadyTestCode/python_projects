# Раздел User, метод POST /user
request = {}
request["id"] = 1
request["username"] = "IvanovIvan"
request["firstName"] = "Ivanov"
request["lastName"] = "Ivan"
request["email"] = "IvanovIvan@mail.ru"
request["password"] = "Qwerty-123"
request["phone"] = "+7(111)123-45-67"
request["userStatus"] = 6

#Раздел Store, метод POST /store/order
request = {}
request["id"] = 1
request["petId"] = 1
request["quantity"] = 3
request["shipDate"] = "2023-09-15T07:24:57.329Z"
request["status"] = "placed"
request["complete"] = True