import pytest
from playwright.sync_api import expect

from pages.organizationPage import OrganizationsPage
from pages.users_page import UsersPage
from utils.test_data_loader import TestDataLoader


# ---------------------------------------
# 1. Org created → Agents visible
# ---------------------------------------
def test_org_agents_visible(authenticated_page, org_with_agents):
    user = UsersPage(authenticated_page)

    user.navigate_to_users_page()
    user.click_add_user_button()
    user.select_organization(org_with_agents["name"])

    user.open_agent_dropdown()
    user.verify_agents_visible(org_with_agents["agents"])
    user.close_dropdown()


# ---------------------------------------
# 2. Add agent → reflected
# ---------------------------------------
def test_add_agent_reflected(authenticated_page, test_data):
    page = authenticated_page
    org = OrganizationsPage(page)
    user = UsersPage(page)

    base_org = test_data["org_with_agents"]
    org_data = TestDataLoader.build_organization(base_org["contact"])
    new_agents = test_data["org_add_agent"]["agents"]

    # Create org
    org.open_form()
    org.fill_basic_info(org_data["name"])
    org.fill_contact_info(**org_data["contact"])
    org.select_agent(base_org["agents"])
    org.submit_form()
    org.verify_success()

    # Edit org
    org.navigate_to_organizations()
    org.edit_organization(org_data["name"])
    org.select_agent(new_agents)
    org.submit_form()
    org.verify_update_success()

    user.navigate_to_users_page()
    user.click_add_user_button()
    user.select_organization(org_data["name"])

    user.open_agent_dropdown()
    user.verify_agents_visible(new_agents)
    user.close_dropdown()


# ---------------------------------------
# 3. Remove agent → not visible
# ---------------------------------------
def test_remove_agent_reflected(authenticated_page, test_data):
    page = authenticated_page
    org = OrganizationsPage(page)
    user = UsersPage(page)

    base_org = test_data["org_with_agents"]
    org_data = TestDataLoader.build_organization(base_org["contact"])
    remove_agents = test_data["org_remove_agent"]["agents"]

    # Create org
    org.open_form()
    org.fill_basic_info(org_data["name"])
    org.fill_contact_info(**org_data["contact"])
    org.select_agent(base_org["agents"])
    org.submit_form()
    org.verify_success()

    # Remove agents
    org.navigate_to_organizations()
    org.edit_organization(org_data["name"])
    org.unselect_agents(remove_agents)
    org.submit_form()
    org.verify_update_success()

    user.navigate_to_users_page()
    user.click_add_user_button()
    user.select_organization(org_data["name"])

    user.open_agent_dropdown()
    user.verify_agents_not_visible(remove_agents)
    user.close_dropdown()


# ---------------------------------------
# 4. Org with no agents
# ---------------------------------------
def test_org_no_agents(authenticated_page, org_without_agents):
    user = UsersPage(authenticated_page)

    user.navigate_to_users_page()
    user.click_add_user_button()
    user.select_organization(org_without_agents["name"])

    user.open_agent_dropdown()
    user.verify_no_agents_message()
    user.close_dropdown()


# ---------------------------------------
# 5. Org switch refresh
# ---------------------------------------
def test_org_switch_refresh(authenticated_page, org_with_agents, org_without_agents):
    user = UsersPage(authenticated_page)

    user.navigate_to_users_page()
    user.click_add_user_button()

    agents1 = user.get_agents_for_organization(org_with_agents["name"])
    agents2 = user.get_agents_for_organization(org_without_agents["name"])

    assert agents1 != agents2


# ---------------------------------------
# 6. Deleted org not visible
# ---------------------------------------
def test_deleted_org_not_visible(authenticated_page, test_data):
    page = authenticated_page
    org = OrganizationsPage(page)
    user = UsersPage(page)

    org_data = TestDataLoader.build_organization(test_data["org_delete"]["contact"])

    org.open_form()
    org.fill_basic_info(org_data["name"])
    org.fill_contact_info(**org_data["contact"])
    org.submit_form()
    org.verify_success()

    org.delete_organization(org_data["name"])
    org.verify_delete_success()

    user.navigate_to_users_page()
    user.click_add_user_button()

    user.open_organization_dropdown()
    user.verify_organization_not_present(org_data["name"])
    user.close_dropdown()


# ---------------------------------------
# 7. User creation
# ---------------------------------------
def test_user_created_with_agent(authenticated_page, org_with_agents, test_data):
    user = UsersPage(authenticated_page)

    base_user = test_data["user_data"]
    user_data = TestDataLoader.build_user(base_user)

    user.navigate_to_users_page()
    user.click_add_user_button()

    user.fill_first_name(user_data["first_name"])
    user.fill_last_name(user_data["last_name"])
    user.fill_email_textbox(user_data["email"])
    user.fill_phone_number(user_data["phone"])
    user.select_role(user_data["role"])
    user.select_organization(org_with_agents["name"])
    user.select_agent(org_with_agents["agents"][0])
    user.fill_password_textbox(user_data["password"])

    user.click_save_button()

    user.verify_search_item_in_table(user_data["email"])


# ---------------------------------------
# 8. Agent disabled without org
# ---------------------------------------
def test_agent_disabled_without_org(authenticated_page):
    user = UsersPage(authenticated_page)

    user.navigate_to_users_page()
    user.click_add_user_button()

    expect(user.agent_combobox).not_to_be_enabled()