import pytest
from pages.base_page import BasePage
from playwright.sync_api import expect

class PermissionPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        # Navigation
        self.menu = page.get_by_label("Directory")
        self.permissions_page_button = page.get_by_role("menuitem", name="Permissions")

        # Add Permission
        
        self.role_dropdown                   = page.get_by_role("combobox").first
        self.role_option_super_admin         = page.get_by_role("option", name="Super Admin")
        self.add_permission_button           = page.get_by_role("button", name="Add Module")
        self.permission_name_textbox         = page.get_by_role("textbox", name="Name")
        self.permission_description_textbox  = page.get_by_role("textbox", name="Description")
        self.save_button                     = page.get_by_role("button", name="Save")
        self.cancel_button                   = page.get_by_role("button", name="Cancel")
        self.search_bar                      = page.get_by_role("textbox", name="Search by Name")
        self.edit_permission_button          = page.get_by_role("button").nth(1)
        self.delete_permission_button        = page.get_by_role("button").nth(2)
        self.delete_permission_confirmation_button = page.get_by_role("button", name="Delete")
        self.success_message                 = page.get_by_text("Module Created Successfully")
        self.update_message                  = page.get_by_text("Module Updated Successfully")
        self.delete_message                  = page.get_by_text("Module Deleted Successfully")
        self.verify_search_data_not_available= page.get_by_text("No data found")

    def navigate_to_permissions_page(self):
        self.menu.click()
        self.permissions_page_button.click()

    def add_permission(self, permission_name, permission_description):
        self.role_dropdown.click()
        self.role_option_super_admin.click()
        self.add_permission_button.click()
        self.permission_name_textbox.fill(permission_name)
        self.permission_description_textbox.fill(permission_description)
        self.save_button.click()
        self.success_message.wait_for(state="visible")

    def edit_permission(self, old_permission_name, new_permission_name, new_permission_description):
        self.search_bar.fill(old_permission_name)
        row = self.page.locator("tr", has_text=old_permission_name).first
        row.wait_for(state="visible")
        row.locator("button").nth(0).click()  # Click edit button in the row

        self.permission_name_textbox.fill(new_permission_name)
        self.permission_description_textbox.fill(new_permission_description)
        self.save_button.click()
        self.update_message.wait_for(state="visible")

    def delete_permission(self, permission_name):
        self.search_bar.fill(permission_name)
        row = self.page.locator("tr", has_text=permission_name).first
        row.wait_for(state="visible")
        row.locator("button").nth(1).click()  # Click delete button in the row
        self.delete_permission_confirmation_button.click()
        self.delete_message.wait_for(state="visible")

    # Verification methods
    def verify_permission_in_table(self, permission_name):
        self.navigate_to_permissions_page()  # Ensure we are on the permissions page
        self.search_bar.fill(permission_name)
        expect(self.page.get_by_role("cell", name=permission_name)).to_be_visible()

    def verify_permission_not_in_table(self, permission_name):
        self.navigate_to_permissions_page()  # Ensure we are on the permissions page
        self.search_bar.fill(permission_name)
        expect(self.page.get_by_role("cell", name=permission_name)).not_to_be_visible()
        expect(self.verify_search_data_not_available).to_be_visible()