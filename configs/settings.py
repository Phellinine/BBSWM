import json
from typing import Any

def detect_first_launch(expected_config_version) -> bool:
    try:
        with open("./configs/settings.json", "r") as f:
            settings = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return True

    if settings["general"]["meta"]["settings_version"] == expected_config_version:
        return False
    else:
        return True

def get_val(location: list[str | int], exp_type: type = str) -> Any:
    try:
        with open("./configs/settings.json", "r") as f:
            settings = json.load(f)
        val = settings
        for item in location:
            print(val)
            val = val[item]
        if exp_type == type(val):
            return val
        else:
            raise TypeError(f"Expected type {exp_type} while loading settings, got {type(val)}")

    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return ""
