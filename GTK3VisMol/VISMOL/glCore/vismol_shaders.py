#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  vismol_shaders.py
#  
#  Copyright 2016 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
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

vertex_shader_sticks = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;

in vec3 vert_coord;
in vec3 vert_color;
const float vert_rad = 0.1;

out vec3 geom_color;
out vec4 geom_coord;
out float geom_rad;

void main(){
    geom_color = vert_color;
    geom_rad = vert_rad;
    geom_coord = view_mat * model_mat * vec4(vert_coord, 1.0);
}
"""
geometry_shader_sticks = """
#version 330

layout (lines) in;
layout (triangle_strip, max_vertices = 40) out;

uniform mat4 proj_mat;

in vec3 geom_color[];
in vec4 geom_coord[];
in float geom_rad[];

out vec3 frag_coord;
out vec3 frag_color;
out vec3 frag_norm;

// This data is used for the cylinder vertices, i.e. the points that form the
// circle in a horizontal cut of the cylinder. The first half are the points
// at the begining of the cylinder, and the last half are the points at the end.
// The quantity of points should be changed to get a smoother cylinder, but that
// will result in more resources used.
vec3 bs_0 = vec3( 1.000000000000, 0.000000000000, 0.000000000000); // base
vec3 bs_1 = vec3( 0.766044443119, 0.000000000000, 0.642787609687); // base
vec3 bs_2 = vec3( 0.173648177667, 0.000000000000, 0.984807753012); // base
vec3 bs_3 = vec3(-0.500000000000, 0.000000000000, 0.866025403784); // base
vec3 bs_4 = vec3(-0.939692620786, 0.000000000000, 0.342020143326); // base
vec3 bs_5 = vec3(-0.939692620786, 0.000000000000,-0.342020143326); // base
vec3 bs_6 = vec3(-0.500000000000, 0.000000000000,-0.866025403784); // base
vec3 bs_7 = vec3( 0.173648177667, 0.000000000000,-0.984807753012); // base
vec3 bs_8 = vec3( 0.766044443119, 0.000000000000,-0.642787609687); // base
vec3 up_0 = vec3( 0.939692620786, 0.000000000000, 0.342020143326); // up
vec3 up_1 = vec3( 0.500000000000, 0.000000000000, 0.866025403784); // up
vec3 up_2 = vec3(-0.173648177667, 0.000000000000, 0.984807753012); // up
vec3 up_3 = vec3(-0.766044443119, 0.000000000000, 0.642787609687); // up
vec3 up_4 = vec3(-1.000000000000, 0.000000000000, 0.000000000000); // up
vec3 up_5 = vec3(-0.766044443119, 0.000000000000,-0.642787609687); // up
vec3 up_6 = vec3(-0.173648177667, 0.000000000000,-0.984807753012); // up
vec3 up_7 = vec3( 0.500000000000, 0.000000000000,-0.866025403784); // up
vec3 up_8 = vec3( 0.939692620786, 0.000000000000,-0.342020143326); // up

// The rotation matrix used for translating the cylinder points to their correct
// places is rot_mat. This matrix is created using the my_glRotatef function,
// see the function documentation to get more information.
varying mat3 rot_mat;

// mid_point is the middle point in the line.
varying vec3 mid_point;

// These points are the vertices calculated for the cylinder.
varying vec3 p_00, p_01, p_02, p_03, p_04, p_05, p_06, p_07, p_08;
varying vec3 p_09, p_10, p_11, p_12, p_13, p_14, p_15, p_16, p_17;
varying vec3 p_18, p_19, p_20, p_21, p_22, p_23, p_24, p_25, p_26;

float get_angle(vec3 vec_A, vec3 vec_B){
    // Returns the angle in radians formed between the vectors A and B. The
    // vectors are initially normalized to avoid errors.
    // The initial result is clamped to the [-1,+1] range to avoid errors in
    // the arc cosine function.
    vec3 vecA_u = normalize(vec_A);
    vec3 vecB_u = normalize(vec_B);
    return acos(clamp(dot(vecA_u, vecB_u), -1.0, 1.0));
}

mat3 get_rot_mat(float my_angle, vec3 dir_vec){
    // The get_rot_mat creates a rotation matrix using an angle and a direction
    // vector. This matrix is used for move points acording to a defined angle
    // in a defined position. We'll use it to obtain the cylinder vertices at
    // the correct orientations.
    mat3 my_mat = mat3(0.0);
    // ndv stands for normalized direction vector
    vec3 ndv = normalize(dir_vec);
    float cosa = cos(my_angle);
    float sina = sin(my_angle);
    my_mat[0][0] = ndv.x*ndv.x*(1-cosa)+cosa;
    my_mat[1][0] = ndv.x*ndv.y*(1-cosa)+ndv.z*sina;
    my_mat[2][0] = ndv.x*ndv.z*(1-cosa)-ndv.y*sina;
    my_mat[0][1] = ndv.x*ndv.y*(1-cosa)-ndv.z*sina;
    my_mat[1][1] = ndv.y*ndv.y*(1-cosa)+cosa;
    my_mat[2][1] = ndv.y*ndv.z*(1-cosa)+ndv.x*sina;
    my_mat[0][2] = ndv.x*ndv.z*(1-cosa)+ndv.y*sina;
    my_mat[1][2] = ndv.y*ndv.z*(1-cosa)-ndv.x*sina;
    my_mat[2][2] = ndv.z*ndv.z*(1-cosa)+cosa;
    return my_mat;
}

void calculate_points(){
    // This void function fills the vertices of the sticks with data.
    p_00.x = (bs_0.x*rot_mat[0][0] + bs_0.y*rot_mat[0][1] + bs_0.z*rot_mat[0][2])*geom_rad[0] + geom_coord[0].x;
    p_00.y = (bs_0.x*rot_mat[1][0] + bs_0.y*rot_mat[1][1] + bs_0.z*rot_mat[1][2])*geom_rad[0] + geom_coord[0].y;
    p_00.z = (bs_0.x*rot_mat[2][0] + bs_0.y*rot_mat[2][1] + bs_0.z*rot_mat[2][2])*geom_rad[0] + geom_coord[0].z;
    p_01.x = (bs_1.x*rot_mat[0][0] + bs_1.y*rot_mat[0][1] + bs_1.z*rot_mat[0][2])*geom_rad[0] + geom_coord[0].x;
    p_01.y = (bs_1.x*rot_mat[1][0] + bs_1.y*rot_mat[1][1] + bs_1.z*rot_mat[1][2])*geom_rad[0] + geom_coord[0].y;
    p_01.z = (bs_1.x*rot_mat[2][0] + bs_1.y*rot_mat[2][1] + bs_1.z*rot_mat[2][2])*geom_rad[0] + geom_coord[0].z;
    p_02.x = (bs_2.x*rot_mat[0][0] + bs_2.y*rot_mat[0][1] + bs_2.z*rot_mat[0][2])*geom_rad[0] + geom_coord[0].x;
    p_02.y = (bs_2.x*rot_mat[1][0] + bs_2.y*rot_mat[1][1] + bs_2.z*rot_mat[1][2])*geom_rad[0] + geom_coord[0].y;
    p_02.z = (bs_2.x*rot_mat[2][0] + bs_2.y*rot_mat[2][1] + bs_2.z*rot_mat[2][2])*geom_rad[0] + geom_coord[0].z;
    p_03.x = (bs_3.x*rot_mat[0][0] + bs_3.y*rot_mat[0][1] + bs_3.z*rot_mat[0][2])*geom_rad[0] + geom_coord[0].x;
    p_03.y = (bs_3.x*rot_mat[1][0] + bs_3.y*rot_mat[1][1] + bs_3.z*rot_mat[1][2])*geom_rad[0] + geom_coord[0].y;
    p_03.z = (bs_3.x*rot_mat[2][0] + bs_3.y*rot_mat[2][1] + bs_3.z*rot_mat[2][2])*geom_rad[0] + geom_coord[0].z;
    p_04.x = (bs_4.x*rot_mat[0][0] + bs_4.y*rot_mat[0][1] + bs_4.z*rot_mat[0][2])*geom_rad[0] + geom_coord[0].x;
    p_04.y = (bs_4.x*rot_mat[1][0] + bs_4.y*rot_mat[1][1] + bs_4.z*rot_mat[1][2])*geom_rad[0] + geom_coord[0].y;
    p_04.z = (bs_4.x*rot_mat[2][0] + bs_4.y*rot_mat[2][1] + bs_4.z*rot_mat[2][2])*geom_rad[0] + geom_coord[0].z;
    p_05.x = (bs_5.x*rot_mat[0][0] + bs_5.y*rot_mat[0][1] + bs_5.z*rot_mat[0][2])*geom_rad[0] + geom_coord[0].x;
    p_05.y = (bs_5.x*rot_mat[1][0] + bs_5.y*rot_mat[1][1] + bs_5.z*rot_mat[1][2])*geom_rad[0] + geom_coord[0].y;
    p_05.z = (bs_5.x*rot_mat[2][0] + bs_5.y*rot_mat[2][1] + bs_5.z*rot_mat[2][2])*geom_rad[0] + geom_coord[0].z;
    p_06.x = (bs_6.x*rot_mat[0][0] + bs_6.y*rot_mat[0][1] + bs_6.z*rot_mat[0][2])*geom_rad[0] + geom_coord[0].x;
    p_06.y = (bs_6.x*rot_mat[1][0] + bs_6.y*rot_mat[1][1] + bs_6.z*rot_mat[1][2])*geom_rad[0] + geom_coord[0].y;
    p_06.z = (bs_6.x*rot_mat[2][0] + bs_6.y*rot_mat[2][1] + bs_6.z*rot_mat[2][2])*geom_rad[0] + geom_coord[0].z;
    p_07.x = (bs_7.x*rot_mat[0][0] + bs_7.y*rot_mat[0][1] + bs_7.z*rot_mat[0][2])*geom_rad[0] + geom_coord[0].x;
    p_07.y = (bs_7.x*rot_mat[1][0] + bs_7.y*rot_mat[1][1] + bs_7.z*rot_mat[1][2])*geom_rad[0] + geom_coord[0].y;
    p_07.z = (bs_7.x*rot_mat[2][0] + bs_7.y*rot_mat[2][1] + bs_7.z*rot_mat[2][2])*geom_rad[0] + geom_coord[0].z;
    p_08.x = (bs_8.x*rot_mat[0][0] + bs_8.y*rot_mat[0][1] + bs_8.z*rot_mat[0][2])*geom_rad[0] + geom_coord[0].x;
    p_08.y = (bs_8.x*rot_mat[1][0] + bs_8.y*rot_mat[1][1] + bs_8.z*rot_mat[1][2])*geom_rad[0] + geom_coord[0].y;
    p_08.z = (bs_8.x*rot_mat[2][0] + bs_8.y*rot_mat[2][1] + bs_8.z*rot_mat[2][2])*geom_rad[0] + geom_coord[0].z;
    
    p_09.x = (up_0.x*rot_mat[0][0] + up_0.y*rot_mat[0][1] + up_0.z*rot_mat[0][2])*geom_rad[0] + mid_point.x;
    p_09.y = (up_0.x*rot_mat[1][0] + up_0.y*rot_mat[1][1] + up_0.z*rot_mat[1][2])*geom_rad[0] + mid_point.y;
    p_09.z = (up_0.x*rot_mat[2][0] + up_0.y*rot_mat[2][1] + up_0.z*rot_mat[2][2])*geom_rad[0] + mid_point.z;
    p_10.x = (up_1.x*rot_mat[0][0] + up_1.y*rot_mat[0][1] + up_1.z*rot_mat[0][2])*geom_rad[0] + mid_point.x;
    p_10.y = (up_1.x*rot_mat[1][0] + up_1.y*rot_mat[1][1] + up_1.z*rot_mat[1][2])*geom_rad[0] + mid_point.y;
    p_10.z = (up_1.x*rot_mat[2][0] + up_1.y*rot_mat[2][1] + up_1.z*rot_mat[2][2])*geom_rad[0] + mid_point.z;
    p_11.x = (up_2.x*rot_mat[0][0] + up_2.y*rot_mat[0][1] + up_2.z*rot_mat[0][2])*geom_rad[0] + mid_point.x;
    p_11.y = (up_2.x*rot_mat[1][0] + up_2.y*rot_mat[1][1] + up_2.z*rot_mat[1][2])*geom_rad[0] + mid_point.y;
    p_11.z = (up_2.x*rot_mat[2][0] + up_2.y*rot_mat[2][1] + up_2.z*rot_mat[2][2])*geom_rad[0] + mid_point.z;
    p_12.x = (up_3.x*rot_mat[0][0] + up_3.y*rot_mat[0][1] + up_3.z*rot_mat[0][2])*geom_rad[0] + mid_point.x;
    p_12.y = (up_3.x*rot_mat[1][0] + up_3.y*rot_mat[1][1] + up_3.z*rot_mat[1][2])*geom_rad[0] + mid_point.y;
    p_12.z = (up_3.x*rot_mat[2][0] + up_3.y*rot_mat[2][1] + up_3.z*rot_mat[2][2])*geom_rad[0] + mid_point.z;
    p_13.x = (up_4.x*rot_mat[0][0] + up_4.y*rot_mat[0][1] + up_4.z*rot_mat[0][2])*geom_rad[0] + mid_point.x;
    p_13.y = (up_4.x*rot_mat[1][0] + up_4.y*rot_mat[1][1] + up_4.z*rot_mat[1][2])*geom_rad[0] + mid_point.y;
    p_13.z = (up_4.x*rot_mat[2][0] + up_4.y*rot_mat[2][1] + up_4.z*rot_mat[2][2])*geom_rad[0] + mid_point.z;
    p_14.x = (up_5.x*rot_mat[0][0] + up_5.y*rot_mat[0][1] + up_5.z*rot_mat[0][2])*geom_rad[0] + mid_point.x;
    p_14.y = (up_5.x*rot_mat[1][0] + up_5.y*rot_mat[1][1] + up_5.z*rot_mat[1][2])*geom_rad[0] + mid_point.y;
    p_14.z = (up_5.x*rot_mat[2][0] + up_5.y*rot_mat[2][1] + up_5.z*rot_mat[2][2])*geom_rad[0] + mid_point.z;
    p_15.x = (up_6.x*rot_mat[0][0] + up_6.y*rot_mat[0][1] + up_6.z*rot_mat[0][2])*geom_rad[0] + mid_point.x;
    p_15.y = (up_6.x*rot_mat[1][0] + up_6.y*rot_mat[1][1] + up_6.z*rot_mat[1][2])*geom_rad[0] + mid_point.y;
    p_15.z = (up_6.x*rot_mat[2][0] + up_6.y*rot_mat[2][1] + up_6.z*rot_mat[2][2])*geom_rad[0] + mid_point.z;
    p_16.x = (up_7.x*rot_mat[0][0] + up_7.y*rot_mat[0][1] + up_7.z*rot_mat[0][2])*geom_rad[0] + mid_point.x;
    p_16.y = (up_7.x*rot_mat[1][0] + up_7.y*rot_mat[1][1] + up_7.z*rot_mat[1][2])*geom_rad[0] + mid_point.y;
    p_16.z = (up_7.x*rot_mat[2][0] + up_7.y*rot_mat[2][1] + up_7.z*rot_mat[2][2])*geom_rad[0] + mid_point.z;
    p_17.x = (up_8.x*rot_mat[0][0] + up_8.y*rot_mat[0][1] + up_8.z*rot_mat[0][2])*geom_rad[0] + mid_point.x;
    p_17.y = (up_8.x*rot_mat[1][0] + up_8.y*rot_mat[1][1] + up_8.z*rot_mat[1][2])*geom_rad[0] + mid_point.y;
    p_17.z = (up_8.x*rot_mat[2][0] + up_8.y*rot_mat[2][1] + up_8.z*rot_mat[2][2])*geom_rad[0] + mid_point.z;
    
    p_18.x = (bs_0.x*rot_mat[0][0] + bs_0.y*rot_mat[0][1] + bs_0.z*rot_mat[0][2])*geom_rad[0] + geom_coord[1].x;
    p_18.y = (bs_0.x*rot_mat[1][0] + bs_0.y*rot_mat[1][1] + bs_0.z*rot_mat[1][2])*geom_rad[0] + geom_coord[1].y;
    p_18.z = (bs_0.x*rot_mat[2][0] + bs_0.y*rot_mat[2][1] + bs_0.z*rot_mat[2][2])*geom_rad[0] + geom_coord[1].z;
    p_19.x = (bs_1.x*rot_mat[0][0] + bs_1.y*rot_mat[0][1] + bs_1.z*rot_mat[0][2])*geom_rad[0] + geom_coord[1].x;
    p_19.y = (bs_1.x*rot_mat[1][0] + bs_1.y*rot_mat[1][1] + bs_1.z*rot_mat[1][2])*geom_rad[0] + geom_coord[1].y;
    p_19.z = (bs_1.x*rot_mat[2][0] + bs_1.y*rot_mat[2][1] + bs_1.z*rot_mat[2][2])*geom_rad[0] + geom_coord[1].z;
    p_20.x = (bs_2.x*rot_mat[0][0] + bs_2.y*rot_mat[0][1] + bs_2.z*rot_mat[0][2])*geom_rad[0] + geom_coord[1].x;
    p_20.y = (bs_2.x*rot_mat[1][0] + bs_2.y*rot_mat[1][1] + bs_2.z*rot_mat[1][2])*geom_rad[0] + geom_coord[1].y;
    p_20.z = (bs_2.x*rot_mat[2][0] + bs_2.y*rot_mat[2][1] + bs_2.z*rot_mat[2][2])*geom_rad[0] + geom_coord[1].z;
    p_21.x = (bs_3.x*rot_mat[0][0] + bs_3.y*rot_mat[0][1] + bs_3.z*rot_mat[0][2])*geom_rad[0] + geom_coord[1].x;
    p_21.y = (bs_3.x*rot_mat[1][0] + bs_3.y*rot_mat[1][1] + bs_3.z*rot_mat[1][2])*geom_rad[0] + geom_coord[1].y;
    p_21.z = (bs_3.x*rot_mat[2][0] + bs_3.y*rot_mat[2][1] + bs_3.z*rot_mat[2][2])*geom_rad[0] + geom_coord[1].z;
    p_22.x = (bs_4.x*rot_mat[0][0] + bs_4.y*rot_mat[0][1] + bs_4.z*rot_mat[0][2])*geom_rad[0] + geom_coord[1].x;
    p_22.y = (bs_4.x*rot_mat[1][0] + bs_4.y*rot_mat[1][1] + bs_4.z*rot_mat[1][2])*geom_rad[0] + geom_coord[1].y;
    p_22.z = (bs_4.x*rot_mat[2][0] + bs_4.y*rot_mat[2][1] + bs_4.z*rot_mat[2][2])*geom_rad[0] + geom_coord[1].z;
    p_23.x = (bs_5.x*rot_mat[0][0] + bs_5.y*rot_mat[0][1] + bs_5.z*rot_mat[0][2])*geom_rad[0] + geom_coord[1].x;
    p_23.y = (bs_5.x*rot_mat[1][0] + bs_5.y*rot_mat[1][1] + bs_5.z*rot_mat[1][2])*geom_rad[0] + geom_coord[1].y;
    p_23.z = (bs_5.x*rot_mat[2][0] + bs_5.y*rot_mat[2][1] + bs_5.z*rot_mat[2][2])*geom_rad[0] + geom_coord[1].z;
    p_24.x = (bs_6.x*rot_mat[0][0] + bs_6.y*rot_mat[0][1] + bs_6.z*rot_mat[0][2])*geom_rad[0] + geom_coord[1].x;
    p_24.y = (bs_6.x*rot_mat[1][0] + bs_6.y*rot_mat[1][1] + bs_6.z*rot_mat[1][2])*geom_rad[0] + geom_coord[1].y;
    p_24.z = (bs_6.x*rot_mat[2][0] + bs_6.y*rot_mat[2][1] + bs_6.z*rot_mat[2][2])*geom_rad[0] + geom_coord[1].z;
    p_25.x = (bs_7.x*rot_mat[0][0] + bs_7.y*rot_mat[0][1] + bs_7.z*rot_mat[0][2])*geom_rad[0] + geom_coord[1].x;
    p_25.y = (bs_7.x*rot_mat[1][0] + bs_7.y*rot_mat[1][1] + bs_7.z*rot_mat[1][2])*geom_rad[0] + geom_coord[1].y;
    p_25.z = (bs_7.x*rot_mat[2][0] + bs_7.y*rot_mat[2][1] + bs_7.z*rot_mat[2][2])*geom_rad[0] + geom_coord[1].z;
    p_26.x = (bs_8.x*rot_mat[0][0] + bs_8.y*rot_mat[0][1] + bs_8.z*rot_mat[0][2])*geom_rad[0] + geom_coord[1].x;
    p_26.y = (bs_8.x*rot_mat[1][0] + bs_8.y*rot_mat[1][1] + bs_8.z*rot_mat[1][2])*geom_rad[0] + geom_coord[1].y;
    p_26.z = (bs_8.x*rot_mat[2][0] + bs_8.y*rot_mat[2][1] + bs_8.z*rot_mat[2][2])*geom_rad[0] + geom_coord[1].z;
}

void main(){
    mid_point = (geom_coord[0].xyz + geom_coord[1].xyz)/2;
    // vec_p0_p1 is the vector defined by the line.
    vec3 vec_p0_p1 = geom_coord[1].xyz - geom_coord[0].xyz;
    // ort_vec is the orthogonal vector between the line vector and the Y axis.
    vec3 ort_vec = normalize(cross(vec3(0,1,0), vec_p0_p1));
    // g_angle is the angle between the line vector and the Y axis.
    float g_angle = get_angle(vec3(0,1,0), vec_p0_p1);
    // g_length is the line vector length or simply the line length.
    float g_length = length(vec_p0_p1);
    rot_mat = get_rot_mat(g_angle, ort_vec);
    calculate_points();
    // Now we send the vertices to the fragment shader in a defined order
    // base-> 0, 9, 1, 10, 2, 11, 3, 12, 4, 13, 5, 14, 6, 15, 7, 16, 8, 17, 0, 9
    gl_Position = proj_mat * vec4(p_00, 1);
    frag_coord = p_00;
    frag_color = geom_color[0];
    frag_norm = p_00 - geom_coord[0].xyz;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_09, 1);
    frag_coord = p_09;
    frag_color = geom_color[0];
    frag_norm = p_09 - mid_point;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_01, 1);
    frag_coord = p_01;
    frag_color = geom_color[0];
    frag_norm = p_01 - geom_coord[0].xyz;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_10, 1);
    frag_coord = p_10;
    frag_color = geom_color[0];
    frag_norm = p_10 - mid_point;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_02, 1);
    frag_coord = p_02;
    frag_color = geom_color[0];
    frag_norm = p_02 - geom_coord[0].xyz;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_11, 1);
    frag_coord = p_11;
    frag_color = geom_color[0];
    frag_norm = p_11 - mid_point;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_03, 1);
    frag_coord = p_03;
    frag_color = geom_color[0];
    frag_norm = p_03 - geom_coord[0].xyz;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_12, 1);
    frag_coord = p_12;
    frag_color = geom_color[0];
    frag_norm = p_12 - mid_point;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_04, 1);
    frag_coord = p_04;
    frag_color = geom_color[0];
    frag_norm = p_04 - geom_coord[0].xyz;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_13, 1);
    frag_coord = p_13;
    frag_color = geom_color[0];
    frag_norm = p_13 - mid_point;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_05, 1);
    frag_coord = p_05;
    frag_color = geom_color[0];
    frag_norm = p_05 - geom_coord[0].xyz;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_14, 1);
    frag_coord = p_14;
    frag_color = geom_color[0];
    frag_norm = p_14 - mid_point;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_06, 1);
    frag_coord = p_06;
    frag_color = geom_color[0];
    frag_norm = p_06 - geom_coord[0].xyz;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_15, 1);
    frag_coord = p_15;
    frag_color = geom_color[0];
    frag_norm = p_15 - mid_point;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_07, 1);
    frag_coord = p_07;
    frag_color = geom_color[0];
    frag_norm = p_07 - geom_coord[0].xyz;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_16, 1);
    frag_coord = p_16;
    frag_color = geom_color[0];
    frag_norm = p_16 - mid_point;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_08, 1);
    frag_coord = p_08;
    frag_color = geom_color[0];
    frag_norm = p_08 - geom_coord[0].xyz;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_17, 1);
    frag_coord = p_17;
    frag_color = geom_color[0];
    frag_norm = p_17 - mid_point;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_00, 1);
    frag_coord = p_00;
    frag_color = geom_color[0];
    frag_norm = p_00 - geom_coord[0].xyz;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_09, 1);
    frag_coord = p_09;
    frag_color = geom_color[0];
    frag_norm = p_09 - mid_point;
    EmitVertex();
    EndPrimitive();
    
    // up-> 9, 18, 10, 19, 11, 20, 12, 21, 13, 22, 14, 23, 15, 24, 16, 25, 17, 26, 9, 18
    gl_Position = proj_mat * vec4(p_09, 1);
    frag_coord = p_09;
    frag_color = geom_color[1];
    frag_norm = p_09 - mid_point;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_18, 1);
    frag_coord = p_18;
    frag_color = geom_color[1];
    frag_norm = p_18 - geom_coord[1].xyz;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_10, 1);
    frag_coord = p_10;
    frag_color = geom_color[1];
    frag_norm = p_10 - mid_point;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_19, 1);
    frag_coord = p_19;
    frag_color = geom_color[1];
    frag_norm = p_19 - geom_coord[1].xyz;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_11, 1);
    frag_coord = p_11;
    frag_color = geom_color[1];
    frag_norm = p_11 - mid_point;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_20, 1);
    frag_coord = p_20;
    frag_color = geom_color[1];
    frag_norm = p_20 - geom_coord[1].xyz;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_12, 1);
    frag_coord = p_12;
    frag_color = geom_color[1];
    frag_norm = p_12 - mid_point;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_21, 1);
    frag_coord = p_21;
    frag_color = geom_color[1];
    frag_norm = p_21 - geom_coord[1].xyz;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_13, 1);
    frag_coord = p_13;
    frag_color = geom_color[1];
    frag_norm = p_13 - mid_point;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_22, 1);
    frag_coord = p_22;
    frag_color = geom_color[1];
    frag_norm = p_22 - geom_coord[1].xyz;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_14, 1);
    frag_coord = p_14;
    frag_color = geom_color[1];
    frag_norm = p_14 - mid_point;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_23, 1);
    frag_coord = p_23;
    frag_color = geom_color[1];
    frag_norm = p_23 - geom_coord[1].xyz;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_15, 1);
    frag_coord = p_15;
    frag_color = geom_color[1];
    frag_norm = p_15 - mid_point;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_24, 1);
    frag_coord = p_24;
    frag_color = geom_color[1];
    frag_norm = p_24 - geom_coord[1].xyz;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_16, 1);
    frag_coord = p_16;
    frag_color = geom_color[1];
    frag_norm = p_16 - mid_point;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_25, 1);
    frag_coord = p_25;
    frag_color = geom_color[1];
    frag_norm = p_25 - geom_coord[1].xyz;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_17, 1);
    frag_coord = p_17;
    frag_color = geom_color[1];
    frag_norm = p_17 - mid_point;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_26, 1);
    frag_coord = p_26;
    frag_color = geom_color[1];
    frag_norm = p_26 - geom_coord[1].xyz;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_09, 1);
    frag_coord = p_09;
    frag_color = geom_color[1];
    frag_norm = p_09 - mid_point;
    EmitVertex();
    gl_Position = proj_mat * vec4(p_18, 1);
    frag_coord = p_18;
    frag_color = geom_color[1];
    frag_norm = p_18 - geom_coord[1].xyz;
    EmitVertex();
    EndPrimitive();
}
"""
fragment_shader_sticks = """
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

vertex_shader_dots_surface = """
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
geometry_shader_dots_surface = """
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
fragment_shader_dots_surface = """
#version 330

uniform vec4 fog_color;
uniform float fog_start;
uniform float fog_end;

in vec3 frag_coord;
in vec3 frag_color;

out vec4 final_color;

void main(){
    float rdist = length(gl_PointCoord - vec2(0.5, 0.5));
    float dist = abs(frag_coord.z);
    if (rdist > 0.5)
        discard;
    float ligth_dist = length(gl_PointCoord - vec2(0.3, 0.3));
    vec4 my_color = mix(vec4(frag_color, 1), vec4(0, 0, 0, 1), sqrt(ligth_dist)*.78);
    if(dist>=fog_start){
        float fog_factor = (fog_end-dist)/(fog_end-fog_start);
        final_color = mix(fog_color, my_color, fog_factor);
    }
    else{
        final_color = my_color;
    }
}
"""

vertex_shader_lines = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;

in vec3 vert_coord;
in vec3 vert_color;

out vec3 geom_color;
out vec4 geom_coord;

void main(){
    geom_color = vert_color;
    geom_coord = view_mat * model_mat * vec4(vert_coord, 1.0);
}
"""
geometry_shader_lines = """
#version 330

layout (lines) in;
layout (line_strip, max_vertices = 4) out;

uniform mat4 proj_mat;

in vec3 geom_color[];
in vec4 geom_coord[];

out vec3 frag_color;
out vec4 frag_coord;

void main(){
    vec4 mid_coord = vec4((geom_coord[0].xyz + geom_coord[1].xyz)/2, 1.0);
    gl_Position = proj_mat * geom_coord[0];
    frag_color = geom_color[0];
    frag_coord = geom_coord[0];
    EmitVertex();
    gl_Position = proj_mat * mid_coord;
    frag_color = geom_color[0];
    frag_coord = mid_coord;
    EmitVertex();
    EndPrimitive();
    gl_Position = proj_mat * mid_coord;
    frag_color = geom_color[1];
    frag_coord = mid_coord;
    EmitVertex();
    gl_Position = proj_mat * geom_coord[1];
    frag_coord = geom_coord[1];
    frag_color = geom_color[1];
    EmitVertex();
    EndPrimitive();
}
"""
fragment_shader_lines = """
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
out vec4 frag_coord;
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
    frag_coord = view_mat * model_mat * vec4(vert_coord, 1);
    gl_Position = proj_mat * view_mat * model_mat * vec4(vert_coord, 1);
    gl_PointSize = vert_dot_size + 2*(vert_ext_linewidth + 1.5*vert_int_antialias);
}
"""
fragment_shader_dots = """
#version 330

uniform vec4 fog_color;
uniform float fog_start;
uniform float fog_end;

in vec4 frag_coord;
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
    float dist =  abs(frag_coord.z);
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
            float alpha = d/frag_int_antialias;
            alpha = exp(-alpha*alpha);
            if (r > 0){
                final_color = frag_bckgrnd_color;
            }
            else{
                if (dist > fog_start){
                    float fog_factor = (fog_end-dist)/(fog_end-fog_start);
                    vec4 my_color = mix(frag_dot_color, frag_bckgrnd_color, alpha);
                    final_color = mix(fog_color, my_color, fog_factor);
                }
                else{
                    final_color = mix(frag_dot_color, frag_bckgrnd_color, alpha);
                }
            }
        }
    }
}
"""

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

vertex_shader_spheres = """
#version 330

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

vertex_shader_picked = """
#version 330

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
fragment_shader_picked = """
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

uniform vec4 fog_color;
uniform float fog_start;
uniform float fog_end;

const float alpha = 0.5;

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
    
    vec4 my_color = vec4(ambient + diffuse + specular, alpha);
    
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

vertex_shader_picking_dots = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 proj_mat;
uniform float vert_ext_linewidth;

in vec3  vert_coord;
in vec3  vert_color;
varying float frag_ext_linewidth;
out vec3 index_color;

void main(){
    gl_Position  = proj_mat * view_mat * model_mat * vec4(vert_coord, 1.0);
    gl_PointSize = 15;
    index_color = vert_color;
}
"""
fragment_shader_picking_dots = """
#version 330

in vec3 index_color;

void main(){
    gl_FragColor = vec4(index_color,1);
}

"""

################################## SELECTION ###################################

sel_vertex_shader_lines = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;

in vec3 vert_coord;
in vec3 vert_color;

out vec3 geom_color;
out vec4 geom_coord;

void main(){
    geom_color = vert_color;
    geom_coord = view_mat * model_mat * vec4(vert_coord, 1.0);
}
"""
sel_geometry_shader_lines = """
#version 330

layout (lines) in;
layout (line_strip, max_vertices = 4) out;

uniform mat4 proj_mat;

in vec3 geom_color[];
in vec4 geom_coord[];

out vec3 frag_color;

void main(){
    vec4 mid_coord = vec4((geom_coord[0].xyz + geom_coord[1].xyz)/2, 1.0);
    gl_Position = proj_mat * geom_coord[0];
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * mid_coord;
    frag_color = geom_color[0];
    EmitVertex();
    EndPrimitive();
    gl_Position = proj_mat * mid_coord;
    frag_color = geom_color[1];
    EmitVertex();
    gl_Position = proj_mat * geom_coord[1];
    frag_color = geom_color[1];
    EmitVertex();
    EndPrimitive();
}
"""
sel_fragment_shader_lines = """
#version 330

in vec3 frag_color;

out vec4 final_color;

void main(){
    final_color = vec4(frag_color, 1.0);
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

sel_vertex_shader_sticks = """
#version 330

uniform mat4 model_mat;
uniform mat4 view_mat;

in vec3 vert_coord;
in vec3 vert_color;
const float vert_rad = 0.1;

out vec3 geom_color;
out vec4 geom_coord;
out float geom_rad;

void main(){
    geom_color = vert_color;
    geom_rad = vert_rad;
    geom_coord = view_mat * model_mat * vec4(vert_coord, 1.0);
}
"""
sel_geometry_shader_sticks = """
#version 330

layout (lines) in;
layout (triangle_strip, max_vertices = 40) out;

uniform mat4 proj_mat;

in vec3 geom_color[];
in vec4 geom_coord[];
in float geom_rad[];

out vec3 frag_color;

// This data is used for the cylinder vertices, i.e. the points that form the
// circle in a horizontal cut of the cylinder. The first half are the points
// at the begining of the cylinder, and the last half are the points at the end.
// The quantity of points should be changed to get a smoother cylinder, but that
// will result in more resources used.
vec3 bs_0 = vec3( 1.000000000000, 0.000000000000, 0.000000000000); // base
vec3 bs_1 = vec3( 0.766044443119, 0.000000000000, 0.642787609687); // base
vec3 bs_2 = vec3( 0.173648177667, 0.000000000000, 0.984807753012); // base
vec3 bs_3 = vec3(-0.500000000000, 0.000000000000, 0.866025403784); // base
vec3 bs_4 = vec3(-0.939692620786, 0.000000000000, 0.342020143326); // base
vec3 bs_5 = vec3(-0.939692620786, 0.000000000000,-0.342020143326); // base
vec3 bs_6 = vec3(-0.500000000000, 0.000000000000,-0.866025403784); // base
vec3 bs_7 = vec3( 0.173648177667, 0.000000000000,-0.984807753012); // base
vec3 bs_8 = vec3( 0.766044443119, 0.000000000000,-0.642787609687); // base
vec3 up_0 = vec3( 0.939692620786, 0.000000000000, 0.342020143326); // up
vec3 up_1 = vec3( 0.500000000000, 0.000000000000, 0.866025403784); // up
vec3 up_2 = vec3(-0.173648177667, 0.000000000000, 0.984807753012); // up
vec3 up_3 = vec3(-0.766044443119, 0.000000000000, 0.642787609687); // up
vec3 up_4 = vec3(-1.000000000000, 0.000000000000, 0.000000000000); // up
vec3 up_5 = vec3(-0.766044443119, 0.000000000000,-0.642787609687); // up
vec3 up_6 = vec3(-0.173648177667, 0.000000000000,-0.984807753012); // up
vec3 up_7 = vec3( 0.500000000000, 0.000000000000,-0.866025403784); // up
vec3 up_8 = vec3( 0.939692620786, 0.000000000000,-0.342020143326); // up

// The rotation matrix used for translating the cylinder points to their correct
// places is rot_mat. This matrix is created using the my_glRotatef function,
// see the function documentation to get more information.
varying mat3 rot_mat;

// mid_point is the middle point in the line.
varying vec3 mid_point;

// These points are the vertices calculated for the cylinder.
varying vec3 p_00, p_01, p_02, p_03, p_04, p_05, p_06, p_07, p_08;
varying vec3 p_09, p_10, p_11, p_12, p_13, p_14, p_15, p_16, p_17;
varying vec3 p_18, p_19, p_20, p_21, p_22, p_23, p_24, p_25, p_26;

float get_angle(vec3 vec_A, vec3 vec_B){
    // Returns the angle in radians formed between the vectors A and B. The
    // vectors are initially normalized to avoid errors.
    // The initial result is clamped to the [-1,+1] range to avoid errors in
    // the arc cosine function.
    vec3 vecA_u = normalize(vec_A);
    vec3 vecB_u = normalize(vec_B);
    return acos(clamp(dot(vecA_u, vecB_u), -1.0, 1.0));
}

mat3 get_rot_mat(float my_angle, vec3 dir_vec){
    // The get_rot_mat creates a rotation matrix using an angle and a direction
    // vector. This matrix is used for move points acording to a defined angle
    // in a defined position. We'll use it to obtain the cylinder vertices at
    // the correct orientations.
    mat3 my_mat = mat3(0.0);
    // ndv stands for normalized direction vector
    vec3 ndv = normalize(dir_vec);
    float cosa = cos(my_angle);
    float sina = sin(my_angle);
    my_mat[0][0] = ndv.x*ndv.x*(1-cosa)+cosa;
    my_mat[1][0] = ndv.x*ndv.y*(1-cosa)+ndv.z*sina;
    my_mat[2][0] = ndv.x*ndv.z*(1-cosa)-ndv.y*sina;
    my_mat[0][1] = ndv.x*ndv.y*(1-cosa)-ndv.z*sina;
    my_mat[1][1] = ndv.y*ndv.y*(1-cosa)+cosa;
    my_mat[2][1] = ndv.y*ndv.z*(1-cosa)+ndv.x*sina;
    my_mat[0][2] = ndv.x*ndv.z*(1-cosa)+ndv.y*sina;
    my_mat[1][2] = ndv.y*ndv.z*(1-cosa)-ndv.x*sina;
    my_mat[2][2] = ndv.z*ndv.z*(1-cosa)+cosa;
    return my_mat;
}

void calculate_points(){
    // This void function fills the vertices of the sticks with data.
    p_00.x = (bs_0.x*rot_mat[0][0] + bs_0.y*rot_mat[0][1] + bs_0.z*rot_mat[0][2])*geom_rad[0] + geom_coord[0].x;
    p_00.y = (bs_0.x*rot_mat[1][0] + bs_0.y*rot_mat[1][1] + bs_0.z*rot_mat[1][2])*geom_rad[0] + geom_coord[0].y;
    p_00.z = (bs_0.x*rot_mat[2][0] + bs_0.y*rot_mat[2][1] + bs_0.z*rot_mat[2][2])*geom_rad[0] + geom_coord[0].z;
    p_01.x = (bs_1.x*rot_mat[0][0] + bs_1.y*rot_mat[0][1] + bs_1.z*rot_mat[0][2])*geom_rad[0] + geom_coord[0].x;
    p_01.y = (bs_1.x*rot_mat[1][0] + bs_1.y*rot_mat[1][1] + bs_1.z*rot_mat[1][2])*geom_rad[0] + geom_coord[0].y;
    p_01.z = (bs_1.x*rot_mat[2][0] + bs_1.y*rot_mat[2][1] + bs_1.z*rot_mat[2][2])*geom_rad[0] + geom_coord[0].z;
    p_02.x = (bs_2.x*rot_mat[0][0] + bs_2.y*rot_mat[0][1] + bs_2.z*rot_mat[0][2])*geom_rad[0] + geom_coord[0].x;
    p_02.y = (bs_2.x*rot_mat[1][0] + bs_2.y*rot_mat[1][1] + bs_2.z*rot_mat[1][2])*geom_rad[0] + geom_coord[0].y;
    p_02.z = (bs_2.x*rot_mat[2][0] + bs_2.y*rot_mat[2][1] + bs_2.z*rot_mat[2][2])*geom_rad[0] + geom_coord[0].z;
    p_03.x = (bs_3.x*rot_mat[0][0] + bs_3.y*rot_mat[0][1] + bs_3.z*rot_mat[0][2])*geom_rad[0] + geom_coord[0].x;
    p_03.y = (bs_3.x*rot_mat[1][0] + bs_3.y*rot_mat[1][1] + bs_3.z*rot_mat[1][2])*geom_rad[0] + geom_coord[0].y;
    p_03.z = (bs_3.x*rot_mat[2][0] + bs_3.y*rot_mat[2][1] + bs_3.z*rot_mat[2][2])*geom_rad[0] + geom_coord[0].z;
    p_04.x = (bs_4.x*rot_mat[0][0] + bs_4.y*rot_mat[0][1] + bs_4.z*rot_mat[0][2])*geom_rad[0] + geom_coord[0].x;
    p_04.y = (bs_4.x*rot_mat[1][0] + bs_4.y*rot_mat[1][1] + bs_4.z*rot_mat[1][2])*geom_rad[0] + geom_coord[0].y;
    p_04.z = (bs_4.x*rot_mat[2][0] + bs_4.y*rot_mat[2][1] + bs_4.z*rot_mat[2][2])*geom_rad[0] + geom_coord[0].z;
    p_05.x = (bs_5.x*rot_mat[0][0] + bs_5.y*rot_mat[0][1] + bs_5.z*rot_mat[0][2])*geom_rad[0] + geom_coord[0].x;
    p_05.y = (bs_5.x*rot_mat[1][0] + bs_5.y*rot_mat[1][1] + bs_5.z*rot_mat[1][2])*geom_rad[0] + geom_coord[0].y;
    p_05.z = (bs_5.x*rot_mat[2][0] + bs_5.y*rot_mat[2][1] + bs_5.z*rot_mat[2][2])*geom_rad[0] + geom_coord[0].z;
    p_06.x = (bs_6.x*rot_mat[0][0] + bs_6.y*rot_mat[0][1] + bs_6.z*rot_mat[0][2])*geom_rad[0] + geom_coord[0].x;
    p_06.y = (bs_6.x*rot_mat[1][0] + bs_6.y*rot_mat[1][1] + bs_6.z*rot_mat[1][2])*geom_rad[0] + geom_coord[0].y;
    p_06.z = (bs_6.x*rot_mat[2][0] + bs_6.y*rot_mat[2][1] + bs_6.z*rot_mat[2][2])*geom_rad[0] + geom_coord[0].z;
    p_07.x = (bs_7.x*rot_mat[0][0] + bs_7.y*rot_mat[0][1] + bs_7.z*rot_mat[0][2])*geom_rad[0] + geom_coord[0].x;
    p_07.y = (bs_7.x*rot_mat[1][0] + bs_7.y*rot_mat[1][1] + bs_7.z*rot_mat[1][2])*geom_rad[0] + geom_coord[0].y;
    p_07.z = (bs_7.x*rot_mat[2][0] + bs_7.y*rot_mat[2][1] + bs_7.z*rot_mat[2][2])*geom_rad[0] + geom_coord[0].z;
    p_08.x = (bs_8.x*rot_mat[0][0] + bs_8.y*rot_mat[0][1] + bs_8.z*rot_mat[0][2])*geom_rad[0] + geom_coord[0].x;
    p_08.y = (bs_8.x*rot_mat[1][0] + bs_8.y*rot_mat[1][1] + bs_8.z*rot_mat[1][2])*geom_rad[0] + geom_coord[0].y;
    p_08.z = (bs_8.x*rot_mat[2][0] + bs_8.y*rot_mat[2][1] + bs_8.z*rot_mat[2][2])*geom_rad[0] + geom_coord[0].z;
    
    p_09.x = (up_0.x*rot_mat[0][0] + up_0.y*rot_mat[0][1] + up_0.z*rot_mat[0][2])*geom_rad[0] + mid_point.x;
    p_09.y = (up_0.x*rot_mat[1][0] + up_0.y*rot_mat[1][1] + up_0.z*rot_mat[1][2])*geom_rad[0] + mid_point.y;
    p_09.z = (up_0.x*rot_mat[2][0] + up_0.y*rot_mat[2][1] + up_0.z*rot_mat[2][2])*geom_rad[0] + mid_point.z;
    p_10.x = (up_1.x*rot_mat[0][0] + up_1.y*rot_mat[0][1] + up_1.z*rot_mat[0][2])*geom_rad[0] + mid_point.x;
    p_10.y = (up_1.x*rot_mat[1][0] + up_1.y*rot_mat[1][1] + up_1.z*rot_mat[1][2])*geom_rad[0] + mid_point.y;
    p_10.z = (up_1.x*rot_mat[2][0] + up_1.y*rot_mat[2][1] + up_1.z*rot_mat[2][2])*geom_rad[0] + mid_point.z;
    p_11.x = (up_2.x*rot_mat[0][0] + up_2.y*rot_mat[0][1] + up_2.z*rot_mat[0][2])*geom_rad[0] + mid_point.x;
    p_11.y = (up_2.x*rot_mat[1][0] + up_2.y*rot_mat[1][1] + up_2.z*rot_mat[1][2])*geom_rad[0] + mid_point.y;
    p_11.z = (up_2.x*rot_mat[2][0] + up_2.y*rot_mat[2][1] + up_2.z*rot_mat[2][2])*geom_rad[0] + mid_point.z;
    p_12.x = (up_3.x*rot_mat[0][0] + up_3.y*rot_mat[0][1] + up_3.z*rot_mat[0][2])*geom_rad[0] + mid_point.x;
    p_12.y = (up_3.x*rot_mat[1][0] + up_3.y*rot_mat[1][1] + up_3.z*rot_mat[1][2])*geom_rad[0] + mid_point.y;
    p_12.z = (up_3.x*rot_mat[2][0] + up_3.y*rot_mat[2][1] + up_3.z*rot_mat[2][2])*geom_rad[0] + mid_point.z;
    p_13.x = (up_4.x*rot_mat[0][0] + up_4.y*rot_mat[0][1] + up_4.z*rot_mat[0][2])*geom_rad[0] + mid_point.x;
    p_13.y = (up_4.x*rot_mat[1][0] + up_4.y*rot_mat[1][1] + up_4.z*rot_mat[1][2])*geom_rad[0] + mid_point.y;
    p_13.z = (up_4.x*rot_mat[2][0] + up_4.y*rot_mat[2][1] + up_4.z*rot_mat[2][2])*geom_rad[0] + mid_point.z;
    p_14.x = (up_5.x*rot_mat[0][0] + up_5.y*rot_mat[0][1] + up_5.z*rot_mat[0][2])*geom_rad[0] + mid_point.x;
    p_14.y = (up_5.x*rot_mat[1][0] + up_5.y*rot_mat[1][1] + up_5.z*rot_mat[1][2])*geom_rad[0] + mid_point.y;
    p_14.z = (up_5.x*rot_mat[2][0] + up_5.y*rot_mat[2][1] + up_5.z*rot_mat[2][2])*geom_rad[0] + mid_point.z;
    p_15.x = (up_6.x*rot_mat[0][0] + up_6.y*rot_mat[0][1] + up_6.z*rot_mat[0][2])*geom_rad[0] + mid_point.x;
    p_15.y = (up_6.x*rot_mat[1][0] + up_6.y*rot_mat[1][1] + up_6.z*rot_mat[1][2])*geom_rad[0] + mid_point.y;
    p_15.z = (up_6.x*rot_mat[2][0] + up_6.y*rot_mat[2][1] + up_6.z*rot_mat[2][2])*geom_rad[0] + mid_point.z;
    p_16.x = (up_7.x*rot_mat[0][0] + up_7.y*rot_mat[0][1] + up_7.z*rot_mat[0][2])*geom_rad[0] + mid_point.x;
    p_16.y = (up_7.x*rot_mat[1][0] + up_7.y*rot_mat[1][1] + up_7.z*rot_mat[1][2])*geom_rad[0] + mid_point.y;
    p_16.z = (up_7.x*rot_mat[2][0] + up_7.y*rot_mat[2][1] + up_7.z*rot_mat[2][2])*geom_rad[0] + mid_point.z;
    p_17.x = (up_8.x*rot_mat[0][0] + up_8.y*rot_mat[0][1] + up_8.z*rot_mat[0][2])*geom_rad[0] + mid_point.x;
    p_17.y = (up_8.x*rot_mat[1][0] + up_8.y*rot_mat[1][1] + up_8.z*rot_mat[1][2])*geom_rad[0] + mid_point.y;
    p_17.z = (up_8.x*rot_mat[2][0] + up_8.y*rot_mat[2][1] + up_8.z*rot_mat[2][2])*geom_rad[0] + mid_point.z;
    
    p_18.x = (bs_0.x*rot_mat[0][0] + bs_0.y*rot_mat[0][1] + bs_0.z*rot_mat[0][2])*geom_rad[0] + geom_coord[1].x;
    p_18.y = (bs_0.x*rot_mat[1][0] + bs_0.y*rot_mat[1][1] + bs_0.z*rot_mat[1][2])*geom_rad[0] + geom_coord[1].y;
    p_18.z = (bs_0.x*rot_mat[2][0] + bs_0.y*rot_mat[2][1] + bs_0.z*rot_mat[2][2])*geom_rad[0] + geom_coord[1].z;
    p_19.x = (bs_1.x*rot_mat[0][0] + bs_1.y*rot_mat[0][1] + bs_1.z*rot_mat[0][2])*geom_rad[0] + geom_coord[1].x;
    p_19.y = (bs_1.x*rot_mat[1][0] + bs_1.y*rot_mat[1][1] + bs_1.z*rot_mat[1][2])*geom_rad[0] + geom_coord[1].y;
    p_19.z = (bs_1.x*rot_mat[2][0] + bs_1.y*rot_mat[2][1] + bs_1.z*rot_mat[2][2])*geom_rad[0] + geom_coord[1].z;
    p_20.x = (bs_2.x*rot_mat[0][0] + bs_2.y*rot_mat[0][1] + bs_2.z*rot_mat[0][2])*geom_rad[0] + geom_coord[1].x;
    p_20.y = (bs_2.x*rot_mat[1][0] + bs_2.y*rot_mat[1][1] + bs_2.z*rot_mat[1][2])*geom_rad[0] + geom_coord[1].y;
    p_20.z = (bs_2.x*rot_mat[2][0] + bs_2.y*rot_mat[2][1] + bs_2.z*rot_mat[2][2])*geom_rad[0] + geom_coord[1].z;
    p_21.x = (bs_3.x*rot_mat[0][0] + bs_3.y*rot_mat[0][1] + bs_3.z*rot_mat[0][2])*geom_rad[0] + geom_coord[1].x;
    p_21.y = (bs_3.x*rot_mat[1][0] + bs_3.y*rot_mat[1][1] + bs_3.z*rot_mat[1][2])*geom_rad[0] + geom_coord[1].y;
    p_21.z = (bs_3.x*rot_mat[2][0] + bs_3.y*rot_mat[2][1] + bs_3.z*rot_mat[2][2])*geom_rad[0] + geom_coord[1].z;
    p_22.x = (bs_4.x*rot_mat[0][0] + bs_4.y*rot_mat[0][1] + bs_4.z*rot_mat[0][2])*geom_rad[0] + geom_coord[1].x;
    p_22.y = (bs_4.x*rot_mat[1][0] + bs_4.y*rot_mat[1][1] + bs_4.z*rot_mat[1][2])*geom_rad[0] + geom_coord[1].y;
    p_22.z = (bs_4.x*rot_mat[2][0] + bs_4.y*rot_mat[2][1] + bs_4.z*rot_mat[2][2])*geom_rad[0] + geom_coord[1].z;
    p_23.x = (bs_5.x*rot_mat[0][0] + bs_5.y*rot_mat[0][1] + bs_5.z*rot_mat[0][2])*geom_rad[0] + geom_coord[1].x;
    p_23.y = (bs_5.x*rot_mat[1][0] + bs_5.y*rot_mat[1][1] + bs_5.z*rot_mat[1][2])*geom_rad[0] + geom_coord[1].y;
    p_23.z = (bs_5.x*rot_mat[2][0] + bs_5.y*rot_mat[2][1] + bs_5.z*rot_mat[2][2])*geom_rad[0] + geom_coord[1].z;
    p_24.x = (bs_6.x*rot_mat[0][0] + bs_6.y*rot_mat[0][1] + bs_6.z*rot_mat[0][2])*geom_rad[0] + geom_coord[1].x;
    p_24.y = (bs_6.x*rot_mat[1][0] + bs_6.y*rot_mat[1][1] + bs_6.z*rot_mat[1][2])*geom_rad[0] + geom_coord[1].y;
    p_24.z = (bs_6.x*rot_mat[2][0] + bs_6.y*rot_mat[2][1] + bs_6.z*rot_mat[2][2])*geom_rad[0] + geom_coord[1].z;
    p_25.x = (bs_7.x*rot_mat[0][0] + bs_7.y*rot_mat[0][1] + bs_7.z*rot_mat[0][2])*geom_rad[0] + geom_coord[1].x;
    p_25.y = (bs_7.x*rot_mat[1][0] + bs_7.y*rot_mat[1][1] + bs_7.z*rot_mat[1][2])*geom_rad[0] + geom_coord[1].y;
    p_25.z = (bs_7.x*rot_mat[2][0] + bs_7.y*rot_mat[2][1] + bs_7.z*rot_mat[2][2])*geom_rad[0] + geom_coord[1].z;
    p_26.x = (bs_8.x*rot_mat[0][0] + bs_8.y*rot_mat[0][1] + bs_8.z*rot_mat[0][2])*geom_rad[0] + geom_coord[1].x;
    p_26.y = (bs_8.x*rot_mat[1][0] + bs_8.y*rot_mat[1][1] + bs_8.z*rot_mat[1][2])*geom_rad[0] + geom_coord[1].y;
    p_26.z = (bs_8.x*rot_mat[2][0] + bs_8.y*rot_mat[2][1] + bs_8.z*rot_mat[2][2])*geom_rad[0] + geom_coord[1].z;
}

void main(){
    mid_point = (geom_coord[0].xyz + geom_coord[1].xyz)/2;
    // vec_p0_p1 is the vector defined by the line.
    vec3 vec_p0_p1 = geom_coord[1].xyz - geom_coord[0].xyz;
    // ort_vec is the orthogonal vector between the line vector and the Y axis.
    vec3 ort_vec = normalize(cross(vec3(0,1,0), vec_p0_p1));
    // g_angle is the angle between the line vector and the Y axis.
    float g_angle = get_angle(vec3(0,1,0), vec_p0_p1);
    // g_length is the line vector length or simply the line length.
    float g_length = length(vec_p0_p1);
    rot_mat = get_rot_mat(g_angle, ort_vec);
    calculate_points();
    // Now we send the vertices to the fragment shader in a defined order
    // base-> 0, 9, 1, 10, 2, 11, 3, 12, 4, 13, 5, 14, 6, 15, 7, 16, 8, 17, 0, 9
    gl_Position = proj_mat * vec4(p_00, 1);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_09, 1);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_01, 1);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_10, 1);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_02, 1);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_11, 1);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_03, 1);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_12, 1);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_04, 1);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_13, 1);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_05, 1);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_14, 1);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_06, 1);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_15, 1);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_07, 1);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_16, 1);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_08, 1);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_17, 1);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_00, 1);
    frag_color = geom_color[0];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_09, 1);
    frag_color = geom_color[0];
    EmitVertex();
    EndPrimitive();
    
    // up-> 9, 18, 10, 19, 11, 20, 12, 21, 13, 22, 14, 23, 15, 24, 16, 25, 17, 26, 9, 18
    gl_Position = proj_mat * vec4(p_09, 1);
    frag_color = geom_color[1];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_18, 1);
    frag_color = geom_color[1];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_10, 1);
    frag_color = geom_color[1];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_19, 1);
    frag_color = geom_color[1];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_11, 1);
    frag_color = geom_color[1];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_20, 1);
    frag_color = geom_color[1];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_12, 1);
    frag_color = geom_color[1];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_21, 1);
    frag_color = geom_color[1];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_13, 1);
    frag_color = geom_color[1];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_22, 1);
    frag_color = geom_color[1];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_14, 1);
    frag_color = geom_color[1];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_23, 1);
    frag_color = geom_color[1];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_15, 1);
    frag_color = geom_color[1];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_24, 1);
    frag_color = geom_color[1];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_16, 1);
    frag_color = geom_color[1];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_25, 1);
    frag_color = geom_color[1];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_17, 1);
    frag_color = geom_color[1];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_26, 1);
    frag_color = geom_color[1];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_09, 1);
    frag_color = geom_color[1];
    EmitVertex();
    gl_Position = proj_mat * vec4(p_18, 1);
    frag_color = geom_color[1];
    EmitVertex();
    EndPrimitive();
}
"""
sel_fragment_shader_sticks = """
#version 330

in vec3 frag_color;

out vec4 final_color;

void main(){
    final_color = vec4(frag_color, 1.0);
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

sel_vertex_shader_spheres = """
#version 330

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

in vec3 frag_color;

out vec4 final_color;

void main(){
    final_color = vec4(frag_color, 1.0);
}
"""

############################### VisMolDrawWidget ###############################

v_shader_spheres = """
#version 330

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
f_shader_spheres = """
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
