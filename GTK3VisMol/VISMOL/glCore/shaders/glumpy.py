
vertex_shader_glumpy = """
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
    v_light_direction = normalize(vec3(0,0,2));
    gl_Position = proj_mat * frag_coord;
    vec4 p = proj_mat * vec4(vert_dot_size, vert_dot_size, frag_coord.z, frag_coord.w);
    f_size = 512.0 * p.x / p.w;
    gl_PointSize = f_size + 5.0;
}
"""
fragment_shader_glumpy = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

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
    gl_FragColor = outline(distance, 1.0, 1.0, vec4(0,0,0,1), color);
    // gl_FragColor = color;
}
"""
