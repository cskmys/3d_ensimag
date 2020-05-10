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
#                              2: t.quaternion_from_euler(180, 0, 0),
#                              4: t.quaternion_from_euler(360, 0, 0)}
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
#                              2: t.quaternion_from_euler(360, 0, 0),
#                              4: t.quaternion_from_euler(180, 0, 0)}
#                              # 2: t.quaternion_from_euler(0, 0, 0),
#                              # 4: t.quaternion_from_euler(0, 0, 0)}
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


def fig8_motion():
    r = 50
    speed = 100
    angle = (glfw.get_time() * speed) % 360
    x = r * np.cos(np.deg2rad(angle))
    y = r/20 * (np.cos(np.deg2rad(angle)) + np.sin(np.deg2rad(angle)))
    z = r * np.sin(np.deg2rad(angle))

    trans_mat = t.rotate((0, 1, 0), 90 + angle) @ t.translate(x, y, z)
    keyframe_transform = trans_mat
    return keyframe_transform


def circ_motion():
    r = 5
    speed = 5
    angle = (glfw.get_time() * speed) % 360
    x = r * np.cos(np.deg2rad(angle))
    y = r/2 * np.sin(np.deg2rad(angle))
    z = r * np.sin(np.deg2rad(angle))
    trans_mat = t.translate(x, y, z) @ t.rotate((0, 1, 0), 270 - angle)
    keyframe_transform = trans_mat
    return keyframe_transform


def get_world_node(world_shader):
    #     fish_lst = ['ReefFish12', 'TinyYellowFish', 'YellowTang', 'Barracuda', 'ReefFish17',
    #                 'ReefFish14', 'BlueStarfish', 'BottlenoseDolphin', 'GiantGrouper', 'ClownFish2',
    #                 'ReefFish16', 'ReefFish8', 'NurseShark', 'ReefFish20', 'SeaHorse',
    #                 'LionFish', 'WhaleShark', 'ReefFish7', 'ReefFish3', 'BlueTang',
    #                 'ReefFish5', 'ReefFish0', 'ReefFish4', 'SeaSnake']
    scale = 0.5
    axis_shape = Node(transform=t.translate(0.0, 0.0, 0.0) @ t.scale(10000))
    axis_shape.add(o.Axis(world_shader))

    starfish_boid_shape = b.get_boid(world_shader, 'BlueStarfish', 5, np.array([-10.0, -10.0, -10.0]), np.array([10.0, -10.0, 10.0]))

    seahorse_shape = Node(transform=t.translate(-12.5, 1.0, -1.0) @ t.scale(scale * 2))
    seahorse_shape.add(o.Fish(world_shader, 'Seahorse'))
    seahorse_animnode = ProceduralAnim(sin_motion)
    seahorse_animnode.add(seahorse_shape)

    clownfish_boid_shape = b.get_boid(world_shader, 'ClownFish2', 25, np.array([-4, -2, -10]), np.array([4, 2, -12]), rot_axis=(0, 1, 0), rot_angle=-90)
    gaintgrouper_shape = Node(transform=t.translate(8, 0, -9) @ t.rotate((0, 1, 0), -100) @ t.scale(scale*2))
    gaintgrouper_shape.add(o.Fish(world_shader, 'GiantGrouper'))
    clownfish_boid_animnode = ProceduralAnim(fig8_motion)
    clownfish_boid_animnode.add(*clownfish_boid_shape, gaintgrouper_shape)

    reeffish_boid_shape = b.get_boid(world_shader, 'reeffish17', 50, np.array([-20, -5, -2]), np.array([20, 5, 2]), rot_axis=(0, 1, 0), rot_angle=90, scale=scale*0.25)
    reeffish_boid_animnode = ProceduralAnim(circ_motion)
    reeffish_boid_animnode.add(*reeffish_boid_shape)

    whaleshark_shape = Node(transform=t.translate(50, -5, -200) @ t.scale(scale * 2))
    whaleshark_shape.add(o.Fish(world_shader, 'whaleshark'))
    # whaleshark_keynode = ObjectKeyFrameControlNode

    world_shape = Node()
    world_shape.add(axis_shape, *starfish_boid_shape, seahorse_animnode, clownfish_boid_animnode, reeffish_boid_animnode, whaleshark_shape)
    return world_shape


# def get_world_node(world_shader):
#     fish_lst = ['ReefFish12', 'TinyYellowFish', 'YellowTang', 'Barracuda', 'ReefFish17',
#                 'ReefFish14', 'BlueStarfish', 'BottlenoseDolphin', 'GiantGrouper', 'ClownFish2',
#                 'ReefFish16', 'ReefFish8', 'NurseShark', 'ReefFish20', 'SeaHorse',
#                 'LionFish', 'WhaleShark', 'ReefFish7', 'ReefFish3', 'BlueTang',
#                 'ReefFish5', 'ReefFish0', 'ReefFish4', 'SeaSnake']
#
#     cube_siz = 5
#     boid_lst = list()
#     for i in range(5):
#         for j in range(5):
#             try:
#                 boid_shape = b.get_boid(world_shader, fish_lst[(i * 5) + j], i+1, np.array([(i*cube_siz), 0, (j*cube_siz)]),
#                                         np.array([((i+1) * cube_siz) - 1, 0, ((j+1) * cube_siz) - 1]))
#                 boid_lst.append(boid_shape)
#             except Exception:
#                 break
#     boid_shape_list = [item for sublist in boid_lst for item in sublist]
#
#     boid_lst_keynode = ProceduralAnim(sin_motion)
#     boid_lst_keynode.add(*boid_shape_list)
#
#     world_shape = Node()
#     world_shape.add(boid_lst_keynode)
#
#     return world_shape
