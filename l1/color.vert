#version 330 core

layout(location = 0) in vec3 position;
//layout(location = 1) in vec3 aNormal;
//layout(location = 2) in vec3 aColor;
layout(location = 1) in vec3 aColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 inColor;

void main() {
    gl_Position = projection * view * model * vec4(position, 1);
    inColor = aColor;
}
