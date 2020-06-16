#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  glumpy.py
#  
#  Copyright 2020 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


vertex_shader_dot_sphere_backup = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;
const vec3 ligth_pos = vec3(0,0,2);

in vec3 vert_coord;     // attribute vec3 position;
in vec3 vert_color;     // attribute vec3 color;
//in float vert_dot_size; // attribute float radius;
const float vert_dot_size = 0.5;  // attribute float radius;

out vec3 frag_color;    // varying vec3 v_color;
out float frag_radius;  // varying float v_radius;
out float frag_size;    // varying float v_size;
out vec4 frag_coord;    // varying vec4 v_eye_position;

varying vec3 v_light_direction;

void main (void)
{
    frag_color = vert_color;
    frag_radius = vert_dot_size;
    frag_coord = view_mat * model_mat * vec4(vert_coord, 1.0);
    v_light_direction = normalize(ligth_pos);
    gl_Position = projection_mat * frag_coord;
    vec4 p = projection_mat * vec4(vert_dot_size, vert_dot_size, frag_coord.z, frag_coord.w);
    frag_size = 512.0 * p.x / p.w;
    gl_PointSize = frag_size + 5.0;
}
"""


fragment_shader_dot_sphere_backup = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;

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
in float frag_radius;        // varying float v_radius;
in float frag_size;          // varying float v_size;
in vec4 frag_coord;       // varying vec4 v_eye_position;
out vec4 color;
varying vec3 v_light_direction;

void main()
{
    vec2 P = gl_PointCoord.xy - vec2(0.5,0.5);
    float point_size = frag_size  + 5.0;
    float distance = length(P*point_size) - frag_size/2;
    vec2 texcoord = gl_PointCoord* 2.0 - vec2(1.0);
    float x = texcoord.x;
    float y = texcoord.y;
    float d = 1.0 - x*x - y*y;
    if (d <= 0.0) discard;
    float z = sqrt(d);
    vec4 pos = frag_coord;
    pos.z += frag_radius*z;
    vec3 pos2 = pos.xyz;
    pos = projection_mat * pos;
    gl_FragDepth = 0.5*(pos.z / pos.w)+0.5;
    vec3 normal = vec3(x,y,z);
    float diffuse = clamp(dot(normal, v_light_direction), 0.0, 1.0);
    vec4 color = vec4((0.5 + 0.5*diffuse)*frag_color, 1.0);
    gl_FragColor = outline(distance, 1.0, 1.0, vec4(0,0,0,1), color);
}
"""







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
vertex_shader_dot_simple  = """
# version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;


in vec3 vert_coord;
in vec3 vert_color;
out vec3 v_color;

void main()
{
    gl_Position = proj_mat * view_mat * model_mat * vec4(vert_coord, 1.0);
    v_color     = vert_color; 
}
"""

fragment_shader_dot_simple  = """
# version 330

uniform vec4 fog_color;
uniform float fog_start;
//uniform float fog_end;


in vec3 v_color;
out vec4 out_color;

void main()
{
    float dist = length(gl_PointCoord.xy - vec2(0.5,0.5));
    if (dist > 0.5)
        discard;
    
    
    //if(dist>=fog_start){
    //    float fog_factor = (fog_end-dist)/(fog_end-fog_start);
    //    out_color = mix(fog_color, vec4(v_color, 1.0), fog_factor);
    //}
    //else{
    //   out_color = vec4(v_color, 1.0);    
    //}
    out_color = vec4(v_color, 1.0);
}
"""


vertex_shader_dot_simple2  = """
# version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;


in vec3 vert_coord;
in vec3 vert_color;
out vec3 v_color;

void main()
{
    gl_Position = proj_mat * view_mat * model_mat * vec4(vert_coord, 1.0);
    v_color     = vert_color; 
}
"""

fragment_shader_dot_simple2  = """
# version 330

in vec3 v_color;
out vec4 out_color;

void main()
{
    float dist = length(gl_PointCoord.xy - vec2(0.5,0.5));
    if (dist > 0.5)
        discard;

	float ligth_dist = length(gl_PointCoord - vec2(0.3, 0.3));
	out_color = mix(vec4(v_color, 1), vec4(0, 0, 0, 1), sqrt(ligth_dist)*.78);

    //out_color = vec4(v_color, 1.0);
}
"""




vertex_shader_dot_simple3  = """
# version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;


in vec3 vert_coord;
in vec3 vert_color;
out vec3 v_color;
out vec4 frag_pos;

void main()
{
	frag_pos = view_mat * model_mat * vec4(vert_coord, 1.0);
    gl_Position = proj_mat * view_mat * model_mat * vec4(vert_coord, 1.0);
    v_color     = vert_color; 
}
"""

fragment_shader_dot_simple3  = """
# version 330
uniform mat4 proj_mat;

in vec3 v_color;
in vec4 frag_pos;
out vec4 out_color;

void main()
{

    vec2 P = gl_PointCoord.xy - vec2(0.5,0.5);
    float point_size = 5.0;
    float distance = length(P);
    vec2 texcoord = gl_PointCoord* 2.0 - vec2(1.0);
    float x = texcoord.x;
    float y = texcoord.y;
    float d = 1.0 - x*x - y*y;
    if (d <= 0.0)
        discard;
    float z = sqrt(d);
    vec4 pos = frag_pos;
    pos.z += z;
    pos = proj_mat * pos;
    gl_FragDepth = 0.5*(pos.z / pos.w)+0.5;

    float dist = length(gl_PointCoord.xy - vec2(0.5,0.5));
    if (dist > 0.5)
        discard;

	float ligth_dist = length(gl_PointCoord - vec2(0.3, 0.3));
	out_color = mix(vec4(v_color, 1), vec4(0, 0, 0, 1), sqrt(ligth_dist)*.78);

    //out_color = vec4(v_color, 1.0);
}
"""






shader_type ={
			0: { 'vertex_shader'      : vertex_shader_dot_simple     ,
			     'fragment_shader'    : fragment_shader_dot_simple   ,
				 'sel_vertex_shader'  : vertex_shader_dot_simple     ,
                 'sel_fragment_shader': fragment_shader_dot_simple

			   },
			
			
			1: {'vertex_shader'      : vertex_shader_dot_simple2   ,
			    'fragment_shader'    : fragment_shader_dot_simple2 ,
			    'sel_vertex_shader'  : vertex_shader_dot_simple           ,
			    'sel_fragment_shader': fragment_shader_dot_simple
				},



			2: {'vertex_shader'      : vertex_shader_dot_simple3  ,
			    'fragment_shader'    : fragment_shader_dot_simple3,
			    'sel_vertex_shader'  : vertex_shader_dot_simple           ,
			    'sel_fragment_shader': fragment_shader_dot_simple
				}

}













