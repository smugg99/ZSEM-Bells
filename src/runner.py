#!/usr/bin/env python3

import sys
import os
import json
import locale
import glob

from dialog import Dialog
from typing import Dict, Optional, List, Callable, Tuple, Any

from classes.user_config_manager import UserConfigManager
from classes.dialog_wrapper import DialogWrapper, DialogScreen, DialogScreenType, DialogChoice, DialogChoiceType

import utils
import config


# Open a different terminal for output
# Replace '/dev/pts/X' with the appropriate terminal device
output_terminal = open('/dev/pts/2', 'w')

# Redirect stdout to the new terminal
sys.stdout = output_terminal

dw = DialogWrapper(Dialog(dialog="dialog", autowidgetsize=True))

language_keys: List[str] = []
language: Dict[str, Any] = None

user_config: Dict[str, Any] = UserConfigManager().get_config()


# ================# Functions #================ #

def clear_and_exit():
    dw.d.clear()
    sys.exit(1)


def load_language(language_code: str) -> Optional[Dict[str, Any]]:
    json_files = glob.glob(os.path.join(config.LANGS_FOLDER_PATH, "*.json"))

    global language_keys
    language_keys = [os.path.splitext(os.path.basename(file))[
        0] for file in json_files]

    try:
        with open(f"{config.LANGS_FOLDER_PATH}/{language_code}.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        utils.logger.error(f"Language file not found for {language_code}.")
        sys.exit(1)
    except json.JSONDecodeError:
        utils.logger.error(
            f"Invalid JSON in the language file for {language_code}.")
        sys.exit(1)


# Formats bool to "enabled" for True and "disabled" for False
def bool_to_e_d(value: bool, to_state: Optional[bool] = False) -> str:
    _enabled: str = "enabled_state" if to_state else "enabled"
    _disabled: str = "disabled_state" if to_state else "disabled"

    return language[_enabled if value else _disabled]


def force_option_key_width(key: str, value: str, forced_width: int) -> str:
    max_separators: int = forced_width - len(key) - len(value)
    return " " * max_separators + value


def initialize_dialog_screens():
    _ws_lang: Dict[str, str] = language["welcome"]
    _ws_lang["description"] = _ws_lang["description"].format(
        config.REPO_LINK, config.AUTHOR_NAME, config.VERSION)

    _ms_lang: Dict[str, str] = language["menu"]

    welcome_screen = DialogScreen(
        dw, _ws_lang, DialogScreenType.MSG_BOX, on_ok="menu")

    _ms_choices: List[DialogChoice] = [
        DialogChoice(dw, DialogChoiceType.LOCATION_CHANGER, "welcome screen",
                     location="welcome"),
        DialogChoice(dw, DialogChoiceType.LOCATION_CHANGER, "welcome screen again",
                     location="welcome")
    ]

    menu_screen = DialogScreen(
        dw, _ms_lang, DialogScreenType.MENU, choices=_ms_choices)

    dw.set_screens(screens={
        "welcome": welcome_screen,
        "menu": menu_screen
    })

    welcome_screen.display()
    menu_screen.display()


def main():
    # Get the language code from the command-line
    # argument or use the user specified one

    # language_code: str = sys.argv[1] or utils.user_config.get("runner_lang")
    language_code: str = utils.user_config.get("runner_lang")

    # Set the locale to the specified runner locale,
    # used for measurements, units, date formats etc.
    locale.setlocale(locale.LC_ALL, config.LANGUAGE_BINDINGS.get(
        language_code, config.LANGUAGE_BINDINGS["en"]))

    # Load translations for the specified language
    global language
    language = load_language(language_code)

    global dw
    dw.d.set_background_title(language["title"])
    dw.d.add_persistent_args(["--no-nl-expand"])

    initialize_dialog_screens()

# ================# Functions #================ #


if __name__ == "__main__":
    main()
