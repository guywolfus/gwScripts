
import os
import sys
import importlib

from gwScripts.utils.helpers import get_title


self = sys.modules[__name__]
self.__all__ = []
self.folder = os.path.dirname(__file__)

for tool_name in os.listdir(self.folder):
    if os.path.isdir(os.path.join(self.folder, tool_name)) and not tool_name.startswith("_"):
        module_name = get_title(tool_name)
        module = importlib.import_module("{}.{}".format(__name__, tool_name))
        setattr(self, module_name, module)
        self.__all__.append(module_name)
