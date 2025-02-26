import json
import pytest
from fastapi.testclient import TestClient
from app import app, PhoneBookBase,phonebook_engine



# Create a test client
client = TestClient(app)

# Create the tables in the test database
PhoneBookBase.metadata.create_all(bind=phonebook_engine)

# Test cases for different scenarios

def test_add_person():
    response = client.post(
        "/PhoneBook/add",
        json={"full_name": "John Doe", "phone_number": "1234567890"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Person added successfully"

def test_add_person_invalid_data():
    response = client.post(
        "/PhoneBook/add",
        json={"full_name": "<script>alert('XSS')</script>", "phone_number": "invalid"}
    )
    assert response.status_code == 400

def test_delete_by_name():
    # Add a person to delete later
    client.post("/PhoneBook/add", json={"full_name": "Jane Doe", "phone_number": "9876543210"})

    response = client.put("/PhoneBook/deleteByName", params={"full_name": "Jane Doe"})
    assert response.status_code == 200
    assert response.json()["message"] == "Person deleted successfully"

def test_delete_by_name_not_found():
    response = client.put("/PhoneBook/deleteByName", params={"full_name": "Nonexistent"})
    assert response.status_code == 404

def test_delete_by_number():
    # Add a person to delete later
    client.post("/PhoneBook/add", json={"full_name": "Alice", "phone_number": "5551234567"})

    response = client.put("/PhoneBook/deleteByNumber", params={"phone_number": "5551234567"})
    assert response.status_code == 200
    assert response.json()["message"] == "Person deleted successfully"

def test_delete_by_number_not_found():
    response = client.put("/PhoneBook/deleteByNumber", params={"phone_number": "9999999999"})
    assert response.status_code == 404

def test_list_phonebook():
    # Add a person to the phonebook for testing listing
    client.post("/PhoneBook/add", json={"full_name": "Bob", "phone_number": "1112223333"})

    response = client.get("/PhoneBook/list")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(person["full_name"] == "Bob" for person in data)
# Test cases for acceptable names
def test_add_person_acceptable_names():
    names = [
        "Bruce Schneier",
        "Schneier, Bruce",
        "Schneier, Bruce Wayne",
        "O’Malley, John F.",
        "John O’Malley-Smith",
        "Cher"
    ]

    for name in names:
        response = client.post(
            "/PhoneBook/add",
            json={"full_name": name, "phone_number": "1234567890"}
        )
        print(response.json())
        assert response.status_code == 200
        assert response.json()["message"] == "Person added successfully"
if __name__ == "__main__":
    pytest.main()
