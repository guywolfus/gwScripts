
from gwScripts.tools.shots_data_manager.ui.window import Window
from gwScripts.tools.shots_data_manager.ui.controller import Controller
from gwScripts.utils import logutil

import sys


# maintains a reference to the currently-active window
self = sys.modules[__name__]
self.logger = logutil.get_logger(__name__, __file__)
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
        self.window = Window(controller=Controller, logger=self.logger)

    self.window.display_ui()
