
import maya.cmds as cmds


CAMERA = "follow"
OFFSET = CAMERA + "_grp"
ATTR = CAMERA + "Cam"


class _Camera():
    """
    Private classification to be used throughout the script,
    packs the transform and shape nodes into one object.
    """
    def __init__(self, transform, shape):
        self.transform = transform
        self.shape = shape


def get_follow_camera():
    """
    :return: A camera object in the scene that has the
    custom follow attribute, or None if not found.
    :rtype: _Camera | None
    """
    for cam_shape in cmds.ls(type='camera'):
        if cmds.attributeQuery(ATTR, node=cam_shape, exists=True):
            cam_transform = cmds.listRelatives(cam_shape, parent=True)
            return _Camera(cam_transform, cam_shape)


def create_follow_camera():
    """
    :return: A camera object of the new camera.
    :rtype: _Camera
    """
    cam_shape = cmds.createNode('camera', name=CAMERA + "Shape")
    cam_transform = cmds.listRelatives(cam_shape, parent=True)
    cam_transform = cmds.rename(cam_transform, cam_shape.replace("Shape",""))

    for node in [cam_transform, cam_shape]:
        cmds.addAttr(node, longName=ATTR, attributeType="message")

    return _Camera(cam_transform, cam_shape)


def frame_camera(cam, active_cam):
    """
    Frames the camera around the selected object in the scene,
    taking the current active camera angle into consideration.

    :arg _Camera cam: The camera to frame.
    :return: None
    :rtype: None
    """
    cmds.matchTransform(cam.transform, active_cam)
    cmds.lookThru(cam.transform)
    cmds.viewFit(cam.shape)


def constraint_camera(cam, selection):
    """
    Creates a constraint setup for the camera based on the selected object in the scene.
    
    :arg _Camera cam: The camera to create the constraint setup for.
    :arg str selection: The name of the object to use for the constraint.
    :return: None
    :rtype: None
    """
    cam_offset = cmds.createNode('transform', name=OFFSET)
    cmds.addAttr(cam_offset, longName=ATTR, attributeType="message")

    cmds.matchTransform(cam_offset, cam.transform)
    cmds.parent(cam.transform, cam_offset)
    cmds.parentConstraint(selection, cam_offset, maintainOffset=True)


def delete_follow_camera():
    """
    Deletes all camera and transform nodes in the scene
    that have the follow camera attribute.
    
    :return: None
    :rtype: None
    """
    delete_list = []
    nodes = cmds.ls(type='transform')
    nodes.extend(cmds.ls(type='camera'))
    for node in nodes:
        if cmds.attributeQuery(ATTR, node=node, exists=True):
            delete_list.append(node)
    cmds.delete(delete_list)
