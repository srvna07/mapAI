import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


class DataReader:

    @staticmethod
    def load_json(path: str) -> dict:
        resolved = Path(path) if Path(path).is_absolute() else PROJECT_ROOT / path
        if resolved.suffix in (".yaml", ".yml"):
            resolved = resolved.with_suffix(".json")
        with open(resolved) as f:
            return json.load(f)

    load_yaml = load_json
