from typing import List, Dict, Tuple, Optional, Any

from classes.dialog_choice import DialogChoice
from dialog import Dialog
from enum import Enum


# ================# Functions #================ #

def dialog_choices_to_tuple(choices: List[DialogChoice]) -> Tuple[Any]:
	return ()

# ================# Functions #================ #


# ================# Enums #================ #

class DialogScreenType(Enum):
	MSG_BOX = "msg_box",
	MENU = "menu"

# ================# Enums #================ #


# ================# Classes #================ #


class DialogScreen:
	def __init__(self, d: Dialog, language: Dict[str, str], screen_type: DialogScreenType, choices: Optional[List[DialogChoice]] = []):
		self.dialog: Dialog = d
		self.language: Dict[str, str] = language
		self.choices: Optional[List[DialogChoice]] = choices
		self.screen_type: DialogScreenType = screen_type

	def display(self):
		match self.screen_type:
			case DialogScreenType.MSG_BOX:
				code, tag = self.dialog.msgbox(
					text=self.language["description"],
					title=self.language["title"]
				)
			case DialogScreenType.MENU:
				code, tag = self.dialog.menu(
					text=self.language["description"],
					title=self.language["title"],
					choices=dialog_choices_to_tuple(self.choices)
				)

# ================# Classes #================ #
