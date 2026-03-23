import pytest
from playwright.sync_api import Page, expect


# App is reachable
@pytest.mark.smoke
def test_app_is_reachable(login_page, config_fixture):
    login_page.navigate()
    login_page.verify_page_loaded()


#  Dashboard loads after login
@pytest.mark.smoke
def test_dashboard_loads_after_login(authenticated_page, config_fixture):
    # Validate user is logged in 
    from pages.login_page import LoginPage

    page = LoginPage(authenticated_page)
    page.verify_login_success()


# Basic UI check
@pytest.mark.smoke
def test_new_chat_button_visible(authenticated_page):
    from pages.login_page import LoginPage
    page = LoginPage(authenticated_page)
    page.verify_new_chat_btn_present()


# Navigate to Organization page
@pytest.mark.smoke
def test_navigate_to_organization(authenticated_page, organization_page):
    page = organization_page
    page.navigate_to_organizations()
    page.verify_organization_page_loaded()
    page.open_form()



#  Navigate to Users page
# @pytest.mark.smoke
# def test_navigate_to_users(authenticated_page, users_page):
#     page = users_page
#     page.navigate_to_users()
#     page.open_form()

#     # Update locator if needed
#     assert page.locator("text=Users").is_visible()


#  API health check
@pytest.mark.smoke
def test_agents_api_smoke(api_client):
    response = api_client.get("/api/v1/agents/all")
    assert response.status_code == 200