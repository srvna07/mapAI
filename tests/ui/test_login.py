import pytest
from playwright.sync_api import expect


@pytest.fixture
def login_page_ready(login_page, config_fixture):
    login_page.navigate(config_fixture["base_url"])
    login_page.verify_page_loaded()
    return login_page


@pytest.mark.medium
def test_login_page_loads(login_page_ready):
    pass


@pytest.mark.low
def test_password_field_is_masked(login_page_ready):
    expect(login_page_ready.password_input).to_have_attribute("type", "password")


@pytest.mark.high
def test_valid_login_redirects_to_dashboard(login_page_ready, credentials, config_fixture):
    login_page_ready.login(credentials["username"], credentials["password"])
    expect(login_page_ready.page).to_have_url(
        f"{config_fixture['base_url']}/dashboard", timeout=15_000
    )
