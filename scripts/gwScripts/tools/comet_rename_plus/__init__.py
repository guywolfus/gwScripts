
from gwScripts.tools.comet_rename_plus.ui.window import Window

import sys


# maintains a reference to the currently-active window
self = sys.modules[__name__]
self.window = None


def run(reset=False):
    """
    The entry point for the tool.

    :arg bool reset: Resets the state of the tool.
    :return: None
    :rtype: None
    """
    if self.window and reset is True:
        self.window.delete_ui()
        self.window = None

    if not self.window:
        self.window = Window()

    self.window.display_ui()
