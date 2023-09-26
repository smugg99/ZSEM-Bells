import sys

from typing import List, Dict, Tuple, Optional, Any, Type
from dialog import Dialog

from enum import Enum

# Open a different terminal for output
# Replace '/dev/pts/X' with the appropriate terminal device
output_terminal = open('/dev/pts/2', 'w')

# Redirect stdout to the new terminal
sys.stdout = output_terminal


# ================# Enums #================ #

class DialogScreenType(Enum):
    MSG_BOX = "msg_box",
    MENU = "menu"


class DialogChoiceType(Enum):
    LOCATION_CHANGER = "change_location"
    BOOL_TOGGLER = "toggle_bool"

# ================# Enums #================ #


# =============# Functions #================ #

def dialog_choices_to_list(choices: List[Type["DialogChoice"]]) -> Tuple[Any]:
    # ("1", language["menu"]["options"]["service_manager"]),
    # ("2", language["menu"]["options"]["user_config"]),
    # ("3", language["menu"]["options"]["show_about"]),

    valid_choices: List[Tuple(str, str)] = []
    print(choices)
    for i, choice in enumerate(choices):
        valid_choices.append((str(i), choice.text_content))

    return valid_choices

# ================# Functions #================ #


# ================# Classes #================ #

class DialogChoice:
    def __init__(self, choice_type: DialogChoiceType, text_content: str, location: Optional[Type["DialogScreen"]] = None):
        self.choice_type: DialogChoiceType = choice_type
        self.text_content: str = text_content
        self.location: Optional[Type["DialogScreen"]] = location

    def chosen(self, code: Optional[str] = None, tag: Optional[str] = None):
        match self.choice_type:
            case DialogChoiceType.LOCATION_CHANGER:
                self.location.display()
            case DialogChoiceType.BOOL_TOGGLER:
                pass


class DialogScreen:
    def __init__(self, dw: Type["DialogWrapper"], language: Dict[str, str], screen_type: DialogScreenType, choices: Optional[List[DialogChoice]] = []):
        self.dw: Type["DialogWrapper"] = dw
        self.language: Dict[str, str] = language
        self.choices: Optional[List[DialogChoice]] = choices
        self.screen_type: DialogScreenType = screen_type

    def display(self):
        match self.screen_type:
            case DialogScreenType.MSG_BOX:
                code, tag = self.dw.d.msgbox(
                    text=self.language["description"],
                    title=self.language["title"]
                )

                print(code, tag)
            case DialogScreenType.MENU:
                code, tag = self.dw.d.menu(
                    text=self.language["description"],
                    title=self.language["title"],
                    choices=dialog_choices_to_list(self.choices)
                )

                chosen_choice: DialogChoice = self.choices[int(tag)]
                print(chosen_choice, tag, code)

                chosen_choice.chosen()


class DialogWrapper(Dialog):
    def __init__(self, d: Dialog):
        self.d = d
        self.screens: Dict[str, DialogScreen] = None

    def set_screens(self, screens: Dict[str, DialogScreen]):
        self.screens = screens

# ================# Classes #================ #
