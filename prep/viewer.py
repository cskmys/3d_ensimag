#!/usr/bin/env python3
import os
import OpenGL.GL as GL  # standard Python OpenGL wrapper
import glfw  # lean window system wrapper for OpenGL
from itertools import cycle
from transform import Trackball, identity, rotate, translate, scale, vec, lerp, quaternion_slerp, quaternion_matrix, quaternion, quaternion_from_euler

from gpu import Shader
from model import Node
from control import GLFWTrackball
from loaders import load_model
from anim import KeyFrameControlNode


class Viewer(Node):
    """ GLFW viewer window, with classic initialization & graphics loop """

    def __init__(self, width=640, height=480):
        super().__init__()

        # version hints: create GL window with >= OpenGL 3.3 and core profile
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, False)
        self.win = glfw.create_window(width, height, 'Viewer', None, None)

        # make win's OpenGL context current; no OpenGL calls can happen before
        glfw.make_context_current(self.win)

        # register event handlers
        glfw.set_key_callback(self.win, self.on_key)

        # useful message to check OpenGL renderer characteristics
        print('OpenGL', GL.glGetString(GL.GL_VERSION).decode() + ', GLSL',
              GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode() +
              ', Renderer', GL.glGetString(GL.GL_RENDERER).decode())

        # initialize GL by setting viewport and default render characteristics
        GL.glClearColor(0.1, 0.1, 0.1, 0.1)
        GL.glEnable(GL.GL_DEPTH_TEST)  # depth test now enabled (TP2)
        GL.glEnable(GL.GL_CULL_FACE)  # backface culling enabled (TP2)

        # initialize trackball
        self.trackball = GLFWTrackball(self.win)

        # cyclic iterator to easily toggle polygon rendering modes
        self.fill_modes = cycle([GL.GL_LINE, GL.GL_POINT, GL.GL_FILL])

    def run(self):
        """ Main render loop for this OpenGL window """
        while not glfw.window_should_close(self.win):
            # clear draw buffer and depth buffer (<-TP2)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            win_size = glfw.get_window_size(self.win)
            view = self.trackball.view_matrix()
            projection = self.trackball.projection_matrix(win_size)

            # draw our scene objects
            self.draw(projection, view, identity())

            # flush render commands, and swap draw buffers
            glfw.swap_buffers(self.win)

            # Poll for and process events
            glfw.poll_events()

    def on_key(self, _win, key, _scancode, action, _mods):
        """ 'Q' or 'Escape' quits """
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_ESCAPE or key == glfw.KEY_Q:
                glfw.set_window_should_close(self.win, True)
            if key == glfw.KEY_W:
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, next(self.fill_modes))

            self.key_handler(key)


class Suzy(Node):
    def __init__(self, shader, light_dir):
        super().__init__()
        self.add(*[mesh for mesh in load_phong_mesh('suzzane.obj', shader, light_dir)])


class Fish(Node):
    def __init__(self, shader, Name):
        super().__init__()
        light_dir = (0, -1, 0)
        for root, dirs, files in os.walk('./Fish'):
            for dir in dirs:
                if dir.lower() == Name.lower():
                    for root, dirs, files in os.walk(os.path.join(root, dir)):
                        for file in files:
                            if str(file).split('.')[1] == 'obj':
                                self.add(*[mesh for mesh in load_model(os.path.join(root, file), shader, light_dir)])
                                return
        raise Exception('Fish ' + Name + ' not found')


# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    shader = Shader("prep.vert", "prep.frag")
    # ['ReefFish12', 'TinyYellowFish', 'YellowTang', 'Barracuda', 'ReefFish17', 'ReefFish14',
    # 'BlueStarfish', 'BottlenoseDolphin', 'GiantGrouper', 'ClownFish2', 'ReefFish16', 'ReefFish8',
    # 'NurseShark', 'ReefFish20', 'SeaHorse', 'LionFish', 'WhaleShark', 'ReefFish7', 'ReefFish3',
    # 'BlueTang', 'ReefFish5', 'ReefFish0', 'ReefFish4', 'SeaSnake']

    tPlane = Fish(shader, 'ReefFish5')
    # translate_keys = {0: vec(0, 0, 0), 2: vec(1, 1, 0), 4: vec(0, 0, 0)}
    # rotate_keys = {0: quaternion(), 2: quaternion_from_euler(180, 45, 90),
    #                3: quaternion_from_euler(180, 0, 180), 4: quaternion()}
    # scale_keys = {0: 1, 2: 0.5, 4: 1}
    translate_keys = {0: vec(0, 0, 0)}
    rotate_keys = {0: quaternion(),
                   2: quaternion_from_euler(180, 0, 0),
                   4: quaternion_from_euler(360, 0, 0)}
    scale_keys = {0: 1}
    keynode = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
    keynode.add(tPlane)

    viewer.add(keynode)
    viewer.run()


if __name__ == '__main__':
    glfw.init()  # initialize window system glfw
    main()  # main function keeps variables locally scoped
    glfw.terminate()  # destroy all glfw windows and GL contexts
