#!/usr/bin/env python3

import assimpcy  # 3D resource loader
import os  # os function, i.e. checking file status

from material import Texture, TexturedPhongMesh


def load_model(file, shader, light_dir, tex_file=None):
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
        mesh = TexturedPhongMesh(shader, mat['diffuse_map'], attributes, mesh.mFaces,
                         k_d=mat.get('COLOR_DIFFUSE', (1, 1, 1)),
                         k_s=mat.get('COLOR_SPECULAR', (1, 1, 1)),
                         k_a=mat.get('COLOR_AMBIENT', (0, 0, 0)),
                         s=mat.get('SHININESS', 16.),
                         light_dir=light_dir)
        meshes.append(mesh)

    size = sum((mesh.mNumFaces for mesh in scene.mMeshes))
    print('Loaded %s\t(%d meshes, %d faces)' % (file, len(meshes), size))
    return meshes


# def load_textured(file, shader, tex_file=None):
#     """ load resources from file using assimp, return list of TexturedMesh """
#     try:
#         pp = assimpcy.aiPostProcessSteps
#         flags = pp.aiProcess_Triangulate | pp.aiProcess_FlipUVs
#         scene = assimpcy.aiImportFile(file, flags)
#     except assimpcy.all.AssimpError as exception:
#         print('ERROR loading', file + ': ', exception.args[0].decode())
#         return []
#
#     path = os.path.dirname(file) if os.path.dirname(file) != '' else './'
#     for mat in scene.mMaterials:
#         if not tex_file and 'TEXTURE_BASE' in mat.properties:  # texture token
#             name = os.path.basename(mat.properties['TEXTURE_BASE'])
#             # search texture in file's whole subdir since path often screwed up
#             paths = os.walk(path, followlinks=True)
#             found = [os.path.join(d, f) for d, _, n in paths for f in n
#                      if name.startswith(f) or f.startswith(name)]
#             assert found, 'Cannot find texture %s in %s subtree' % (name, path)
#             tex_file = found[0]
#         if tex_file:
#             mat.properties['diffuse_map'] = Texture(tex_file=tex_file)
#
#     # prepare textured mesh
#     meshes = []
#     for mesh in scene.mMeshes:
#         mat = scene.mMaterials[mesh.mMaterialIndex].properties
#         assert mat['diffuse_map'], "Trying to map using a textureless material"
#         attributes = [mesh.mVertices, mesh.mTextureCoords[0]]
#         mesh = TexturedMesh(shader, mat['diffuse_map'], attributes, mesh.mFaces)
#         meshes.append(mesh)
#
#     size = sum((mesh.mNumFaces for mesh in scene.mMeshes))
#     print('Loaded %s\t(%d meshes, %d faces)' % (file, len(meshes), size))
#     return meshes