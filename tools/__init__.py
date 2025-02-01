
import os
import importlib

__all__ = []

for tool_name in os.listdir(os.path.dirname(__file__)):
    if os.path.isdir(os.path.join(os.path.dirname(__file__), tool_name)) and not tool_name.startswith("_"):
        module_name = "".join(word.capitalize() for word in tool_name.split("_"))
        globals()[module_name] = importlib.import_module("{}.{}".format(__name__, tool_name))
        __all__.append(module_name)
