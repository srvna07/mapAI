import pytest

@pytest.mark.smoke
def test_navigate_to_permissions_page(authenticated_page, permission_page):
    page = permission_page
    page.navigate_to_permissions_page()

@pytest.mark.smoke
def test_add_permission(authenticated_page, permission_page, new_permission_data):
    page = permission_page
    page.navigate_to_permissions_page()
    page.add_permission(new_permission_data["permission"]["name"], new_permission_data["permission"]["Description"])
    page.verify_permission_in_table(new_permission_data["permission"]["name"])

@pytest.mark.smoke
def test_edit_permission(authenticated_page, permission_page, new_permission_data):
    page = permission_page
    page.navigate_to_permissions_page()
    page.edit_permission(new_permission_data["permission"]["name"], new_permission_data["edited_permission"]["name"], new_permission_data["edited_permission"]["Description"])
    page.verify_permission_in_table(new_permission_data["edited_permission"]["name"])

@pytest.mark.smoke
def test_delete_permission(authenticated_page, permission_page, new_permission_data):
    page = permission_page
    page.navigate_to_permissions_page()
    page.delete_permission(new_permission_data["edited_permission"]["name"])
    page.verify_permission_not_in_table(new_permission_data["edited_permission"]["name"])