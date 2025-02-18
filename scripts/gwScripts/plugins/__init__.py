
import os
import sys
import importlib


self = sys.modules[__name__]
self.__all__ = []
self.folder = os.path.dirname(__file__)

for module_name in os.listdir(self.folder):
    if os.path.isdir(os.path.join(self.folder, module_name)) and not module_name.startswith("_"):
        module = importlib.import_module("{}.{}".format(__name__, module_name))
        setattr(self, module_name, module)
        self.__all__.append(module_name)
