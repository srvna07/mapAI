import pytest
from utils.data_factory import DataFactory


@pytest.mark.high
def test_get_all_users(api_client):
    response = api_client.get("/api/v1/users")
    assert response.status_code == 200, f"Failed to get all users: {response.text}"
    body = response.json()
    assert "data" in body
    assert isinstance(body["data"], list)
    return response.json()

@pytest.mark.high
@pytest.mark.skip(reason="BUG: GET user API returns 201 instead of 200")
def test_get_user_by_user_id(api_client, new_user_data):

    # Step 1: Create user
    payload = DataFactory.user(new_user_data)

    create_res = api_client.post("/api/v1/users", payload=payload)
    assert create_res.status_code == 201, f"User creation failed: {create_res.text}"

    user_id = create_res.json()["id"]

    # Step 2: Get user
    response = api_client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200, f"Failed to get user with id {user_id}: {response.text}"

@pytest.mark.high
@pytest.mark.skip(reason="BUG: API returns 500 instead of 404 for invalid user_id")
def test_get_user_by_invalid_user_id(api_client, user_test_data):
    invalid_user_id = user_test_data["invalid_data"]["user_id"]
    
    response = api_client.get(f"/api/v1/users/{invalid_user_id}")

    assert response.status_code == 404, f"Expected 404 Not Found for invalid user_id, got {response.status_code}"
    
@pytest.mark.high
@pytest.mark.skip(reason="BUG: Deleted user still retrievable (GET returns 400 instead of 404)")
def test_user_create_get_delete(api_client, new_user_data):

    # Step 1: Create User
    payload = DataFactory.user(new_user_data)

    create_res = api_client.post("/api/v1/users", payload=payload)
    assert create_res.status_code == 201, f"User creation failed: {create_res.text}"

    create_body = create_res.json()
    user_id = create_body["id"]


    # Step 2: Delete User
    delete_res = api_client.delete(f"/api/v1/users/{user_id}")
    assert delete_res.status_code == 200, f"Failed to delete user with id {user_id}: {delete_res.text}"

    # Step 3: Verify Deletion 
    verify_res = api_client.get(f"/api/v1/users/{user_id}")
    assert verify_res.status_code == 404, f"Expected 404 Not Found after deletion, got {verify_res.status_code}"
