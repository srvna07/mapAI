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
