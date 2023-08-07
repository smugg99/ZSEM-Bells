import json
from typing import Dict

import data.config as config

# ================# Classes #================ #


class UserConfigManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.config: Dict[str, any] = {}
        with open(config.USER_CONFIG_FILE_PATH, 'r') as file:
            self.config = json.load(file)

    def get_config(self) -> Dict[str, any]:
        return self.config

# ================# Classes #================ #
