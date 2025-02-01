
"""
Redirects to the import of the "gwScripts" module.
"""

import os
import sys
import importlib.util


# get the absolute path to the module file
module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
module_name = os.path.basename(module_path)
module_init = os.path.join(module_path, "__init__.py")

# load and add as a module
spec = importlib.util.spec_from_file_location(module_name, module_init)
module = importlib.util.module_from_spec(spec)
sys.modules[module_name] = module
spec.loader.exec_module(module)
