#!/usr/bin/env python3

import glfw
from model import Node

import transform as t
import numpy as np
import math


class RotationControlNode(Node):
    def __init__(self, key_up, key_down, axis, angle=0):
        super().__init__()
        self.angle, self.axis = angle, axis
        self.key_up, self.key_down = key_up, key_down

    def key_handler(self, key):
        self.angle += 5 * int(key == self.key_up)
        self.angle -= 5 * int(key == self.key_down)
        self.transform = t.rotate(self.axis, self.angle)
        super().key_handler(key)


# a trackball class based on provided quaternion functions -------------------
class Trackball:
    """Virtual trackball for 3D scene viewing. Independent of window system."""

    def __init__(self, yaw=0., roll=0., pitch=0., distance=3., radians=None):
        """ Build a new trackball with specified view, angles in degrees """
        self.rotation = t.quaternion_from_euler(yaw, roll, pitch, radians)
        self.distance = max(distance, 0.001)
        self.pos2d = t.vec(0.0, 0.0)

    def drag(self, old, new, winsize):
        """ Move trackball from old to new 2d normalized window position """
        old, new = ((2*t.vec(pos) - winsize) / winsize for pos in (old, new))
        self.rotation = t.quaternion_mul(self._rotate(old, new), self.rotation)

    def zoom(self, delta, size):
        """ Zoom trackball by a factor delta normalized by window size """
        self.distance = max(0.001, self.distance * (1 - 50*delta/size))

    def pan(self, old, new):
        """ Pan in camera's reference by a 2d vector factor of (new - old) """
        self.pos2d += (t.vec(new) - old) * 0.001 * self.distance

    def view_matrix(self):
        """ View matrix transformation, including distance to target point """
        return t.translate(*self.pos2d, -self.distance) @ self.matrix()

    def projection_matrix(self, winsize):
        """ Projection matrix with z-clipping range adaptive to distance """
        z_range = t.vec(0.1, 100) * self.distance  # proportion to dist
        return t.perspective(35, winsize[0] / winsize[1], *z_range)

    def matrix(self):
        """ Rotational component of trackball position """
        return t.quaternion_matrix(self.rotation)

    def _project3d(self, position2d, radius=0.8):
        """ Project x,y on sphere OR hyperbolic sheet if away from center """
        p2, r2 = sum(position2d*position2d), radius*radius
        zcoord = math.sqrt(r2 - p2) if 2*p2 < r2 else r2 / (2*math.sqrt(p2))
        return t.vec(*position2d, zcoord)

    def _rotate(self, old, new):
        """ Rotation of axis orthogonal to old & new's 3D ball projections """
        old, new = (t.normalized(self._project3d(pos)) for pos in (old, new))
        phi = 2 * math.acos(np.clip(np.dot(old, new), -1, 1))
        return t.quaternion_from_axis_angle(np.cross(old, new), radians=phi)


# ------------  Viewer class & window management ------------------------------
class GLFWTrackball(Trackball):
    """ Use in Viewer for interactive viewpoint control """

    def __init__(self, win):
        """ Init needs a GLFW window handler 'win' to register callbacks """
        super().__init__()
        self.mouse = (0, 0)
        glfw.set_cursor_pos_callback(win, self.on_mouse_move)
        glfw.set_scroll_callback(win, self.on_scroll)

    def on_mouse_move(self, win, xpos, ypos):
        """ Rotate on left-click & drag, pan on right-click & drag """
        old = self.mouse
        self.mouse = (xpos, glfw.get_window_size(win)[1] - ypos)
        if glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_LEFT):
            self.drag(old, self.mouse, glfw.get_window_size(win))
        if glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_RIGHT):
            self.pan(old, self.mouse)

    def on_scroll(self, win, _deltax, deltay):
        """ Scroll controls the camera distance to trackball center """
        self.zoom(deltay, glfw.get_window_size(win)[1])
