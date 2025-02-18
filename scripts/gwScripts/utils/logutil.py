
from .helpers import get_maya_default_logger, get_title

import os
import logging


LOGGER_PREFIX = "gwScripts: "


def _get_file_handler(log_filename, log_dirpath, mode='w'):
    filepath = os.path.join(log_dirpath, log_filename)
    handler = logging.FileHandler(filepath, mode=mode)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(
        "(%(asctime)s) %(levelname)s: %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    return handler

def get_logger(module_name, module_filepath=None):
    """
    Retrieves a logger with several handlers; one for display
    in Maya's Script Editor, another for logging to the package's
    "main" log file, and possibly a third to a specified file path.

    :arg str name: Expects to use the plug-in/tool `__name__`.
    :arg str file: Expects to use the plug-in/tool `__file__`.
        Defaults to `None`, in which case it will not use a FileHandler.
    :return: A dedicated Logger object.
    :rtype: logging.Logger
    """
    module_basename = module_name.rpartition(".")[-1]
    logger_basename = LOGGER_PREFIX + get_title(module_basename)

    logger = logging.getLogger(logger_basename)
    logger.setLevel(logging.DEBUG)

    # prevent logs from propagating to Maya's built-in handlers
    logger.propagate = False
    logger.handlers = []

    # maya gui handler
    maya_gui_handler = get_maya_default_logger()
    logger.addHandler(maya_gui_handler)

    # package file handler
    package_dir_path = os.environ.get("GWSCRIPTS_PACKAGE_PATH", "")
    if package_dir_path:
        package_file_handler = _get_file_handler(
            log_filename = "gwScripts.log",
            log_dirpath = package_dir_path
        )
        logger.addHandler(package_file_handler)
    else:
        logger.error("Failed to get the environment variable for the gwScripts' package base path.")
        logger.warning("Skipping setting up the file handler for the package's logger.")

    # module file handler
    if module_filepath:
        if os.path.isfile(module_filepath):
            module_file_handler = _get_file_handler(
                log_filename = module_basename + ".log",
                log_dirpath = os.path.dirname(module_filepath)
            )
            logger.addHandler(module_file_handler)
        else:
            logger.error("Expected the following argument to be a file: {}".format(module_filepath))
            logger.warning("Skipping setting up the file handler for the module's logger.")

    return logger
