#!/usr/bin/env python3

import sys
import locale

from typing import Dict, Optional, List, Callable, Tuple, Any

from classes.user_config_manager import UserConfigManager
from lib.dialog_wrapper.dialog_wrapper import DialogWrapper, DialogScreen, DialogScreenType, DialogChoice, DialogChoiceType

import utils
import config


# Open a different terminal for output
output_terminal = open('/dev/pts/3', 'w')

# Redirect stdout to the new terminal
sys.stdout = output_terminal

user_config: Dict[str, Any] = UserConfigManager().get_config()

dw = DialogWrapper(user_config.get("runner_lang"))


# ================# Functions #================ #


def initialize_dialog_screens():
    _ws_lang: Dict[str, str] = dw.language["welcome"]
    _ws_lang["description"] = _ws_lang["description"].format(
        config.REPO_LINK, config.AUTHOR_NAME, config.VERSION)

    welcome_screen = DialogScreen(
        dw, DialogScreenType.MSG_BOX, name="welcome", on_ok="menu")
    
    _ms_choices: List[DialogChoice] = [
        DialogChoice(dw, DialogChoiceType.LOCATION_CHANGER, "welcome screen",
                     location="welcome"),
        DialogChoice(dw, DialogChoiceType.LOCATION_CHANGER, "welcome screen again",
                     location="welcome"),
        DialogChoice(dw, DialogChoiceType.BOOL_TOGGLER, "foreskin",
                     config_keys=["foreskin_enabled"])
    ]

    menu_screen = DialogScreen(
        dw, DialogScreenType.MENU, name="menu", choices=_ms_choices)

    dw.set_screens([welcome_screen, menu_screen])

    welcome_screen.display()


def main():
    initialize_dialog_screens()

# ================# Functions #================ #


if __name__ == "__main__":
    main()
