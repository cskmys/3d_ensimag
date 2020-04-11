#version 330 core

layout(location = 0) in vec3 position;
vec3 newPos;
void main() {
    newPos.x = position.x + 1.0;
    newPos.y = position.y + 0.5;
    newPos.z = position.z + 0.5;
    gl_Position = vec4(newPos, 1);
}
