
vertex_shader_freetype =  """
#version 330

uniform mat4 view_mat;

in vec3 vert_coord;
in vec4 vert_uv;

out vec4 geom_coord;
out vec4 geom_text_uv;

void main(){
    geom_coord = view_mat * vec4(vert_coord, 1.0);
    geom_text_uv = vert_uv;
}
"""
geometry_shader_freetype = """
#version 330

layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

uniform mat4 proj_mat;
uniform vec2 offset;

in vec4 geom_coord[];
in vec4 geom_text_uv[];

out vec2 frag_text_uv;

void calculate_uv(in vec4 coord, out vec2 uvA, out vec2 uvB, out vec2 uvC, out vec2 uvD){
    // Taking the data from the upper-left and lower-right points of the quad,
    // it generates the coordinates of two triangles to form the letter.
    // The quad is created using the following pattern:
    //                                
    // uvA       uvD     uvA      uvD 
    //  |         |       |     /  |  
    //  |         |  -->  |   /    |  
    //  |         |       | /      |  
    // uvB-------uvC     uvB      uvC 
    //                                
    uvA = vec2(coord.xy);
    uvB = vec2(coord.xw);
    uvC = vec2(coord.zw);
    uvD = vec2(coord.zy);
}

void calculate_points(in vec4 coord, out vec4 pA, out vec4 pB, out vec4 pC, out vec4 pD){
    // Creates the coordinates for a quad using the coord vector as center and
    // the xyz_offset as margins, defining the letter size. You can change the
    // xyz_value to get a bigger letter, but this will reduce the resolution.
    // Using # as a coordinate example, the quad is constructed as:
    //                                
    //                \|/         ┌--┐ 
    //      #   -->   -#-   -->   |  | 
    //                /|\         └--┘ 
    //                                
    pA = vec4(coord.x - offset.x, coord.y + offset.y, coord.z, 1.0);
    pB = vec4(coord.x - offset.x, coord.y - offset.y, coord.z, 1.0);
    pC = vec4(coord.x + offset.x, coord.y - offset.y, coord.z, 1.0);
    pD = vec4(coord.x + offset.x, coord.y + offset.y, coord.z, 1.0);
}

void main(){
    vec2 textA, textB, textC, textD;
    vec4 pointA, pointB, pointC, pointD;
    calculate_uv(geom_text_uv[0], textA, textB, textC, textD);
    calculate_points(geom_coord[0], pointA, pointB, pointC, pointD);
    gl_Position = proj_mat * pointA; frag_text_uv = textA; EmitVertex();
    gl_Position = proj_mat * pointB; frag_text_uv = textB; EmitVertex();
    gl_Position = proj_mat * pointD; frag_text_uv = textD; EmitVertex();
    gl_Position = proj_mat * pointC; frag_text_uv = textC; EmitVertex();
    EndPrimitive();
}
"""
fragment_shader_freetype = """
#version 330

uniform sampler2D textu;
uniform vec4 text_color;

in vec2 frag_text_uv;

out vec4 final_color;

void main(){
    vec4 sampled = vec4(1.0, 1.0, 1.0, texture(textu, frag_text_uv).r);
    if (sampled.a==0.0)
        discard;
    final_color = text_color * sampled;
}
"""


v_shader_freetype =  """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;

in vec3 vert_coord;
in vec4 vert_uv;

out vec4 geom_coord;
out vec4 geom_text_uv;

void main(){
    geom_coord = view_mat * model_mat * vec4(vert_coord.xy, 0.0, 1.0);
    geom_text_uv = vert_uv;
}
"""
g_shader_freetype = """
#version 330

layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

uniform mat4 proj_mat;
uniform vec2 offset;

in vec4 geom_coord[];
in vec4 geom_text_uv[];

out vec2 frag_text_uv;

void calculate_uv(in vec4 coord, out vec2 uvA, out vec2 uvB, out vec2 uvC, out vec2 uvD){
    // Taking the data from the upper-left and lower-right points of the quad,
    // it generates the coordinates of two triangles to form the letter.
    // The quad is created using the following pattern:
    //                                
    // uvA       uvD     uvA      uvD 
    //  |         |       |     /  |  
    //  |         |  -->  |   /    |  
    //  |         |       | /      |  
    // uvB-------uvC     uvB      uvC 
    //                                
    uvA = vec2(coord.xy);
    uvB = vec2(coord.xw);
    uvC = vec2(coord.zw);
    uvD = vec2(coord.zy);
}

void calculate_points(in vec4 coord, out vec4 pA, out vec4 pB, out vec4 pC, out vec4 pD){
    // Creates the coordinates for a quad using the coord vector as center and
    // the xyz_offset as margins, defining the letter size. You can change the
    // xyz_value to get a bigger letter, but this will reduce the resolution.
    // Using # as a coordinate example, the quad is constructed as:
    //                                
    //                \|/         ┌--┐ 
    //      #   -->   -#-   -->   |  | 
    //                /|\         └--┘ 
    //                                
    pA = vec4(coord.x - offset.x, coord.y + offset.y, coord.z, 1.0);
    pB = vec4(coord.x - offset.x, coord.y - offset.y, coord.z, 1.0);
    pC = vec4(coord.x + offset.x, coord.y - offset.y, coord.z, 1.0);
    pD = vec4(coord.x + offset.x, coord.y + offset.y, coord.z, 1.0);
}

void main(){
    vec2 textA, textB, textC, textD;
    vec4 pointA, pointB, pointC, pointD;
    calculate_uv(geom_text_uv[0], textA, textB, textC, textD);
    calculate_points(geom_coord[0], pointA, pointB, pointC, pointD);
    gl_Position = proj_mat * pointA; frag_text_uv = textA; EmitVertex();
    gl_Position = proj_mat * pointB; frag_text_uv = textB; EmitVertex();
    gl_Position = proj_mat * pointD; frag_text_uv = textD; EmitVertex();
    gl_Position = proj_mat * pointC; frag_text_uv = textC; EmitVertex();
    EndPrimitive();
}
"""
f_shader_freetype = """
#version 330

uniform sampler2D textu;
uniform vec4 text_color;

in vec2 frag_text_uv;

out vec4 final_color;

void main(){
    vec4 sampled = vec4(1.0, 1.0, 1.0, texture(textu, frag_text_uv).r);
    if (sampled.a==0.0)
        discard;
    final_color = text_color * sampled;
}
"""
