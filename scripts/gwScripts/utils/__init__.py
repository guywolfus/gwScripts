
import os


__all__ = []
for file_name in os.listdir(os.path.dirname(__file__)):
    if file_name.endswith(".py") and file_name != "__init__.py":
        module_name = os.path.splitext(os.path.basename(file_name))[0]
        __all__.append(module_name)

for module_name in __all__:
    __import__("{}.{}".format(__name__, module_name))
