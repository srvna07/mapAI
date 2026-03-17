import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_create_a_organization_to_users_testing(authenticated_page, organization_page, users_test_data):
    data = users_test_data["organization"]
    agents = users_test_data["agent"]

    # Navigation
    organization_page.open_form()

    # Form Filling
    organization_page.fill_basic_info(data["name"])
    organization_page.fill_contact_info(
        data["address1"], 
        data["address2"], 
        data["country"], 
        data["city"], 
        data["state"], 
        data["zip_code"]
    )
    
    # Selecting agents
    organization_page.select_agent(agents)

    # Save
    organization_page.submit_form()
    organization_page.verify_success()

@pytest.mark.smoke
def test_create_another_organization_to_users_testing(authenticated_page, organization_page, users_test_data):
    data = users_test_data["another_organization"]
    agents = users_test_data["agent"]

    # Navigation
    organization_page.open_form()

    # Form Filling
    organization_page.fill_basic_info(data["name"])

    # Pass the data as strings by removing the extra brackets []
    organization_page.fill_contact_info(
        data["address1"], 
        data["address2"], 
        data["country"], 
        data["city"], 
        data["state"], 
        data["zip_code"]
    )
    
    # Selecting agents
    organization_page.select_agent(agents)

    # Save
    organization_page.submit_form()
    organization_page.verify_success()


# 1
@pytest.mark.smoke
def test_create_new_user(authenticated_page, users_page, users_test_data):
    data = users_test_data["users"]
    org_name = users_test_data["organization"]["name"]
    agents = users_test_data["agent"]
    
    users_page.navigate_to_users_page()
    users_page.click_add_user_button()
    
    users_page.fill_first_name(data["first_name"])
    users_page.fill_last_name(data["last_name"])
    users_page.fill_email_textbox(data["email"])
    users_page.fill_phone_number(data["phone"])
    
    users_page.select_role(data["admin_role"])
    users_page.select_organization(org_name)
    users_page.select_agent(agents[0])

    users_page.fill_password_textbox(data["password"])
    users_page.click_save_button()

#2
@pytest.mark.smoke
def test_edit_created_user(authenticated_page, users_page, users_test_data):
    data = users_test_data["edited_users"]
    created_email = users_test_data["users"]["email"]
    
    users_page.navigate_to_users_page()
    users_page.search_user(created_email)
    users_page.click_edit_button()
    
    users_page.fill_first_name(data["first_name"])
    users_page.fill_last_name(data["last_name"])
    users_page.fill_email_textbox(data["email"])
    users_page.fill_phone_number(data["phone"])
    
    users_page.select_organization(data["organization"])
    users_page.select_agent(users_test_data["agent"][1])

    users_page.fill_password_textbox(data["password"])
    users_page.click_save_button()

# 3
# @pytest.mark.smoke
# def test_edit_organization_for_the_created_user(authenticated_page, users_page, users_test_data):
#     org_data = users_test_data["organization"]
#     edit_org_data = users_test_data["edited_organization"]

#     users_page.navigate_to_users_page()
#     users_page.search_user(edit) 

# 4
@pytest.mark.smoke
def test_delete_user(authenticated_page, users_page, users_test_data):
    data = users_test_data["edited_user"]["name"]

    users_page.search_user(data)
    users_page.click_delete_button()
    users_page.click_delete_button()
    users_page.verify_table_is_empty()

#5
@pytest.mark.smoke
def test_check_duplicate_user_creation(authenticated_page, users_page, users_test_data):
    data = users_test_data["edited_users"]
    
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
    users_page.select_agent(data["agent"])

    users_page.fill_password_textbox(data["password"])
    users_page.click_save_button()

    expect(users_page.pop_ups("User already Exist"))

    users_page.click_close_button()
    
    expect(users_page.is_text_in_table_visible(data["email"]))