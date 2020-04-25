#!/usr/bin/env python3

import numpy as np  # all matrix manipulations & OpenGL args
from PIL import Image               # load images for textures
import OpenGL.GL as GL
import glfw
from itertools import cycle

from model import Mesh
import sh_var_lst as svl


# -------------- OpenGL Texture Wrapper ---------------------------------------
class Texture:
    """ Helper class to create and automatically destroy textures """
    def __init__(self, tex_file, wrap_mode=GL.GL_REPEAT, min_filter=GL.GL_LINEAR,
                 mag_filter=GL.GL_LINEAR_MIPMAP_LINEAR):
        self.glid = GL.glGenTextures(1)
        try:
            # imports image as a numpy array in exactly right format
            tex = np.asarray(Image.open(tex_file).convert('RGBA'))
            GL.glBindTexture(GL.GL_TEXTURE_2D, self.glid)
            GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, tex.shape[1],
                            tex.shape[0], 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, tex)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, wrap_mode)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, wrap_mode)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, min_filter)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, mag_filter)
            GL.glGenerateMipmap(GL.GL_TEXTURE_2D)
            message = 'Loaded texture %s\t(%s, %s, %s, %s)'
            print(message % (tex_file, tex.shape, wrap_mode, min_filter, mag_filter))
        except FileNotFoundError:
            print("ERROR: unable to load texture file %s" % tex_file)

    def __del__(self):  # delete GL texture from GPU when object dies
        GL.glDeleteTextures(self.glid)


class TexturedPhongMesh(Mesh):
    def __init__(self, shader, texture, attributes, index=None, 
                 light_dir=(0, -1, 0),  # directional light (in world coords)
                 k_a=(0, 0, 0), k_d=(1, 1, 0), k_s=(1, 1, 1), s=16.):
        super().__init__(shader, attributes, index)
        self._PhongInit(light_dir, k_a, k_d, k_s, s)
        self._TexturedMeshInit(texture)

    def draw(self, projection, view, model, primitives=GL.GL_TRIANGLES):
        GL.glUseProgram(self.shader.glid)

        self._TexturedMeshDraw()
        self._PhongDraw(view)
        super().draw(projection, view, model, primitives)

        self._TexturedMeshPostDraw()
        GL.glUseProgram(0)

    def _PhongInit(self, light_dir, k_a, k_d, k_s, s):
        self.light_dir = light_dir
        self.k_a, self.k_d, self.k_s, self.s = k_a, k_d, k_s, s

        names = [svl.light_dir, svl.k_a, svl.s, svl.k_s, svl.k_d, svl.camera_position]

        loc = {n: GL.glGetUniformLocation(self.shader.glid, n) for n in names}
        self.loc.update(loc)

    def _PhongDraw(self, view):
        self.light_dir = [np.sin(glfw.get_time() * val) for val in [2.0, 0.7, 1.3]]
        GL.glUniform3fv(self.loc[svl.light_dir], 1, self.light_dir)

        GL.glUniform3fv(self.loc[svl.k_a], 1, self.k_a)
        GL.glUniform3fv(self.loc[svl.k_d], 1, self.k_d)
        GL.glUniform3fv(self.loc[svl.k_s], 1, self.k_s)
        GL.glUniform1f(self.loc[svl.s], max(self.s, 0.001))

        w_camera_position = np.linalg.inv(view)[:, 3]
        GL.glUniform3fv(self.loc[svl.camera_position], 1, w_camera_position)

    def _TexturedMeshInit(self, texture):
        loc = {svl.diffuse_map: GL.glGetUniformLocation(self.shader.glid, svl.diffuse_map)}
        self.loc.update(loc)
        self.texture = texture

    def _TexturedMeshDraw(self):
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture.glid)
        GL.glUniform1i(self.loc[svl.diffuse_map], 0)

    def _TexturedMeshPostDraw(self):
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)


# # -------------- Example texture plane class ----------------------------------
# class TexturedPlane(Mesh):
#     """ Simple first textured object """
#
#     def __init__(self, tex_file, shader):
#
#         vertices = 100 * np.array(
#             ((-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)), np.float32)
#         faces = np.array(((0, 1, 2), (0, 2, 3)), np.uint32)
#         super().__init__(shader, [vertices], faces)
#
#         loc = GL.glGetUniformLocation(shader.glid, 'diffuse_map')
#         self.loc['diffuse_map'] = loc
#
#         # interactive toggles
#         self.wrap = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
#                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
#         self.filter = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
#                              (GL.GL_LINEAR, GL.GL_LINEAR),
#                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
#         self.wrap_mode, self.filter_mode = next(self.wrap), next(self.filter)
#         self.tex_file = tex_file
#
#         # setup texture and upload it to GPU
#         self.texture = Texture(tex_file, self.wrap_mode, *self.filter_mode)
#
#     def key_handler(self, key):
#         # some interactive elements
#         if key == glfw.KEY_F6:
#             self.wrap_mode = next(self.wrap)
#             self.texture = Texture(self.tex_file, self.wrap_mode, *self.filter_mode)
#             print('F6')
#         if key == glfw.KEY_F7:
#             self.filter_mode = next(self.filter)
#             self.texture = Texture(self.tex_file, self.wrap_mode, *self.filter_mode)
#             print('F7')
#
#     def draw(self, projection, view, model, primitives=GL.GL_TRIANGLES):
#         GL.glUseProgram(self.shader.glid)
#
#         # texture access setups
#         GL.glActiveTexture(GL.GL_TEXTURE0)
#         GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture.glid)
#         GL.glUniform1i(self.loc['diffuse_map'], 0)
#         super().draw(projection, view, model, primitives)
