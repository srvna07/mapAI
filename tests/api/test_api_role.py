import pytest
from utils.data_factory import DataFactory


@pytest.mark.high
def get_all_roles(api_client):
    response = api_client.get("/api/v1/role")
    assert response.status_code == 200, f"Failed to get all roles: {response.text}"
    body = response.json()
    assert "data" in body
    assert isinstance(body["data"], list)
    return response.json()

@pytest.mark.high
def test_get_role_by_role_id(api_client, new_user_data):
    roles = get_all_roles(api_client)

    # Get role name from user test data
    role_name = new_user_data["role"]["name"]

    # Find role by name
    role = next(
        (r for r in roles["data"] if r.get("name") == role_name),
        None
    )
    assert role is not None, f"Role '{role_name}' not found"

    role_id = role["id"]

    # Get role by ID
    response = api_client.get(f"/api/v1/role/{role_id}")
    assert response.status_code == 200, f"Failed to get role with id {role_id}: {response.text}"
    body = response.json()
    assert isinstance(body, dict)
    assert body["name"] == role_name