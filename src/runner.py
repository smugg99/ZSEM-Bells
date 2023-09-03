#!/usr/bin/env python3

import sys
import os
import json
import locale
import glob

from dialog import Dialog
from typing import Dict, Optional, List, Callable, Tuple, Any

from classes.user_config_manager import UserConfigManager
from classes.dialog_screen import DialogScreen, DialogScreenType

import utils
import config


# Open a different terminal for output
# Replace '/dev/pts/X' with the appropriate terminal device
output_terminal = open('/dev/pts/0', 'w')

# Redirect stdout to the new terminal
sys.stdout = output_terminal

d = Dialog(dialog="dialog", autowidgetsize=True)

language_keys: List[str] = []
language: Dict[str, Any] = None

user_config: Dict[str, Any] = UserConfigManager().get_config()

dialog_screens: Dict[str, DialogScreen] = {}


# ================# Functions #================ #

def clear_and_exit():
    d.clear()
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


def prompt_welcome_screen():
    d.msgbox(
        text=language["welcome"]["description"].format(
            config.REPO_LINK, config.AUTHOR_NAME, config.VERSION),
        title=language["welcome"]["title"]
    )

    prompt_menu_screen()


def prompt_user_config_screen():
    global user_config

    # ================# Local Functions #================ #

    def create_update_function(key, value) -> Callable:
        return lambda: UserConfigManager().update_key([key], not value)

    def prompt_language_change_screen():
        radiolist_options: List[Tuple(str, str, bool)] = []

        current_language_code: str = user_config.get("runner_lang")

        for language_code, locale in config.LANGUAGE_BINDINGS.items():
            radiolist_options.append(
                (locale, language_code, True if language_code == current_language_code else False))

        code, tag = d.radiolist(
            text=language["language_config"]["description"],
            title=language["language_config"]["title"],
            choices=radiolist_options
        )

        if code == d.CANCEL:
            prompt_user_config_screen()

    # ================# Local Functions #================ #

    config_bool_keys: List[str] = [
        "logs_enabled",
        "wasteful_debug_enabled",
        "gpio_pins_enabled",
        "schedule_sync_enabled",
        "clock_sync_enabled"
    ]

    menu_options: List[Tuple(str, str)] = [
        ("1", language["user_config"]["options"]["sync_timestamps"]),
        ("2", language["user_config"]["options"]["which_gpio_pins"]),
        ("3", language["user_config"]["options"]["runner_lang"]),
    ]

    choice_bindings: Dict[str, Callable] = {
        "1": prompt_welcome_screen,
        "2": prompt_welcome_screen,
        "3": prompt_language_change_screen,
    }

    options_index_start: int = len(menu_options) + 1
    longest_str_lenght: int = len(max(config_bool_keys, key=len) or "")

    for i, config_bool_key in enumerate(config_bool_keys):
        language_str: str = language["user_config"]["options"][config_bool_key]
        config_value: bool = user_config.get(config_bool_key)
        e_d_str: str = bool_to_e_d(config_value, True)

        formatted_str: str = language_str.format(force_option_key_width(
            language_str, e_d_str, longest_str_lenght))

        _tag: bool = str(i + options_index_start)

        # Assuming len(menu_options) == len(choice_bindings)
        menu_options.append((_tag, formatted_str))
        choice_bindings[_tag] = create_update_function(
            config_bool_key, config_value)

    code, tag = d.menu(
        text=language["user_config"]["description"],
        title=language["user_config"]["title"],
        choices=menu_options
    )

    if code == d.CANCEL:
        prompt_menu_screen()
    else:
        # Note: Only when used on "bool changing" items in the list
        choice_bindings.get(tag, clear_and_exit)()

        # Update the user config with new settings
        user_config = UserConfigManager().get_config()

        # Update the dialog menu with new settings
        prompt_user_config_screen()


def prompt_menu_screen():
    menu_options: List[Tuple(str, str)] = [
        ("1", language["menu"]["options"]["service_manager"]),
        ("2", language["menu"]["options"]["user_config"]),
        ("3", language["menu"]["options"]["show_about"]),
    ]

    _, tag = d.menu(
        text=language["menu"]["description"],
        title=language["menu"]["title"],
        choices=menu_options,
    )

    choice_bindings: Dict[str, Callable] = {
        "1": prompt_welcome_screen,
        "2": prompt_user_config_screen,
        "3": prompt_welcome_screen
    }

    choice_bindings.get(tag, clear_and_exit)()


def initialize_dialog_screens():
    _ws_lang: Dict[str, str] = language["welcome"]
    _ws_lang["description"] = _ws_lang["description"].format(
        config.REPO_LINK, config.AUTHOR_NAME, config.VERSION)

    welcome_screen = DialogScreen(d, _ws_lang, DialogScreenType.MSG_BOX)

    global dialog_screens
    dialog_screens = {
        "welcome_screen": welcome_screen,
    }

    welcome_screen.display()

def main():
    # Get the language code from the command-line
    # argument or use the user specified one
    language_code: str = sys.argv[1] or utils.user_config.get("runner_lang")

    # Set the locale to the specified runner locale,
    # used for measurements, units, date formats etc.
    locale.setlocale(locale.LC_ALL, config.LANGUAGE_BINDINGS.get(
        language_code, config.LANGUAGE_BINDINGS["en"]))

    # Load translations for the specified language
    global language
    language = load_language(language_code)

    global d
    d.set_background_title(language["title"])
    d.add_persistent_args(["--no-nl-expand"])

    initialize_dialog_screens()

# ================# Functions #================ #


if __name__ == "__main__":
    main()
