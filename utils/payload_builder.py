import pytest

class PayloadBuilder:

    @staticmethod
    def organization(data, agent_ids=None):
        return {
            "organizationName": data["organization"]["name"],
            "org_logo": "string",
            "addressline_1": data["contact"]["address1"],
            "addressline_2": data["contact"]["address2"],
            "state": data["contact"]["state"],
            "city": data["contact"]["city"],
            "country": data["contact"]["country"],
            "zipcode": data["contact"]["zip_code"],
            "agent_id": agent_ids or []
        }

    @staticmethod
    def user(data, role_id, organization_id):
        return {
            "email": data["email"],
            "firstName": data["firstName"],
            "lastName": data["lastName"],
            "phoneNumber": data["phoneNumber"],
            "profile_pic": data.get("profile_pic", "string"),
            "isActive": True,
            "roleId": role_id,
            "ai_token_limit": data.get("ai_token_limit", 0),
            "branchId": data.get("branchId", ""),
            "organizationId": organization_id
        }