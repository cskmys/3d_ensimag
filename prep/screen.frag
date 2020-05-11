#version 330 core
out vec4 FragColor;

in vec2 TexCoords;

uniform sampler2D screenTexture;
uniform float exposure;
uniform int effect;
uniform float tim_f;

vec3 apply_kernel(float kernel[9]);

void main(){
    vec3 col = vec3(0.0);
    switch(effect){
        case 0:
            // water floating effect
            col = texture( screenTexture, TexCoords + 0.005*vec2( sin(tim_f+1*TexCoords.x),cos(tim_f+0.75*TexCoords.y)) ).xyz ;
        break;
        case 1:
            //     INVERTED
            col = vec3(1.0 - texture(screenTexture, TexCoords));
        break;
        case 2:
            //     BW
            col = texture(screenTexture, TexCoords).xyz;
            float average = 0.2126 * col.r + 0.7152 * col.g + 0.0722 * col.b;
            col = vec3(average, average, average);
        break;
        case 3:
            // sharpen kernel
            float sharpen[9] = float[](
                -1, -1, -1,
                -1,  9, -1,
                -1, -1, -1
            );
            col += apply_kernel(sharpen);
        break;
        case 4:
            // gaussian kernel
            float blur[9] = float[](
                1.0 / 16, 2.0 / 16, 1.0 / 16,
                2.0 / 16, 4.0 / 16, 2.0 / 16,
                1.0 / 16, 2.0 / 16, 1.0 / 16
            );
            col += apply_kernel(blur);
        break;
        case 5:
            // edge
            float edge[9] = float[](
                1.0, 1.0, 1.0,
                1.0, -8.0, 1.0,
                1.0, 1.0, 1.0
            );
            col += apply_kernel(edge);
        break;
        default:
        case 6:
            col = texture( screenTexture, TexCoords ).xyz ;
        break;
    }

    FragColor = vec4(col * exposure, 1.0);
}


vec3 apply_kernel(float kernel[9]){
    vec3 col = vec3(0.0);

    // kernel based
    const float offset = 1.0 / 300.0;
    vec2 offsets[9] = vec2[](
        vec2(-offset,  offset), // top-left
        vec2( 0.0f,    offset), // top-center
        vec2( offset,  offset), // top-right
        vec2(-offset,  0.0f),   // center-left
        vec2( 0.0f,    0.0f),   // center-center
        vec2( offset,  0.0f),   // center-right
        vec2(-offset, -offset), // bottom-left
        vec2( 0.0f,   -offset), // bottom-center
        vec2( offset, -offset)  // bottom-right
    );

    vec3 sampleTex[9];
    for(int i = 0; i < 9; i++){
        sampleTex[i] = vec3(texture(screenTexture, TexCoords.st + offsets[i]));
    }

    for(int i = 0; i < 9; i++){
        col += sampleTex[i] * kernel[i];
    }
    return col;
}