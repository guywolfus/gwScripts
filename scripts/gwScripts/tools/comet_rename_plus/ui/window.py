
from gwScripts.tools.comet_rename_plus import core
from gwScripts.utils.dialog import Dialog
from gwScripts.utils.helpers import undo_chunk

import maya.cmds as cmds

try:
    from PySide6 import QtCore
    from PySide6 import QtGui
    from PySide6 import QtWidgets
except:
    from PySide2 import QtCore
    from PySide2 import QtGui
    from PySide2 import QtWidgets


class Window(Dialog):
    """
    A simple renaming GUI utility that helps with
    batch name manipulation for Maya nodes.
    """

    def __init__(self, parent=None, logger=None):
        """
        Initializes the dialog.

        :arg QtWidgets.QWidget parent: Optional. Use to parent the dialog to another widget.
            Defaults to `None`.
        :return: None
        :rtype: None
        """
        super(Window, self).__init__(parent,
            settings=self.load_settings(__file__), logger=logger, init_actions=False
        )

    def create_widgets(self):
        """
        Override of :meth:`Dialog.create_widgets`.
        Creates the necessary widgets for the dialog window.

        :return: None
        :rtype: None
        """
        # replace
        self.lnedit_search = QtWidgets.QLineEdit()
        self.lnedit_replace = QtWidgets.QLineEdit()
        self.btn_replace = QtWidgets.QPushButton(self.settings.get('btn_replace'))

        # prefix
        self.lnedit_prefix = QtWidgets.QLineEdit()
        self.btn_prefix = QtWidgets.QPushButton(self.settings.get('btn_prefix'))

        # suffix
        self.lnedit_suffix = QtWidgets.QLineEdit()
        self.btn_suffix = QtWidgets.QPushButton(self.settings.get('btn_suffix'))

        # rename
        self.lnedit_rename = QtWidgets.QLineEdit()
        self.lnedit_start_num = QtWidgets.QLineEdit()
        self.lnedit_padding = QtWidgets.QLineEdit()
        self.btn_rename = QtWidgets.QPushButton(self.settings.get('btn_rename'))

        # set specific line edit settings
        for lnedit in [
            self.lnedit_search,
            self.lnedit_replace,
            self.lnedit_prefix,
            self.lnedit_suffix,
            self.lnedit_rename
        ]:
            lnedit.setClearButtonEnabled(True)

        for i, lnedit in enumerate([
            self.lnedit_padding,
            self.lnedit_start_num
        ]):
            lnedit.setText(self.settings.get('lnedits_text')[str(i)])
            lnedit.setMaximumWidth(self.settings.get('lnedits_width'))
            limit =  self.settings.get('lnedits_limit')[str(i)]
            lnedit.setValidator(QtGui.QIntValidator(0, limit))

    def create_layouts(self):
        """
        Override of :meth:`Dialog.create_layouts`.
        Creates the necessary layouts for the dialog window.

        :return: None
        :rtype: None
        """
        def add_line():
            line = QtWidgets.QFrame()
            line.setFrameShape(QtWidgets.QFrame.HLine)
            line.setFrameShadow(QtWidgets.QFrame.Sunken)
            return line

        # main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(6, 6, 6, 6)
        self.main_layout.setSpacing(1)

        # replace
        self.main_layout.addLayout(self._add_lnedit(self.settings.get('search'), self.lnedit_search))
        self.main_layout.addLayout(self._add_lnedit(self.settings.get('replace'), self.lnedit_replace))
        self.main_layout.addWidget(self.btn_replace)
        self.main_layout.addWidget(add_line())

        # prefix
        self.main_layout.addLayout(self._add_lnedit(self.settings.get('prefix'), self.lnedit_prefix))
        self.main_layout.addWidget(self.btn_prefix)
        self.main_layout.addWidget(add_line())

        # suffix
        self.main_layout.addLayout(self._add_lnedit(self.settings.get('suffix'), self.lnedit_suffix))
        self.main_layout.addWidget(self.btn_suffix)
        self.main_layout.addWidget(add_line())

        # rename
        self.main_layout.addLayout(self._add_lnedit(self.settings.get('rename'), self.lnedit_rename))
        self.main_layout.addLayout(self._add_lnedit(self.settings.get('start_num'), self.lnedit_start_num, True))
        self.main_layout.addLayout(self._add_lnedit(self.settings.get('padding'), self.lnedit_padding, True))
        self.main_layout.addWidget(self.btn_rename)

    def create_connections(self):
        """
        Override of :meth:`Dialog.create_connections`.
        Creates the necessary connections for the dialog window.

        :return: None
        :rtype: None
        """
        self.btn_replace.clicked.connect(self.search_and_replace)
        self.btn_prefix.clicked.connect(self.add_prefix)
        self.btn_suffix.clicked.connect(self.add_suffix)
        self.btn_rename.clicked.connect(self.rename_and_number)

    def _add_lnedit(self, label_text, lnedit_widget, add_stretch=False):
        """
        :arg str label_text:
        :arg QtWidgets.QLineEdit lnedit_widget:
        :arg bool add_stretch: Defaults to False.
        :return: Layout of a label and a line edit widget.
        :rtype: QtWidgets.QHBoxLayout
        """
        label = QtWidgets.QLabel(label_text)
        label.setMinimumWidth(self.settings.get('labels_width'))
        label.setAlignment(QtCore.Qt.AlignRight)
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(label)
        hlayout.addWidget(lnedit_widget)
        if add_stretch:
            hlayout.addStretch()
        return hlayout

    @undo_chunk
    def add_prefix(self):
        """
        Adds the prefix text to the selected nodes.

        :return: None
        :rtype: None
        """
        prefix = self.lnedit_prefix.text()
        if not prefix:
            self.logger.warning(self.settings.get('prefix_missing_warning'))
            return
        if not cmds.ls(sl=True):
            self.logger.warning(self.settings.get('no_objects_selected_warning'))
            return
        core.add_prefix(prefix)

    @undo_chunk
    def add_suffix(self):
        """
        Adds the suffix text to the selected nodes.

        :return: None
        :rtype: None
        """
        suffix = self.lnedit_suffix.text()
        if not suffix:
            self.logger.warning(self.settings.get('suffix_missing_warning'))
            return
        if not cmds.ls(sl=True):
            self.logger.warning(self.settings.get('no_objects_selected_warning'))
            return
        core.add_suffix(suffix)

    @undo_chunk
    def search_and_replace(self):
        """
        Searches and replaces the texts for the selected nodes.

        :return: None
        :rtype: None
        """
        search = self.lnedit_search.text()
        replace = self.lnedit_replace.text()
        if not search:
            self.logger.error(self.settings.get('search_missing_error'))
            return
        if not cmds.ls(sl=True):
            self.logger.warning(self.settings.get('no_objects_selected_warning'))
            return
        core.search_and_replace(search, replace)

    @undo_chunk
    def rename_and_number(self):
        """
        Renames and renumbers the selected nodes.

        :return: None
        :rtype: None
        """
        new_name = self.lnedit_rename.text()
        if not new_name:
            self.logger.warning(self.settings.get('name_name_missing_warning'))
            return
        if not cmds.ls(sl=True):
            self.logger.warning(self.settings.get('no_objects_selected_warning'))
            return
        start_num = int(self.lnedit_start_num.text())
        padding = int(self.lnedit_padding.text())
        core.rename_and_number(new_name, start_num, padding)
