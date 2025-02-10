
import os
import json

from gwScripts.utils import LOGGER, helpers

import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

try:
    from PySide6 import QtWidgets
except:
    from PySide2 import QtWidgets


class Dialog(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    """
    Base dialog class for GW tools and scripts.
    """
    _undocked_size = None
    _default_settings = {
        'tool_name': "Dialog",
        'window_width': 300,
        'window_height': 450
    }

    def __init__(self, parent=None, settings=None,
                 init_actions=True, init_widgets=True, init_layouts=True, init_connections=True
        ):
        """
        Initializes the dialog.

        :arg QtWidgets.QWidget parent: Optional. Use to parent the dialog to another widget.
            Defaults to `None`.
        :arg dict settings: Optional. Pass a dictionary of settings to the dialog
            such as 'tool_name', 'window_width' and 'window_height'.
            Defaults to `None`.
        :arg bool init_actions: Optional. Whether to initialize the window's actions.
            Defaults to `True`.
        :arg bool init_widgets: Optional. Whether to initialize the window's widgets.
            Defaults to `True`.
        :arg bool init_layouts: Optional. Whether to initialize the window's layouts.
            Defaults to `True`.
        :arg bool init_connections: Optional. Whether to initialize the window's connections.
            Defaults to `True`.
        :return: None
        :rtype: None
        """
        super(Dialog, self).__init__(parent)
        self.settings = settings if settings else self._default_settings

        # sets the dialog object properly via mayaMixin functionality
        self.setObjectName(helpers.validate_string(self.settings.get('tool_name')))

        # dialog properties
        self.setWindowTitle(self.settings.get('tool_name'))
        self.setMinimumSize( self.settings.get('window_width'), self.settings.get('window_height'))
        self.resize(self.settings.get('window_width'), self.settings.get('window_height'))

        # run the abstract methods
        if init_actions:
            self.create_actions()
        if init_widgets:
            self.create_widgets()
        if init_layouts:
            self.create_layouts()
        if init_connections:
            self.create_connections()

    def create_actions(self):
        """
        Create the necessary actions for the dialog window.

        :return: None
        :rtype: None
        """
        raise NotImplementedError

    def create_widgets(self):
        """
        Create the necessary widgets for the dialog window.

        :return: None
        :rtype: None
        """
        raise NotImplementedError

    def create_layouts(self):
        """
        Create the necessary layouts for the dialog window.

        :return: None
        :rtype: None
        """
        raise NotImplementedError

    def create_connections(self):
        """
        Create the necessary connections for the dialog window.

        :return: None
        :rtype: None
        """
        raise NotImplementedError

    @property
    def workspace_control_name(self):
        return "{}WorkspaceControl".format(self.objectName())

    def delete_ui(self):
        """
        Properly delete the workspace control of this window.

        :return: Whether the window was deleted or not.
        :rtype: bool
        """
        if cmds.workspaceControl(self.workspace_control_name, exists=True):
            self.display_ui()
            # force floating and closing the window before we reset, to avoid weird behavior on initialization
            cmds.workspaceControl(self.workspace_control_name, e=True, floating=True, close=True)
            cmds.deleteUI(self.workspace_control_name)
            return True
        return False

    def display_ui(self):
        """
        Used to properly display the window regardless of it's current state.

        :return: None
        :rtype: None
        """
        if self.isHidden():
            self.show(dockable=True)
        else:
            self.raise_()
            self.activateWindow()

    def floatingChanged(self, isFloating):
        """
        Override of :meth:`MayaQWidgetDockableMixin.floatingChanged`.
        Resize the window on detect dock/undock events.

        :arg bool isFloating: Whether the window is docked.
        :return: None
        :rtype: None
        """
        if isFloating:
            # restore undocked size if it was previously stored
            if self._undocked_size:
                self.resize(self._undocked_size)
                self.adjustSize()
        else:
            # save the current size before docking
            self._undocked_size = self.size()

        return super(Dialog, self).floatingChanged(isFloating)

    def info_dialog(self, title, message):
        """
        Prompt the user with an informative dialog. (e.g. if an operation was successfull or not)

        :arg str title: The title of the dialog.
        :arg str message: The text message of the dialog.
        :return: None
        :rtype: None
        """
        LOGGER.info(message)
        QtWidgets.QMessageBox.information(self, title, message,
            QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

    def confirmation_dialog(self, title, message, disable_warning=False):
        """
        Prompt the user with a dialog that requires confirmation.

        :arg str title: The title of the dialog.
        :arg str message: The text message of the dialog.
        :arg bool disable_warning: Disable displaying the warning sent to the Maya console.
        :return: Whether the user confirmed the dialog.
        :rtype: bool
        """
        if not disable_warning:
            LOGGER.warning(message)
        dialog = QtWidgets.QMessageBox.warning(self, title, message,
            QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Cancel)
        if dialog == QtWidgets.QMessageBox.StandardButton.FirstButton:
            return True
        return False

    @staticmethod
    def load_settings(filepath):
        """
        Load the 'settings.json' file in the same directory as the filepath.

        :arg str filepath: The filepath to use in order to reach the directory of the 'settings.json' file.
        :return: The loaded json file as a dictionary.
        :rtype: dict
        """
        script_dir = os.path.dirname(os.path.abspath(filepath))    
        settings_path = os.path.join(script_dir, 'settings.json')

        # check if the file exists
        if not os.path.isfile(settings_path):
            raise IOError("The 'settings.json' file does not exist in the script's directory.")

        # open and load the JSON file
        with open(settings_path, 'r') as f:
            try:
                settings = json.load(f)
            except ValueError:
                raise ValueError("Failed to parse 'settings.json'. Ensure it is a valid JSON file.")

        return settings
