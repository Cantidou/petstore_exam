import pytest
from pydantic import ValidationError
@pytest.fixture(scope="session")
def pet_data():
    data = {
            "id": 3,
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
    return data


@pytest.fixture(scope="function")
def validate_status(status):
    match status:
        case "sold" | "pending" | "available":
            return True
        case _:
            raise ValidationError("Invalid status")


