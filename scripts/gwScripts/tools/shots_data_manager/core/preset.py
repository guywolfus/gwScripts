
import json
from collections import OrderedDict

from gwScripts.tools.shots_data_manager.core.shots import Shots


# define basestring for string input guard clauses
try:
    basestring  # type: ignore
except NameError:
    basestring = str


class Preset(OrderedDict):
    """
    A data class that defines the preset structure.
    """
    def __init__(self, file_path):
        super(Preset, self).__init__()
        self.file_path = file_path

        self['Shots'] = None
        self['RenameShots'] = OrderedDict([
            ('Name', ""),
            ('StartNum', 10),
            ('Increment', 10),
            ('Padding', 3)
        ])
        self['Settings'] = OrderedDict([
            ('ExportPath', ""),
            ('Normalize', True),
            ('NormalizeFrame', 0),
            ('SaveAs', "ma")
        ])

    @property
    def shots(self):
        return self['Shots']

    @shots.setter
    def shots(self, value):
        if isinstance(value, Shots):
            self['Shots'] = value
        else:
            raise ValueError("Shots must be a `Shots()` object.")

    @property
    def rename_shots_name(self):
        return self['RenameShots']['Name']

    @rename_shots_name.setter
    def rename_shots_name(self, value):
        if isinstance(value, basestring):
            self['RenameShots']['Name'] = value
        else:
            raise ValueError("Name must be a string.")

    @property
    def rename_shots_start_num(self):
        return self['RenameShots']['StartNum']

    @rename_shots_start_num.setter
    def rename_shots_start_num(self, value):
        if isinstance(value, int):
            self['RenameShots']['StartNum'] = value
        else:
            raise ValueError("StartNum must be an integer.")

    @property
    def rename_shots_increment(self):
        return self['RenameShots']['Increment']

    @rename_shots_increment.setter
    def rename_shots_increment(self, value):
        if isinstance(value, int):
            self['RenameShots']['Increment'] = value
        else:
            raise ValueError("Increment must be an integer.")

    @property
    def rename_shots_padding(self):
        return self['RenameShots']['Padding']

    @rename_shots_padding.setter
    def rename_shots_padding(self, value):
        if isinstance(value, int):
            self['RenameShots']['Padding'] = value
        else:
            raise ValueError("Padding must be an integer.")

    @property
    def export_path(self):
        return self['Settings']['ExportPath']

    @export_path.setter
    def export_path(self, value):
        if isinstance(value, basestring):
            self['Settings']['ExportPath'] = value
        else:
            raise ValueError("ExportPath must be a string.")

    @property
    def normalize(self):
        return self['Settings']['Normalize']

    @normalize.setter
    def normalize(self, value):
        if isinstance(value, bool):
            self['Settings']['Normalize'] = value
        else:
            raise ValueError("Normalize must be a boolean.")

    @property
    def normalize_frame(self):
        return self['Settings']['NormalizeFrame']

    @normalize_frame.setter
    def normalize_frame(self, value):
        if isinstance(value, int):
            self['Settings']['NormalizeFrame'] = value
        else:
            raise ValueError("NormalizeFrame must be an integer.")

    @property
    def save_as(self):
        return self['Settings']['SaveAs']

    @save_as.setter
    def save_as(self, value):
        if value in ('ma', 'mb'):
            self['Settings']['SaveAs'] = value
        else:
            raise ValueError("SaveAs must be either 'ma' or 'mb'.")

    def save(self):
        """
        Save the preset into the preset's `file_path`.

        :return: Whether the operation succeeded or not.
        :rtype: tuple[bool, None | tuple[str, IOError]]
        """
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self, f, indent=2)
            return True, None
        except IOError as e:
            return False, (self.file_path, e)

    @classmethod
    def load(cls, file_path):
        """
        Constructor method for the class.
        Load the preset from the given `file_path`.

        :return: A preset object with the loaded data from `file_path`.
        :rtype: Preset
        """
        with open(file_path, 'r') as f:
            loaded_data = json.load(f, object_pairs_hook=OrderedDict)

        preset = cls(file_path)
        preset.update(loaded_data)
        # cast the shots information into a valid Shots object
        preset.shots = Shots((int(row), shot) for row, shot in preset.shots.items())

        return preset
