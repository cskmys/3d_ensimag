#version 330 core
out vec4 FragColor;

in vec2 TexCoords;

uniform sampler2D screenTexture;
uniform float exposure;

void main(){
        // water floating effect
//        vec3 col = texture( screenTexture, TexCoords + 0.005*vec2( sin(exposure+1*TexCoords.x),cos(exposure+0.75*TexCoords.y)) ).xyz ;
            vec3 col = texture( screenTexture, TexCoords ).xyz ;
    FragColor = vec4(col, 1.0);
// NORMAL
    //    vec3 col = texture(screenTexture, TexCoords).rgb;
//    FragColor = vec4(col * exposure, 1.0);
    // INVERTED
    //    FragColor = vec4(vec3(1.0 - texture(screenTexture, TexCoords)), 1.0);
    // BW
//    FragColor = texture(screenTexture, TexCoords);
//    float average = 0.2126 * FragColor.r + 0.7152 * FragColor.g + 0.0722 * FragColor.b;
//    FragColor = vec4(average, average, average, 1.0);

// sharpen kernel
//        float kernel[9] = float[](
//        -1, -1, -1,
//        -1,  9, -1,
//        -1, -1, -1
//    );

    // kernel based
//    const float offset = 1.0 / 300.0;
//    vec2 offsets[9] = vec2[](
//        vec2(-offset,  offset), // top-left
//        vec2( 0.0f,    offset), // top-center
//        vec2( offset,  offset), // top-right
//        vec2(-offset,  0.0f),   // center-left
//        vec2( 0.0f,    0.0f),   // center-center
//        vec2( offset,  0.0f),   // center-right
//        vec2(-offset, -offset), // bottom-left
//        vec2( 0.0f,   -offset), // bottom-center
//        vec2( offset, -offset)  // bottom-right
//    );
//
//
//    vec3 sampleTex[9];
//    for(int i = 0; i < 9; i++)
//    {
//        sampleTex[i] = vec3(texture(screenTexture, TexCoords.st + offsets[i]));
//    }
//    vec3 col = vec3(0.0);
//    for(int i = 0; i < 9; i++)
//        col += sampleTex[i] * kernel[i];
//
//    FragColor = vec4(col, 1.0);
}