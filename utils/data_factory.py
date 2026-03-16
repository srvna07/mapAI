import random
import string
from datetime import datetime


class DataFactory:

    @staticmethod
    def random_string(length: int = 4) -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def random_username(prefix: str = "test_user_") -> str:
        return prefix + DataFactory.random_string()

    @staticmethod
    def random_email(prefix: str = "test_user_", domain: str = "@example.com") -> str:
        return prefix + DataFactory.random_string() + domain

    @staticmethod
    def random_name(prefix: str = "test_") -> str:
        return prefix + DataFactory.random_string()

    @staticmethod
    def timestamped_name(prefix: str = "test") -> str:
        return f"{prefix}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    @staticmethod
    def generate_first_name(prefix: str = "User") -> str:
        return f"{prefix}_{DataFactory.random_string()}"
    
    @staticmethod
    def generate_last_name(prefix: str = "Test") -> str:
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
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return "".join(random.choices(chars, k=length))
    
    @staticmethod
    def generate_org_name(prefix="test_org"):
        return f"{prefix}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
