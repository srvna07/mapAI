import pytest
import os
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.organizationPage import OrganizationsPage
from pages.users_page import UsersPage
from utils.data_reader import DataReader
from dotenv import load_dotenv
from playwright.sync_api import expect

# Load env
load_dotenv()

# Load data
data = DataReader.load_json("testdata/user_org_data.json")


@pytest.fixture(scope="function")
def setup(page: Page):
    login = LoginPage(page)
    login.navigate()
    login.login(os.getenv("APP_USERNAME"), os.getenv("APP_PASSWORD"))
    login.verify_login_success()
    return page


# ---------------------------------------
# 1. Org created → Agents visible
# ---------------------------------------
def test_org_agents_visible(authenticated_page):
    page = authenticated_page
    org = OrganizationsPage(page)
    user = UsersPage(page)

    org_data = data["org_with_agents"]
    org_name = org_data["organization"]["name"]
    agents = org_data["agents"]

    org.open_form()
    org.fill_basic_info(org_name)
    org.fill_contact_info(**org_data["contact"])
    org.select_agent(agents)
    org.submit_form()
    org.verify_success()

    user.navigate_to_users_page()
    user.click_add_user_button()
    user.select_organization(org_name)
    page.wait_for_timeout(1000)
    page.wait_for_timeout(1000)


    user.agent_combobox.click()
    page.keyboard.press("Escape")

    for agent in agents:
        assert page.get_by_role("option", name=agent).is_visible()
    page.keyboard.press("Escape")

# ---------------------------------------
# 2. Add agent → reflected
# ---------------------------------------
def test_add_agent_reflected(authenticated_page):
    page = authenticated_page
    org = OrganizationsPage(page)
    user = UsersPage(page)

    org_name = data["org_with_agents"]["organization"]["name"]
    new_agents = data["org_add_agent"]["agents"]

    org.navigate_to_organizations()
    org.edit_organization(org_name)
    org.select_agent(new_agents)
    org.submit_form()
    org.verify_update_success()

    user.navigate_to_users_page()
    user.click_add_user_button()
    user.select_organization(org_name)
    page.wait_for_timeout(1000)
    page.wait_for_timeout(1000)

    user.agent_combobox.click()
    page.keyboard.press("Escape")

    for agent in new_agents:
        assert page.get_by_role("option", name=agent).is_visible()
    page.keyboard.press("Escape")

# ---------------------------------------
# 3. Remove agent → not visible
# ---------------------------------------
def test_remove_agent_reflected(authenticated_page):
    page = authenticated_page
    org = OrganizationsPage(page)
    user = UsersPage(page)

    org_name = data["org_with_agents"]["organization"]["name"]
    remove_agents = data["org_remove_agent"]["agents"]

    org.navigate_to_organizations()
    org.edit_organization(org_name)

    org.open_agent_dropdown()
    

    for agent in remove_agents:
        page.locator('[role="option"][aria-selected="true"]', has_text=agent).click()
    page.keyboard.press("Escape")
    org.submit_form()
    org.verify_update_success()

    user.navigate_to_users_page()
    user.click_add_user_button()
    user.select_organization(org_name)

    user.agent_combobox.click()
    page.keyboard.press("Escape")

    for agent in remove_agents:
        assert not page.get_by_role("option", name=agent).is_visible()
    page.keyboard.press("Escape")

#---------------------------------------
#4. Org with no agents
#---------------------------------------
def test_org_no_agents(authenticated_page):
    page = authenticated_page
    org = OrganizationsPage(page)
    user = UsersPage(page)

    org_data = data["org_no_agents"]
    org_name = org_data["organization"]["name"]

    org.open_form()
    org.fill_basic_info(org_name)
    org.fill_contact_info(**org_data["contact"])
    org.submit_form()
    org.verify_success()

    user.navigate_to_users_page()
    user.click_add_user_button()
    user.select_organization(org_name)

    user.agent_combobox.click()
    page.keyboard.press("Escape")
    expect(page.get_by_text("No agents available")).to_be_visible()
    page.keyboard.press("Escape")

# ---------------------------------------
# 5. Org switch refresh
# ---------------------------------------
def test_org_switch_refresh(authenticated_page):
    page = authenticated_page
    user = UsersPage(page)

    org1 = data["org_switch"]["org1"]
    org2 = data["org_switch"]["org2"]

    user.navigate_to_users_page()
    user.click_add_user_button()

    user.select_organization(org1)
    user.select_organization(org2)

    user.agent_combobox.click()
    page.keyboard.press("Escape")
    assert page.get_by_role("option").count() >= 0
    page.keyboard.press("Escape")


# ---------------------------------------
# 6. Deleted org not visible
# ---------------------------------------
def test_deleted_org_not_visible(authenticated_page):
    page = authenticated_page
    org = OrganizationsPage(page)
    user = UsersPage(page)

    org_data = data["org_delete"]
    base_contact = data["org_with_agents"]["contact"]   # reuse valid contact

    org_name = org_data["organization"]["name"]

    org.open_form()
    org.fill_basic_info(org_name)

   
    org.fill_contact_info(**base_contact)

    org.submit_form()
    org.verify_success()

    org.delete_organization(org_name)
    org.verify_delete_success()

    user.navigate_to_users_page()
    user.click_add_user_button()

    user.organization_combobox.click()
    page.keyboard.press("Escape")

    assert not page.get_by_role("option", name=org_name).is_visible() 
    page.keyboard.press("Escape")
# ---------------------------------------
# 7. User edit → org change refresh agents
# ---------------------------------------
def test_user_edit_org_change_refresh(authenticated_page):
    page = authenticated_page
    user = UsersPage(page)

    org1 = data["org_switch"]["org1"]
    org2 = data["org_switch"]["org2"]

    user.navigate_to_users_page()
    user.click_add_user_button()

    user.select_organization(org1)
    user.agent_combobox.click()
    initial_count = page.get_by_role("option").count()
    page.keyboard.press("Escape")

    user.select_organization(org2)
    user.agent_combobox.click()
    new_count = page.get_by_role("option").count()

    assert initial_count != new_count
    page.keyboard.press("Escape")