import pytest
import requests


class TestAPI:
    @pytest.mark.parametrize("status", [('sold'), ('lost')])
    def test_get_status(self, status):
        pet = requests.get(f"https://petstore.swagger.io/v2/pet/findByStatus?status={status}")
        if status == 'lost':
            assert pet.status_code == 400
        else:
            assert pet.status_code == 200

    @pytest.mark.parametrize("pet_data", [({
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
        }), ({})])
    def test_post_pet(self, pet_data):
        pet = requests.post("https://petstore.swagger.io/v2/pet", json=pet_data)
        print(pet_data)
        if len(pet_data) == 0:
            assert pet.status_code == 405
        else:
            assert pet.status_code == 200

    @pytest.mark.parametrize("status, method", [("sold", "put"), ("lost", "put")])
    def test_change_pet(self, status, method):
        data = {
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
            "status": "sold"
        }
        if method == "put":
            data["status"] = status
            pet = requests.put("https://petstore.swagger.io/v2/pet", json=data)
            if data["status"] == "sold" or data["status"] == "pending" or data["status"] == "available":
                assert pet.status_code == 200
            else:
                assert pet.status_code == 405

    @pytest.mark.parametrize("object, id", [("human", 3), ("pet", 0)])
    def test_wrong_changes(self, object, id):
        pet = requests.post(f"https://petstore.swagger.io/v2/{object}/{id}")
        print(pet.status_code)
        if id == 0:
            assert pet.status_code == 400
        else:
            assert pet.status_code == 404

    @pytest.mark.parametrize("status", [("sold"), ("lost")])
    def test_find_by_status(self, status):
        pet = requests.get(f"https://petstore.swagger.io/v2/pet/findByStatus?status={status}")
        if status == "sold" or status == "pending" or status == "available":
            assert pet.status_code == 200
        else:
            assert pet.status_code == 400

    @pytest.mark.parametrize("id", [(3), ("f")])
    def test_delete_pet(self, id):
        print(type(id))
        if type(id) != int:
            pet = requests.delete(f"https://petstore.swagger.io/v2/pet/{id}")
            assert pet.status_code == 400

        pet = requests.delete(f"https://petstore.swagger.io/v2/pet/{id}")
        assert pet.status_code == 200
        pet = requests.delete(f"https://petstore.swagger.io/v2/pet/{id}")
        assert pet.status_code == 404
