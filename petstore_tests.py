import pytest
import requests
import allure
from pydantic import BaseModel, field_validator


class Status(BaseModel):
    id: int
    category: dict
    name: str
    photoUrls: list
    tags: list
    status: str

    @field_validator("status")
    @classmethod
    def check_status(cls, value) -> str:
        if value in ["available", "pending", "sold"]:
            return value
        raise ValueError(f"Value {value} is not valid")


class TestAPI:
    url = "https://petstore.swagger.io/v2"
    test_data = {
        "id": 0,
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "doggie",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": "available"
    }

    @allure.title("Test create object")
    @allure.description(
        "Создание: "
        "- полноценный объект, статус available 200 "
        "- пустой словарь 405 "
        "- пустое тело запроса 415")
    @allure.tag("post", "pets")
    @pytest.mark.parametrize("pet_data", [test_data, {}, None])
    def test_post_pet(self, pet_data):
        pet = requests.post(self.url + "/pet", json=pet_data)
        if pet_data is None:
            with allure.step("Test response with empty body"):
                assert pet.status_code == 415
        elif len(pet_data) == 0:
            with allure.step("Test response with empty dictionary"):
                assert pet.status_code == 405
        else:
            with allure.step("Test response with posting new data"):
                assert pet.status_code == 200

    @allure.title("Test change object")
    @allure.description("Изменение: "
                        "- поменять статус на sold 200 "
                        "- поменять статус на lost 405")
    @allure.tag("put", "pets")
    @pytest.mark.parametrize("status", ["sold", "lost"])
    def test_change_pet(self, status, pet_data):

        pet_data["status"] = status

        pet = requests.put(self.url + "/pet", json=pet_data)
        if pet_data["status"] in ["sold", "pending", "available"]:
            with allure.step("Test response with changing object with correct data"):
                assert pet.status_code == 200
        else:
            with allure.step("Test response with changing missing object"):
                Status.check_status(pet_data["status"])  # Validate status
                assert pet.status_code == 405

    @allure.title("Test change incorrect object")
    @allure.description(
        "Изменение: "
        "- попробовать изменить несуществующий объект 404 "
        "- попробовать изменить объект с некорректным id 400")
    @allure.tag("put", "pets")
    @pytest.mark.parametrize("object, id", [("human", 3), ("pet", None)])
    def test_wrong_changes(self, object, id):
        pet = requests.post(self.url + f"/{object}/{id}")
        print(pet.status_code)
        if id is None:
            with allure.step("Test response with invalid ID"):
                assert pet.status_code == 400
        else:
            with allure.step("Test response with invalid object"):
                assert pet.status_code == 404

    @allure.title("Test find by status")
    @allure.tag("get", "pets")
    @allure.description("Поиск по статусу: "
                        "- найти свое животное в статусе sold 200 "
                        "- поискать животное в статусе lost 400")
    @pytest.mark.parametrize("status", [('sold'), ('lost')])
    def test_get_status(self, status):
        pet = requests.get(self.url + f"/pet/findByStatus?status={status}")
        if status == 'lost':
            with allure.step(f"Test response with invalid status:{status}"):
                assert pet.status_code == 400
        else:
            with allure.step(f"Test response with valid status:{status}"):
                assert pet.status_code == 200

    @allure.title("Test delete object")
    @allure.tag("delete", "pets")
    @allure.description("Удаление: "
                        "- удалить своё животное 200 "
                        "- удалить ещё раз 404 "
                        "- удалить с некорректным id 400")
    @pytest.mark.parametrize("id", [3, "f"])
    def test_delete_pet(self, id, pet_data):
        if type(id) is not int:
            with allure.step(f"Test responce with invalid id:{id}"):
                pet = requests.delete(self.url + f"/pet/{id}")
                assert pet.status_code == 400
        else:
            with allure.step(f"Create pet in the store with id:{id} for deleting"):
                requests.post(self.url + "/pet", json=pet_data)
            with allure.step(f"Test delete pet with id:{id}"):
                pet = requests.delete(self.url + f"/pet/{id}")
                assert pet.status_code == 200
            with allure.step(f"Test delete non-exist object"):
                pet = requests.delete(self.url + f"/pet/{id}")
                assert pet.status_code == 404