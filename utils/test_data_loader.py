import json
import os
from datetime import datetime
from utils.data_factory import DataFactory


class TestDataLoader:

    @staticmethod
    def _unique_suffix():
        worker = os.getenv("PYTEST_XDIST_WORKER", "gw0")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        return f"{worker}_{timestamp}"   # ✅ keep underscoreissues

    @staticmethod
    def build_user(base_user: dict):
        """
        Generates dynamic user data (unique every run)
        Ensures:
        - No '_' in email
        - All values start with 'test'
        """
        suffix = TestDataLoader._unique_suffix()

        return {
            "first_name": f"test{DataFactory.generate_first_name()}{suffix}",
            "last_name": f"test{DataFactory.generate_last_name()}{suffix}",
            "email": f"test{suffix.replace('_', '')}@abc.com",   # ✅ clean email (no "_")
            "phone": DataFactory.generate_phone(),
            "role": base_user["role"],
            "password": base_user["password"]
        }

    @staticmethod
    def build_organization(contact_data: dict):
        """
        Generates dynamic organization data
        """
        suffix = TestDataLoader._unique_suffix()

        return {
            "name": f"test_{suffix}",   
            "contact": contact_data
        }


def load_test_data(file_path):
    """
    Loads static JSON test data
    """
    with open(file_path, "r") as file:
        return json.load(file)