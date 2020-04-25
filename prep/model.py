#!/usr/bin/env python3

#!/usr/bin/env python3
"""
Python OpenGL practical application.
"""
# Python built-in modules
import os  # os function, i.e. checking file status
from itertools import cycle
import sys

import OpenGL.GL as GL
from transform import identity
from gpu import Shader, VertexArray
import sh_var_lst as svl


# ------------  Scene object classes ------------------------------------------
class Node:
    """ Scene graph transform and parameter broadcast node """

    def __init__(self, children=(), transform=identity()):
        self.transform = transform
        self.children = list(iter(children))

    def add(self, *drawables):
        """ Add drawables to this node, simply updating children list """
        self.children.extend(drawables)

    def draw(self, projection, view, model):
        """ Recursive draw, passing down updated model matrix. """
        for child in self.children:
            child.draw(projection, view, model @ self.transform)

    def key_handler(self, key):
        """ Dispatch keyboard events to children """
        for child in self.children:
            if hasattr(child, 'key_handler'):
                child.key_handler(key)


# -------------- Phong rendered Mesh class -----------------------------------
# mesh to refactor all previous classes
class Mesh:

    def __init__(self, shader, attributes, index=None):
        self.shader = shader
        names = [svl.view, svl.projection, svl.model]
        self.loc = {n: GL.glGetUniformLocation(shader.glid, n) for n in names}
        self.vertex_array = VertexArray(attributes, index)

    def draw(self, projection, view, model, primitives=GL.GL_TRIANGLES):
        GL.glUseProgram(self.shader.glid)

        GL.glUniformMatrix4fv(self.loc[svl.view], 1, True, view)
        GL.glUniformMatrix4fv(self.loc[svl.projection], 1, True, projection)
        GL.glUniformMatrix4fv(self.loc[svl.model], 1, True, model)

        # draw triangle as GL_TRIANGLE vertex array, draw array call
        self.vertex_array.execute(primitives)