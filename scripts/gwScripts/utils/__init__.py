
import os
import sys
import importlib


self = sys.modules[__name__]
self.__all__ = []

for file_name in os.listdir(os.path.dirname(__file__)):
    if file_name.endswith(".py") and file_name != "__init__.py":
        module_name = os.path.splitext(os.path.basename(file_name))[0]
        module = importlib.import_module("{}.{}".format(__name__, module_name))
        setattr(self, module_name, module)
        self.__all__.append(module_name)
