#создание URLs

main_url = "https://petstore.swagger.io/v2"
url_pet_post = main_url + "/" + "pet"
url_pet_user = main_url + "/" + "user"

def url_pet_get_id(pet_id):
    return url_pet_post + "/" + pet_id

def url_pet_get_findbystatus(status):
    return url_pet_post + "/findByStatus?status=" + status

def url_pet_post_uploadimage(pet_id):
    print("url_1", url_pet_post + "/" + pet_id + "/uploadImage")
    return url_pet_post + "/" + pet_id + "/uploadImage"
