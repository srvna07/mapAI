import pytest
from utils.data_factory import DataFactory
import json
from pathlib import Path


file_path = Path(__file__).resolve().parents[2] / "testdata" / "new_role_data.json"



@pytest.mark.high
def test_get_all_roles(api_client):
    response = api_client.get("/api/v1/role")
    assert response.status_code == 200, f"Failed to get all roles: {response.text}"
    body = response.json()
    assert "data" in body
    assert isinstance(body["data"], list)


@pytest.mark.high
def test_create_role(api_client, role_data):

    payload = {
        "name": role_data["role"]["name"]
    }

    response = api_client.post(
        "/api/v1/role",
        payload=payload
    )

    assert response.status_code == 201, \
        f"Role creation failed: {response.text}"

    role_id = response.json()["id"]
    print(f"Created Role ID: {role_id}")

    # Save id into test data file
    with open(file_path, "r") as file:
        data = json.load(file)

    data["role"]["id"] = role_id

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


@pytest.mark.high
def test_get_role_by_id(api_client):

    with open(file_path, "r") as file:
        data = json.load(file)

    role_id = data["role"]["id"]

    response = api_client.get(
        f"/api/v1/role/{role_id}"
    )

    assert response.status_code == 200, \
        f"Failed getting role {role_id}: {response.text}"


@pytest.mark.high
def test_update_role_by_id(api_client):

    with open(file_path, "r") as file:
        data = json.load(file)

    role_id = data["role"]["id"]

    update_payload = {
        "id": role_id,
        "name": data["edited_role"]["name"]
    }

    response = api_client.patch(
        "/api/v1/role",
        payload=update_payload
    )

    print(response.text)

    assert response.status_code == 200, \
        f"Update failed: {response.text}"


@pytest.mark.high
def test_delete_role_by_id(api_client):

    with open(file_path, "r") as file:
        data = json.load(file)

    role_id = data["role"]["id"]

    response = api_client.delete(
        f"/api/v1/role/{role_id}"
    )

    assert response.status_code in [200, 204], \
        f"Delete failed: {response.text}"

