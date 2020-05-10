import numpy as np
import transform as t
import objects as o
from model import Node

boid_cnt = 10


def new_flock(count, lower_limits, upper_limits):
    width = upper_limits - lower_limits
    return (lower_limits[:, np.newaxis] + np.random.rand(3, count) * width[:, np.newaxis]).T


positions = new_flock(boid_cnt, np.array([10, 90, 0]), np.array([20, 110, 0]))


def get_boid(shader, fish, count, lower_limits, upper_limits, rot_axis=(0.0, 0.0, 0.0), rot_angle=0.0, scale=1.0):
    boid_shape = []
    positions = new_flock(count, lower_limits, upper_limits)
    for i in range(count):
        boid_shape.append(Node(transform=t.translate(positions[i][0], positions[i][1], positions[i][2]) @ t.rotate(rot_axis, rot_angle) @ t.scale(scale)))
        boid_shape[i].add(o.Fish(shader, fish))
    return boid_shape
