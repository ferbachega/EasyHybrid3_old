
vertex_shader_glumpy  = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

uniform vec3 u_campos;

in vec3 vert_coord;        // attribute vec3 position;
in vec3 vert_color;        // attribute vec3 color;
in float vert_dot_size;   // attribute float radius;
float hw_ratio;

out vec3 frag_color;       // varying vec3 v_color;
out float f_radius;        // varying float v_radius;
out float f_size;          // varying float v_size;
out vec4 frag_coord;       // varying vec4 v_eye_position;

void main (void){
    hw_ratio = proj_mat[0][0] * proj_mat[1][1];
    frag_color = vert_color;
    f_radius = vert_dot_size;
    frag_coord = view_mat * model_mat * vec4(vert_coord, 1.0);
    gl_Position = proj_mat * frag_coord;
    vec4 p = proj_mat * vec4(vert_dot_size, vert_dot_size, frag_coord.z, frag_coord.w);
    f_size = 256.0 * hw_ratio * vert_dot_size / p.w;
    gl_PointSize = f_size;
}
"""

fragment_shader_glumpy = """
#version 330

struct Light {
   vec3 position;
   //vec3 color;
   vec3 intensity;
   //vec3 specular_color;
   float ambient_coef;
   float shininess;
};

uniform Light my_light;

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

uniform vec4 fog_color;
uniform float fog_start;
uniform float fog_end;

vec4 outline(float distance, float linewidth, float antialias, vec4 fg_color, vec4 bg_color){
    vec4 frag_color;
    float t = linewidth/2.0 - antialias;
    float signed_distance = distance;
    float border_distance = abs(signed_distance) - t;
    float alpha = border_distance/antialias;
    alpha = exp(-alpha*alpha);

    if( border_distance < 0.0 )
        frag_color = fg_color;
    else if( signed_distance < 0.0 )
        frag_color = mix(bg_color, fg_color, sqrt(alpha));
    else {
        if( abs(signed_distance) < (linewidth/2.0 + antialias) ) {
            frag_color = vec4(fg_color.rgb, fg_color.a * alpha);
        } else {
            discard;
        }
    }
    return frag_color;
}

in vec3 frag_color;       // varying vec3 v_color;
in float f_radius;        // varying float v_radius;
in float f_size;          // varying float v_size;
in vec4 frag_coord;       // varying vec4 v_eye_position;

out vec4 final_color;

vec4 calculate_color(vec3 fnrm, vec3 fcrd, vec3 fcol){
    vec3 normal = normalize(fnrm);
    vec3 vert_to_light = normalize(my_light.position);
    vec3 vert_to_cam = normalize(fcrd);
    // Ambient Component
    vec3 ambient = my_light.ambient_coef * fcol * my_light.intensity;
    // Diffuse component
    float diffuse_coef = max(0.0, dot(normal, vert_to_light));
    vec3 diffuse = diffuse_coef * fcol * my_light.intensity;
    // Specular component
    float specular_coef = 0.0;
    if (diffuse_coef > 0.0)
        specular_coef = pow(max(0.0, dot(vert_to_cam, reflect(vert_to_light, normal))), my_light.shininess);
    vec3 specular = specular_coef * my_light.intensity;
    specular = specular * (vec3(1) - diffuse);
    vec4 out_color = vec4(ambient + diffuse + specular, 1.0);
    return out_color;
}

void main(){
    vec2 P = gl_PointCoord.xy - vec2(0.5,0.5);
    float distance = length(P*f_size) - f_size/2;
    vec2 texcoord = gl_PointCoord* 2.0 - vec2(1.0);
    float x = texcoord.x;
    float y = texcoord.y;
    float d = 1.0 - x*x - y*y;
    if (d <= 0.0){
        discard;
    }
    float z = sqrt(d);
    vec4 pos = frag_coord;
    pos.z += f_radius*z;
    vec3 pos2 = pos.xyz;
    pos = proj_mat * pos;
    gl_FragDepth = 0.5*(pos.z / pos.w)+0.5;
    vec3 normal = vec3(x,-y,z);
    vec4 color = calculate_color(normal, frag_coord.xyz, frag_color);
    //vec4 temp_color = outline(distance, 1.0, 1.0, vec4(0,0,0,1), color);
    float dist = abs(frag_coord.z);
    if(dist>=fog_start){
        float fog_factor = (fog_end-dist)/(fog_end-fog_start);
        final_color = mix(fog_color, color, fog_factor);
    }
    else{
       final_color = color;
    }
}
"""

sel_fragment_shader_glumpy = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in vec3 frag_color;       // varying vec3 v_color;
in float f_radius;        // varying float v_radius;
in float f_size;          // varying float v_size;
in vec4 frag_coord;       // varying vec4 v_eye_position;

out vec4 final_color;

void main()
{
    vec2 P = gl_PointCoord.xy - vec2(0.5,0.5);
    float distance = length(P*f_size) - f_size/2;
    vec2 texcoord = gl_PointCoord* 2.0 - vec2(1.0);
    float x = texcoord.x;
    float y = texcoord.y;
    float d = 1.0 - x*x - y*y;
    if (d <= 0.0){
        discard;
    }
    float z = sqrt(d);
    vec4 pos = frag_coord;
    pos.z += f_radius*z;
    pos = proj_mat * pos;
    gl_FragDepth = 0.5*(pos.z / pos.w)+0.5;
    final_color = vec4(frag_color, 1.0);
}
"""














vertex_shader_glumpy_0  = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in vec3 vert_coord;        // attribute vec3 position;
in vec3 vert_color;        // attribute vec3 color;
//in float vert_dot_size;   // attribute float radius;
const float vert_dot_size = 0.1;  // attribute float radius;

out vec3 frag_color;       // varying vec3 v_color;
out float f_radius;        // varying float v_radius;
out float f_size;          // varying float v_size;
out vec4 frag_coord;       // varying vec4 v_eye_position;

varying vec3 v_light_direction;

void main (void)
{
    frag_color = vert_color;
    f_radius = vert_dot_size;
    frag_coord = view_mat * model_mat * vec4(vert_coord, 1.0);
    v_light_direction = normalize(vec3(-2.5,-2.5,3.0));
    gl_Position = proj_mat * frag_coord;
    vec4 p = proj_mat * vec4(vert_dot_size, vert_dot_size, frag_coord.z, frag_coord.w);
    f_size = 512.0 * p.x / p.w;
    gl_PointSize = f_size + 5.0;
}
"""
fragment_shader_glumpy_0 = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

uniform vec4 fog_color;
uniform float fog_start;
uniform float fog_end;

vec4 outline(float distance, float linewidth, float antialias, vec4 fg_color, vec4 bg_color){
    vec4 frag_color;
    float t = linewidth/2.0 - antialias;
    float signed_distance = distance;
    float border_distance = abs(signed_distance) - t;
    float alpha = border_distance/antialias;
    alpha = exp(-alpha*alpha);

    if( border_distance < 0.0 )
        frag_color = fg_color;
    else if( signed_distance < 0.0 )
        frag_color = mix(bg_color, fg_color, sqrt(alpha));
    else {
        if( abs(signed_distance) < (linewidth/2.0 + antialias) ) {
            frag_color = vec4(fg_color.rgb, fg_color.a * alpha);
        } else {
            discard;
        }
    }
    return frag_color;
}

in vec3 frag_color;       // varying vec3 v_color;
in float f_radius;        // varying float v_radius;
in float f_size;          // varying float v_size;
in vec4 frag_coord;       // varying vec4 v_eye_position;

varying vec3 v_light_direction;

void main()
{
    vec2 P = gl_PointCoord.xy - vec2(0.5,0.5);
    float point_size = f_size  + 5.0;
    float distance = length(P*point_size) - f_size/2;
    vec2 texcoord = gl_PointCoord* 2.0 - vec2(1.0);
    float x = texcoord.x;
    float y = texcoord.y;
    float d = 1.0 - x*x - y*y;
    if (d <= 0.0) discard;
    float z = sqrt(d);
    vec4 pos = frag_coord;
    pos.z += f_radius*z;
    vec3 pos2 = pos.xyz;
    pos = proj_mat * pos;
    gl_FragDepth = 0.5*(pos.z / pos.w)+0.5;
    vec3 normal = vec3(x,y,z);
    float diffuse = clamp(dot(normal, v_light_direction), 0.0, 1.0);
    vec4 color = vec4((0.5 + 0.5*diffuse)*frag_color, 1.0);
    //gl_FragColor = outline(distance, 1.0, 1.0, vec4(0,0,0,1), color);
    vec4 temp_color = outline(distance, 1.0, 1.0, vec4(0,0,0,1), color);
    // gl_FragColor = color;
    float dist = abs(frag_coord.z);
    if(dist>=fog_start){
        float fog_factor = (fog_end-dist)/(fog_end-fog_start);
        gl_FragColor = mix(fog_color, temp_color, fog_factor);
    }
    else{
       gl_FragColor = temp_color;
    }
}
"""






vertex_shader_glumpy_1 = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in vec3 vert_coord;        // attribute vec3 position;
in vec3 vert_color;        // attribute vec3 color;
//in float vert_dot_size;   // attribute float radius;
const float vert_dot_size = 0.1;  // attribute float radius;

out vec3 frag_color;       // varying vec3 v_color;
out float f_radius;        // varying float v_radius;
out float f_size;          // varying float v_size;
out vec4 frag_coord;       // varying vec4 v_eye_position;

varying vec3 v_light_direction;

void main (void)
{
    frag_color = vert_color;
    f_radius = vert_dot_size;
    frag_coord = view_mat * model_mat * vec4(vert_coord, 1.0);
    v_light_direction = normalize(vec3(-2.5,-2.5,3.0));
    gl_Position = proj_mat * frag_coord;
    vec4 p = proj_mat * vec4(vert_dot_size, vert_dot_size, frag_coord.z, frag_coord.w);
    f_size = 512.0 * p.x / p.w;
    gl_PointSize = f_size + 5.0;
}
"""
fragment_shader_glumpy_1 = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

uniform vec4 fog_color;
uniform float fog_start;
uniform float fog_end;

vec4 outline(float distance, float linewidth, float antialias, vec4 fg_color, vec4 bg_color){
    vec4 frag_color;
    float t = linewidth/2.0 - antialias;
    float signed_distance = distance;
    float border_distance = abs(signed_distance) - t;
    float alpha = border_distance/antialias;
    alpha = exp(-alpha*alpha);

    if( border_distance < 0.0 )
        frag_color = fg_color;
    else if( signed_distance < 0.0 )
        frag_color = mix(bg_color, fg_color, sqrt(alpha));
    else {
        if( abs(signed_distance) < (linewidth/2.0 + antialias) ) {
            frag_color = vec4(fg_color.rgb, fg_color.a * alpha);
        } else {
            discard;
        }
    }
    return frag_color;
}

in vec3 frag_color;       // varying vec3 v_color;
in float f_radius;        // varying float v_radius;
in float f_size;          // varying float v_size;
in vec4 frag_coord;       // varying vec4 v_eye_position;

varying vec3 v_light_direction;

void main()
{
    vec2 P = gl_PointCoord.xy - vec2(0.5,0.5);
    float point_size = f_size  + 5.0;
    float distance = length(P*point_size) - f_size/2;
    vec2 texcoord = gl_PointCoord* 2.0 - vec2(1.0);
    float x = texcoord.x;
    float y = texcoord.y;
    float d = 1.0 - x*x - y*y;
    if (d <= 0.0) discard;
    float z = sqrt(d);
    vec4 pos = frag_coord;
    pos.z += f_radius*z;
    vec3 pos2 = pos.xyz;
    pos = proj_mat * pos;
    gl_FragDepth = 0.5*(pos.z / pos.w)+0.5;
    vec3 normal = vec3(x,y,z);
    float diffuse = clamp(dot(normal, v_light_direction), 0.0, 1.0);
    vec4 color = vec4((0.5 + 0.5*diffuse)*frag_color, 1.0);
    //gl_FragColor = outline(distance, 1.0, 1.0, vec4(0,0,0,1), color);
    vec4 temp_color = outline(distance, 1.0, 1.0, vec4(0,0,0,1), color);
    // gl_FragColor = color;
    float dist = abs(frag_coord.z);
    if(dist>=fog_start){
        float fog_factor = (fog_end-dist)/(fog_end-fog_start);
        gl_FragColor = mix(fog_color, temp_color, fog_factor);
    }
    else{
       gl_FragColor = temp_color;
    }
}
"""



v_shader_imposter = """
#version 330
precision highp float;

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in vec3 vert_coord;
in vec3 vert_color;

//in float vert_rad;
const float vert_rad = 0.5;

uniform vec3 u_campos;

const float atom_rad = 0.90;
const float uAtomShade = 0.9;

out vec3 geom_color;
out vec3 geom_coord;
out vec3 geom_center;
out vec3 geom_cam;
out float geom_radius;

void main() {
    geom_color = vert_color;
    geom_coord = vert_coord;
    geom_center = vert_coord;
    geom_cam = u_campos;
    geom_radius = vert_rad;
}
"""
g_shader_imposter = """
#version 330

layout (points) in;
layout (triangle_strip, max_vertices = 18) out;

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in vec3 geom_color[];
in vec3 geom_coord[];
in vec3 geom_center[];
in vec3 geom_cam[];
in float geom_radius[];

out vec3 frag_color;
out vec3 frag_coord;
out vec3 frag_center;
out vec3 frag_cam;
out float frag_radius;

vec3 p_1 = vec3(-1.0,-1.0,-1.0);
vec3 p_2 = vec3(-1.0,-1.0, 1.0);
vec3 p_3 = vec3( 1.0,-1.0, 1.0);
vec3 p_4 = vec3( 1.0,-1.0,-1.0);
vec3 p_5 = vec3(-1.0, 1.0,-1.0);
vec3 p_6 = vec3(-1.0, 1.0, 1.0);
vec3 p_7 = vec3( 1.0, 1.0, 1.0);
vec3 p_8 = vec3( 1.0, 1.0,-1.0);

void main(){
    vec3 point1 = geom_coord[0] + p_1 * geom_radius[0];
    vec3 point2 = geom_coord[0] + p_2 * geom_radius[0];
    vec3 point3 = geom_coord[0] + p_3 * geom_radius[0];
    vec3 point4 = geom_coord[0] + p_4 * geom_radius[0];
    vec3 point5 = geom_coord[0] + p_5 * geom_radius[0];
    vec3 point6 = geom_coord[0] + p_6 * geom_radius[0];
    vec3 point7 = geom_coord[0] + p_7 * geom_radius[0];
    vec3 point8 = geom_coord[0] + p_8 * geom_radius[0];
    
    gl_Position = proj_mat * view_mat * model_mat * vec4(point1, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(model_mat * vec4(point1, 1.0));
    frag_center = vec3(model_mat * vec4(geom_center[0], 1.0));
    frag_cam = vec3(model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point6, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(model_mat * vec4(point6, 1.0));
    frag_center = vec3(model_mat * vec4(geom_center[0], 1.0));
    frag_cam = vec3(model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point2, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(model_mat * vec4(point2, 1.0));
    frag_center = vec3(model_mat * vec4(geom_center[0], 1.0));
    frag_cam = vec3(model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point7, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(model_mat * vec4(point7, 1.0));
    frag_center = vec3(model_mat * vec4(geom_center[0], 1.0));
    frag_cam = vec3(model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point3, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(model_mat * vec4(point3, 1.0));
    frag_center = vec3(model_mat * vec4(geom_center[0], 1.0));
    frag_cam = vec3(model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point8, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(model_mat * vec4(point8, 1.0));
    frag_center = vec3(model_mat * vec4(geom_center[0], 1.0));
    frag_cam = vec3(model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point4, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(model_mat * vec4(point4, 1.0));
    frag_center = vec3(model_mat * vec4(geom_center[0], 1.0));
    frag_cam = vec3(model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point5, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(model_mat * vec4(point5, 1.0));
    frag_center = vec3(model_mat * vec4(geom_center[0], 1.0));
    frag_cam = vec3(model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point1, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(model_mat * vec4(point1, 1.0));
    frag_center = vec3(model_mat * vec4(geom_center[0], 1.0));
    frag_cam = vec3(model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point6, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(model_mat * vec4(point6, 1.0));
    frag_center = vec3(model_mat * vec4(geom_center[0], 1.0));
    frag_cam = vec3(model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    
    EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point1, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(model_mat * vec4(point1, 1.0));
    frag_center = vec3(model_mat * vec4(geom_center[0], 1.0));
    frag_cam = vec3(model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point2, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(model_mat * vec4(point2, 1.0));
    frag_center = vec3(model_mat * vec4(geom_center[0], 1.0));
    frag_cam = vec3(model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point4, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(model_mat * vec4(point4, 1.0));
    frag_center = vec3(model_mat * vec4(geom_center[0], 1.0));
    frag_cam = vec3(model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point3, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(model_mat * vec4(point3, 1.0));
    frag_center = vec3(model_mat * vec4(geom_center[0], 1.0));
    frag_cam = vec3(model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    EndPrimitive();

    gl_Position = proj_mat * view_mat * model_mat * vec4(point5, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(model_mat * vec4(point5, 1.0));
    frag_center = vec3(model_mat * vec4(geom_center[0], 1.0));
    frag_cam = vec3(model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point6, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(model_mat * vec4(point6, 1.0));
    frag_center = vec3(model_mat * vec4(geom_center[0], 1.0));
    frag_cam = vec3(model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point8, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(model_mat * vec4(point8, 1.0));
    frag_center = vec3(model_mat * vec4(geom_center[0], 1.0));
    frag_cam = vec3(model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    gl_Position = proj_mat * view_mat * model_mat * vec4(point7, 1.0);
    frag_color = geom_color[0];
    frag_coord = vec3(model_mat * vec4(point7, 1.0));
    frag_center = vec3(model_mat * vec4(geom_center[0], 1.0));
    frag_cam = vec3(model_mat * vec4(geom_cam[0], 1.0));
    frag_radius = geom_radius[0];
    EmitVertex();
    EndPrimitive();
}
"""
f_shader_imposter = """
#version 330
#extension GL_EXT_frag_depth: enable
precision highp float;

struct Light {
    vec3 position;
    //vec3 color;
    vec3 intensity;
    //vec3 specular_color;
    float ambient_coef;
    float shininess;
};

uniform Light my_light;

uniform float u_depth;

in vec3 frag_color;
in vec3 frag_coord;
in vec3 frag_center;
in vec3 frag_cam;
in float frag_radius;

float sphIntersect(vec3 ro, vec3 rd, vec3 sph, float rad){
    vec3 oc = ro - sph;
    float b = dot(oc, rd);
    float c = dot(oc, oc) - rad*rad;
    float h = b*b - c;
    if( h<0.0 ) return -1.0;
    return -b - sqrt(h);
}

void main() {
    vec3 ro = frag_cam;
    vec3 rd = normalize(frag_coord - frag_cam);
    float t = sphIntersect(ro, rd, frag_center, frag_radius);
    if (t < 0.0) discard;
    vec3 coord = ro + rd * t;
    vec3 normal = normalize(coord - frag_center);
    vec3 vert_to_light = normalize(my_light.position);
    vec3 vert_to_cam = normalize(frag_coord);
    
    // Ambient Component
    vec3 ambient = my_light.ambient_coef * frag_color * my_light.intensity;
    
    // Diffuse component
    float diffuse_coef = max(0.0, dot(normal, vert_to_light));
    vec3 diffuse = diffuse_coef * frag_color * my_light.intensity;
    
    gl_FragColor = vec4(ambient + diffuse, 1.0);
    
    vec3 depth_coord = frag_center + normal * frag_radius;
    //gl_FragDepthEXT = -length(depth_coord - frag_cam)/u_depth;
}
"""





shader_type ={
			#0: { 'vertex_shader'      : vertex_shader_glumpy_0  ,
			#     'fragment_shader'    : fragment_shader_glumpy_0,
			#	 'sel_vertex_shader'  : vertex_shader_glumpy_0  ,
            #     'sel_fragment_shader': fragment_shader_glumpy_0
            #
			#   },
			#
			0: { 'vertex_shader'      : vertex_shader_glumpy  ,
			     'fragment_shader'    : fragment_shader_glumpy,
				 'sel_vertex_shader'  : vertex_shader_glumpy  ,
                 'sel_fragment_shader': sel_fragment_shader_glumpy

			   },
			
			
			1: {'vertex_shader'      : vertex_shader_glumpy_1  ,
			    'fragment_shader'    : fragment_shader_glumpy_1,
			    'sel_vertex_shader'  : vertex_shader_glumpy_1  ,
			    'sel_fragment_shader': fragment_shader_glumpy_1
				},
			
			2: {'vertex_shader'      : v_shader_imposter,
			    'fragment_shader'    : f_shader_imposter,
			    'geometry_shader'    : g_shader_imposter,
			    
                'sel_vertex_shader'  : vertex_shader_glumpy_1  ,
			    'sel_fragment_shader': fragment_shader_glumpy_1
				}


}


















