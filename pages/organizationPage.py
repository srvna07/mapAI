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
        self.next_btn                 = page.get_by_role("button", name="Next")
        self.search_input             = page.get_by_role("textbox", name="Search")
        self.agents_to_configure_tittle = page.get_by_text("Select Agents to Configure")
        self.update_agent_tittle         = page.get_by_text("Update Agent")

        self.organization_name        = page.get_by_role("textbox", name="Organization Name")
        self.address_1                = page.get_by_role("textbox", name="Address Line 1")
        self.address_2                = page.get_by_role("textbox", name="Address Line 2")
        self.city                     = page.get_by_role("textbox", name="City")
        self.state                    = page.get_by_role("textbox", name="State")
        self.country                  = page.get_by_role("textbox", name="Country")
        self.zip_code                 = page.get_by_role("textbox", name="Zip Code")
        self.agent_dropdown           = page.locator("label:has-text('Agent')").locator("..").locator("[role='combobox']")

        self.upload_button            = page.get_by_role("button", name="UPLOAD PROFILE PICTURE")
        
        self.success_message          = page.get_by_text("Organization Created Successfully")
        self.update_success_message   = page.get_by_text("Organization updated successfully")
        self.delete_success_message   = page.get_by_text("Organization deleted successfully")
        self.rejected_error_message   = page.get_by_text("Rejected")
        self.agents_success_message   = page.get_by_text("Agents Updated Successfully")
        self.model_dropdown           = page.locator("label:has-text('Model *') >> xpath=.. >> [role='combobox']")
        self.instructions_field       = page.get_by_label("Instructions *")
        self.tools_section            = page.get_by_text("TOOLS")

        self.code_interpreter_checkbox = page.get_by_label("code_interpreter")
        self.total_agents              = 0
        self.review_title              = page.get_by_text("Review & Save")
        self.success_icon_text         = page.get_by_text("All agents configured")
        self.ready_status              = page.get_by_text("Ready")
        self.choose_agent              = page.get_by_text("Choose Agent")



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
        self.total_agents = len(agent_name)
        expect(self.agents_to_configure_tittle).to_be_visible()
        for agent in agent_name:
           
            agent_locator = self.page.get_by_role("button", name=agent, exact=True)

            expect(agent_locator).to_be_visible()
            agent_locator.click()
        self.next_btn.click()

    
    def select_model(self, models: list[str], instructions_list: list[str]):

        agent_step = self.page.locator("text=/Agent \\d+ of \\d+/")

        for i in range(self.total_agents):

            # Validate step indicator
            expect(agent_step).to_contain_text(f"Agent {i+1} of {self.total_agents}")

            # Validate modal
            expect(self.update_agent_tittle).to_be_visible()

            # Select model
            self.model_dropdown.click()
            self.page.get_by_role("option", name=models[i], exact=True).click()

            # Fill instructions
            self.instructions_field.fill(instructions_list[i])

            # Validate tools
            expect(self.tools_section).to_be_visible()
            expect(self.code_interpreter_checkbox).to_be_visible()

            # Next step
            self.next_btn.click()
        
    def review_and_save_agents(self, agent_names: list[str], models: list[str]):
        # --- Scope to Review Modal ---
        review_modal = self.page.get_by_role("dialog")
        # --- Validate Review Popup ---
        expect(self.review_title).to_be_visible()
        expect(self.success_icon_text).to_be_visible()

        # --- Get all agent rows (each row has Ready status) ---
        rows = review_modal.locator("div:has-text('Ready')")

        for i in range(len(agent_names)):
            row = rows.nth(i)

            # Validate agent name (scoped → no duplicate issue)
            expect(row).to_contain_text(agent_names[i])

            # Validate model (no substring issue)
            expect(row).to_contain_text(models[i])

            # Validate status
            expect(row).to_contain_text("Ready")

        # --- Click Save ---
        self.save_btn.click()

        # --- Validate Success Message ---
        expect(self.agents_success_message).to_be_visible()
                
            
    def open_agent_dropdown(self):
        self.agent_dropdown.click()

    def submit_form(self):
        self.save_btn.click()

    def search_organization(self, org_name):
        self.search_input.click()
        self.search_input.fill(str(org_name))

    def edit_organization(self, org_name: str):
        self.search_organization(org_name)
        row = self.page.locator("tr", has_text=org_name).first
        row.wait_for(state="visible")
        row.locator("button").nth(0).click()  # Click edit button in the row
    
    def edit_agents(self, org_name: str):
        self.search_organization(org_name)
        row = self.page.locator("tr", has_text=org_name).first
        row.wait_for(state="visible")
        row.locator("button").nth(0).click()  # Click edit button in the row
        self.page.get_by_role("button", name="Edit Agents").click()

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

    def verify_agents_update_success(self):
        expect(self.agents_success_message).to_be_visible(timeout=10000)

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

    
    def verify_agents(self, org_name, agent_names):

        # Search and open organization
        self.search_organization(org_name)

        row = self.page.locator("tr", has_text=org_name).first

        #  Click the agent chip inside that row
        agent_chip = row.locator("div[role='button']", has_text=agent_names[0]).first
        expect(agent_chip).to_be_visible()
        agent_chip.click()

        # Validate popup
        expect(self.agents_to_configure_tittle).to_be_visible()

        for agent in agent_names:
            agent_locator = self.page.get_by_role("button", name=agent, exact=True)

            # Verify agent visible
            expect(agent_locator).to_be_visible()

            # Verify checkbox selected
            checkbox = agent_locator.locator("input[type='checkbox']")

            if checkbox.count() > 0:
                expect(checkbox).to_be_checked()
            else:
                # fallback (MUI)
                expect(agent_locator).to_have_attribute("aria-checked", "true")
        self.next_btn.click()

        

    def verify_models(self, models):

        # Validate Update Agent modal
        expect(self.update_agent_tittle).to_be_visible()

        agent_step = self.page.locator("text=/Agent \\d+ of \\d+/")

        for i in range(len(models)):

            # Validate step
            expect(agent_step).to_contain_text(f"Agent {i+1} of {len(models)}")

            # Validate selected model is visible
            model_locator = self.page.get_by_text(models[i], exact=True)
            expect(model_locator).to_be_visible()

            # Go to next agent
            self.next_btn.click()
        
    def verify_organization_page_loaded(self):
        expect(self.page.get_by_text("Organizations", exact=True)).to_be_visible()

    def verify_Select_Agents_to_Configure_visible(self):
        expect(self.agents_to_configure_tittle).to_be_visible()
    
    def verify_agents_in_list(self, agent_names):     
        self.total_agents = len(agent_names)
        expect(self.agents_to_configure_tittle).to_be_visible()
        for agent in agent_names:
           
            agent_locator = self.page.get_by_role("button", name=agent, exact=True)

            expect(agent_locator).to_be_visible()