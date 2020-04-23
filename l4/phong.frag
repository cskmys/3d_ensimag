#version 330 core

// fragment position and normal of the fragment, in WORLD coordinates
// (you can also compute in VIEW coordinates, your choice! rename variables)
in vec3 w_position, w_normal;   // in world coodinates

// light dir, in world coordinates
uniform vec3 light_dir;

// material properties
uniform vec3 k_a;
uniform vec3 k_d;
uniform vec3 k_s;
uniform float s;

// world camera position
uniform vec3 w_camera_position;

out vec4 out_color;

void main() {
    vec3 ambient = k_a;

    vec3 n = normalize(w_normal);
    vec3 l = normalize(-light_dir);

    float diff = max(0, dot(n, l));
    vec3 diffuse = k_d * diff;

    vec3 camDir = normalize(w_camera_position - w_position);
    vec3 reflectDir = reflect(-light_dir, n);
    float spec = pow(max(dot(camDir, reflectDir), 0.0), s);
    vec3 specular = k_s * spec;

    vec3 result = ambient + diffuse + specular;
    out_color = vec4(result, 1);
}
