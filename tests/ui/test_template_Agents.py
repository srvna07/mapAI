import pytest

@pytest.mark.smoke
def test_navigate_to_agents_page(authenticated_page, agent_page):
    page = agent_page
    page.navigate_to_agents_page()

@pytest.mark.smoke
def test_add_template_agent(authenticated_page, agent_page, new_template_agent_data):
    page = agent_page
    page.navigate_to_agents_page()
    page.add_template_agent(new_template_agent_data["template_agent"]["name"], new_template_agent_data["template_agent"]["instructions"])
    page.verify_template_agent_in_table(new_template_agent_data["template_agent"]["name"])

@pytest.mark.smoke
def test_edit_template_agent(authenticated_page, agent_page, new_template_agent_data):
    page = agent_page
    page.navigate_to_agents_page()
    page.edit_template_agent(new_template_agent_data["template_agent"]["name"], new_template_agent_data["edited_template_agent"]["name"], new_template_agent_data["edited_template_agent"]["instructions"])
    page.verify_template_agent_in_table(new_template_agent_data["edited_template_agent"]["name"])

@pytest.mark.smoke
def test_check_created_agent_in_organization(authenticated_page, organization_page, agent_page, new_template_agent_data, new_organization_data):
    org_page = organization_page
    agent_pg = agent_page
    
    org_page    = organization_page
    org_page.navigate_to_organizations()
    org     = new_organization_data["organization"]
    contact = new_organization_data["contact"]

    org_page.open_form()
    org_page.fill_basic_info(org["name"])
    org_page.fill_contact_info(**contact)
        

    org_page.submit_form()

    org_page.verify_success()
    org_page.verify_Select_Agents_to_Configure_visible()
    org_page.verify_agents_in_organizationlist(new_template_agent_data["edited_template_agent"]["name"])

def test_check_agent_in_chat_page(authenticated_page, agent_page, new_template_agent_data, new_chat_page,new_organization_data):
    page = agent_page
    page.navigate_to_agents_page()
    chat_page= new_chat_page
    org_name = new_organization_data["organization"]["name"]
    combined_agent = f"{org_name}-{new_template_agent_data['edited_template_agent']['name']}"

    chat_page.verify_agent_in_chat(combined_agent)

@pytest.mark.smoke
def test_delete_template_agent(authenticated_page, agent_page, new_template_agent_data):
    page = agent_page
    page.navigate_to_agents_page()
    page.delete_template_agent(new_template_agent_data["edited_template_agent"]["name"])
    page.verify_template_agent_not_in_table(new_template_agent_data["edited_template_agent"]["name"])