

vertex_shader_dots_surface  = """
#version 330

in vec3 vert_coord;
in vec3 vert_color;
const float vert_rad = 0.9;

out vec3 geom_color;
out vec4 geom_coord;
out float geom_rad;

void main(){
    geom_color = vert_color;
    geom_rad = vert_rad;
    geom_coord = vec4(vert_coord, 1.0);
}
"""
geometry_shader_dots_surface  = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

layout (points) in;
layout (points, max_vertices = 42) out;

vec3 p_00 = vec3( 0.850650787354, 0.525731086731, 0.000000000000);
vec3 p_01 = vec3(-0.850650787354, 0.525731086731, 0.000000000000);
vec3 p_02 = vec3(-0.850650787354,-0.525731086731, 0.000000000000);
vec3 p_03 = vec3( 0.850650787354,-0.525731086731, 0.000000000000);
vec3 p_04 = vec3( 0.525731086731, 0.000000000000, 0.850650787354);
vec3 p_05 = vec3( 0.525731086731, 0.000000000000,-0.850650787354);
vec3 p_06 = vec3(-0.525731086731, 0.000000000000,-0.850650787354);
vec3 p_07 = vec3(-0.525731086731, 0.000000000000, 0.850650787354);
vec3 p_08 = vec3( 0.000000000000, 0.850650787354, 0.525731086731);
vec3 p_09 = vec3( 0.000000000000,-0.850650787354, 0.525731086731);
vec3 p_10 = vec3( 0.000000000000,-0.850650787354,-0.525731086731);
vec3 p_11 = vec3( 0.000000000000, 0.850650787354,-0.525731086731);
vec3 p_12 = vec3( 0.309016972780, 0.499999970198, 0.809016942978);
vec3 p_13 = vec3(-0.309016972780, 0.499999970198, 0.809016942978);
vec3 p_14 = vec3( 0.000000000000, 0.000000000000, 0.999999940395);
vec3 p_15 = vec3(-0.309016972780,-0.499999970198, 0.809016942978);
vec3 p_16 = vec3( 0.309016972780,-0.499999970198, 0.809016942978);
vec3 p_17 = vec3( 0.000000000000, 0.000000000000,-0.999999940395);
vec3 p_18 = vec3(-0.309016972780, 0.499999970198,-0.809016942978);
vec3 p_19 = vec3( 0.309016972780, 0.499999970198,-0.809016942978);
vec3 p_20 = vec3( 0.309016972780,-0.499999970198,-0.809016942978);
vec3 p_21 = vec3(-0.309016972780,-0.499999970198,-0.809016942978);
vec3 p_22 = vec3( 0.809016942978, 0.309016972780, 0.499999970198);
vec3 p_23 = vec3( 0.809016942978,-0.309016972780, 0.499999970198);
vec3 p_24 = vec3( 0.999999940395, 0.000000000000, 0.000000000000);
vec3 p_25 = vec3( 0.809016942978,-0.309016972780,-0.499999970198);
vec3 p_26 = vec3( 0.809016942978, 0.309016972780,-0.499999970198);
vec3 p_27 = vec3(-0.809016942978,-0.309016972780, 0.499999970198);
vec3 p_28 = vec3(-0.809016942978, 0.309016972780, 0.499999970198);
vec3 p_29 = vec3(-0.999999940395, 0.000000000000, 0.000000000000);
vec3 p_30 = vec3(-0.809016942978, 0.309016972780,-0.499999970198);
vec3 p_31 = vec3(-0.809016942978,-0.309016972780,-0.499999970198);
vec3 p_32 = vec3( 0.499999970198, 0.809016942978, 0.309016972780);
vec3 p_33 = vec3( 0.499999970198, 0.809016942978,-0.309016972780);
vec3 p_34 = vec3( 0.000000000000, 0.999999940395, 0.000000000000);
vec3 p_35 = vec3(-0.499999970198, 0.809016942978,-0.309016972780);
vec3 p_36 = vec3(-0.499999970198, 0.809016942978, 0.309016972780);
vec3 p_37 = vec3( 0.000000000000,-0.999999940395, 0.000000000000);
vec3 p_38 = vec3( 0.499999970198,-0.809016942978,-0.309016972780);
vec3 p_39 = vec3( 0.499999970198,-0.809016942978, 0.309016972780);
vec3 p_40 = vec3(-0.499999970198,-0.809016942978, 0.309016972780);
vec3 p_41 = vec3(-0.499999970198,-0.809016942978,-0.309016972780);

in vec3 geom_color[];
in vec4 geom_coord[];
in float geom_rad[];

out vec3 frag_coord;
out vec3 frag_color;

void main(){
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_00*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_00*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();  
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_01*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_01*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_02*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_02*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_03*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_03*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_04*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_04*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_05*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_05*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_06*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_06*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_07*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_07*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_08*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_08*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_09*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_09*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_10*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_10*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_11*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_11*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_12*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_12*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_13*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_13*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_14*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_14*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_15*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_15*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_16*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_16*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_17*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_17*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_18*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_18*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_19*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_19*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_20*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_20*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_21*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_21*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_22*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_22*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_23*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_23*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_24*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_24*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_25*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_25*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_26*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_26*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_27*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_27*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_28*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_28*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_29*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_29*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_30*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_30*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_31*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_31*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_32*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_32*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_33*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_33*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_34*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_34*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_35*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_35*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_36*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_36*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_37*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_37*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_38*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_38*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_39*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_39*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_40*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_40*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_41*geom_rad[0]) + geom_coord[0].xyz, 1); frag_coord = p_41*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
}
"""
fragment_shader_dots_surface   = """
#version 330

uniform vec4 fog_color;
uniform float fog_start;
uniform float fog_end;

in vec3 frag_coord;
in vec3 frag_color;

out vec4 final_color;

void main(){
    final_color = vec4(frag_color, 1.0);
    
    
    //comentei o codigo antigo para simplificar a representacao
    //float rdist = length(gl_PointCoord - vec2(0.5, 0.5));
    //float dist = abs(frag_coord.z);
    //if (rdist > 0.5)
    //    discard;
    //float ligth_dist = length(gl_PointCoord - vec2(0.3, 0.3));
    //vec4 my_color = mix(vec4(frag_color, 1), vec4(0, 0, 0, 1), sqrt(ligth_dist)*.78);
    //if(dist>=fog_start){
    //    float fog_factor = (fog_end-dist)/(fog_end-fog_start);
    //    final_color = mix(fog_color, my_color, fog_factor);
    //}
    //else{
    //    final_color = my_color;
    //}
}
"""



sel_vertex_shader_dots_surface = """
#version 330

in vec3 vert_coord;
in vec3 vert_color;
const float vert_rad = 0.31;

out vec3 geom_color;
out vec4 geom_coord;
out float geom_rad;

void main(){
    geom_color = vert_color;
    geom_rad = vert_rad;
    geom_coord = vec4(vert_coord, 1.0);
}
"""
sel_geometry_shader_dots_surface = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

layout (points) in;
layout (points, max_vertices = 42) out;

vec3 p_00 = vec3( 0.850650787354, 0.525731086731, 0.000000000000);
vec3 p_01 = vec3(-0.850650787354, 0.525731086731, 0.000000000000);
vec3 p_02 = vec3(-0.850650787354,-0.525731086731, 0.000000000000);
vec3 p_03 = vec3( 0.850650787354,-0.525731086731, 0.000000000000);
vec3 p_04 = vec3( 0.525731086731, 0.000000000000, 0.850650787354);
vec3 p_05 = vec3( 0.525731086731, 0.000000000000,-0.850650787354);
vec3 p_06 = vec3(-0.525731086731, 0.000000000000,-0.850650787354);
vec3 p_07 = vec3(-0.525731086731, 0.000000000000, 0.850650787354);
vec3 p_08 = vec3( 0.000000000000, 0.850650787354, 0.525731086731);
vec3 p_09 = vec3( 0.000000000000,-0.850650787354, 0.525731086731);
vec3 p_10 = vec3( 0.000000000000,-0.850650787354,-0.525731086731);
vec3 p_11 = vec3( 0.000000000000, 0.850650787354,-0.525731086731);
vec3 p_12 = vec3( 0.309016972780, 0.499999970198, 0.809016942978);
vec3 p_13 = vec3(-0.309016972780, 0.499999970198, 0.809016942978);
vec3 p_14 = vec3( 0.000000000000, 0.000000000000, 0.999999940395);
vec3 p_15 = vec3(-0.309016972780,-0.499999970198, 0.809016942978);
vec3 p_16 = vec3( 0.309016972780,-0.499999970198, 0.809016942978);
vec3 p_17 = vec3( 0.000000000000, 0.000000000000,-0.999999940395);
vec3 p_18 = vec3(-0.309016972780, 0.499999970198,-0.809016942978);
vec3 p_19 = vec3( 0.309016972780, 0.499999970198,-0.809016942978);
vec3 p_20 = vec3( 0.309016972780,-0.499999970198,-0.809016942978);
vec3 p_21 = vec3(-0.309016972780,-0.499999970198,-0.809016942978);
vec3 p_22 = vec3( 0.809016942978, 0.309016972780, 0.499999970198);
vec3 p_23 = vec3( 0.809016942978,-0.309016972780, 0.499999970198);
vec3 p_24 = vec3( 0.999999940395, 0.000000000000, 0.000000000000);
vec3 p_25 = vec3( 0.809016942978,-0.309016972780,-0.499999970198);
vec3 p_26 = vec3( 0.809016942978, 0.309016972780,-0.499999970198);
vec3 p_27 = vec3(-0.809016942978,-0.309016972780, 0.499999970198);
vec3 p_28 = vec3(-0.809016942978, 0.309016972780, 0.499999970198);
vec3 p_29 = vec3(-0.999999940395, 0.000000000000, 0.000000000000);
vec3 p_30 = vec3(-0.809016942978, 0.309016972780,-0.499999970198);
vec3 p_31 = vec3(-0.809016942978,-0.309016972780,-0.499999970198);
vec3 p_32 = vec3( 0.499999970198, 0.809016942978, 0.309016972780);
vec3 p_33 = vec3( 0.499999970198, 0.809016942978,-0.309016972780);
vec3 p_34 = vec3( 0.000000000000, 0.999999940395, 0.000000000000);
vec3 p_35 = vec3(-0.499999970198, 0.809016942978,-0.309016972780);
vec3 p_36 = vec3(-0.499999970198, 0.809016942978, 0.309016972780);
vec3 p_37 = vec3( 0.000000000000,-0.999999940395, 0.000000000000);
vec3 p_38 = vec3( 0.499999970198,-0.809016942978,-0.309016972780);
vec3 p_39 = vec3( 0.499999970198,-0.809016942978, 0.309016972780);
vec3 p_40 = vec3(-0.499999970198,-0.809016942978, 0.309016972780);
vec3 p_41 = vec3(-0.499999970198,-0.809016942978,-0.309016972780);

in vec3 geom_color[];
in vec4 geom_coord[];
in float geom_rad[];

out vec3 frag_color;

void main(){
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_00*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_01*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_02*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_03*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_04*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_05*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_06*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_07*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_08*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_09*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_10*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_11*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_12*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_13*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_14*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_15*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_16*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_17*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_18*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_19*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_20*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_21*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_22*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_23*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_24*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_25*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_26*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_27*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_28*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_29*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_30*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_31*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_32*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_33*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_34*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_35*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_36*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_37*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_38*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_39*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_40*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
    gl_Position = proj_mat * view_mat * model_mat * vec4((p_41*geom_rad[0]) + geom_coord[0].xyz, 1); frag_color = geom_color[0]; EmitVertex(); EndPrimitive();
}
"""
sel_fragment_shader_dots_surface = """
#version 330

in vec3 frag_color;

out vec4 final_color;

void main(){
    float rdist = length(gl_PointCoord - vec2(0.5, 0.5));
    if (rdist > 0.5)
        discard;
    final_color = vec4(frag_color, 1.0);
}
"""



vertex_shader_dots = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;
uniform float vert_ext_linewidth;
uniform float vert_int_antialias;
uniform float vert_dot_factor;

in vec3 vert_coord;
in vec3 vert_color;
in float vert_dot_size;

attribute vec4 bckgrnd_color;

varying float frag_dot_size;
varying float frag_ext_linewidth;
varying float frag_int_antialias;
varying vec4 frag_dot_color;
varying vec4 frag_bckgrnd_color;

void main(){
    frag_dot_size = vert_dot_size * vert_dot_factor;
    frag_ext_linewidth = vert_ext_linewidth;
    frag_int_antialias = vert_int_antialias;
    frag_dot_color = vec4(vert_color, 1.0);
    frag_bckgrnd_color = bckgrnd_color;
    gl_Position = proj_mat * view_mat * model_mat * vec4(vert_coord, 1);
    gl_PointSize = vert_dot_size + 2*(vert_ext_linewidth + 1.5*vert_int_antialias);
}
"""
fragment_shader_dots = """
#version 330

uniform vec4 fog_color;
uniform float fog_start;
uniform float fog_end;

out vec4 final_color;

varying vec4 frag_bckgrnd_color;
varying vec4 frag_dot_color;
varying float frag_dot_size;
varying float frag_ext_linewidth;
varying float frag_int_antialias;

float disc(vec2 P, float size){
     float r = length((P.xy - vec2(0.5,0.5))*size);
     r -= frag_dot_size/2;
     return r;
}

void main(){
    // Calculate the distance of the object
    float size = frag_dot_size +2*(frag_ext_linewidth + 1.5*frag_int_antialias);
    float t = frag_ext_linewidth/2.0-frag_int_antialias;
    
    // gl_PointCoord is the pixel in the coordinate
    float r = disc(gl_PointCoord, size);
    float d = abs(r) - t;
    
    // This if else statement makes the circle ilusion
    if( r > (frag_ext_linewidth/2.0+frag_int_antialias)){
        discard;
    }
    else{
        if( d < 0.0 ){
            final_color = frag_bckgrnd_color;
        }
        else{
            if (r > 0){
                final_color = frag_bckgrnd_color;
            }
            else{
                final_color = frag_dot_color;
            }
        }
    }
}
"""




sel_vertex_shader_dots = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;
uniform float vert_ext_linewidth;
uniform float vert_int_antialias;
uniform float vert_dot_factor;

in vec3 vert_coord;
in vec3 vert_color;
in float vert_dot_size;

attribute vec4 bckgrnd_color;

varying float frag_dot_size;
varying float frag_ext_linewidth;
varying float frag_int_antialias;
varying vec4 frag_dot_color;
varying vec4 frag_bckgrnd_color;

void main(){
    frag_dot_size = vert_dot_size * vert_dot_factor;
    frag_ext_linewidth = vert_ext_linewidth;
    frag_int_antialias = vert_int_antialias;
    frag_dot_color = vec4(vert_color, 1.0);
    frag_bckgrnd_color = bckgrnd_color;
    gl_Position = proj_mat * view_mat * model_mat * vec4(vert_coord, 1);
    gl_PointSize = vert_dot_size + 2*(vert_ext_linewidth + 1.5*vert_int_antialias);
}
"""
sel_fragment_shader_dots = """
#version 330

uniform vec4 fog_color;
uniform float fog_start;
uniform float fog_end;

out vec4 final_color;

varying vec4 frag_bckgrnd_color;
varying vec4 frag_dot_color;
varying float frag_dot_size;
varying float frag_ext_linewidth;
varying float frag_int_antialias;

float disc(vec2 P, float size){
     float r = length((P.xy - vec2(0.5,0.5))*size);
     r -= frag_dot_size/2;
     return r;
}

void main(){
    // Calculate the distance of the object
    float size = frag_dot_size +2*(frag_ext_linewidth + 1.5*frag_int_antialias);
    float t = frag_ext_linewidth/2.0-frag_int_antialias;
    
    // gl_PointCoord is the pixel in the coordinate
    float r = disc(gl_PointCoord, size);
    float d = abs(r) - t;
    
    // This if else statement makes the circle ilusion
    if( r > (frag_ext_linewidth/2.0+frag_int_antialias)){
        discard;
    }
    else{
        if( d < 0.0 ){
            final_color = frag_bckgrnd_color;
        }
        else{
            if (r > 0){
                final_color = frag_bckgrnd_color;
            }
            else{
                final_color = frag_dot_color;
            }
        }
    }
}
"""







#sel_vertex_shader_dots  = """
##version 330
#
#uniform mat4 model_mat;
#uniform mat4 view_mat;
#uniform mat4 proj_mat;
#uniform float vert_ext_linewidth;
#
#in vec3  vert_coord;
#in vec3  vert_color;
#varying float frag_ext_linewidth;
#out vec3 index_color;
#
#void main(){
#    gl_Position  = proj_mat * view_mat * model_mat * vec4(vert_coord, 1.0);
#    gl_PointSize = 15;
#    index_color = vert_color;
#}
#"""
#sel_fragment_shader_dots  = """
##version 330
#
#in vec3 index_color;
#
#void main(){
#    gl_FragColor = vec4(index_color,1);
#}
#
#"""
#
#
#
#
#
#
#
#
#
#
#sel_vertex_shader_dots2 = """
## version 330
#
#uniform mat4 model_mat;
#uniform mat4 view_mat;
#uniform mat4 proj_mat;
#
#//attribute vec4 bckgrnd_color;
#
#in vec3 vert_coord;
#in vec3 vert_color;
#
#out vec3 v_color;
#
#void main()
#{
#    gl_Position = proj_mat * view_mat * model_mat * vec4(vert_coord, 1);
#    v_color     = vert_color; 
#    //frag_dot_color = vec4(vert_color, 1.0);
#    //frag_bckgrnd_color = bckgrnd_color;
#    
#}
#"""
#
#sel_fragment_shader_dots2 = """
# version 330
#
#in vec3 v_color;
#out vec4 out_color;
#
#void main()
#{
#    out_color = vec4(v_color, 1.0);
#}
#"""























