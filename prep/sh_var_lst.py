#!/usr/bin/env python3
# list of all vs 'in' and uniforms of both vs n fs

world_shader = {'vs': 'world.vert', 'fs': 'world.frag'}
skybox_shader = {'vs': 'skybox.vert', 'fs': 'skybox.frag'}
screen_shader = {'vs': 'screen.vert', 'fs': 'screen.frag'}

screen_texture = 'screenTexture'
exposure = 'exposure'

model = 'mvp.model'
view = 'mvp.view'
projection = 'mvp.projection'

s = 'material.s'
diffuse_map = 'material.diffuse_map'

skybox = 'skybox'

light_dir = 'dlamp.light_dir'
d_k_a = 'dlamp.k_a'
d_k_d = 'dlamp.k_d'
d_k_s = 'dlamp.k_s'


"""
    cubeShader.setVec3("pLamp[3].position", plampPos[3]);
    cubeShader.setFloat("pLamp[3].constant",  1.0f);
    cubeShader.setFloat("pLamp[3].linear",    0.09f);
    cubeShader.setFloat("pLamp[3].quadratic", 0.032f);
    cubeShader.setVec3("pLamp[3].ambient", lampAmbientColor);
    cubeShader.setVec3("pLamp[3].diffuse", lampDiffuseColor);
    cubeShader.setVec3("pLamp[3].specular", lampSpecIntensity);
"""

p = 'plamp'
p_nb = 4
p_pos = 'position'

p_c = 'constant'
p_l = 'linear'
p_q = 'quadratic'

p_k_a = 'k_a'
p_k_d = 'k_d'
p_k_s = 'k_s'


def get_plamp_i(idx, var):
    return str('{lamp}[{idx}].{var}').format(lamp=p, idx=idx, var=var)


camera_position = 'camera.camera_position'