#!/usr/bin/env python3
"""
Python OpenGL practical application.
"""
# Python built-in modules
import os                           # os function, i.e. checking file status

# External, non built-in modules
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args
import ctypes


# ------------ low level OpenGL object wrappers ----------------------------
class Shader:
    """ Helper class to create and automatically destroy shader program """
    @staticmethod
    def _compile_shader(src, shader_type):
        src = open(src, 'r').read() if os.path.exists(src) else src
        src = src.decode('ascii') if isinstance(src, bytes) else src
        shader = GL.glCreateShader(shader_type)
        GL.glShaderSource(shader, src)
        GL.glCompileShader(shader)
        status = GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS)
        src = ('%3d: %s' % (i+1, l) for i, l in enumerate(src.splitlines()))
        if not status:
            log = GL.glGetShaderInfoLog(shader).decode('ascii')
            GL.glDeleteShader(shader)
            src = '\n'.join(src)
            print('Compile failed for %s\n%s\n%s' % (shader_type, log, src))
            return None
        return shader

    def __init__(self, vertex_source, fragment_source):
        """ Shader can be initialized with raw strings or source file names """
        self.glid = None
        vert = self._compile_shader(vertex_source, GL.GL_VERTEX_SHADER)
        frag = self._compile_shader(fragment_source, GL.GL_FRAGMENT_SHADER)
        if vert and frag:
            self.glid = GL.glCreateProgram()  # pylint: disable=E1111
            GL.glAttachShader(self.glid, vert)
            GL.glAttachShader(self.glid, frag)
            GL.glLinkProgram(self.glid)
            GL.glDeleteShader(vert)
            GL.glDeleteShader(frag)
            status = GL.glGetProgramiv(self.glid, GL.GL_LINK_STATUS)
            if not status:
                print(GL.glGetProgramInfoLog(self.glid).decode('ascii'))
                GL.glDeleteProgram(self.glid)
                self.glid = None

    def __del__(self):
        GL.glUseProgram(0)
        if self.glid:                      # if this is a valid shader object
            GL.glDeleteProgram(self.glid)  # object dies => destroy GL object


vertices = np.array(((0.5, 0.5, 0.0), (1.0, 0.0, 0.0),
                    (0.5, -0.5, 0.0), (0.0, 1.0, 0.0),
                    (-0.5, -0.5, 0.0), (0.0, 0.0, 1.0),
                    (-0.5,  0.5, 0.0), (1.0,  0.0, 0.0)), 'f')

indices = np.array((0, 1, 3, 1, 2, 3), np.uint32)

positions = np.array(((0.5, 0.5, 0.0), (1.0, 0.0, 0.0),  # 0
                          (0.5, -0.5, 0.0), (1.0, 0.0, 0.0),  # 1
                          (-0.5, 0.5, 0.0), (1.0, 0.0, 0.0),  # 3
                          (0.5, -0.5, 0.0), (0.0, 1.0, 0.0),  # 1
                          (-0.5, -0.5, 0.0), (0.0, 1.0, 0.0),  # 2
                          (-0.5, 0.5, 0.0), (0.0, 1.0, 0.0)),  # 3
                         'f')


class SimpleSolidRectangle:
    """Hello triangle object"""

    def __init__(self, shader):
        self.shader = shader

        GL.glUseProgram(shader.glid)

        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)
        self.vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)

        GL.glBufferData(GL.GL_ARRAY_BUFFER, positions, GL.GL_STATIC_DRAW)

        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, 6 * np.dtype(np.float32).itemsize, ctypes.c_void_p(0 * np.dtype(np.float32).itemsize))
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, False, 6 * np.dtype(np.float32).itemsize, ctypes.c_void_p(3 * np.dtype(np.float32).itemsize))
        GL.glEnableVertexAttribArray(0)
        GL.glEnableVertexAttribArray(1)

        # cleanup and unbind so no accidental subsequent state update
        GL.glBindVertexArray(0)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

    def draw(self, projection, view, model):
        GL.glUseProgram(self.shader.glid)

        GL.glBindVertexArray(self.vao)

        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)

        GL.glBindVertexArray(0)

    def __del__(self):
        GL.glDeleteVertexArrays(1, self.vao)
        GL.glDeleteBuffers(1, self.vbo)


class SimpleRectangle:
    """Hello triangle object"""

    def __init__(self, shader):
        self.shader = shader

        GL.glUseProgram(shader.glid)

        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)
        self.vbo = GL.glGenBuffers(1)
        self.ebo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ebo)

        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices, GL.GL_STATIC_DRAW)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices, GL.GL_STATIC_DRAW)

        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, 6 * np.dtype(np.float32).itemsize, ctypes.c_void_p(0 * np.dtype(np.float32).itemsize))
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, False, 6 * np.dtype(np.float32).itemsize, ctypes.c_void_p(3 * np.dtype(np.float32).itemsize))
        GL.glEnableVertexAttribArray(0)
        GL.glEnableVertexAttribArray(1)

        # cleanup and unbind so no accidental subsequent state update
        GL.glBindVertexArray(0)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)

    def draw(self, projection, view, model):
        GL.glUseProgram(self.shader.glid)

        GL.glBindVertexArray(self.vao)

        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        GL.glDrawElements(GL.GL_TRIANGLES, indices.size, GL.GL_UNSIGNED_INT, None)

        GL.glBindVertexArray(0)

    def __del__(self):
        GL.glDeleteVertexArrays(1, self.vao)
        GL.glDeleteBuffers(1, self.vbo)
        GL.glDeleteBuffers(1, self.ebo)


# ------------  Viewer class & window management ------------------------------
class Viewer:
    """ GLFW viewer window, with classic initialization & graphics loop """

    def __init__(self, width=640, height=480):

        # version hints: create GL window with >= OpenGL 3.3 and core profile
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self.win = glfw.create_window(width, height, 'Viewer', None, None)
        if self.win is None:
            print("Failed to create GLFW window")
            glfw.terminate()
            exit(-1)

        # make win's OpenGL context current; no OpenGL calls can happen before
        glfw.make_context_current(self.win)

        # register event handlers
        glfw.set_framebuffer_size_callback(self.win, self.framebuffer_size_callback)
        glfw.set_key_callback(self.win, self.on_key)

        GL.glViewport(0, 0, width, height)
        GL.glEnable(GL.GL_DEPTH_TEST)
        # GL.glEnable(GL.GL_CULL_FACE) # uncomment at modeling stage

        # useful message to check OpenGL renderer characteristics
        print('OpenGL', GL.glGetString(GL.GL_VERSION).decode() + ', GLSL',
              GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode() +
              ', Renderer', GL.glGetString(GL.GL_RENDERER).decode())

        # initially empty list of object to draw
        self.drawables = []

    def run(self):
        """ Main render loop for this OpenGL window """
        while not glfw.window_should_close(self.win):

            GL.glClearColor(0.2, 0.3, 0.3, 1.0)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            for drawable in self.drawables:
                drawable.draw(None, None, None)

            glfw.swap_buffers(self.win)
            glfw.poll_events()

    def add(self, *drawables):
        """ add objects to draw in this window """
        self.drawables.extend(drawables)

    def on_key(self, _win, key, _scancode, action, _mods):
        """ 'Q' or 'Escape' quits """
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_ESCAPE or key == glfw.KEY_Q:
                glfw.set_window_should_close(self.win, True)

            for drawable in self.drawables:
                if hasattr(drawable, 'key_handler'):
                    drawable.key_handler(key)

    def framebuffer_size_callback(self, _win, width, height):
        GL.glViewport(0, 0, width, height)

# -------------- main program and scene setup --------------------------------
def main():
    """ create window, add shaders & scene objects, then run rendering loop """
    viewer = Viewer()
    color_shader = Shader("color.vert", "color.frag")

    # viewer.add(SimpleRectangle(color_shader))
    viewer.add(SimpleSolidRectangle(color_shader))

    viewer.run()


if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
