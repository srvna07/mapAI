import pytest
from utils.data_factory import DataFactory

@pytest.mark.smoke
def test_api_health_check(api_client):
    response = api_client.get("/api/v1/healthcheck")
    assert response.status_code == 200, f"Health check failed: {response.text}"


@pytest.mark.high
def test_api_health_check_status(api_client):
    response = api_client.get("/api/v1/healthcheck/check")
    assert response.status_code == 200, f"Health check status failed: {response.text}"

@pytest.mark.high
def test_api_get_agents(api_client):
    response = api_client.get("/api/v1/agents/all")
    assert response.status_code == 200, f"Failed to get all agents: {response.text}"
    body = response.json()
    assert "data" in body
    assert isinstance(body["data"], list)
    