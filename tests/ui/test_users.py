import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_create_new_user(authenticated_page, users_page, test_data):
    data = test_data["users"]
    
    # Navigation
    users_page.navigate_to_users_page()
    users_page.click_add_user_button()
    
    # Form Filling (Values are now dynamic from the fixture)
    users_page.fill_first_name(data["first_name"])
    users_page.fill_last_name(data["last_name"])
    users_page.fill_email_textbox(data["email"])
    users_page.fill_phone_number(data["phone"])
    
    # Dropdowns (Still pulled from JSON)
    users_page.select_role(data["role"])
    users_page.select_organization(data["organization"])
    users_page.select_agent(data["agent"])

    users_page.fill_password_textbox(data["password"])
    users_page.click_save_button()

@pytest.mark.smoke
def test_edit_created_user(authenticated_page, users_page, test_data):
    data = test_data["edited_users"]
    
    # Navigation
    # users_page.navigate_to_users_page()
    users_page.click_edit_button()
    
    # Form Filling (Values are now dynamic from the fixture)
    users_page.fill_first_name(data["first_name"])
    users_page.fill_last_name(data["last_name"])
    users_page.fill_email_textbox(data["email"])
    users_page.fill_phone_number(data["phone"])
    
    # Dropdowns (Still pulled from JSON)
    users_page.select_role(data["role"])
    users_page.select_organization(data["organization"])
    users_page.select_agent(test_data["agent"])

    users_page.fill_password_textbox(data["password"])
    users_page.click_save_button()

@pytest.mark.smoke
def test_edit_organization_for_the_created_user(authenticated_page, users_page, test_data)