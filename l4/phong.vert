#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;

uniform mat4 model, view, projection;

// position and normal for the fragment shader, in WORLD coordinates
// (you can also compute in VIEW coordinates, your choice! rename variables)
out vec3 w_position, w_normal;   // in world coordinates

void main() {
    gl_Position = projection * view * model * vec4(position, 1.0);

    w_position = vec3(model * vec4(position, 1.0)); // fragment position
    w_normal = mat3(transpose(inverse(model))) * normal;
}