
import maya.cmds as cmds


def _selected():
    """
    By using a generator of flattened names for selected nodes,
    we guarantee that we never try to access non-existing node names
    which might happen when renaming nodes in a tree structure.

    :yields: Names of selected nodes.
    :rtype: str
    """
    i = 0
    while i < len(cmds.ls(sl=True, fl=True)):
        yield cmds.ls(sl=True, fl=True)[i]
        i += 1

def _shortname(longname):
    """
    Given a flattened (full path) node name,
    extract the short name of that node.

    :param longname: Unique flattened path of the node.
    :type longname: str

    :return: Short name, might not be unique.
    :rtype: str
    """
    return longname.rpartition("|")[-1]

def add_prefix(prefix):
    """
    Adds the prefix text to the selected nodes.

    :param prefix: Prefix string.
    :type prefix: str

    :return: None
    :rtype: None
    """
    for node in _selected():
        cmds.rename(node, prefix + _shortname(node))

def add_suffix(suffix):
    """
    Adds the suffix text to the selected nodes.

    :param suffix: Suffix string.
    :type suffix: str

    :return: None
    :rtype: None
    """
    for node in _selected():
        cmds.rename(node, _shortname(node) + suffix)

def search_and_replace(search, replace):
    """
    Searches and replaces the texts for the selected nodes.

    :param search: Search string.
    :type search: str

    :param replace: Replace string.
    :type replace: str

    :return: None
    :rtype: None
    """
    for node in _selected():
        cmds.rename(node, _shortname(node).replace(search, replace))

def rename_and_number(new_name, start_num, padding):
    """
    Renames and renumbers the selected nodes.

    :param new_name: The node's new name.
    :type new_name: str

    :param start_num: The starting number.
    :type start_num: int

    :param padding: Amount of padding to the numbering.
    :type padding: int

    :return: None
    :rtype: None
    """
    for i, node in enumerate(_selected()):
        k = i + start_num
        cmds.rename(node, new_name + str(k).zfill(padding))
