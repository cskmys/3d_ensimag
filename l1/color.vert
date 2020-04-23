#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 aInColor;

out vec3 inColor;

void main() {
    gl_Position = vec4(position, 1);
    inColor = aInColor;
}
