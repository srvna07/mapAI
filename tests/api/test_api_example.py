import pytest


@pytest.mark.smoke
def test_api_health_check(api_client):
    response = api_client.get("/health")
    assert response.status_code == 200


@pytest.mark.high
def test_api_requires_auth(api_client):
    response = api_client.get("/protected-endpoint")
    assert response.status_code == 401
