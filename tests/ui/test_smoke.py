import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
def test_app_is_reachable(login_page, config_fixture):
    login_page.navigate(config_fixture["base_url"])
    login_page.verify_page_loaded()


@pytest.mark.smoke
def test_dashboard_loads_after_login(authenticated_page: Page, config_fixture):
    expect(authenticated_page).to_have_url(
        f"{config_fixture['base_url']}/dashboard", timeout=10_000
    )
