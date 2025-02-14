
from .helpers import get_maya_default_logger, get_title

import os
import logging


LOGGER_PREFIX = "gwScripts: "


def get_logger(module_name, module_filepath=None):
    """
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

    # file handler
    if module_filepath:
        log_filename = module_basename + ".log"
        log_dir_path = os.path.dirname(module_filepath)
        log_filepath = os.path.join(log_dir_path, log_filename)

        file_handler = logging.FileHandler(log_filepath, mode='w')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(
            "(%(asctime)s) %(levelname)s: %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        logger.addHandler(file_handler)

    return logger
