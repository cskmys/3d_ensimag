#version 330 core

uniform vec3 dynamic_color;
in vec3 col;
out vec4 outColor;

vec3 chk_range(vec3 c){
    vec3 r;
    for(int i = 0; i < 3; ++i){
        if(c[i] > 1.0){
            r[i] = 1.0;
        } else if(c[i] < 0.0){
            r[i] = 0.0;
        } else {
            r[i] = c[i];
        }
    }
    return r;
}

void main() {
    outColor = vec4(chk_range(col + dynamic_color), 1);
}
