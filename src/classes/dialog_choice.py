import json
import logging

from typing import Dict, Any, List
from enum import Enum

import config


# ================# Enums #================ #

class DialogChoiceType(Enum):
    LOCATION_CHANGER = "change_location"
    BOOL_TOGGLER = "toggle_bool"


# ================# Enums #================ #


# ================# Classes #================ #


class DialogChoice:
    def __init__(self, choice_type: DialogChoiceType):
        self.choice_type: DialogChoiceType = choice_type


# ================# Classes #================ #
