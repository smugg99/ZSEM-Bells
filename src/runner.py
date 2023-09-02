#!/usr/bin/env python3

import sys
import json
import locale
from dialog import Dialog
from typing import Dict, Optional, List, Callable, Tuple, Any

from classes.user_config_manager import UserConfigManager

import utils
import config

d = Dialog(dialog="dialog", autowidgetsize=True)
language: Dict[str, Any] = None

user_config: Dict[str, Any] = UserConfigManager().get_config()


# ================# Functions #================ #

def load_language(language_code: str) -> Optional[Dict[str, Any]]:
    # Load the language resource based on the language code
    with open(f"{config.LANGS_FOLDER_PATH}/{language_code}.json", "r", encoding="utf-8") as file:
        language_data = json.load(file)
    return language_data


def clear_and_exit():
    d.clear()
    sys.exit(1)


# Formats bool to "enabled" for True and "disabled" for False
def bool_to_e_d(value: bool, to_state: bool = False) -> str:
    _enabled: str = "enabled_state" if to_state else "enabled"
    _disabled: str = "disabled_state" if to_state else "disabled"

    return language[_enabled if value else _disabled]


def prompt_welcome_screen():
    d.msgbox(
        text=language["welcome"]["description"].format(
            config.REPO_LINK, config.AUTHOR_NAME, config.VERSION),
        title=language["welcome"]["title"]
    )

    prompt_menu_screen()


def prompt_service_manager_screen():
    menu_options = [
        ("1", language["service_manager"]["options"]["start_service"]),
        ("2", language["service_manager"]["options"]["stop_service"]),
        ("3", language["service_manager"]["options"]["restart_service"]),
        ("4", language["service_manager"]["options"]["enable_service"]),
        ("5", language["service_manager"]["options"]["disable_service"]),
        ("6", language["service_manager"]["options"]["get_status"]),
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

    _logs: str = language["user_config"]["options"]["logs"]
    _wasteful_debug: str = language["user_config"]["options"]["wasteful_debug"]
    _gpio_pins: str = language["user_config"]["options"]["gpio_pins"]
    _schedule_sync: str = language["user_config"]["options"]["schedule_sync"]
    _clock_sync: str = language["user_config"]["options"]["clock_sync"]

    _logs_enabled: bool = user_config.get("logs_enabled")
    _wasteful_debug_enabled: bool = user_config.get("wasteful_debug_enabled")
    _gpio_pins_enabled: bool = user_config.get("gpio_pins_enabled")
    _schedule_sync_enabled: bool = user_config.get("schedule_sync_enabled")
    _clock_sync_enabled: bool = user_config.get("clock_sync_enabled")

    menu_options: List[Tuple(str, str)] = [
        ("1", language["user_config"]["options"]["sync_timestamps"]),
        ("2", language["user_config"]["options"]["which_gpio_pins"]),
        ("3", language["user_config"]["options"]["runner_lang"]),
        ("4", _logs.format(bool_to_e_d(_logs_enabled, True))),
        ("5", _wasteful_debug.format(bool_to_e_d(_wasteful_debug_enabled, True))),
        ("6", _gpio_pins.format(bool_to_e_d(_gpio_pins_enabled, True))),
        ("7", _schedule_sync.format(bool_to_e_d(_schedule_sync_enabled, True))),
        ("8", _clock_sync.format(bool_to_e_d(_clock_sync_enabled, True))),
    ]

    code, tag = d.menu(
        text=language["user_config"]["description"],
        title=language["user_config"]["title"],
        choices=menu_options,
        default_item=_default_tag or menu_options[0][0],
    )

    choice_bindings: Dict[str, Callable] = {
        "1": prompt_welcome_screen,
        "2": prompt_welcome_screen,
        "3": prompt_welcome_screen,
        "4": lambda: UserConfigManager().update_key(["logs_enabled"], not _logs_enabled),
        "5": lambda: UserConfigManager().update_key(["wasteful_debug_enabled"], not _wasteful_debug_enabled),
        "6": lambda: UserConfigManager().update_key(["gpio_pins_enabled"], not _gpio_pins_enabled),
        "7": lambda: UserConfigManager().update_key(["schedule_sync_enabled"], not _schedule_sync_enabled),
        "8": lambda: UserConfigManager().update_key(["clock_sync_enabled"], not _clock_sync_enabled)
    }

    if code == d.CANCEL:
        prompt_menu_screen()
    else:
        # Note: Only when used on "bool changing" items in the list
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
