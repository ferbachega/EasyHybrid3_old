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


vertex_shader_glumpy = """
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


fragment_shader_glumpy = """
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
