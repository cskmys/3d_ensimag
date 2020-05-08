#!/usr/bin/env python3

from bisect import bisect_left
import transform as t
import glfw

from model import Node


class KeyFrames:
    """ Stores keyframe pairs for any value type with interpolation_function"""
    def __init__(self, time_value_pairs, interpolation_function=t.lerp):
        if isinstance(time_value_pairs, dict):  # convert to list of pairs
            time_value_pairs = time_value_pairs.items()
        keyframes = sorted(((key[0], key[1]) for key in time_value_pairs))
        self.times, self.values = zip(*keyframes)  # pairs list -> 2 lists
        self.interpolate = interpolation_function

    def value(self, time):
        """ Computes interpolated value from keyframes, for a given time """
        if time <= self.times[0]:
            return self.values[0]
        if time >= self.times[-1]:
            return self.values[-1]
        # 2. search for closest index entry in self.times, using bisect_left function
        idx = bisect_left(self.times, time)
        # 3. using the retrieved index, interpolate between the two neighboring values
        val = self.interpolate(self.values[idx-1], self.values[idx], (time - self.times[idx-1])/(self.times[idx]-self.times[idx-1]))
        # in self.values, using the initially stored self.interpolate function
        return val


class TransformKeyFrames:
    """ KeyFrames-like object dedicated to 3D transforms """

    def __init__(self, translate_keys, rotate_keys, scale_keys):
        """ stores 3 keyframe sets for translation, rotation, scale """
        self.translate_keys = KeyFrames(translate_keys)
        self.rotate_keys = KeyFrames(rotate_keys, t.quaternion_slerp)
        self.scale_keys = KeyFrames(scale_keys)

    def value(self, time):
        """ Compute each component's interpolation and compose TRS matrix """
        trans_mat = t.translate(self.translate_keys.value(time))
        rot_mat = t.quaternion_matrix(self.rotate_keys.value(time))
        scale_mat = t.scale(self.scale_keys.value(time))
        keyframe_transform = trans_mat @ (rot_mat @ scale_mat)
        return keyframe_transform


class ObjectKeyFrameControlNode(Node):
    """ Place node with transform keys above a controlled subtree """
    def __init__(self, translate_keys, rotate_keys, scale_keys):
        super().__init__()
        self.keyframes = TransformKeyFrames(translate_keys, rotate_keys, scale_keys)

    def draw(self, projection, view, model):
        """ When redraw requested, interpolate our node transform from keys """
        self.transform = self.keyframes.value(glfw.get_time())  # transform belongs to parent class i,e, Node
        super().draw(projection, view, model)

    def key_handler(self, key):
        if key == glfw.KEY_SPACE:
            glfw.set_time(0)
            super().key_handler(key)


class ProceduralAnim(Node):
    """ Place node with transform keys above a controlled subtree """
    def __init__(self, anim_func):
        super().__init__()
        self.gen_keyframe = anim_func

    def draw(self, projection, view, model):
        """ When redraw requested, interpolate our node transform from keys """
        self.transform = self.gen_keyframe()  # transform belongs to parent class i,e, Node
        super().draw(projection, view, model)


class CameraKeyFrameControlNode(Node):
    """ Place node with transform keys above a controlled subtree """
    def __init__(self, translate_keys, rotate_keys, scale_keys):
        super().__init__()
        self.keyframes = TransformKeyFrames(translate_keys, rotate_keys, scale_keys)

    def draw(self, projection, view, model):
        """ When redraw requested, interpolate our node transform from keys """
        self.transform = self.keyframes.value(glfw.get_time())  # transform belongs to parent class i,e, Node
        super().draw(projection, view, model)

    def key_handler(self, key):
        glfw.set_time(0)
        super().key_handler(key)
