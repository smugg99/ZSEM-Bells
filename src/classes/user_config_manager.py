import json
import logging
from typing import Dict, Any, List

import config


# ================# Classes #================ #


class UserConfigManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self):
        try:
            with open(config.USER_CONFIG_FILE_PATH, 'r') as file:
                self.config = json.load(file)
        except FileNotFoundError:
            # Handle the case where the config file doesn't exist
            logging.error("Config file not found")
            raise FileNotFoundError("Config file not found")
        except json.JSONDecodeError:
            # Handle the case where the config file is not valid JSON
            logging.error("Error decoding JSON in config file")
            raise ValueError("Error decoding JSON in config file")

    def get_config(self) -> Dict[str, Any]:
        return self.config

    def save_config(self):
        try:
            with open(config.USER_CONFIG_FILE_PATH, 'w') as file:
                json.dump(self.config, file, indent=4)
        except IOError:
            # Handle the case where there was an issue writing the config file
            logging.error("Error writing to config file")
            raise IOError("Error writing to config file")

    def update_key(self, keys: List[str], value: Any) -> None:
        # Traverse the nested dictionary using the list of keys
        current_dict = self.config
        for key in keys[:-1]:
            if key in current_dict and isinstance(current_dict[key], dict):
                current_dict = current_dict[key]
            else:
                # Handle the case where the key doesn't exist or is not a dictionary
                logging.error(f"Key '{key}' is not found or not a dictionary")
                raise KeyError(
                    f"Key '{key}' is not found or not a dictionary")

        # Update the value at the last key in the list
        last_key = keys[-1]
        current_dict[last_key] = value

        # Save the updated configuration to the file
        self.save_config()


# ================# Classes #================ #
