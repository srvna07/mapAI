from playwright.sync_api import Page, expect
from .base_page import BasePage
from time import sleep


class OrganizationsPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.settings_icon            = page.get_by_label("Directory")
        self.organization_btn         = page.get_by_role("menuitem", name="Organization")
        self.new_organization_btn     = page.get_by_role("button", name="Add Organization")
        self.save_btn                 = page.get_by_role("button", name="Save")
        self.cancel_btn               = page.get_by_role("button", name="Cancel")
        self.delete_btn               = page.get_by_role("button", name="Delete")
        self.edit_btn                 = page.get_by_role("button", name="Edit")
        self.search_input             = page.get_by_role("textbox", name="Search")

        self.organization_name        = page.get_by_role("textbox", name="Organization Name")
        self.address_1                = page.get_by_role("textbox", name="Address Line 1")
        self.address_2                = page.get_by_role("textbox", name="Address Line 2")
        self.city                     = page.get_by_role("textbox", name="City")
        self.state                    = page.get_by_role("textbox", name="State")
        self.country                  = page.get_by_role("textbox", name="Country")
        self.zip_code                 = page.get_by_role("textbox", name="Zip Code")
        self.agent_dropdown           = page.locator("label:has-text('Agent')").locator("..").locator("[role='combobox']")

        self.upload_button            = page.get_by_role("button", name="UPLOAD PROFILE PICTURE")
        
        self.success_message          = page.get_by_text("Organization created successfully")
        self.update_success_message   = page.get_by_text("Organization updated successfully")
        self.delete_success_message   = page.get_by_text("Organization deleted successfully")
        self.rejected_error_message   = page.get_by_text("Rejected")

    def open_form(self):
        self.settings_icon.click()
        self.organization_btn.click()
        self.new_organization_btn.click()

    def navigate_to_organizations(self):
        self.settings_icon.click()
        self.organization_btn.click()

    def fill_basic_info(self, org_name: str):
        self.organization_name.fill(org_name)
        
    def fill_contact_info(self,  address1: str, address2: str,
                          city: str, state: str, country: str, zip_code: str):
        
        self.address_1.fill(address1)
        self.address_2.fill(address2)
        self.city.fill(city)
        self.state.fill(state)
        self.country.fill(country)
        self.zip_code.fill(zip_code)
        
    def select_agent(self, agent_name: str):
        self.agent_dropdown.click()
        for agent in agent_name:
            self.page.get_by_role("option", name=agent,exact=True).click()
        self.agent_dropdown.press("Escape")  # Close dropdown after selection
    def open_agent_dropdown(self):
        self.agent_dropdown.click()

    def submit_form(self):
        self.save_btn.click()

    def search_organization(self, org_name: str):
        self.search_input.click()
        self.search_input.fill(org_name)

    def edit_organization(self, org_name: str):
        self.search_organization(org_name)
        row = self.page.locator("tr", has_text=org_name).first
        row.wait_for(state="visible")
        row.locator("button").nth(0).click()  # Click edit button in the row

    def delete_organization(self, org_name: str):
        self.search_organization(org_name)
        row = self.page.locator("tr", has_text=org_name).first
        row.wait_for(state="visible")
        # Click delete icon in row
        row.locator("button").nth(1).click()

        self.delete_btn.click()
        

    def _clear_field(self, field):
        if field.input_value():
            field.clear()

    def update_organization(self, update_data: dict):
        contact = update_data["contact"]

        
        self._clear_field(self.address_1)
        self.address_1.fill(contact["address1"])
        self._clear_field(self.address_2)
        self.address_2.fill(contact["address2"])
        self._clear_field(self.city)
        self.city.fill(contact["city"])
        self._clear_field(self.state)
        self.state.fill(contact["state"])
        self._clear_field(self.country)
        self.country.fill(contact["country"])
        self._clear_field(self.zip_code)
        self.zip_code.fill(contact["zip_code"])

    def verify_success(self):
        expect(self.success_message).to_be_visible(timeout=10000)

    def verify_update_success(self):
        expect(self.update_success_message).to_be_visible(timeout=10000)

    def verify_delete_success(self):
        expect(self.delete_success_message).to_be_visible(timeout=10000)

    def verify_duplicate_error(self):
        expect(self.rejected_error_message).to_be_visible()

    def verify_organization_in_table(self, org_name: str):
        self.search_organization(org_name)
        expect(self.page.get_by_text(org_name).first).to_be_visible()

    def verify_organization_not_in_table(self, org_name: str):
        self.search_organization(org_name)
        expect(self.page.get_by_role("cell", name=org_name).first).not_to_be_visible()

    
    def verify_agents(self, agent_names):
        self.open_agent_dropdown()
        for agent in agent_names:
            expect(
                self.page.get_by_role("option", name=agent, exact=True)).to_be_visible()

    def verify_organization_in_table(self, org_name: str):
        self.search_organization(org_name)
        expect(self.page.get_by_text(org_name).first).to_be_visible()
