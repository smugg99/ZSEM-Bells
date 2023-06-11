import json
import config

# ================# Classes #================ #


class ConfigManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.config : dict = {}
        with open(config.USER_CONFIG_FILE_PATH, 'r') as file:
            self.config = json.load(file) 

    def get_config(self):
        return self.config
    
# ================# Classes #================ #