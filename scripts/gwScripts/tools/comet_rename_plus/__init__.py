
import sys

from gwScripts.tools.comet_rename_plus.ui.window import Window
from gwScripts.utils import logutil


# maintains a reference to the currently-active window
self = sys.modules[__name__]
self.logger = logutil.get_logger(__name__, __file__)
self.window = None


def run(reset=False):
    """
    The entry point for the tool.

    :param reset: Resets the state of the tool.
    :type reset: bool, optional
    :return: None
    :rtype: None
    """
    if self.window and reset is True:
        self.window.delete_ui()
        self.window = None

    if not self.window:
        self.window = Window(logger=self.logger)

    self.window.display_ui()
