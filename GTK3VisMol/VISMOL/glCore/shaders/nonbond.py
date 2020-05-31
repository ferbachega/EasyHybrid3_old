
vertex_shader_non_bonded = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;

const float xyz_offset = 0.2;

in vec3 vert_coord;
in vec3 vert_color;

out vec3 geom_color;
out vec4 geom_coord_1;
out vec4 geom_coord_2;
out vec4 geom_coord_3;
out vec4 geom_coord_4;
out vec4 geom_coord_5;
out vec4 geom_coord_6;

void main(){
    geom_color = vert_color;
    geom_coord_1 = view_mat * model_mat * vec4((vert_coord.x - xyz_offset), vert_coord.y, vert_coord.z, 1.0);
    geom_coord_2 = view_mat * model_mat * vec4((vert_coord.x + xyz_offset), vert_coord.y, vert_coord.z, 1.0);
    geom_coord_3 = view_mat * model_mat * vec4(vert_coord.x, (vert_coord.y - xyz_offset), vert_coord.z, 1.0);
    geom_coord_4 = view_mat * model_mat * vec4(vert_coord.x, (vert_coord.y + xyz_offset), vert_coord.z, 1.0);
    geom_coord_5 = view_mat * model_mat * vec4(vert_coord.x, vert_coord.y, (vert_coord.z - xyz_offset), 1.0);
    geom_coord_6 = view_mat * model_mat * vec4(vert_coord.x, vert_coord.y, (vert_coord.z + xyz_offset), 1.0);
}
"""
geometry_shader_non_bonded = """
#version 330

const float xyz_offset = 0.5;

layout (points) in;
layout (line_strip, max_vertices = 6) out;

uniform mat4 proj_mat;

in vec3 geom_color[];
in vec4 geom_coord_1[];
in vec4 geom_coord_2[];
in vec4 geom_coord_3[];
in vec4 geom_coord_4[];
in vec4 geom_coord_5[];
in vec4 geom_coord_6[];

out vec3 frag_color;
out vec4 frag_coord;

void main(){
    gl_Position = proj_mat * geom_coord_1[0];
    frag_color = geom_color[0];
    frag_coord = geom_coord_1[0];
    EmitVertex();
    gl_Position = proj_mat * geom_coord_2[0];
    frag_color = geom_color[0];
    frag_coord = geom_coord_2[0];
    EmitVertex();
    EndPrimitive();
    
    gl_Position = proj_mat * geom_coord_3[0];
    frag_color = geom_color[0];
    frag_coord = geom_coord_3[0];
    EmitVertex();
    gl_Position = proj_mat * geom_coord_4[0];
    frag_color = geom_color[0];
    frag_coord = geom_coord_4[0];
    EmitVertex();
    EndPrimitive();
    
    gl_Position = proj_mat * geom_coord_5[0];
    frag_color = geom_color[0];
    frag_coord = geom_coord_5[0];
    EmitVertex();
    gl_Position = proj_mat * geom_coord_6[0];
    frag_color = geom_color[0];
    frag_coord = geom_coord_6[0];
    EmitVertex();
    EndPrimitive();
}
"""
fragment_shader_non_bonded = """
#version 330

uniform vec4 fog_color;
uniform float fog_start;
uniform float fog_end;

in vec3 frag_color;
in vec4 frag_coord;

out vec4 final_color;

void main(){
    float dist = abs(frag_coord.z);
    if(dist>=fog_start){
        float fog_factor = (fog_end-dist)/(fog_end-fog_start);
        final_color = mix(fog_color, vec4(frag_color, 1.0), fog_factor);
    }
    else{
       final_color = vec4(frag_color, 1.0);
    }
}
"""





sel_vertex_shader_non_bonded = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;

const float xyz_offset = 0.5;

in vec3 vert_coord;
in vec3 vert_color;

out vec3 geom_color;
out vec4 geom_coord_1;
out vec4 geom_coord_2;
out vec4 geom_coord_3;
out vec4 geom_coord_4;
out vec4 geom_coord_5;
out vec4 geom_coord_6;

void main(){
    geom_color = vert_color;
    geom_coord_1 = view_mat * model_mat * vec4((vert_coord.x - xyz_offset), vert_coord.y, vert_coord.z, 1.0);
    geom_coord_2 = view_mat * model_mat * vec4((vert_coord.x + xyz_offset), vert_coord.y, vert_coord.z, 1.0);
    geom_coord_3 = view_mat * model_mat * vec4(vert_coord.x, (vert_coord.y - xyz_offset), vert_coord.z, 1.0);
    geom_coord_4 = view_mat * model_mat * vec4(vert_coord.x, (vert_coord.y + xyz_offset), vert_coord.z, 1.0);
    geom_coord_5 = view_mat * model_mat * vec4(vert_coord.x, vert_coord.y, (vert_coord.z - xyz_offset), 1.0);
    geom_coord_6 = view_mat * model_mat * vec4(vert_coord.x, vert_coord.y, (vert_coord.z + xyz_offset), 1.0);
}
"""
sel_geometry_shader_non_bonded = """
#version 330

const float xyz_offset = 0.5;

layout (points) in;
layout (line_strip, max_vertices = 6) out;

uniform mat4 proj_mat;

in vec3 geom_color[];
in vec4 geom_coord_1[];
in vec4 geom_coord_2[];
in vec4 geom_coord_3[];
in vec4 geom_coord_4[];
in vec4 geom_coord_5[];
in vec4 geom_coord_6[];

out vec3 frag_color;

void main(){
    gl_Position = proj_mat * geom_coord_1[0];
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * geom_coord_2[0];
    frag_color = geom_color[0];
    EmitVertex();
    EndPrimitive();
    
    gl_Position = proj_mat * geom_coord_3[0];
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * geom_coord_4[0];
    frag_color = geom_color[0];
    EmitVertex();
    EndPrimitive();
    
    gl_Position = proj_mat * geom_coord_5[0];
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * geom_coord_6[0];
    frag_color = geom_color[0];
    EmitVertex();
    EndPrimitive();
}
"""
sel_fragment_shader_non_bonded = """
#version 330

in vec3 frag_color;

out vec4 final_color;

void main(){
    final_color = vec4(frag_color, 1.0);
}
"""



