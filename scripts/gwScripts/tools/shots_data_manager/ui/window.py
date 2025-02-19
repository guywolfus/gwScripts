
import os

import maya.cmds as cmds
try:
    from PySide6 import QtGui
    from PySide6 import QtWidgets
    from PySide6.QtGui import QAction
except:
    from PySide2 import QtGui
    from PySide2 import QtWidgets
    from PySide2.QtWidgets import QAction

from gwScripts.tools.shots_data_manager.core.preset import Preset
from gwScripts.tools.shots_data_manager.core.widgets import NumericDelegate, Table
from gwScripts.utils.dialog import Dialog
from gwScripts.utils.helpers import open_dir, validate_string


class Window(Dialog):
    """
    A handy tool for Maya that allows splitting a scene into several
    other scenes, mainly envisioned to be used on a layout scene
    in order to split it into numbered shots.
    """
    def __init__(self, parent=None, controller=None, logger=None):
        """
        Initializes the dialog.

        :param parent: Use to parent the dialog to another widget.
        :type parent: QtWidgets.QWidget, optional

        :param controller: The controller for this window.
        :type controller: Controller, optional

        :param logger: Pass a specific logger for the window.
        :type logger: logging.Logger, optional

        :return: None
        :rtype: None
        """
        super(Window, self).__init__(parent, settings=self.load_settings(__file__), logger=logger)
        self.controller = controller
        self._unicode_error = False
        self._preset_path = ""
        self._export_path = ""

        # initialize shots data
        start_frame = int(cmds.playbackOptions(q=True, min=True))
        end_frame = int(cmds.playbackOptions(q=True, max=True))
        selection = cmds.ls(sl=True)
        keys = self.controller.get_keys_on_selected() if selection else [start_frame, end_frame]
        self.shots_data_table.populate(self.controller.keys_to_shots_data(keys))
        self.shots_data_table.rename_shots(*self._shots_naming_convention)

        # update the GUI info
        self._update_shot_name_display()
        self._update_normalize_frames()
        self._update_export_path()

    def create_actions(self):
        """
        Override of :meth:`Dialog.create_actions`.
        Creates the necessary actions for the dialog window.

        :return: None
        :rtype: None
        """
        self.buttons_export_btn = QtWidgets.QPushButton(self.settings.get('action_export'), self)
        self.buttons_close_btn = QtWidgets.QPushButton(self.settings.get('action_close'), self)

    def create_widgets(self):
        """
        Override of :meth:`Dialog.create_widgets`.
        Creates the necessary widgets for the dialog window.

        :return: None
        :rtype: None
        """
        # presets
        self.action_preset_save = QAction(self.settings.get('action_save_title'), self)
        self.action_preset_save.setShortcut(self.settings.get('action_save_shortcut'))
        self.action_preset_save.setStatusTip(self.settings.get('action_save_tooltip'))
        self.action_preset_load = QAction(self.settings.get('action_load_title'), self)
        self.action_preset_load.setShortcut(self.settings.get('action_load_shortcut'))
        self.action_preset_load.setStatusTip(self.settings.get('action_load_tooltip'))

        # shots data
        self.shots_data_grpbox = QtWidgets.QGroupBox("", self)

        self.shots_data_table = Table(parent=self.shots_data_grpbox)
        numeric_delegate = NumericDelegate(self.shots_data_table)
        self.shots_data_table.setItemDelegateForColumn(1, numeric_delegate)
        self.shots_data_table.setItemDelegateForColumn(2, numeric_delegate)

        self.shots_data_insert_row_btn = QtWidgets.QPushButton(
            self.settings.get('shots_data_insert_row'), self.shots_data_grpbox
        )
        self.shots_data_remove_row_btn = QtWidgets.QPushButton(
            self.settings.get('shots_data_remove_row'), self.shots_data_grpbox
        )
        self.shots_data_extract_btn = QtWidgets.QPushButton(
            self.settings.get('shots_data_extract'), self.shots_data_grpbox
        )
        self.shots_data_extract_btn.setToolTip(self.settings.get('shots_data_extract_tooltip'))
        self.shots_data_extract_btn.setStatusTip(self.settings.get('shots_data_extract_tooltip'))
        self.shots_data_clear_btn = QtWidgets.QPushButton(
            self.settings.get('shots_data_clear'), self.shots_data_grpbox
        )

        # rename shots
        self.rename_shots_grpbox = QtWidgets.QGroupBox(
            self.settings.get('rename_shots'), self
        )

        self.rename_shots_name_lbl = QtWidgets.QLabel(
            self.settings.get('rename_shots_title'), self.rename_shots_grpbox
        )
        self.rename_shots_name_edt = QtWidgets.QLineEdit(self.rename_shots_grpbox)
        self.rename_shots_name_edt.setText(
            self._scenename + self.settings.get('rename_shots_default_prefix')
        )

        self.rename_shots_num_start_lbl = QtWidgets.QLabel(
            self.settings.get('rename_shots_num_start'), self.rename_shots_grpbox
        )
        self.rename_shots_num_start_spnbox = QtWidgets.QSpinBox(self.rename_shots_grpbox)
        self.rename_shots_num_start_spnbox.setMinimumWidth(
            self.settings.get('window_width') * 0.153
        )
        self.rename_shots_num_start_spnbox.setMinimum(NumericDelegate.MIN_RANGE)
        self.rename_shots_num_start_spnbox.setMaximum(NumericDelegate.MAX_RANGE)
        self.rename_shots_num_start_spnbox.setProperty(
            'value', self.settings.get('rename_shots_num_start_value')
        )

        self.rename_shots_num_incr_lbl = QtWidgets.QLabel(
            self.settings.get('rename_shots_num_incr'), self.rename_shots_grpbox
        )
        self.rename_shots_num_incr_spnbox = QtWidgets.QSpinBox(self.rename_shots_grpbox)
        self.rename_shots_num_incr_spnbox.setMinimumWidth(self.settings.get('window_width') * 0.153)
        self.rename_shots_num_incr_spnbox.setMinimum(NumericDelegate.BASE_RANGE)
        self.rename_shots_num_incr_spnbox.setMaximum(NumericDelegate.MAX_RANGE)
        self.rename_shots_num_incr_spnbox.setProperty(
            'value', self.settings.get('rename_shots_num_incr_value')
        )

        self.rename_shots_num_padd_lbl = QtWidgets.QLabel(
            self.settings.get('rename_shots_num_padd'), self.rename_shots_grpbox
        )
        self.rename_shots_num_padd_spnbox = QtWidgets.QSpinBox(self.rename_shots_grpbox)
        self.rename_shots_num_padd_spnbox.setMinimumWidth(self.settings.get('window_width') * 0.153)
        self.rename_shots_num_padd_spnbox.setMinimum(len(str(NumericDelegate.BASE_RANGE)))
        self.rename_shots_num_padd_spnbox.setMaximum(len(str(NumericDelegate.MAX_RANGE)))
        self.rename_shots_num_padd_spnbox.setProperty(
            'value', self.settings.get('rename_shots_num_padd_value')
        )

        self.rename_shots_apply_lbl = QtWidgets.QLabel("", self.rename_shots_grpbox)
        self.rename_shots_apply_lbl.setEnabled(False)
        self.rename_shots_apply_btn = QtWidgets.QPushButton(
            self.settings.get('rename_shots_apply'), self.rename_shots_grpbox
        )

        # settings
        self.settings_grpbox = QtWidgets.QGroupBox(self.settings.get('settings_title'), self)

        self.settings_export_path_lbl = QtWidgets.QLabel(
            self.settings.get('settings_export_path'), self.settings_grpbox
        )
        self.settings_export_path_edt = QtWidgets.QLineEdit(self.settings_grpbox)
        self.settings_export_path_actn = self.settings_export_path_edt.addAction(
            QtGui.QIcon(":/browseFolder.png"),
            QtWidgets.QLineEdit.TrailingPosition
        )

        self.settings_normalize_frames_ckb = QtWidgets.QCheckBox(
            self.settings.get('settings_normalize_frames'), self.settings_grpbox
        )
        self.settings_normalize_frames_ckb.setToolTip(
            self.settings.get('settings_normalize_frames_tooltip')
        )
        self.settings_normalize_frames_ckb.setStatusTip(
            self.settings.get('settings_normalize_frames_tooltip')
        )
        self.settings_normalize_frames_ckb.setChecked(True)
        self.settings_normalize_frames_spnbox = QtWidgets.QSpinBox(self.settings_grpbox)
        self.settings_normalize_frames_spnbox.setMinimumWidth(
            self.settings.get('window_width') * 0.449
        )
        self.settings_normalize_frames_spnbox.setMinimum(NumericDelegate.MIN_RANGE)
        self.settings_normalize_frames_spnbox.setMaximum(NumericDelegate.MAX_RANGE)

        self.settings_filetype_lbl = QtWidgets.QLabel(
            self.settings.get('settings_filetype'), self.settings_grpbox
        )
        self.settings_filetype_ma_radbtn = QtWidgets.QRadioButton(
            self.settings.get('settings_filetype_ma'), self.settings_grpbox
        )
        self.settings_filetype_mb_radbtn = QtWidgets.QRadioButton(
            self.settings.get('settings_filetype_mb'), self.settings_grpbox
        )
        self.settings_filetype_ma_radbtn.setChecked(True)
        self.settings_filetype_radgrp = QtWidgets.QButtonGroup(self.settings_grpbox)
        self.settings_filetype_radgrp.addButton(self.settings_filetype_ma_radbtn)
        self.settings_filetype_radgrp.addButton(self.settings_filetype_mb_radbtn)

    def create_layouts(self):
        """
        Override of :meth:`Dialog.create_layouts`.
        Creates the necessary layouts for the dialog window.

        :return: None
        :rtype: None
        """
        def spacer_item(w=0, h=20):
            return QtWidgets.QSpacerItem(
                w, h, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
            )

        # presets
        menu_bar = QtWidgets.QMenuBar(self)
        menu_preset = QtWidgets.QMenu(self.settings.get('preset_menu'), menu_bar)
        menu_preset.addAction(self.action_preset_save)
        menu_preset.addAction(self.action_preset_load)
        menu_bar.addAction(menu_preset.menuAction())

        # shots data
        shots_data_edit_hlayout = QtWidgets.QHBoxLayout()
        shots_data_edit_hlayout.addWidget(self.shots_data_insert_row_btn)
        shots_data_edit_hlayout.addWidget(self.shots_data_remove_row_btn)
        shots_data_edit_hlayout.addItem(spacer_item())
        shots_data_edit_hlayout.addWidget(self.shots_data_extract_btn)
        shots_data_edit_hlayout.addWidget(self.shots_data_clear_btn)

        shots_data_vlayout = QtWidgets.QVBoxLayout(self.shots_data_grpbox)
        shots_data_vlayout.addWidget(self.shots_data_table)
        shots_data_vlayout.addLayout(shots_data_edit_hlayout)

        # rename shots
        rename_shots_name_hlayout = QtWidgets.QHBoxLayout()
        rename_shots_name_hlayout.addWidget(self.rename_shots_name_lbl)
        rename_shots_name_hlayout.addWidget(self.rename_shots_name_edt)

        rename_shots_num_hlayout = QtWidgets.QHBoxLayout()
        rename_shots_num_hlayout.addWidget(self.rename_shots_num_start_lbl)
        rename_shots_num_hlayout.addWidget(self.rename_shots_num_start_spnbox)
        rename_shots_num_hlayout.addItem(spacer_item())
        rename_shots_num_hlayout.addWidget(self.rename_shots_num_incr_lbl)
        rename_shots_num_hlayout.addWidget(self.rename_shots_num_incr_spnbox)
        rename_shots_num_hlayout.addItem(spacer_item())
        rename_shots_num_hlayout.addWidget(self.rename_shots_num_padd_lbl)
        rename_shots_num_hlayout.addWidget(self.rename_shots_num_padd_spnbox)

        rename_shots_apply_hlayout = QtWidgets.QHBoxLayout()
        rename_shots_apply_hlayout.addWidget(self.rename_shots_apply_lbl)
        rename_shots_apply_hlayout.addItem(spacer_item())
        rename_shots_apply_hlayout.addWidget(self.rename_shots_apply_btn)

        rename_shots_vlayout = QtWidgets.QVBoxLayout(self.rename_shots_grpbox)
        rename_shots_vlayout.addLayout(rename_shots_name_hlayout)
        rename_shots_vlayout.addLayout(rename_shots_num_hlayout)
        rename_shots_vlayout.addLayout(rename_shots_apply_hlayout)

        # settings
        settings_export_path_hlayout = QtWidgets.QHBoxLayout()
        settings_export_path_hlayout.addWidget(self.settings_export_path_lbl)
        settings_export_path_hlayout.addWidget(self.settings_export_path_edt)

        settings_normalize_frames_hlayout = QtWidgets.QHBoxLayout()
        settings_normalize_frames_hlayout.addWidget(self.settings_normalize_frames_ckb)
        settings_normalize_frames_hlayout.addWidget(self.settings_normalize_frames_spnbox)

        settings_filetype_hlayout = QtWidgets.QHBoxLayout()
        settings_filetype_hlayout.addWidget(self.settings_filetype_lbl)
        settings_filetype_hlayout.addWidget(self.settings_filetype_ma_radbtn)
        settings_filetype_hlayout.addWidget(self.settings_filetype_mb_radbtn)
        settings_filetype_hlayout.addItem(spacer_item())

        settings_vlayout = QtWidgets.QVBoxLayout(self.settings_grpbox)
        settings_vlayout.addLayout(settings_export_path_hlayout)
        settings_vlayout.addLayout(settings_normalize_frames_hlayout)
        settings_vlayout.addLayout(settings_filetype_hlayout)

        # actions
        buttons_hlayout = QtWidgets.QHBoxLayout()
        buttons_hlayout.addWidget(self.buttons_export_btn)
        buttons_hlayout.addWidget(self.buttons_close_btn)

        # main
        main_vlayout = QtWidgets.QVBoxLayout(self)
        main_vlayout.setMenuBar(menu_bar)
        main_vlayout.addWidget(self.shots_data_grpbox)
        main_vlayout.addWidget(self.rename_shots_grpbox)
        main_vlayout.addWidget(self.settings_grpbox)
        main_vlayout.addLayout(buttons_hlayout)

    def create_connections(self):
        """
        Override of :meth:`Dialog.create_connections`.
        Creates the necessary connections for the dialog window.

        :return: None
        :rtype: None
        """
        self.action_preset_save.triggered.connect(self.preset_save)
        self.action_preset_load.triggered.connect(self.preset_load)
        self.shots_data_insert_row_btn.clicked.connect(self.shots_data_table.insertRow)
        self.shots_data_remove_row_btn.clicked.connect(self.shots_data_table.removeRow)
        self.shots_data_extract_btn.clicked.connect(self.shots_data_from_selected)
        self.shots_data_clear_btn.clicked.connect(self.clear_shots_data)
        self.rename_shots_name_edt.textChanged.connect(self._update_shot_name_display)
        self.rename_shots_num_start_spnbox.valueChanged.connect(self._update_shot_name_display)
        self.rename_shots_num_incr_spnbox.valueChanged.connect(self._update_shot_name_display)
        self.rename_shots_num_padd_spnbox.valueChanged.connect(self._update_shot_name_display)
        self.rename_shots_apply_btn.clicked.connect(self.rename_shots_data)
        self.settings_export_path_actn.triggered.connect(self.browse_export_path)
        self.settings_export_path_edt.textChanged.connect(self._update_export_path)
        self.settings_normalize_frames_ckb.clicked.connect(self._update_normalize_frames)
        self.buttons_export_btn.clicked.connect(self.run_export_shots)
        self.buttons_close_btn.clicked.connect(self.close)

    def preset_save(self):
        """
        Save a preset (Json) file based on the GUI's shots data.

        :return: None
        :rtype: None
        """
        # set the preset path
        preset_path = self._preset_path if self._preset_path else cmds.workspace(q=True, rd=True)
        save_path = cmds.fileDialog2(
            dialogStyle=2,  # maya style, consistent across platforms
            caption="Save Preset...",
            startingDirectory=preset_path,
            fileFilter='Json (*.json)',
            fileMode=0  # any file, whether it exists or not
        )
        if not save_path:
            return
        self._preset_path = save_path[0]

        # build the preset data
        preset = Preset(self._preset_path)
        preset.shots = self.shots_data_table.shots_data
        preset.rename_shots_name = self.rename_shots_name_edt.text()
        preset.rename_shots_start_num = self.rename_shots_num_start_spnbox.value()
        preset.rename_shots_increment = self.rename_shots_num_incr_spnbox.value()
        preset.rename_shots_padding = self.rename_shots_num_padd_spnbox.value()
        preset.export_path = self.settings_export_path_edt.text()
        preset.normalize = self.settings_normalize_frames_ckb.isChecked()
        preset.normalize_frame = self.settings_normalize_frames_spnbox.value()
        preset.save_as = 'ma' if self.settings_filetype_ma_radbtn.isChecked() else 'mb'
        save, args = preset.save()
        if not save:
            self.logger.error(
                self.settings.get('save_preset_io_error') + " \"{}\".".format(args[0])
            )
            self.logger.error(args[1])

        # confirmation
        self.info_dialog(title="Done!", message=self.settings.get('preset_saved_confirm'))

    def preset_load(self, preset=None):
        """
        Loads a preset (Json) file into the GUI's shots data.

        :param preset: The preset to load (in JSON format) as a `Preset` object.
        :type preset: dict, optional

        :return: None
        :rtype: None
        """
        # get the preset if not passed as an argument
        if not preset:
            preset_path = (self._preset_path
                           if self._preset_path
                           else cmds.workspace(q=True, rd=True))
            load_path = cmds.fileDialog2(
                dialogStyle=2,  # maya style, consistent across platforms
                caption="Load Preset...",
                startingDirectory=preset_path,
                fileFilter='Json (*.json)',
                fileMode=1  # a single existing file
            )
            if not load_path:
                return
            self._preset_path = load_path[0]

            try:
                preset = Preset.load(self._preset_path)
            except IOError:
                self.logger.error("{}: \"{}\".".format(
                    self.settings.get('load_preset_file_not_found_error'),
                    self._preset_path
                ))
                return
            except ValueError:
                self.logger.error("{}: \"{}\".".format(
                    self.settings.get('load_preset_json_decode_error'),
                    self._preset_path
                ))
                return

        # populate the table based on the preset
        try:
            self.shots_data_table.populate(preset.shots)
        except Exception as e:
            self.logger.error(e)
            self.logger.error(self.settings.get('load_preset_shots_data_error'))
            return

        # set the GUI fields to match the preset
        self.rename_shots_name_edt.setText(preset.rename_shots_name)
        self.rename_shots_num_start_spnbox.setValue(preset.rename_shots_start_num)
        self.rename_shots_num_incr_spnbox.setValue(preset.rename_shots_increment)
        self.rename_shots_num_padd_spnbox.setValue(preset.rename_shots_padding)
        self.settings_export_path_edt.setText(preset.export_path)
        self.settings_normalize_frames_ckb.setChecked(preset.normalize)
        self.settings_normalize_frames_spnbox.setValue(preset.normalize_frame)
        self.settings_filetype_ma_radbtn.setChecked(preset.save_as == 'ma')
        self.settings_filetype_mb_radbtn.setChecked(preset.save_as == 'mb')

        # update the GUI info
        self._update_shot_name_display()
        self._update_normalize_frames()
        self._update_export_path()

        # confirmation
        self.info_dialog(title="Done!", message=self.settings.get('preset_loaded_confirm'))

    def shots_data_from_selected(self):
        """
        Prompts the user to apply the shots' data from selection, and sets it in the GUI.

        :return: None
        :rtype: None
        """
        if not cmds.ls(sl=True):
            self.logger.error("{}{}".format(
                self.settings.get('no_object_selected_error'),
                self.settings.get('select_keyframes_error')
            ))
            return
        if not self.controller.get_keys_on_selected():
            self.logger.error("{}{}".format(
                self.settings.get('no_keyframes_error'),
                self.settings.get('select_keyframes_error')
            ))
            return

        if self.shots_data_table.shots_data and not self.confirmation_dialog(
            title=self.settings.get('from_selected_dialog_title'),
            message=self.settings.get('from_selected_dialog_message')
        ):
            return

        shots_data = self.controller.keys_to_shots_data(self.controller.get_keys_on_selected())
        self.shots_data_table.populate(shots_data)
        self.shots_data_table.rename_shots(*self._shots_naming_convention)

    def clear_shots_data(self):
        """
        Prompts the user to clear the shots' data, and clears the GUI.

        :return: None
        :rtype: None
        """
        if self.shots_data_table.shots_data:
            if self.confirmation_dialog(
                title=self.settings.get('clear_shots_dialog_title'),
                message=self.settings.get('clear_shots_dialog_message')
            ):
                self.shots_data_table.clear()

    def rename_shots_data(self):
        """
        Prompts the user to rename the shots, and sets them in the GUI.

        :return: None
        :rtype: None
        """
        if self.shots_data_table.shots_data and not self.confirmation_dialog(
            title=self.settings.get('rename_shots_dialog_title'),
            message=self.settings.get('rename_shots_dialog_message')
        ):
            return
        self.shots_data_table.rename_shots(*self._shots_naming_convention)

    def browse_export_path(self):
        """
        Prompts the user to browse and select a folder for the export path,
        and sets it in the GUI if selected.

        :return: None
        :rtype: None
        """
        browse_path = (self._export_path
                       if os.path.exists(self._export_path)
                       else cmds.workspace(q=True, rd=True))
        selected_dir = cmds.fileDialog2(
            dialogStyle=2,  # maya style, consistent across platforms
            caption="Select Directory...",
            startingDirectory=browse_path,
            fileMode=3  # the name of a directory
                        # only directories are displayed in the dialog
        )
        if selected_dir:
            self.settings_export_path_edt.setText(selected_dir[0])

    def run_export_shots(self):
        """
        Runs the Maya files' export operation based on the shots data in the GUI.
        Exists if canceled during scene validation.

        :return: None
        :rtype: None
        """
        # validate the scene before export
        if cmds.file(q=True, modified=True):
            if not self.confirmation_dialog(
                title=self.settings.get('export_shots_dialog_title'),
                message=self.settings.get('export_shots_dialog_message')
            ):
                return

            if not cmds.file(q=True, sn=True):
                browse_path = (self._export_path
                               if os.path.exists(self._export_path)
                               else cmds.workspace(q=True, rd=True))
                save_scene = cmds.fileDialog2(
                    dialogStyle=2,  # maya style, consistent across platforms
                    caption="Save As",
                    startingDirectory=browse_path,
                    fileFilter="Maya ASCII (*.ma);;Maya Binary (*.mb)",
                    fileMode=0  # any file, whether it exists or not
                )
                if not save_scene:
                    return
                cmds.file(rename=save_scene[0])
            cmds.file(save=True)
        main_file = cmds.file(q=True, sn=True)

        # determine attrs from window input
        normalize = (self.settings_normalize_frames_spnbox.value()
                     if self.settings_normalize_frames_ckb.isChecked()
                     else None)
        save_as_filetype = ('mayaAscii'
                            if self.settings_filetype_ma_radbtn.isChecked()
                            else 'mayaBinary')

        # run the export operation
        for shot_data in self.shots_data_table.shots_data.values():
            shot_name, start_frame, end_frame = shot_data.values()

            if not main_file == cmds.file(q=True, sn=True):
                cmds.file(main_file, force=True, loadReferenceDepth="all")
            failed_anim_curves = self.controller.apply_shot(start_frame, end_frame, normalize)
            if failed_anim_curves:
                for anim_curve in failed_anim_curves:
                    self.logger.warning("Skipping \"{}\": {}".format(
                        anim_curve, self.settings.get('failed_anim_curve_warning')
                    ))
            cmds.file(rename=os.path.join(self._export_path, shot_name))
            cmds.file(save=True, force=True, type=save_as_filetype)

        # finalize
        cmds.file(main_file, force=True, loadReferenceDepth="all")
        open_dir(self._export_path)
        self.logger.info(self.settings.get('export_shots_confirm'))

    def _update_shot_name_display(self):
        """
        Sets the "rename shots" label to show the example based on the GUI options.
        Sets and clears the unciode error internal flag in case the name is not valid.

        :return: None
        :rtype: None
        """
        name, start, incr, padd = self._shots_naming_convention

        eg1 = name + str(start).zfill(padd)
        eg2 = name + str(start + incr).zfill(padd)
        eg3 = name + str(start + incr*2).zfill(padd)

        try:
            self.rename_shots_apply_lbl.setText(
                "e.g. \"{}\", \"{}\", \"{}\"...".format(eg1, eg2, eg3)
            )
            if self._unicode_error:
                print("")
                self._unicode_error = False
        except UnicodeEncodeError:
            if not self._unicode_error:
                self.logger.error(self.settings.get('shot_name_display_error'))
                self._unicode_error = True

    def _update_normalize_frames(self):
        """
        Enables/disables the "normalize frames" spinbox based on whether the checkbox is checked.

        :return: None
        :rtype: None
        """
        self.settings_normalize_frames_spnbox.setEnabled(
            self.settings_normalize_frames_ckb.isChecked()
        )

    def _update_export_path(self):
        """
        Enables/disables the "export" button based on whether the path is a valid path.

        :return: None
        :rtype: None
        """
        check_export_path = os.path.abspath(self.settings_export_path_edt.text())
        if self.settings_export_path_edt.text() and os.path.isdir(check_export_path):
            self._export_path = check_export_path
            self.buttons_export_btn.setEnabled(True)
            self.buttons_export_btn.setToolTip("")
        else:
            self.buttons_export_btn.setEnabled(False)
            self.buttons_export_btn.setToolTip(self.settings.get('export_path_error'))

    @property
    def _scenename(self):
        """
        Internal for the current scene name.
        """
        scenename = os.path.basename(cmds.file(q=True, sn=True)).split(".")[0]
        return scenename if cmds.file(q=True, sn=True) else "untitled"

    @property
    def _shots_naming_convention(self):
        """
        Internal for valid shots' naming conventions.
        """
        name = validate_string(
            input_str=self.rename_shots_name_edt.text(),
            replace_with="_"
        )
        return (name,
                self.rename_shots_num_start_spnbox.value(),
                self.rename_shots_num_incr_spnbox.value(),
                self.rename_shots_num_padd_spnbox.value()
        )
