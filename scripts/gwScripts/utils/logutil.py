
import os
import logging

from .helpers import get_maya_default_logger, get_title


PACKAGE_NAME = "gwScripts"
PACKAGE_DIR_PATH = "GWSCRIPTS_PACKAGE_PATH"


def get_logger(module_name, module_filepath=None):
    """
    Retrieves a logger with several handlers; one for display
    in Maya's Script Editor, another for logging to the package's
    "main" log file, and possibly a third to a specified file path.

    :param name: Expects to use the plugin/tool `__name__`.
    :type name: str

    :param file: Expects to use the plugin/tool `__file__`. 
        Defaults to `None`, in which case it will not use
        a FileHandler for the module scope.
    :type file: str, optional

    :return: A dedicated Logger object.
    :rtype: logging.Logger
    """
    module_basename = module_name.rpartition(".")[-1]
    logger_basename = "{}: {}".format(PACKAGE_NAME, get_title(module_basename))

    logger = logging.getLogger(logger_basename)
    logger.setLevel(logging.DEBUG)

    # prevent logs from propagating to Maya's built-in handlers
    logger.propagate = False
    logger.handlers = []

    # maya gui handler
    maya_gui_handler = get_maya_default_logger()
    logger.addHandler(maya_gui_handler)

    # package file handler
    package_dir_path = os.environ.get(PACKAGE_DIR_PATH, "")
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

def _get_file_handler(log_filename, log_dirpath, mode='w'):
    """
    Creates and configures a FileHandler for logging.

    :param log_filename: The name of the log file.
    :type log_filename: str

    :param log_dirpath: The directory path where the log file is located.
    :type log_dirpath: str

    :param mode: The mode in which to open the log file. Defaults to `'w'`.
    :type mode: str, optional

    :return: A configured FileHandler for logging.
    :rtype: logging.FileHandler
    """
    filepath = os.path.join(log_dirpath, log_filename)
    handler = logging.FileHandler(filepath, mode=mode)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(
        "(%(asctime)s) %(levelname)s: %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    return handler
