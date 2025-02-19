
import sys

import maya.cmds as cmds

from gwScripts.tools.follow_camera import core
from gwScripts.utils import logutil


# maintain a reference to the current active camera
self = sys.modules[__name__]
self.logger = logutil.get_logger(__name__, __file__)
self.active_camera = cmds.lookThru(q=True)


def toggle():
    """
    The entry point for the tool.

    :return: None
    :rtype: None
    """
    follow_cam = core.get_follow_camera()

    # if none, create a new one and apply all the necessary logic to it
    if not follow_cam:
        self.active_camera = cmds.lookThru(q=True)  # update

        # verify user input
        selection = cmds.ls(sl=True, typ='transform')
        if not selection:
            self.logger.error(
                "No objects selected, please select an object to create a FollowCamera for."
            )
            return

        follow_cam = core.create_follow_camera()
        core.frame_camera(follow_cam, self.active_camera)
        core.constraint_camera(follow_cam, selection[0])
        self.logger.info("FollowCamera activated for \"{}\".".format(selection[0]))

    # if found, delete it and return to the last used camera
    else:
        cmds.lookThru(self.active_camera)  # restore
        core.delete_follow_camera()
        self.logger.info("FollowCamera deactivated.")

# TODO: add a visual component to the viewport to indicate
# when the toggle is in effect.
