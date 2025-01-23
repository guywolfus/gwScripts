
import os
import platform
import subprocess
import logging

import maya.cmds as cmds


LOGGER = logging.getLogger("gwScripts")


def open_dir(dir_path):
    """
    Opens a directory path on any system.
    :arg str dir_path: The path to open.
    :return: None
    :rtype: None
    """
    if platform.system() == 'Windows':
        os.startfile(dir_path.replace('/','\\'))
    elif platform.system() == 'Darwin':
        subprocess.Popen(['open', dir_path])
    else:
        subprocess.Popen(['xdg-open', dir_path])

def validate_string(input_str, replace_with=""):
    """
    Replaces invalid characters from a string.

    :arg str input_str: Input string to validate.
    :arg str replace_with: What to replace invalid characters with.
        Defaults to an empty string.
    :return: The valid manipulated string.
    :rtype: str
    """
    for c in ' +=?!@#$%^&*:;~|/\\`\'"<>()[]\{\}':
        input_str = input_str.replace(c, replace_with)
    return input_str

def undo_chunk(func):
    """
    Decorator that wraps functions in a single undo chunk.

    :arg Callable func: The function to run.
    :return: The result of the input function, wrapped as a callable.
    :rtype: Callable
    """
    def func_call(*args, **kwargs):
        cmds.undoInfo(openChunk=True, chunkName=func.__name__)
        result = func(*args,**kwargs)
        cmds.undoInfo(closeChunk=True, chunkName=func.__name__)
        return result
    return func_call
