#!/usr/bin/env python3

import sys
import json
from dialog import Dialog
from typing import Dict, Optional, Any

import config

JSON = Dict[str, Any]

global d, language
d = Dialog(dialog="dialog", autowidgetsize=True)
language: JSON = None


# ================# Functions #================ #

def load_language(language_code) -> Optional[JSON]:
    # Load the language resource based on the language code
    with open(f"{config.LANGS_FOLDER_PATH}/{language_code}.json", "r", encoding="utf-8") as file:
        language_data = json.load(file)
    return language_data


def clear_and_exit():
    d.clear()
    sys.exit(1)


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

    # Check the user's choice
    if code == d.OK:
        match tag:
            case "1":
                prompt_service_manager_screen()
            case "2":
                prompt_user_config_screen()
            case "3":
                prompt_welcome_screen()
            case "4":
                prompt_welcome_screen()
            case "5":
                pass
            case "6":
                pass
            case _:
                clear_and_exit()
    elif code == d.CANCEL:
        prompt_menu_screen()
    else:
        clear_and_exit()


def prompt_user_config_screen():
    pass


def prompt_menu_screen():
    menu_options = [
        ("1", language["menu"]["options"]["service_manager"]),
        ("2", language["menu"]["options"]["user_config"]),
        ("3", language["menu"]["options"]["show_about"]),
    ]

    # Create a menu with options
    code, tag = d.menu(
        text=language["menu"]["description"],
        title=language["menu"]["title"],
        choices=menu_options,
    )

    # Check the user's choice
    if code == d.OK:
        match tag:
            case "1":
                prompt_service_manager_screen()
            case "2":
                prompt_user_config_screen()
            case "3":
                prompt_welcome_screen()
            case _:
                clear_and_exit()
    else:
        clear_and_exit()


def main():
    # Check if a language code argument is provided
    if len(sys.argv) < 2:
        print("Usage: python3 your_script.py <language_code>")
        sys.exit(1)

    # Get the language code from the command-line argument
    language_code = sys.argv[1]

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
