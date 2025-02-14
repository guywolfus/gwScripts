
from gwScripts.utils.helpers import get_title

import os
import importlib


__all__ = []

for tool_name in os.listdir(os.path.dirname(__file__)):
    if os.path.isdir(os.path.join(os.path.dirname(__file__), tool_name)) and not tool_name.startswith("_"):
        module_name = get_title(tool_name)
        globals()[module_name] = importlib.import_module("{}.{}".format(__name__, tool_name))
        __all__.append(module_name)
