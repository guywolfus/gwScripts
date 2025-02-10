
from gwScripts.tools.follow_camera import core
from gwScripts import utils

import sys
import maya.cmds as cmds


# maintain a reference to the current active camera
self = sys.modules[__name__]
self._active_camera = cmds.lookThru(q=True)


def run():
    """
    The entry point for the tool.

    :return: None
    :rtype: None
    """
    follow_cam = core.get_follow_camera()

    # if none, create a new one and apply all the necessary logic to it
    if not follow_cam:
        self._active_camera = cmds.lookThru(q=True)  # update

        # verify user input
        selection = cmds.ls(sl=True, typ='transform')
        if not selection:
            utils.LOGGER.error("No objects selected, please select an object to create a FollowCamera for.")
            return

        follow_cam = core.create_follow_camera()
        core.frame_camera(follow_cam, self._active_camera)
        core.constraint_camera(follow_cam, selection[0])

    # if found, delete it and return to the last used camera
    else:
        cmds.lookThru(self._active_camera)  # restore
        core.delete_follow_camera()
