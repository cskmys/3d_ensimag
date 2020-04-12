#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;
out vec3 col;

uniform mat4 transform_mat;

void main() {
    col = color;
    gl_Position = transform_mat * vec4(position, 1);
}
