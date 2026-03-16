import pytest
from playwright.sync_api import expect

# 001
@pytest.mark.smoke
def test_create_new_user(authenticated_page, users_page, users_test_data):
    data = users_test_data["users"]
    
    # Navigation
    users_page.navigate_to_users_page()
    users_page.click_add_user_button()
    
    # Form Filling (Values are now dynamic from the fixture)
    users_page.fill_first_name(data["first_name"])
    users_page.fill_last_name(data["last_name"])
    users_page.fill_email_textbox(data["email"])
    users_page.fill_phone_number(data["phone"])
    
    # Dropdowns (Still pulled from JSON)
    users_page.select_role(data["super_admin_role"])
    users_page.select_organization(data["organization"])
    users_page.select_agent(data["agent"])

    users_page.fill_password_textbox(data["password"])
    users_page.click_save_button()

# #002
# @pytest.mark.smoke
# def test_edit_created_user(authenticated_page, users_page, users_test_data):
#     data = users_test_data["edited_users"]
    
#     # Navigation
#     # users_page.navigate_to_users_page()
#     users_page.click_edit_button()
    
#     # Form Filling (Values are now dynamic from the fixture)
#     users_page.fill_first_name(data["first_name"])
#     users_page.fill_last_name(data["last_name"])
#     users_page.fill_email_textbox(data["email"])
#     users_page.fill_phone_number(data["phone"])
    
#     # Dropdowns (Still pulled from JSON)
#     users_page.select_role(data["role"])
#     users_page.select_organization(data["organization"])
#     users_page.select_agent(data["agent"])

#     users_page.fill_password_textbox(data["password"])
#     users_page.click_save_button()
# #011
# @pytest.mark.smoke
# def test_check_duplicate_user_creation(authenticated_page, users_page, users_test_data):
#     data = users_test_data["edited_users"]
    
#     # Navigation
#     # users_page.navigate_to_users_page()
#     users_page.click_edit_button()
    
#     # Form Filling (Values are now dynamic from the fixture)
#     users_page.fill_first_name(data["first_name"])
#     users_page.fill_last_name(data["last_name"])
#     users_page.fill_email_textbox(data["email"])
#     users_page.fill_phone_number(data["phone"])
    
#     # Dropdowns (Still pulled from JSON)
#     users_page.select_role(data["role"])
#     users_page.select_organization(data["organization"])
#     users_page.select_agent(data["agent"])

#     users_page.fill_password_textbox(data["password"])
#     users_page.click_save_button()

#     expect(users_page.pop_ups("User already Exisist"))

#     users_page.click_close_button()
    
#     expect(users_page.is_text_in_table_visible(data["email"]))

# #003
# # @pytest.mark.smoke
# # def test_edit_organization_for_the_created_user(authenticated_page, users_page, users_test_data):
