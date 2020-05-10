import objects as o
import transform as t
import boid as b
import numpy as np

from anim import ProceduralAnim
from model import Node
from anim import ObjectKeyFrameControlNode

import glfw


def get_skybox_node(skybox_shader):
    skybox_shape = Node()
    skybox_shape.add(o.Skybox(skybox_shader))
    return skybox_shape


def get_scr_node(screen_shader, width, height):
    screen_shape = Node()
    screen_shape.add(o.Framebuffer(screen_shader, width, height))
    return screen_shape


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


def circA_motion():
    r = 5
    speed = 5
    angle = (glfw.get_time() * speed) % 360
    angle = 180 + angle
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
    # axis_shape = Node(transform=t.translate(0.0, 0.0, 0.0) @ t.scale(0.1))
    # axis_shape.add(o.Axis(world_shader))

    starfish_boid_shape = b.get_boid(world_shader, 'BlueStarfish', 5,
                                     np.array([-10.0, -10.0, -10.0]), np.array([10.0, -10.0, 10.0]))

    seahorse_shape = Node(transform=t.translate(-12.5, 1.0, -1.0) @ t.scale(scale * 2))
    seahorse_shape.add(o.Fish(world_shader, 'Seahorse'))
    seahorse_animnode = ProceduralAnim(sin_motion)
    seahorse_animnode.add(seahorse_shape)

    clownfish_boid_shape = b.get_boid(world_shader, 'ClownFish2', 25, np.array([-4, -2, -10]), np.array([4, 2, -12]),
                                      rot_axis=(0, 1, 0), rot_angle=-90)
    gaintgrouper_shape = Node(transform=t.translate(8, 0, -9) @ t.rotate((0, 1, 0), -100) @ t.scale(scale*2))
    gaintgrouper_shape.add(o.Fish(world_shader, 'GiantGrouper'))
    clownfish_boid_animnode = ProceduralAnim(fig8_motion)
    clownfish_boid_animnode.add(*clownfish_boid_shape, gaintgrouper_shape)

    reeffish_boid_shape = b.get_boid(world_shader, 'reeffish17', 50, np.array([-20, -5, -2]), np.array([20, 5, 2]),
                                     rot_axis=(0, 1, 0), rot_angle=90, scale=scale*0.25)
    reeffish_boid_animnode = ProceduralAnim(circ_motion)
    reeffish_boid_animnode.add(*reeffish_boid_shape)

    whaleshark_pos = (50, 5, -100)
    whaleshark_shape = Node(transform=t.translate(whaleshark_pos) @ t.rotate((0, 1, 0), -20) @ t.scale(scale * 2))
    whaleshark_shape.add(o.Fish(world_shader, 'whaleshark'))
    whaleshark_translate_keys = {0: t.vec(whaleshark_pos),
                                 15: t.vec(-100, -10, 210)}
    whaleshark_rotate_keys = {0: t.quaternion()}
    whaleshark_scale_keys = {0: 1,
                             15: 1,
                             16: 0.1}
    whaleshark_keynode = ObjectKeyFrameControlNode(whaleshark_translate_keys, whaleshark_rotate_keys,
                                                   whaleshark_scale_keys)
    whaleshark_keynode.add(whaleshark_shape)

    lionfish_shape = Node(transform=t.translate(15, 1.0, -1.0)  @ t.rotate((0, 1, 0), 180) @ t.scale(scale))
    lionfish_shape.add(o.Fish(world_shader, 'lionfish'))
    lionfish_translate_keys = {0: t.vec(0, 0, 0),
                               8: t.vec(1, 0, -2),
                               10: t.vec(10, 0, 0)}
    lionfish_rotate_keys = {0: t.quaternion()}
    lionfish_scale_keys = {0: 1,
                           9: 1,
                           10: 0.001}
    lionfish_keynode = ObjectKeyFrameControlNode(lionfish_translate_keys, lionfish_rotate_keys, lionfish_scale_keys)
    lionfish_keynode.add(lionfish_shape)
    lionfish_animnode = ProceduralAnim(sin_motion)
    lionfish_animnode.add(lionfish_keynode)

    reeffishA_boid_shape = b.get_boid(world_shader, 'reeffish17', 50, np.array([-20, -5, -2]), np.array([20, 5, 2]),
                                      rot_axis=(0, 1, 0), rot_angle=90, scale=scale*0.25)
    reeffishA_boid_animnode = ProceduralAnim(circA_motion)
    reeffishA_boid_animnode.add(*reeffishA_boid_shape)

    world_shape = Node()
    # world_shape.add(axis_shape, *starfish_boid_shape, lionfish_animnode, whaleshark_keynode, seahorse_animnode,
    #                 clownfish_boid_animnode, reeffish_boid_animnode, reeffishA_boid_animnode)
    world_shape.add(*starfish_boid_shape, lionfish_animnode, whaleshark_keynode, seahorse_animnode,
                    clownfish_boid_animnode, reeffish_boid_animnode, reeffishA_boid_animnode)
    return world_shape
