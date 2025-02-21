
import maya.cmds as cmds

from gwScripts.tools.shots_data_manager.core.shots import Shots
from gwScripts.utils.helpers import unique_list


class Controller:
    """
    The controller for ShotsDataManager.
    """
    @staticmethod
    def get_keys_on_selected():
        """
        :return: The sorted list of keyframes on the currently selected objects.
        :rtype: list[int]
        """
        return unique_list(cmds.keyframe(cmds.ls(sl=True)[-1], q=True), ordered=True)

    @staticmethod
    def keys_to_shots_data(keys):
        """
        Given keyframe numbers, returns a ShotsDataDict object with shots
        that are split from one key until the next.
        e.g. keys = [0, 100, 250] will result in shots (0, 99) and (100, 249).

        :param keys: List of integers representing keyframe numbers.
        :type keys: list

        :return: The shots data, split on the given keyframes.
        :rtype: ShotsDataDict
        """
        shots_data = Shots()
        for i, key in enumerate(keys):
            if i == 0:
                # skip first keyframe since we need a start and end
                continue
            shots_data.insert_shot(
                row=i-1,
                shot_name="",
                start_frame=int(keys[i-1]),
                end_frame=int(key) - 1
            )
        return shots_data

    def apply_shot(self, start_frame, end_frame, normalize):
        """
        The shot manipulation operations, based on the shot data passed.

        :param start_frame: The start frame of the shot.
        :type start_frame: int

        :param end_frame: The end frame of the shot.
        :type end_frame: int

        :param normalize: The normalization value by which to push all the keyframes back.
        :type normalize: int

        :return: List of curves that failed the keying operation, or empty list.
        :rtype: list[str]
        """
        # query all anim curves and keyframe numbers in scene
        anim_curves = cmds.ls(type=['animCurveTL', 'animCurveTA', 'animCurveTT', 'animCurveTU'])
        anim_keyframes = list(dict.fromkeys(cmds.keyframe(anim_curves, q=True)))
        anim_keyframes.sort()

        # create keys for all anim curves at the cut frames
        failed_anim_curves = []
        for anim_curve in anim_curves:
            if cmds.referenceQuery(anim_curve, inr=True):
                continue
            try:
                cmds.setKeyframe(anim_curve, t=[start_frame, end_frame], itt='linear', ott='linear')
            except:
                failed_anim_curves.append(anim_curve)

        # if needed, delete keys before and after the cut frames
        if anim_keyframes[0] < start_frame:
            cmds.cutKey(anim_curves, t=(anim_keyframes[0], start_frame-1))
        if anim_keyframes[-1] > end_frame:
            cmds.cutKey(anim_curves, t=(end_frame+1, anim_keyframes[-1]))

        # get adjusted cut positions, taking frame normalization into account
        adjust_value = 0
        if normalize is not None:
            adjust_value = normalize - start_frame
        adjusted_start_frame = start_frame + adjust_value
        adjusted_end_frame = end_frame + adjust_value

        # push all the existing animation to the correct frame
        for anim_curve in anim_curves:
            cmds.keyframe(anim_curve, e=True, r=True, tc=adjust_value)

        # set time slider range at the cut
        cmds.playbackOptions(
            min=adjusted_start_frame, ast=adjusted_start_frame,
            max=adjusted_end_frame, aet=adjusted_end_frame
        )

        return failed_anim_curves
