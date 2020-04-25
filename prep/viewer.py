#!/usr/bin/env python3
import os
import OpenGL.GL as GL  # standard Python OpenGL wrapper
import glfw  # lean window system wrapper for OpenGL
from itertools import cycle
import transform as t

from gpu import Shader
from model import Node
from camera import init_camera  # GLFWTrackball
from loaders import load_model
from anim import ObjectKeyFrameControlNode


class Viewer(Node):
    """ GLFW viewer window, with classic initialization & graphics loop """

    def __init__(self, width=640, height=480):
        super().__init__()

        # version hints: create GL window with >= OpenGL 3.3 and core profile
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        self.win = glfw.create_window(width, height, 'Viewer', None, None)
        glfw.set_input_mode(self.win, glfw.CURSOR, glfw.CURSOR_DISABLED)
        # make win's OpenGL context current; no OpenGL calls can happen before
        glfw.make_context_current(self.win)

        # register event handlers
        glfw.set_key_callback(self.win, self.on_key)
        glfw.set_cursor_pos_callback(self.win, self.mouse_callback)
        glfw.set_scroll_callback(self.win, self.scroll_callback)
        glfw.set_framebuffer_size_callback(self.win, self.framebuffer_size_callback)

        # useful message to check OpenGL renderer characteristics
        print('OpenGL', GL.glGetString(GL.GL_VERSION).decode() + ', GLSL',
              GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode() +
              ', Renderer', GL.glGetString(GL.GL_RENDERER).decode())

        GL.glViewport(0, 0, width, height)
        # initialize GL by setting viewport and default render characteristics
        GL.glClearColor(0.1, 0.1, 0.1, 0.1)
        GL.glEnable(GL.GL_DEPTH_TEST)  # depth test now enabled (TP2)
        GL.glEnable(GL.GL_CULL_FACE)  # backface culling enabled (TP2)

        # initialize trackball
        # self.trackball = GLFWTrackball(self.win)
        self.camera = init_camera(position=t.vec(0.0, 0.0, 3.0))
        # cyclic iterator to easily toggle polygon rendering modes
        self.fill_modes = cycle([GL.GL_LINE, GL.GL_POINT, GL.GL_FILL])

        self.last_mouse_pos = [width/2, height/2]
        self.first_mouse = True

        self.delta_time = 0
        self.last_frame = 0

    def run(self):
        """ Main render loop for this OpenGL window """
        while not glfw.window_should_close(self.win):
            current_frame = glfw.get_time()
            self.delta_time = current_frame - self.last_frame
            self.last_frame = current_frame - self.last_frame
            # clear draw buffer and depth buffer (<-TP2)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            win_size = glfw.get_window_size(self.win)
            # view = self.trackball.view_matrix()
            # projection = self.trackball.projection_matrix(win_size)
            view = self.camera.get_view_matrix()
            projection = t.perspective(self.camera.Zoom, win_size[0] / win_size[1], 0.1, 100.0)

            # draw our scene objects
            self.draw(projection, view, t.identity())

            # flush render commands, and swap draw buffers
            glfw.swap_buffers(self.win)

            # Poll for and process events
            glfw.poll_events()

    def on_key(self, _win, key, _scancode, action, _mods):
        """ 'Q' or 'Escape' quits """
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_ESCAPE or key == glfw.KEY_Q:
                glfw.set_window_should_close(self.win, True)

            self.key_handler(key)
            if key == glfw.KEY_LEFT_ALT:
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, next(self.fill_modes))
            if key == glfw.KEY_W:
                self.camera.process_keyboard('FORWARD', self.delta_time)
            if key == glfw.KEY_S:
                self.camera.process_keyboard('BACKWARD', self.delta_time)
            if key == glfw.KEY_A:
                self.camera.process_keyboard('LEFT', self.delta_time)
            if key == glfw.KEY_D:
                self.camera.process_keyboard('RIGHT', self.delta_time)


    def mouse_callback(self, _win, xpos, ypos):
        """ Rotate on left-click & drag, pan on right-click & drag """
        if self.first_mouse is True:
            self.last_mouse_pos[0] = xpos
            self.last_mouse_pos[1] = ypos
            self.first_mouse = False
        x_offset = xpos - self.last_mouse_pos[0]
        y_offset = self.last_mouse_pos[1] - ypos
        self.last_mouse_pos = [xpos, ypos]
        self.camera.process_mouse_movement(x_offset, y_offset)

    def scroll_callback(self, _win, _deltax, deltay):
        """ Scroll controls the camera distance to trackball center """
        self.camera.process_mouse_scroll(deltay)

    def framebuffer_size_callback(self, _win, width, height):
        GL.glViewport(0, 0, width, height)


class Suzy(Node):
    def __init__(self, shader, light_dir):
        super().__init__()
        self.add(*[mesh for mesh in load_model('suzzane.obj', shader, light_dir)])


class Fish(Node):
    def __init__(self, shader, name, light_dir=(0, -1, 0)):
        super().__init__()
        for root, dirs, files in os.walk('./Fish'):
            for obj_dir in dirs:
                if obj_dir.lower() == name.lower():
                    for root, dirs, files in os.walk(os.path.join(root, obj_dir)):
                        for file in files:
                            if str(file).split('.')[1] == 'obj':
                                self.add(*[mesh for mesh in load_model(os.path.join(root, file), shader, light_dir)])
                                return
        raise Exception('Fish ' + name + ' not found')


# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    shader = Shader("prep.vert", "prep.frag")
    # ['ReefFish12', 'TinyYellowFish', 'YellowTang', 'Barracuda', 'ReefFish17', 'ReefFish14',
    # 'BlueStarfish', 'BottlenoseDolphin', 'GiantGrouper', 'ClownFish2', 'ReefFish16', 'ReefFish8',
    # 'NurseShark', 'ReefFish20', 'SeaHorse', 'LionFish', 'WhaleShark', 'ReefFish7', 'ReefFish3',
    # 'BlueTang', 'ReefFish5', 'ReefFish0', 'ReefFish4', 'SeaSnake']

    fish_shape = Node(transform=t.translate(0.0, 0.0, 0.0) @ t.scale(0.5))
    fish_shape.add(Fish(shader, 'ReefFish5'))
    translate_keys = {0: t.vec(0, 0, 0)}
    rotate_keys = {0: t.quaternion(),
                   2: t.quaternion_from_euler(180, 0, 0),
                   4: t.quaternion_from_euler(360, 0, 0)}
    scale_keys = {0: 1}
    keynode = ObjectKeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
    keynode.add(fish_shape)

    viewer.add(keynode)
    viewer.run()


if __name__ == '__main__':
    glfw.init()  # initialize window system glfw
    main()  # main function keeps variables locally scoped
    glfw.terminate()  # destroy all glfw windows and GL contexts
