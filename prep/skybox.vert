#version 330 core
layout (location = 0) in vec3 aPos;

out vec3 TexCoords;

struct MVP{
    mat4 model;
    mat4 view;
    mat4 projection;
};
uniform MVP mvp;
void main(){
    TexCoords = aPos;
    vec4 pos = mvp.projection * mvp.view * mvp.model * vec4(aPos, 1.0);
    gl_Position = pos.xyww;
}