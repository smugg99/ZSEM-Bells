#!/usr/bin/env python3

import sys
import json
import locale
from dialog import Dialog
from typing import Dict, Optional, List, Callable, Tuple, Any

from classes.user_config_manager import UserConfigManager

import utils
import config


# Open a different terminal for output
# Replace '/dev/pts/X' with the appropriate terminal device
output_terminal = open('/dev/pts/0', 'w')

# Redirect stdout to the new terminal
sys.stdout = output_terminal

d = Dialog(dialog="dialog", autowidgetsize=True)
language: Dict[str, Any] = None

user_config: Dict[str, Any] = UserConfigManager().get_config()


# ================# Functions #================ #

def clear_and_exit():
    d.clear()
    sys.exit(1)


def load_language(language_code: str) -> Optional[Dict[str, Any]]:
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


def prompt_service_manager_screen():
    _options: Dict[str, str] = language["service_manager"]["options"]

    menu_options = [
        ("1", _options["start_service"]),
        ("2", _options["stop_service"]),
        ("3", _options["restart_service"]),
        ("4", _options["enable_service"]),
        ("5", _options["disable_service"]),
        ("6", _options["get_status"]),
    ]

    # Create a menu with options
    code, tag = d.menu(
        text=language["service_manager"]["description"],
        title=language["service_manager"]["title"],
        choices=menu_options,
    )

    # Not done yet
    choice_bindings: Dict[str, Callable] = {
        "1": prompt_welcome_screen,
        "2": prompt_welcome_screen,
        "3": prompt_welcome_screen,
        "4": prompt_welcome_screen,
        "5": prompt_welcome_screen,
        "6": prompt_welcome_screen
    }

    if code == d.CANCEL:
        prompt_menu_screen()
    else:
        choice_bindings.get(tag, clear_and_exit)()


def prompt_user_config_screen(_default_tag: Optional[str] = None):
    global user_config

    # ================# Local Functions #================ #

    def create_update_function(key, value) -> Callable:
        return lambda: UserConfigManager().update_key([key], not value)

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
        "3": prompt_welcome_screen,
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

    print(menu_options)
    print(choice_bindings)

    code, tag = d.menu(
        text=language["user_config"]["description"],
        title=language["user_config"]["title"],
        choices=menu_options,
        default_item=_default_tag or menu_options[0][0],
    )

    if code == d.CANCEL:
        prompt_menu_screen()
    else:
        # Note: Only when used on "bool changing" items in the list
        print(tag)
        choice_bindings.get(tag, clear_and_exit)()

        # Update the user config with new settings
        user_config = UserConfigManager().get_config()

        # Update the dialog menu with new settings
        prompt_user_config_screen(tag)


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
        "1": prompt_service_manager_screen,
        "2": prompt_user_config_screen,
        "3": prompt_welcome_screen
    }

    choice_bindings.get(tag, clear_and_exit)()


def main():
    # Check if a language code argument is provided
    if len(sys.argv) < 2:
        print("Usage: python3 your_script.py <language_code>")
        sys.exit(1)

    # Get the language code from the command-line
    # argument or use the user specified one
    language_code: str = sys.argv[1] or utils.user_config.get("runner_lang")

    language_bindings: Dict[str, str] = {
        "en": "en_US.UTF-8",
        "pl": "pl_PL.UTF-8"
    }

    # Set the locale to the specified runner locale,
    # used for measurements, units, date formats etc.
    locale.setlocale(locale.LC_ALL, language_bindings.get(
        language_code, language_bindings["en"]))

    # Load translations for the specified language
    global language
    language = load_language(language_code)

    global d
    d.set_background_title(language["title"])
    d.add_persistent_args(["--no-nl-expand"])

    prompt_welcome_screen()

# ================# Functions #================ #


if __name__ == "__main__":
    main()
