import json
import data.config as config

from typing import Dict


# ================# Classes #================ #


class LangBindingsManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.lang_bindings: Dict[str, any] = {}

    def load_bindings(self, bindings_path: str) -> Dict[str, any]:
        with open(bindings_path, 'r') as file:
            self.lang_bindings = json.load(file)

        return self.lang_bindings

    def get_bindings(self) -> Dict[str, any]:
        return self.lang_bindings

# ================# Classes #================ #
