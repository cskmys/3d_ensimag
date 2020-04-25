#version 330 core

in vec2 frag_tex_coords;
in vec3 frag_position, frag_normal;

out vec4 out_color;

struct Material{
    sampler2D diffuse_map;
    float s;
};

struct Lamp {
    vec3 light_dir;
    vec3 k_a;
    vec3 k_d;
    vec3 k_s;
};

struct Camera {
    vec3 camera_position;
};
uniform Material material;
uniform Lamp lamp;
uniform Camera camera;

void main() {
    vec3 ambient = lamp.k_a * vec3(texture(material.diffuse_map, frag_tex_coords));

    vec3 n = normalize(frag_normal);
    vec3 l = normalize(-lamp.light_dir);

    float diff = max(0, dot(n, l));
    vec3 diffuse = lamp.k_d * (diff * vec3(texture(material.diffuse_map, frag_tex_coords)));

    vec3 camDir = normalize(camera.camera_position - frag_position);
    vec3 reflectDir = reflect(-lamp.light_dir, n);
    float spec = pow(max(dot(camDir, reflectDir), 0.0), material.s);
    vec3 specular = lamp.k_s * spec * (diff * vec3(texture(material.diffuse_map, frag_tex_coords)));

    vec3 result = ambient + diffuse + specular;
    out_color = vec4(result, 1);
}
