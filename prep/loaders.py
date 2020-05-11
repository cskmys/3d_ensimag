#!/usr/bin/env python3

import assimpcy  # 3D resource loader
import os  # os function, i.e. checking file status

from material import Texture, TexturedPhongMesh, CubeMap, CubeMapMesh, FrameTexture, FramebufferMesh, TexturedPlaneMesh, AxisMesh


def load_model(file, shader, dlight_dir, tex_file=None):
    """ load resources from file using assimp, return list of Meshes"""
    try:
        pp = assimpcy.aiPostProcessSteps
        flags = pp.aiProcess_Triangulate | pp.aiProcess_GenSmoothNormals | pp.aiProcess_FlipUVs
        scene = assimpcy.aiImportFile(file, flags)
    except assimpcy.all.AssimpError as exception:
        print('ERROR loading', file + ': ', exception.args[0].decode())
        return []

    path = os.path.dirname(file) if os.path.dirname(file) != '' else './'
    for mat in scene.mMaterials:
        if not tex_file and 'TEXTURE_BASE' in mat.properties:  # texture token
            name = os.path.basename(mat.properties['TEXTURE_BASE'])
            # search texture in file's whole subdir since path often screwed up
            paths = os.walk(path, followlinks=True)
            found = [os.path.join(d, f) for d, _, n in paths for f in n
                     if name.startswith(f) or f.startswith(name)]
            assert found, 'Cannot find texture %s in %s subtree' % (name, path)
            tex_file = found[0]
        if tex_file:
            mat.properties['diffuse_map'] = Texture(tex_file=tex_file)

    # prepare mesh nodes
    meshes = []
    for mesh in scene.mMeshes:
        mat = scene.mMaterials[mesh.mMaterialIndex].properties
        assert mat['diffuse_map'], "Trying to map using a textureless material"
        attributes = [mesh.mVertices, mesh.mNormals, mesh.mTextureCoords[0]]
        mesh = TexturedPhongMesh(shader, mat['diffuse_map'], attributes,
                                 dlight_dir, mesh.mFaces,
                                 k_d=mat.get('COLOR_DIFFUSE', (1, 1, 1)),
                                 k_s=mat.get('COLOR_SPECULAR', (1, 1, 1)),
                                 k_a=mat.get('COLOR_AMBIENT', (0, 0, 0)),
                                 s=mat.get('SHININESS', 16.),
                                 )
        meshes.append(mesh)

    size = sum((mesh.mNumFaces for mesh in scene.mMeshes))
    return meshes


def load_cubemap(files, shader):
    """ load resources from file using assimp, return list of Meshes"""
    tex_files = []
    for file in files:
        path = os.path.dirname(file) if os.path.dirname(file) != '' else './'
        name = os.path.basename(file)
        paths = os.walk(path, followlinks=True)
        found = [os.path.join(d, f) for d, _, n in paths for f in n
                    if name.startswith(f) or f.startswith(name)]
        assert found, 'Cannot find texture %s in %s subtree' % (name, path)
        tex_files.append(found[0])
    assert len(tex_files) == 6, '6 textures are needed for cubemap'
    file_order = ['_rt', '_lf', '_up', '_dn', '_ft', '_bk']
    cmap_textures = []
    for order in file_order:
        for file in tex_files:
            if order in file:
                cmap_textures.append(file)
                break

    c_map = CubeMap(cmap_textures)
    mesh = CubeMapMesh(shader, c_map)
    return mesh


def load_framebuffer(shader, width, height):
    frame = FrameTexture(width, height)
    mesh = FramebufferMesh(shader, frame)
    return mesh


def load_floor(file, shader, tex_file=None):
    """ load resources from file using assimp, return list of Meshes"""
    try:
        pp = assimpcy.aiPostProcessSteps
        flags = pp.aiProcess_Triangulate | pp.aiProcess_GenSmoothNormals | pp.aiProcess_FlipUVs
        scene = assimpcy.aiImportFile(file, flags)
    except assimpcy.all.AssimpError as exception:
        print('ERROR loading', file + ': ', exception.args[0].decode())
        return []

    path = os.path.dirname(file) if os.path.dirname(file) != '' else './'
    for mat in scene.mMaterials:
        if not tex_file and 'TEXTURE_BASE' in mat.properties:  # texture token
            name = os.path.basename(mat.properties['TEXTURE_BASE'])
            # search texture in file's whole subdir since path often screwed up
            paths = os.walk(path, followlinks=True)
            found = [os.path.join(d, f) for d, _, n in paths for f in n
                     if name.startswith(f) or f.startswith(name)]
            assert found, 'Cannot find texture %s in %s subtree' % (name, path)
            tex_file = found[0]

    mesh = TexturedPlaneMesh(shader, tex_file)

    size = sum((mesh.mNumFaces for mesh in scene.mMeshes))
    return mesh


def load_axis(shader):
    mesh = AxisMesh(shader)
    return mesh
