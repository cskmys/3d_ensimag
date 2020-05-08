import objects as o
import transform as t
from model import Node
from anim import ObjectKeyFrameControlNode


def get_skybox_node(skybox_shader):
    skybox_shape = Node()
    skybox_shape.add(o.Skybox(skybox_shader))
    return skybox_shape


def get_scr_node(screen_shader, width, height):
    screen_shape = Node()
    screen_shape.add(o.Framebuffer(screen_shader, width, height))
    return screen_shape


# def get_world_node(world_shader):
#     # # ['ReefFish12', 'TinyYellowFish', 'YellowTang', 'Barracuda', 'ReefFish17', 'ReefFish14',
#     # # 'BlueStarfish', 'BottlenoseDolphin', 'GiantGrouper', 'ClownFish2', 'ReefFish16', 'ReefFish8',
#     # # 'NurseShark', 'ReefFish20', 'SeaHorse', 'LionFish', 'WhaleShark', 'ReefFish7', 'ReefFish3',
#     # # 'BlueTang', 'ReefFish5', 'ReefFish0', 'ReefFish4', 'SeaSnake']
#
#     reef_fish_shape = []
#     for i in range(3):
#         reef_fish_shape.append(Node(transform=t.translate(0.25 * (i + 5), 0.0, 0.0) @ t.scale(0.5)))
#         reef_fish_shape[i].add(o.Fish(world_shader, 'ReefFish5'))
#
#     reef_fish_translate_keys = {0: t.vec(0, 0, 0)}
#     reef_fish_rotate_keys = {0: t.quaternion(),
#                              2: t.quaternion_from_euler(0, 0, 0),
#                              4: t.quaternion_from_euler(0, 0, 0)}
#     reef_fish_scale_keys = {0: 1}
#     reef_keynode = ObjectKeyFrameControlNode(reef_fish_translate_keys, reef_fish_rotate_keys, reef_fish_scale_keys)
#     reef_keynode.add(*reef_fish_shape)
#
#
#     blue_tang_shape = []
#     for i in range(3):
#         blue_tang_shape.append(Node(transform=t.translate(0.25 * (i - 5), 0.0, 0.0) @ t.scale(0.5)))
#         blue_tang_shape[i].add(o.Fish(world_shader, 'BlueTang'))
#
#     blue_tang_translate_keys = {0: t.vec(0, 0, 0)}
#     blue_tang_rotate_keys = {0: t.quaternion(),
#                              # 2: t.quaternion_from_euler(360, 0, 0),
#                              # 4: t.quaternion_from_euler(180, 0, 0)}
#                              2: t.quaternion_from_euler(0, 0, 0),
#                              4: t.quaternion_from_euler(0, 0, 0)}
#
#     blue_tang_scale_keys = {0: 1}
#     blue_tang_keynode = ObjectKeyFrameControlNode(blue_tang_translate_keys, blue_tang_rotate_keys, blue_tang_scale_keys)
#     blue_tang_keynode.add(*blue_tang_shape)
#
#
#     world_shape = Node()
#     # not animation
#     # world_shape.add(*reef_fish_shape, *blue_tang_shape)
#     # animate only reef
#     # world_shape.add(reef_keynode, *blue_tang_shape)
#     # animate both reef and bluetang
#     world_shape.add(reef_keynode, blue_tang_keynode)
#
#     return world_shape

import boid as b
import numpy as np
# def get_world_node(world_shader):
#     # # ['ReefFish12', 'TinyYellowFish', 'YellowTang', 'Barracuda', 'ReefFish17', 'ReefFish14',
#     # # 'BlueStarfish', 'BottlenoseDolphin', 'GiantGrouper', 'ClownFish2', 'ReefFish16', 'ReefFish8',
#     # # 'NurseShark', 'ReefFish20', 'SeaHorse', 'LionFish', 'WhaleShark', 'ReefFish7', 'ReefFish3',
#     # # 'BlueTang', 'ReefFish5', 'ReefFish0', 'ReefFish4', 'SeaSnake']
#
#     reef_boid_shape = b.get_boid(world_shader, 'ReefFish17', 10, np.array([1, 1, 0]), np.array([5, 5, 0]))
#
#     lion_boid_shape = b.get_boid(world_shader, 'Lionfish', 10, np.array([5, 1, 0]), np.array([9, 5, 0]))
#
#     world_shape = Node()
#     world_shape.add(*reef_boid_shape, *lion_boid_shape)
#
#     return world_shape
from anim import ProceduralAnim
import glfw


def sin_motion():
    trans_mat = t.translate(0, np.sin(glfw.get_time()), 0)
    keyframe_transform = trans_mat
    return keyframe_transform


def get_world_node(world_shader):
    # # ['ReefFish12', 'TinyYellowFish', 'YellowTang', 'Barracuda', 'ReefFish17', 'ReefFish14',
    # # 'BlueStarfish', 'BottlenoseDolphin', 'GiantGrouper', 'ClownFish2', 'ReefFish16', 'ReefFish8',
    # # 'NurseShark', 'ReefFish20', 'SeaHorse', 'LionFish', 'WhaleShark', 'ReefFish7', 'ReefFish3',
    # # 'BlueTang', 'ReefFish5', 'ReefFish0', 'ReefFish4', 'SeaSnake']

    reef_boid_shape = b.get_boid(world_shader, 'ReefFish17', 10, np.array([1, 1, 0]), np.array([5, 5, 0]))
    reef_boid_keynode = ProceduralAnim(sin_motion)
    reef_boid_keynode.add(*reef_boid_shape)
    world_shape = Node()
    world_shape.add(reef_boid_keynode)

    return world_shape
