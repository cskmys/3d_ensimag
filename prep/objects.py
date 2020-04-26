#!/usr/bin/env python3

import os

import loaders as ld

from model import Node


class Suzy(Node):
    def __init__(self, shader, light_dir):
        super().__init__()
        self.add(*[mesh for mesh in ld.load_model('suzzane.obj', shader, light_dir)])


class Fish(Node):
    def __init__(self, shader, name, light_dir=(0, -1, 0)):
        super().__init__()
        for root, dirs, files in os.walk('./Fish'):
            for obj_dir in dirs:
                if obj_dir.lower() == name.lower():
                    for root, dirs, files in os.walk(os.path.join(root, obj_dir)):
                        for file in files:
                            if str(file).split('.')[1] == 'obj':
                                self.add(*[mesh for mesh in ld.load_model(os.path.join(root, file), shader, light_dir)])
                                return
        raise Exception('Fish ' + name + ' not found')


class Skybox(Node):
    def __init__(self, shader):
        super().__init__()
        skybox_files = []
        for root, dirs, files in os.walk('./skybox'):
            for file in files:
                skybox_files.append(str(os.path.join(root, file)))
        self.add(ld.load_cubemap(skybox_files, shader))
        return


class Framebuffer(Node):
    def __init__(self, shader, width, height):
        super().__init__()
        self.add(ld.load_framebuffer(shader, width, height))
