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


def prompt_welcome_screen():
    d.msgbox(
        text=language["welcome"]["description"].format(
            config.REPO_LINK, config.AUTHOR_NAME, config.VERSION),
        title=language["welcome"]["title"]
    )


def prompt_menu_screen():
    menu_options = [
        ("1", language["menu"]["options"]["manage_service"]),
        ("2", "Description of Option 2"),
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
        selected_option = tag
        print(f"Selected option: {selected_option}")
    else:
        print("User canceled the menu.")


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
    prompt_menu_screen()

# ================# Functions #================ #


if __name__ == "__main__":
    main()
