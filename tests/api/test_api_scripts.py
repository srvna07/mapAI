import pytest
from utils.payload_builder import PayloadBuilder

@pytest.mark.smoke
def test_api_health_check(api_client):
    response = api_client.get("/api/v1/healthcheck")
    assert response.status_code == 200


@pytest.mark.high
def test_api_health_check_status(api_client):
    response = api_client.get("/api/v1/healthcheck/check")
    assert response.status_code == 200

@pytest.mark.high
def test_api_get_agents(api_client):
    response = api_client.get("/api/v1/agents/all")
    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert isinstance(body["data"], list)
    

@pytest.mark.high
def get_all_organizations(api_client):
    response = api_client.get("/api/v1/organization")
    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert isinstance(body["data"], list)
    return response.json()

@pytest.mark.high
def test_get_agent_organization_by_org_id(api_client):
    orgs = get_all_organizations(api_client)

    # Find org by name
    organization = next(
        (org for org in orgs["data"] if org["organizationName"] == "Signa Tech"),
        None
    )
    assert organization is not None, "Organization 'Signa Tech' not found"

    org_id = organization["id"]

    response = api_client.get(f"/api/v1/agents/organization/{org_id}")
    assert response.status_code == 200

@pytest.mark.high
def test_get_agent_organization_by_invalid_org_id(api_client):
    invalid_org_id = "12345678-90ab-cdef"  # Assuming this org ID does not exist

    response = api_client.get(f"/api/v1/agents/organization/{invalid_org_id}")
    assert response.status_code == 500

@pytest.mark.high
def test_delete_organization_by_org_id(api_client, new_organization_data):

    # Step 1: Create organization
    payload = PayloadBuilder.organization(new_organization_data)

    create_res = api_client.post("/api/v1/organization", payload=payload)
    assert create_res.status_code == 201

    org_id = create_res.json()["id"]

    # Step 2: Delete organization
    delete_res = api_client.delete(f"/api/v1/organization/{org_id}")
    assert delete_res.status_code == 200

@pytest.mark.high
def get_all_users(api_client):
    response = api_client.get("/api/v1/users")
    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert isinstance(body["data"], list)
    return response.json()

@pytest.mark.high
def test_get_user_by_user_id(api_client):
    users = get_all_users(api_client)

    # Find user by email
    user = next(
        (u for u in users["data"] if u.get("email") == "map_sa@signatech.com"),
        None
    )
    assert user is not None, "User with email 'map_sa@signatech.com' not found"
    user_id = user["id"]

    response = api_client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 201
    assert isinstance(response.json(), dict)
    
#//unskip after adding user testdata///////////

# @pytest.mark.high
# def test_delete_user_by_id(api_client, user_test_data):

#     #  Step 1: Create user
#     payload = PayloadBuilder.user(
#         user_test_data,
#         role_id="38ea421b-abde-4ac0-becc-330fe8eb240f",
#         organization_id="61d5bc20-88ff-4a40-bd71-1d6bffad7571"
#     )

#     create_res = api_client.post("/api/v1/auth/sign-up", payload=payload)
#     assert create_res.status_code == 200

#     #  Step 2: Get user list → find created user
#     users_res = api_client.get("/api/v1/users")
#     users = users_res.json()["data"]

#     user_id = next(
#         u["id"] for u in users if u["email"] == payload["email"]
#     )

#     #  Step 3: Delete user
#     delete_res = api_client.delete(f"/api/v1/users/{user_id}")
#     assert delete_res.status_code == 200

@pytest.mark.high
def get_all_roles(api_client):
    response = api_client.get("/api/v1/role")
    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert isinstance(body["data"], list)
    return response.json()

@pytest.mark.high
def test_get_role_by_role_id(api_client):
    roles = get_all_roles(api_client)

    # Find role by name
    role = next(
        (r for r in roles["data"] if r.get("name") == "Super Admin"),
        None
    )
    assert role is not None, "Role 'Super Admin' not found"
    role_id = role["id"]

    response = api_client.get(f"/api/v1/role/{role_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
