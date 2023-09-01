#!/usr/bin/env python3

import dialog

d = dialog.Dialog(dialog="dialog")
options = [("Option 1", "Option 1 description"),
           ("Option 2", "Option 2 description")]
code, tag = d.menu("Choose an option:", choices=options)
if code == d.OK:
    print(f"You chose: {tag}")
else:
    print("Canceled")
