#!/usr/bin/env python3

import OpenGL.GL as GL  # standard Python OpenGL wrapper
import glfw  # lean window system wrapper for OpenGL
import transform as t
import sh_var_lst as svl
import nodes as n

from itertools import cycle
from model import Node
from gpu import Shader
from camera import init_camera  # GLFWTrackball

SCR_WIDTH = 1280
SCR_HEIGHT = 720


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

        # initialize camera
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
            GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
            GL.glEnable(GL.GL_DEPTH_TEST)
            GL.glEnable(GL.GL_CULL_FACE)  # backface culling enabled (TP2)
            GL.glDepthMask(GL.GL_TRUE)

            GL.glClearColor(0.1, 0.1, 0.1, 1.0)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            win_size = glfw.get_window_size(self.win)
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


# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer(SCR_WIDTH, SCR_HEIGHT)
    world_shader = Shader(svl.world_shader['vs'], svl.world_shader['fs'])
    skybox_shader = Shader(svl.skybox_shader['vs'], svl.skybox_shader['fs'])
    screen_shader = Shader(svl.screen_shader['vs'], svl.screen_shader['fs'])

    screen_shape = n.get_scr_node(screen_shader, SCR_WIDTH, SCR_HEIGHT)

    skybox_shape = n.get_skybox_node(skybox_shader)

    world_shape = n.get_world_node(world_shader)

    # FOLLOW THIS ORDER STRICTLY IF YOU WANT EVERYTHING TO WORK
    viewer.add(screen_shape, skybox_shape, world_shape)
    # viewer.add(world_shape)
    viewer.run()


if __name__ == '__main__':
    glfw.init()  # initialize window system glfw
    main()  # main function keeps variables locally scoped
    glfw.terminate()  # destroy all glfw windows and GL contexts
