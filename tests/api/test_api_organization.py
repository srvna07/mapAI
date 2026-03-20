import pytest
from utils.data_factory import DataFactory


@pytest.mark.high
def test_get_all_organizations(api_client):
    response = api_client.get("/api/v1/organization")
    assert response.status_code == 200, f"Failed to get all organizations: {response.text}"
    body = response.json()
    assert "data" in body
    assert isinstance(body["data"], list)
    return response.json()

@pytest.mark.high
def test_get_organization_by_org_id(api_client, new_organization_data):

    # Step 1: Create organization
    payload = DataFactory.organization(new_organization_data)

    create_res = api_client.post("/api/v1/organization", payload=payload)
    assert create_res.status_code == 201, f"Organization creation failed: {create_res.text}"
    print(f"Created organization with ID: {create_res.json()['id']}")

    body = create_res.json()
    org_id = body["id"]
    org_name = body["organizationName"]

    # Step 2: Get organization by org_id
    response = api_client.get(f"/api/v1/organization/{org_id}")
    assert response.status_code == 200, f"Failed to get organization with id {org_id}: {response.text}"


@pytest.mark.high
def test_get_organization_by_invalid_org_id(api_client, invalid_organization_data):

    invalid_org_id = invalid_organization_data["invalid_data"]["organization_id"]

    response = api_client.get(
        f"/api/v1/organization/{invalid_org_id}"
    )

    assert response.status_code == 404, f"Expected 404 Not Found for invalid org_id, got {response.status_code}{response.text}"

@pytest.mark.high
def test_delete_organization_by_org_id(api_client, new_organization_data):

    # Step 1: Create organization
    payload = DataFactory.organization(new_organization_data)

    create_res = api_client.post("/api/v1/organization", payload=payload)
    assert create_res.status_code == 201, f"Organization creation failed: {create_res.text}"
    print(f"Created organization with ID: {create_res.json()['id']}")

    org_id = create_res.json()["id"]

    # Step 2: Delete organization
    delete_res = api_client.delete(f"/api/v1/organization/{org_id}")
    assert delete_res.status_code == 200, f"Failed to delete organization with id {org_id}: {delete_res.text}"

    # Step 3: Verify Deletion
    verify_res = api_client.get(f"/api/v1/organization/{org_id}")
    assert verify_res.status_code == 404, f"Expected 404 Not Found after deletion, got {verify_res.status_code}"