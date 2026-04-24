import pytest


@pytest.mark.smoke
def test_navigate_to_roles_page(authenticated_page, role_page):
    page = role_page
    page.navigate_to_roles_page()
    
@pytest.mark.smoke
def test_add_role(authenticated_page, role_page, new_role_data):
    page = role_page
    page.navigate_to_roles_page()
    page.add_role(new_role_data["role"]["name"])
    page.verify_role_in_table(new_role_data["role"]["name"])

@pytest.mark.smoke
def test_edit_role(authenticated_page, role_page, new_role_data):
    page = role_page
    page.navigate_to_roles_page()
    page.edit_role(new_role_data["role"]["name"], new_role_data["edited_role"]["name"])
    page.verify_role_in_table(new_role_data["edited_role"]["name"]) 


@pytest.mark.smoke
def test_delete_role(authenticated_page, role_page, new_role_data):
    page = role_page
    page.navigate_to_roles_page()
    page.delete_role(new_role_data["edited_role"]["name"])
    page.verify_role_not_in_table(new_role_data["edited_role"]["name"])
