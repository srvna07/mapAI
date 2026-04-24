import random
import string
from datetime import datetime
import uuid
import requests


class DataFactory:

    @staticmethod
    def random_string(length: int = 4) -> str:
        return "".join(random.choices(string.ascii_letters, k=length))

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
    def generate_password(length: int = 6) -> str:
        if length < 6:
            raise ValueError("Password must be at least 6 characters long")

        # Ensure all required character types
        password = [
            random.choice(string.ascii_uppercase),  # Uppercase
            random.choice(string.ascii_lowercase),  # Lowercase
            random.choice(string.digits),           # Number
            random.choice("!@#$%^&*"),              # Special character
        ]

        # Fill remaining characters
        all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password += random.choices(all_chars, k=length - 4)

        # Shuffle to avoid predictable pattern
        random.shuffle(password)

        return "".join(password)
        
    
    @staticmethod
    def generate_org_name(prefix="test_org"):
        return f"{prefix}_{DataFactory.random_string(4)}"

    @staticmethod
    def generate_invalid_uuid():
        return str(uuid.uuid4())

    @staticmethod
    def generate_role_name(prefix="test_role"):
        return f"{prefix}_{DataFactory.random_string(4)}"

    @staticmethod
    def generate_permission_name(prefix="test_permission"):
        return f"{prefix}_{DataFactory.random_string(4)}"

    @staticmethod
    def generate_agent_name(prefix="test_agent"):
        return f"{prefix}_{DataFactory.random_string(4)}"

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
    def update_organization(data, org_id):
        return {
            "organizationName": data["organization"]["name"],
            "id": org_id,
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

    
