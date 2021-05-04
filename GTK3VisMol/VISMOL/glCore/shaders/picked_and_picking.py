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


#
#vertex_shader_picked = """
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
#fragment_shader_picked = """
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
#const float alpha = 0.5;
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
#    vec4 my_color = vec4(ambient + diffuse + specular, alpha);
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
#
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
    //gl_PointSize = 15;
    index_color = vert_color;
}
"""
fragment_shader_picking_dots = """
#version 330

in vec3 index_color;

void main(){
    float dist = length(gl_PointCoord.xy - vec2(0.5,0.5));
    if (dist > 0.6)
        discard;
    gl_FragColor = vec4(index_color,1.0);
}

"""

############################### VisMolDrawWidget ###############################













