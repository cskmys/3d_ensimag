#version 330 core

uniform vec3 color;
out vec4 outColor;
in vec3 col;

void main() {
//    outColor = vec4(color, 1);
    outColor = vec4(col, 1);
}
