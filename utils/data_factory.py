import random
import string
from datetime import datetime
import uuid
import requests
import os


class DataFactory:

    @staticmethod
    def random_string(length: int = 4) -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def random_username(prefix: str = "test_user_") -> str:
        return prefix + DataFactory.random_string()

    @staticmethod
    def random_email(prefix: str = "test_user_", domain: str = "@gmail.com") -> str:
        return prefix + DataFactory.random_string() + domain

    @staticmethod
    def random_name(prefix: str = "test_") -> str:
        return prefix + DataFactory.random_string()

    @staticmethod
    def timestamped_name(prefix: str = "test_") -> str:
        return f"{prefix}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    @staticmethod
    def generate_first_name(prefix: str = "test_user") -> str:
        return f"{prefix}_{DataFactory.random_string()}"
    
    @staticmethod
    def generate_last_name(prefix: str = "test_") -> str:
        return f"{prefix}_{DataFactory.random_string()}"
    
    @staticmethod
    def generate_phone() -> str:
        # Generates a random 10-digit number starting with 7, 8, or 9
        first_digit = random.choice("6789")
        remaining = "".join(random.choices(string.digits, k=9))
        return first_digit + remaining
    
    @staticmethod
    def generate_password(length: int = 8) -> str:
        # Ensures password contains letters, digits, and punctuation
        chars = string.ascii_letters + string.digits + "!@#$%^&*A"
        return "".join(random.choices(chars, k=length))
    
    @staticmethod
    def generate_org_name(prefix: str ="test_org") -> str:
        return f"{prefix}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    @staticmethod
    def generate_org_name(prefix="test_org"):
        return f"{prefix}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{DataFactory.random_string(4)}"

    @staticmethod
    def generate_invalid_uuid():
        return str(uuid.uuid4())

    @staticmethod
    def organization(data):
        return {
            "organizationName": data["organization"]["name"],
            "org_logo": "string",
            "addressline_1": data["contact"]["address1"],
            "addressline_2": data["contact"]["address2"],
            "state": data["contact"]["state"],
            "city": data["contact"]["city"],
            "country": data["contact"]["country"],
            "zipcode": data["contact"]["zip_code"]
        }

    @staticmethod
    def user(data):
        return {
            "email": data["user"]["email"],
            "password": data["user"]["password"],        # mandatory
            "firstName": data["user"]["firstName"],
            "lastName": data["user"]["lastName"],
            "phoneNumber": data["user"]["phoneNumber"], 
            "organization_id": data["user"]["organization_id"],           
            "roleId": data["user"]["role_id"],
            "isActive": True
        }
    @staticmethod
    def _unique_suffix():
            """
            Generates a unique suffix using worker + timestamp
            Used for parallel test safety
            """
            import os
            worker = os.getenv("PYTEST_XDIST_WORKER", "gw0")
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
            return f"{worker}_{timestamp}"

    @staticmethod
    def build_user(base_user: dict) -> dict:
        """
        Combines static + dynamic data to create a full user payload
        Rules:
        - All values start with 'test'
        - Email must not contain '_'
        """
        suffix = DataFactory._unique_suffix()

        return {
            "first_name": f"test{DataFactory.generate_first_name()}{suffix}",
            "last_name": f"test{DataFactory.generate_last_name()}{suffix}",
            "email": f"test{suffix.replace('_', '')}@abc.com",
            "phone": DataFactory.generate_phone(),
            "role": base_user["role"],
            "password": base_user["password"]
        }

    @staticmethod
    def build_organization(contact_data: dict) -> dict:
        """
        Creates organization payload with dynamic name
        """
        suffix = DataFactory._unique_suffix()

        return {
            "name": f"test_{suffix}",
            "contact": contact_data
        }

    
