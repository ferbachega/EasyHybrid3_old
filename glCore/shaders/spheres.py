

#vertex_shader_spheres = """
##version 330
#
#uniform mat4 model_mat;
#uniform mat4 view_mat;
#uniform mat4 proj_mat;
#
#in vec3 vert_coord;
#in vec3 vert_centr;
#in vec3 vert_color;
#
#varying vec3 vert_norm;
#
#out vec3 frag_coord;
#out vec3 frag_color;
#out vec3 frag_norm;
#
#void main(){
#    mat4 modelview = view_mat * model_mat;
#    gl_Position = proj_mat * modelview * vec4(vert_coord, 1.0);
#    vert_norm = normalize(vert_coord - vert_centr);
#    frag_coord = -vec3(modelview * vec4(vert_coord, 1.0));
#    frag_norm = mat3(transpose(inverse(model_mat))) * vert_norm;
#    frag_color = vert_color;
#}
#"""
#fragment_shader_spheres = """
##version 330
#
#struct Light {
#    vec3 position;
#    //vec3 color;
#    vec3 intensity;
#    //vec3 specular_color;
#    float ambient_coef;
#    float shininess;
#};
#
#uniform Light my_light;
#
#uniform vec4 fog_color;
#uniform float fog_start;
#uniform float fog_end;
#
#in vec3 frag_coord;
#in vec3 frag_color;
#in vec3 frag_norm;
#
#out vec4 final_color;
#
#void main(){
#    vec3 normal = normalize(frag_norm);
#    vec3 vert_to_light = normalize(my_light.position);
#    vec3 vert_to_cam = normalize(frag_coord);
#    
#    // Ambient Component
#    vec3 ambient = my_light.ambient_coef * frag_color * my_light.intensity;
#    
#    // Diffuse component
#    float diffuse_coef = max(0.0, dot(normal, vert_to_light));
#    vec3 diffuse = diffuse_coef * frag_color * my_light.intensity;
#    
#    // Specular component
#    float specular_coef = 0.0;
#    if (diffuse_coef > 0.0)
#        specular_coef = pow(max(0.0, dot(vert_to_cam, reflect(-vert_to_light, normal))), my_light.shininess);
#    vec3 specular = specular_coef * my_light.intensity;
#    specular = specular * (vec3(1) - diffuse);
#    
#    vec4 my_color = vec4(ambient + diffuse + specular, 1.0);
#    
#    float dist = abs(frag_coord.z);
#    if(dist>=fog_start){
#        float fog_factor = (fog_end-dist)/(fog_end-fog_start);
#        final_color = mix(fog_color, my_color, fog_factor);
#    }
#    else{
#        final_color = my_color;
#    }
#}
#"""
#


sel_vertex_shader_spheres = """
#version 330
precision highp float; 
precision highp int;
uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in vec3 vert_coord;
in vec3 vert_color;

out vec3 frag_color;

void main(){
    gl_Position = proj_mat * view_mat * model_mat * vec4(vert_coord, 1.0);
    frag_color = vert_color;
}
"""
sel_fragment_shader_spheres = """
#version 330
precision highp float; 
precision highp int;
in vec3 frag_color;

out vec4 final_color;

void main(){
    final_color = vec4(frag_color, 1.0);
}
"""





v_shader_spheres_NOT_USED = """
#version 330
precision highp float; 
precision highp int;
uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in vec3 vert_coord;
in vec3 vert_centr;
in vec3 vert_color;

varying vec3 vert_norm;

out vec3 frag_coord;
out vec3 frag_color;
out vec3 frag_norm;

void main(){
   mat4 modelview = view_mat * model_mat;
   gl_Position = proj_mat * modelview * vec4(vert_coord, 1.0);
   vert_norm = normalize(vert_coord - vert_centr);
   frag_coord = -vec3(modelview * vec4(vert_coord, 1.0));
   frag_norm = mat3(transpose(inverse(model_mat))) * vert_norm;
   frag_color = vert_color;
}
"""
f_shader_spheres_NOT_USED = """
#version 330
precision highp float; 
precision highp int;
struct Light {
   vec3 position;
   //vec3 color;
   vec3 intensity;
   //vec3 specular_color;
   float ambient_coef;
   float shininess;
};

uniform Light my_light;

in vec3 frag_coord;
in vec3 frag_color;
in vec3 frag_norm;

out vec4 final_color;

void main(){
   vec3 normal = normalize(frag_norm);
   vec3 vert_to_light = normalize(my_light.position);
   vec3 vert_to_cam = normalize(frag_coord);
   
   // Ambient Component
   vec3 ambient = my_light.ambient_coef * frag_color * my_light.intensity;
   
   // Diffuse component
   float diffuse_coef = max(0.0, dot(normal, vert_to_light));
   vec3 diffuse = diffuse_coef * frag_color * my_light.intensity;
   
   // Specular component
   float specular_coef = 0.0;
   if (diffuse_coef > 0.0)
      specular_coef = pow(max(0.0, dot(vert_to_cam, reflect(-vert_to_light, normal))), my_light.shininess);
   vec3 specular = specular_coef * my_light.intensity;
   specular = specular * (vec3(1) - diffuse);
   
   final_color = vec4(ambient + diffuse + specular, 1.0);
}
"""

vertex_shader_spheres_ON_THE_FLY_NOT_USED = """
#version 330
precision highp float; 
precision highp int;
uniform mat4 model_mat;
uniform mat4 view_mat;

in vec3 vert_coord;
in vec3 vert_color;
const float vert_rad = 0.3;

out vec3 geom_color;
out vec4 geom_coord;
out float geom_rad;

void main(){
    geom_color = vert_color;
    geom_rad = vert_rad;
    geom_coord = view_mat * model_mat * vec4(vert_coord, 1.0);
}
"""
geometry_shader_spheres_ON_THE_FLY_NOT_USED = """
#version 330
precision highp float; 
precision highp int;
uniform mat4 proj_mat;

layout (points) in;
layout (triangle_strip, max_vertices = 100) out;

vec3 p_00 = vec3( 0.000000, 0.000000,-1.000000);
vec3 p_01 = vec3( 0.723607,-0.525725,-0.447220);
vec3 p_02 = vec3(-0.276388,-0.850649,-0.447220);
vec3 p_03 = vec3(-0.894426, 0.000000,-0.447216);
vec3 p_04 = vec3(-0.276388, 0.850649,-0.447220);
vec3 p_05 = vec3( 0.723607, 0.525725,-0.447220);
vec3 p_06 = vec3( 0.276388,-0.850649, 0.447220);
vec3 p_07 = vec3(-0.723607,-0.525725, 0.447220);
vec3 p_08 = vec3(-0.723607, 0.525725, 0.447220);
vec3 p_09 = vec3( 0.276388, 0.850649, 0.447220);
vec3 p_10 = vec3( 0.894426, 0.000000, 0.447216);
vec3 p_11 = vec3( 0.000000, 0.000000, 1.000000);
vec3 p_12 = vec3(-0.162456,-0.499995,-0.850654);
vec3 p_13 = vec3( 0.425323,-0.309011,-0.850654);
vec3 p_14 = vec3( 0.262869,-0.809012,-0.525738);
vec3 p_15 = vec3( 0.850648, 0.000000,-0.525736);
vec3 p_16 = vec3( 0.425323, 0.309011,-0.850654);
vec3 p_17 = vec3(-0.525730, 0.000000,-0.850652);
vec3 p_18 = vec3(-0.688189,-0.499997,-0.525736);
vec3 p_19 = vec3(-0.162456, 0.499995,-0.850654);
vec3 p_20 = vec3(-0.688189, 0.499997,-0.525736);
vec3 p_21 = vec3( 0.262869, 0.809012,-0.525738);
vec3 p_22 = vec3( 0.951058,-0.309013, 0.000000);
vec3 p_23 = vec3( 0.951058, 0.309013, 0.000000);
vec3 p_24 = vec3( 0.000000,-1.000000, 0.000000);
vec3 p_25 = vec3( 0.587786,-0.809017, 0.000000);
vec3 p_26 = vec3(-0.951058,-0.309013, 0.000000);
vec3 p_27 = vec3(-0.587786,-0.809017, 0.000000);
vec3 p_28 = vec3(-0.587786, 0.809017, 0.000000);
vec3 p_29 = vec3(-0.951058, 0.309013, 0.000000);
vec3 p_30 = vec3( 0.587786, 0.809017, 0.000000);
vec3 p_31 = vec3( 0.000000, 1.000000, 0.000000);
vec3 p_32 = vec3( 0.688189,-0.499997, 0.525736);
vec3 p_33 = vec3(-0.262869,-0.809012, 0.525738);
vec3 p_34 = vec3(-0.850648, 0.000000, 0.525736);
vec3 p_35 = vec3(-0.262869, 0.809012, 0.525738);
vec3 p_36 = vec3( 0.688189, 0.499997, 0.525736);
vec3 p_37 = vec3( 0.162456,-0.499995, 0.850654);
vec3 p_38 = vec3( 0.525730, 0.000000, 0.850652);
vec3 p_39 = vec3(-0.425323,-0.309011, 0.850654);
vec3 p_40 = vec3(-0.425323, 0.309011, 0.850654);
vec3 p_41 = vec3( 0.162456, 0.499995, 0.850654);

in vec3 geom_color[];
in vec4 geom_coord[];
in float geom_rad[];

out vec3 frag_coord;
out vec3 frag_color;
out vec3 frag_norm;

void main(){
    gl_Position = proj_mat * vec4((p_04*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_04*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_04; EmitVertex();
    gl_Position = proj_mat * vec4((p_31*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_31*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_31; EmitVertex();
    gl_Position = proj_mat * vec4((p_21*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_21*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_21; EmitVertex();
    gl_Position = proj_mat * vec4((p_30*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_30*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_30; EmitVertex();
    gl_Position = proj_mat * vec4((p_05*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_05*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_05; EmitVertex();
    gl_Position = proj_mat * vec4((p_23*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_23*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_23; EmitVertex();
    gl_Position = proj_mat * vec4((p_15*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_15*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_15; EmitVertex();
    gl_Position = proj_mat * vec4((p_22*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_22*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_22; EmitVertex();
    gl_Position = proj_mat * vec4((p_01*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_01*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_01; EmitVertex();
    gl_Position = proj_mat * vec4((p_15*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_15*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_15; EmitVertex();
    gl_Position = proj_mat * vec4((p_13*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_13*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_13; EmitVertex();
    gl_Position = proj_mat * vec4((p_16*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_16*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_16; EmitVertex();
    gl_Position = proj_mat * vec4((p_00*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_00*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_00; EmitVertex();
    gl_Position = proj_mat * vec4((p_19*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_19*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_19; EmitVertex();
    gl_Position = proj_mat * vec4((p_17*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_17*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_17; EmitVertex();
    gl_Position = proj_mat * vec4((p_00*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_00*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_00; EmitVertex();
    gl_Position = proj_mat * vec4((p_12*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_12*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_12; EmitVertex();
    gl_Position = proj_mat * vec4((p_13*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_13*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_13; EmitVertex();
    gl_Position = proj_mat * vec4((p_14*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_14*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_14; EmitVertex();
    gl_Position = proj_mat * vec4((p_01*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_01*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_01; EmitVertex();
    gl_Position = proj_mat * vec4((p_25*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_25*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_25; EmitVertex();
    gl_Position = proj_mat * vec4((p_22*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_22*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_22; EmitVertex();
    gl_Position = proj_mat * vec4((p_32*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_32*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_32; EmitVertex();
    gl_Position = proj_mat * vec4((p_10*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_10*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_10; EmitVertex();
    gl_Position = proj_mat * vec4((p_38*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_38*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_38; EmitVertex();
    gl_Position = proj_mat * vec4((p_36*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_36*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_36; EmitVertex();
    gl_Position = proj_mat * vec4((p_41*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_41*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_41; EmitVertex();
    gl_Position = proj_mat * vec4((p_09*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_09*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_09; EmitVertex();
    gl_Position = proj_mat * vec4((p_35*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_35*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_35; EmitVertex();
    gl_Position = proj_mat * vec4((p_31*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_31*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_31; EmitVertex();
    gl_Position = proj_mat * vec4((p_28*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_28*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_28; EmitVertex();
    gl_Position = proj_mat * vec4((p_04*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_04*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_04; EmitVertex();
    gl_Position = proj_mat * vec4((p_20*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_20*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_20; EmitVertex();
    gl_Position = proj_mat * vec4((p_19*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_19*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_19; EmitVertex();
    gl_Position = proj_mat * vec4((p_17*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_17*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_17; EmitVertex();
    gl_Position = proj_mat * vec4((p_20*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_20*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_20; EmitVertex();
    gl_Position = proj_mat * vec4((p_03*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_03*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_03; EmitVertex();
    gl_Position = proj_mat * vec4((p_29*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_29*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_29; EmitVertex();
    gl_Position = proj_mat * vec4((p_26*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_26*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_26; EmitVertex();
    gl_Position = proj_mat * vec4((p_34*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_34*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_34; EmitVertex();
    gl_Position = proj_mat * vec4((p_07*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_07*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_07; EmitVertex();
    gl_Position = proj_mat * vec4((p_39*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_39*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_39; EmitVertex();
    gl_Position = proj_mat * vec4((p_33*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_33*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_33; EmitVertex();
    gl_Position = proj_mat * vec4((p_37*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_37*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_37; EmitVertex();
    gl_Position = proj_mat * vec4((p_06*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_06*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_06; EmitVertex();
    gl_Position = proj_mat * vec4((p_32*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_32*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_32; EmitVertex();
    gl_Position = proj_mat * vec4((p_37*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_37*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_37; EmitVertex();
    gl_Position = proj_mat * vec4((p_38*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_38*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_38; EmitVertex();
    gl_Position = proj_mat * vec4((p_11*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_11*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_11; EmitVertex();
    gl_Position = proj_mat * vec4((p_41*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_41*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_41; EmitVertex();
    gl_Position = proj_mat * vec4((p_40*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_40*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_40; EmitVertex();
    gl_Position = proj_mat * vec4((p_35*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_35*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_35; EmitVertex();
    gl_Position = proj_mat * vec4((p_08*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_08*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_08; EmitVertex();
    gl_Position = proj_mat * vec4((p_28*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_28*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_28; EmitVertex();
    gl_Position = proj_mat * vec4((p_29*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_29*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_29; EmitVertex();
    gl_Position = proj_mat * vec4((p_20*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_20*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_20; EmitVertex();
    EndPrimitive();
    
    gl_Position = proj_mat * vec4((p_32*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_32*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_32; EmitVertex();
    gl_Position = proj_mat * vec4((p_25*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_25*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_25; EmitVertex();
    gl_Position = proj_mat * vec4((p_06*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_06*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_06; EmitVertex();
    gl_Position = proj_mat * vec4((p_24*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_24*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_24; EmitVertex();
    gl_Position = proj_mat * vec4((p_33*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_33*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_33; EmitVertex();
    gl_Position = proj_mat * vec4((p_27*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_27*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_27; EmitVertex();
    gl_Position = proj_mat * vec4((p_07*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_07*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_07; EmitVertex();
    gl_Position = proj_mat * vec4((p_26*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_26*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_26; EmitVertex();
    gl_Position = proj_mat * vec4((p_27*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_27*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_27; EmitVertex();
    gl_Position = proj_mat * vec4((p_18*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_18*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_18; EmitVertex();
    gl_Position = proj_mat * vec4((p_02*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_02*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_02; EmitVertex();
    gl_Position = proj_mat * vec4((p_12*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_12*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_12; EmitVertex();
    gl_Position = proj_mat * vec4((p_14*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_14*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_14; EmitVertex();
    gl_Position = proj_mat * vec4((p_02*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_02*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_02; EmitVertex();
    gl_Position = proj_mat * vec4((p_24*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_24*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_24; EmitVertex();
    gl_Position = proj_mat * vec4((p_27*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_27*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_27; EmitVertex();
    EndPrimitive();
    
    gl_Position = proj_mat * vec4((p_04*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_04*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_04; EmitVertex();
    gl_Position = proj_mat * vec4((p_19*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_19*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_19; EmitVertex();
    gl_Position = proj_mat * vec4((p_21*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_21*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_21; EmitVertex();
    gl_Position = proj_mat * vec4((p_16*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_16*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_16; EmitVertex();
    gl_Position = proj_mat * vec4((p_05*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_05*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_05; EmitVertex();
    gl_Position = proj_mat * vec4((p_15*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_15*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_15; EmitVertex();
    EndPrimitive();
    
    gl_Position = proj_mat * vec4((p_29*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_29*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_29; EmitVertex();
    gl_Position = proj_mat * vec4((p_08*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_08*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_08; EmitVertex();
    gl_Position = proj_mat * vec4((p_34*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_34*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_34; EmitVertex();
    gl_Position = proj_mat * vec4((p_40*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_40*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_40; EmitVertex();
    gl_Position = proj_mat * vec4((p_39*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_39*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_39; EmitVertex();
    gl_Position = proj_mat * vec4((p_11*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_11*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_11; EmitVertex();
    gl_Position = proj_mat * vec4((p_37*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_37*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_37; EmitVertex();
    EndPrimitive();
    
    gl_Position = proj_mat * vec4((p_22*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_22*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_22; EmitVertex();
    gl_Position = proj_mat * vec4((p_10*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_10*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_10; EmitVertex();
    gl_Position = proj_mat * vec4((p_23*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_23*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_23; EmitVertex();
    gl_Position = proj_mat * vec4((p_36*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_36*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_36; EmitVertex();
    gl_Position = proj_mat * vec4((p_30*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_30*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_30; EmitVertex();
    gl_Position = proj_mat * vec4((p_09*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_09*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_09; EmitVertex();
    gl_Position = proj_mat * vec4((p_31*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_31*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_31; EmitVertex();
    EndPrimitive();
    
    gl_Position = proj_mat * vec4((p_26*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_26*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_26; EmitVertex();
    gl_Position = proj_mat * vec4((p_03*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_03*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_03; EmitVertex();
    gl_Position = proj_mat * vec4((p_18*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_18*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_18; EmitVertex();
    gl_Position = proj_mat * vec4((p_17*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_17*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_17; EmitVertex();
    gl_Position = proj_mat * vec4((p_12*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_12*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_12; EmitVertex();
    EndPrimitive();
    
    gl_Position = proj_mat * vec4((p_24*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_24*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_24; EmitVertex();
    gl_Position = proj_mat * vec4((p_14*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_14*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_14; EmitVertex();
    gl_Position = proj_mat * vec4((p_25*geom_rad[0])+geom_coord[0].xyz,1); frag_coord = p_25*geom_rad[0]+geom_coord[0].xyz; frag_color = geom_color[0]; frag_norm = p_25; EmitVertex();
    EndPrimitive();
}
"""
fragment_shader_spheres_ON_THE_FLY_NOT_USED = """
#version 330
precision highp float; 
precision highp int;
struct Light {
   vec3 position;
   //vec3 color;
   vec3 intensity;
   //vec3 specular_color;
   float ambient_coef;
   float shininess;
};

uniform Light my_light;

uniform vec4 fog_color;
uniform float fog_start;
uniform float fog_end;

in vec3 frag_coord;
in vec3 frag_color;
in vec3 frag_norm;

out vec4 final_color;

void main(){
    vec3 normal = normalize(frag_norm);
    vec3 vert_to_light = normalize(my_light.position);
    vec3 vert_to_cam = normalize(frag_coord);
    
    // Ambient Component
    vec3 ambient = my_light.ambient_coef * frag_color * my_light.intensity;
    
    // Diffuse component
    float diffuse_coef = max(0.0, dot(normal, vert_to_light));
    vec3 diffuse = diffuse_coef * frag_color * my_light.intensity;
    
    // Specular component
    float specular_coef = 0.0;
    if (diffuse_coef > 0.0)
        specular_coef = pow(max(0.0, dot(vert_to_cam, reflect(vert_to_light, normal))), my_light.shininess);
    vec3 specular = specular_coef * my_light.intensity;
    specular = specular * (vec3(1) - diffuse);
    vec4 my_color = vec4(ambient + diffuse + specular, 1.0);
    
    float dist = abs(frag_coord.z);
    if(dist>=fog_start){
        float fog_factor = (fog_end-dist)/(fog_end-fog_start);
        final_color = mix(fog_color, my_color, fog_factor);
    }
    else{
        final_color = my_color;
    }
}
"""



v_s_glumpy = """
#version 330
precision highp float; 
precision highp int;
uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;
uniform mat3 normal_mat;

in vec3 vert_coord;        // attribute vec3 position;
in vec3 vert_color;        // attribute vec3 color;
in float vert_dot_size;  // attribute float radius;
//const float vert_dot_size = 0.5;  // attribute float radius;

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
    gl_Position = projection_mat * frag_coord;
    vec4 p = projection_mat * vec4(vert_dot_size, vert_dot_size, frag_coord.z, frag_coord.w);
    f_size = 512.0 * p.x / p.w;
    gl_PointSize = f_size + 5.0;
}
"""
f_s_glumpy = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;
uniform mat3 normal_mat;

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
    pos = projection_mat * pos;
    gl_FragDepth = 0.5*(pos.z / pos.w)+0.5;
    vec3 normal = vec3(x,y,z);
    float diffuse = clamp(dot(normal, v_light_direction), 0.0, 1.0);
    vec4 color = vec4((0.5 + 0.5*diffuse)*frag_color, 1.0);
    gl_FragColor = outline(distance, 1.0, 1.0, vec4(0,0,0,1), color);
    // gl_FragColor = color;
}
"""





vertex_shader_spheres = """
#version 330
precision highp float; 
precision highp int;
uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;

in vec3 vert_coord;
in vec3 vert_centr;
in vec3 vert_color;

varying vec3 vert_norm;

out vec3 frag_coord;
out vec3 frag_color;
out vec3 frag_norm;

void main(){
    mat4 modelview = view_mat * model_mat;
    gl_Position = proj_mat * modelview * vec4(vert_coord, 1.0);
    vert_norm = normalize(vert_coord - vert_centr);
    frag_coord = -vec3(modelview * vec4(vert_coord, 1.0));
    frag_norm = mat3(transpose(inverse(model_mat))) * vert_norm;
    frag_color = vert_color;
}
"""
fragment_shader_spheres = """
#version 330
precision highp float; 
precision highp int;
struct Light {
    vec3 position;
    //vec3 color;
    vec3 intensity;
    //vec3 specular_color;
    float ambient_coef;
    float shininess;
};

uniform Light my_light;

uniform vec4 fog_color;
uniform float fog_start;
uniform float fog_end;

in vec3 frag_coord;
in vec3 frag_color;
in vec3 frag_norm;

out vec4 final_color;

void main(){
    vec3 normal = normalize(frag_norm);
    vec3 vert_to_light = normalize(my_light.position);
    vec3 vert_to_cam = normalize(frag_coord);
    
    // Ambient Component
    vec3 ambient = my_light.ambient_coef * frag_color * my_light.intensity;
    
    // Diffuse component
    float diffuse_coef = max(0.0, dot(normal, vert_to_light));
    vec3 diffuse = diffuse_coef * frag_color * my_light.intensity;
    
    // Specular component
    float specular_coef = 0.0;
    if (diffuse_coef > 0.0)
        specular_coef = pow(max(0.0, dot(vert_to_cam, reflect(-vert_to_light, normal))), my_light.shininess);
    vec3 specular = specular_coef * my_light.intensity;
    specular = specular * (vec3(1) - diffuse);
    
    vec4 my_color = vec4(ambient + diffuse + specular, 1.0);
    
    float dist = abs(frag_coord.z);
    if(dist>=fog_start){
        float fog_factor = (fog_end-dist)/(fog_end-fog_start);
        final_color = mix(fog_color, my_color, fog_factor);
    }
    else{
        final_color = my_color;
    }
}
"""

