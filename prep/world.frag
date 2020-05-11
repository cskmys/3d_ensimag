#version 330 core

in vec2 frag_tex_coords;
in vec3 frag_position, frag_normal;

out vec4 out_color;

struct Material{
    sampler2D diffuse_map;
    float s;
};

struct DirLight {
    vec3 light_dir;

    vec3 k_a;
    vec3 k_d;
    vec3 k_s;
};

struct PointLight {
    vec3 position;

    float constant;
    float linear;
    float quadratic;

    vec3 k_a;
    vec3 k_d;
    vec3 k_s;
};

#define NB_POINT_LIGHTS 4

struct Camera {
    vec3 camera_position;
};
uniform Material material;
uniform DirLight dlamp;
uniform PointLight plamp[NB_POINT_LIGHTS];
uniform Camera camera;

vec3 calc_dir_light(DirLight light, vec3 normal, vec3 camDir);
vec3 calc_point_light(PointLight light, vec3 normal, vec3 fragPos, vec3 camDir);

void main() {
    vec3 norm = normalize(frag_normal);
    vec3 cam_dir = normalize(camera.camera_position - frag_position);

    vec3 result = calc_dir_light(dlamp, norm, cam_dir);
    for(int i = 0; i < NB_POINT_LIGHTS; i++){
        result += calc_point_light(plamp[i], norm, frag_position, cam_dir) / 4;
    }
    out_color = vec4(result, 1);
}

vec3 calc_dir_light(DirLight lamp, vec3 normal, vec3 camDir){
    vec3 ambient  = lamp.k_a  * texture(material.diffuse_map, frag_tex_coords).rgb;

    vec3 lightDir = normalize(-lamp.light_dir);
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse  = lamp.k_d  * diff * texture(material.diffuse_map, frag_tex_coords).rgb;

    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(camDir, reflectDir), 0.0), material.s);
    vec3 specular = lamp.k_s * spec * texture(material.diffuse_map, frag_tex_coords).rgb; // using diffuse map for specular as well

    return (ambient + diffuse + specular);
}

vec3 calc_point_light(PointLight lamp, vec3 normal, vec3 fragPos, vec3 camDir){
    vec3 ambient  = lamp.k_a * texture(material.diffuse_map, frag_tex_coords).rgb;

    vec3 lightDir = normalize(lamp.position - fragPos);
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = lamp.k_d * (diff * texture(material.diffuse_map, frag_tex_coords).rgb);

    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(camDir, reflectDir), 0.0), material.s);
    vec3 specular = lamp.k_s * (spec * texture(material.diffuse_map, frag_tex_coords).rgb);

    float distance = length(lamp.position - fragPos);
    float attenuation = 1.0 / (lamp.constant + (lamp.linear * distance) + (lamp.quadratic * (distance * distance)));
    ambient  *= attenuation;
    diffuse  *= attenuation;
    specular *= attenuation;

    return (ambient + diffuse + specular);
}