#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;
layout(location = 2) in vec2 texCoord;

out vec3 frag_pos, frag_normal;
out vec2 frag_tex_coords;

struct MVP{
    mat4 model;
    mat4 view;
    mat4 projection;
};
uniform MVP mvp;

void main() {
    gl_Position = mvp.projection * mvp.view * mvp.model * vec4(position, 1);

    frag_tex_coords = texCoord;

    frag_pos = vec3(mvp.model * vec4(position, 1.0)); // fragment position
    frag_normal = mat3(transpose(inverse(mvp.model))) * normal;
}
