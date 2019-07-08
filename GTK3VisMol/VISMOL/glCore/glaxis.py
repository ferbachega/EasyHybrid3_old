#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  glaxis.py
#  
#  Copyright 2017 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
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

import ctypes
import numpy as np
import VISMOL.glCore.matrix_operations as mop

from OpenGL import GL

class GLAxis:
    """ This class contains all necessary components for the creation of a
        gizmo axis, including shaders, matrices, coordinates and functions to
        represent it in OpenGL. This class was created with the purpose of
        being completely independent from the VisMol widget, i.e. you could
        take this class and implement it in your own window.
        As this class is intended to be independent, almost all the methods
        receive no arguments.
    """
    
    def __init__ (self, cam_pos=np.array([0,0,0],dtype=np.float32)):
        """ For creating a GLAxis object you only need to supply the position
            of your camera or eye as an numpy array of XYZ components.
            The default position for the camera is 0x, 0y, 0z.
            The default position of the gismo is at the bottom left of the
            window, you can change this location by multiplying the coordinates
            by a translation matrix, or using another set of coordinates.
        """
        self.axis_vertices = {'x_axis' : np.array(
        [-0.85000000, -0.87500000,  0.00000000,
         -0.85000000, -0.88232233, -0.01767767,
         -0.85000000, -0.90000000, -0.02500000,
         -0.85000000, -0.91767767, -0.01767767,
         -0.85000000, -0.92500000,  0.00000000,
         -0.85000000, -0.91767767,  0.01767767,
         -0.85000000, -0.90000000,  0.02500000,
         -0.85000000, -0.88232233,  0.01767767,
         -0.81250000, -0.90000000,  0.00000000,
         -0.85000000, -0.90000000,  0.00000000], dtype=np.float32),
        'y_axis' : np.array(
        [-0.90000000, -0.85000000, -0.02500000,
         -0.88232233, -0.85000000, -0.01767767,
         -0.87500000, -0.85000000,  0.00000000,
         -0.88232233, -0.85000000,  0.01767767,
         -0.90000000, -0.85000000,  0.02500000,
         -0.91767767, -0.85000000,  0.01767767,
         -0.92500000, -0.85000000,  0.00000000,
         -0.91767767, -0.85000000, -0.01767767,
         -0.90000000, -0.81250000,  0.00000000,
         -0.90000000, -0.85000000,  0.00000000], dtype=np.float32),
        'z_axis' : np.array(
        [-0.90000000, -0.87500000, -0.05000000,
         -0.88232233, -0.88232233, -0.05000000,
         -0.87500000, -0.90000000, -0.05000000,
         -0.88232233, -0.91767767, -0.05000000,
         -0.90000000, -0.92500000, -0.05000000,
         -0.91767767, -0.91767767, -0.05000000,
         -0.92500000, -0.90000000, -0.05000000,
         -0.91767767, -0.88232233, -0.05000000,
         -0.90000000, -0.90000000, -0.08750000,
         -0.90000000, -0.90000000, -0.05000000], dtype=np.float32)}
        self.axis_normals = {'x_axis' : np.array(
        [-0.60000062,  0.79999954,  0.00000000,
         -0.60000032,  0.56568521, -0.56568539,
         -0.60000026,  0.00000000, -0.79999983,
         -0.60000032, -0.56568521, -0.56568539,
         -0.59999973, -0.80000031,  0.00000000,
         -0.60000032, -0.56568521,  0.56568539,
         -0.60000026,  0.00000000,  0.79999983,
         -0.60000032,  0.56568521,  0.56568539,
          1.00000000,  0.00000000,  0.00000000,
         -1.00000000,  0.00000000,  0.00000000], dtype=np.float32),
        'y_axis' : np.array(
        [ 0.00000000, -0.60000026, -0.79999983,
          0.56568521, -0.60000032, -0.56568539,
          0.79999954, -0.60000062,  0.00000000,
          0.56568521, -0.60000032,  0.56568539,
          0.00000000, -0.60000026,  0.79999983,
         -0.56568521, -0.60000032,  0.56568539,
         -0.80000031, -0.59999973,  0.00000000,
         -0.56568521, -0.60000032, -0.56568539,
          0.00000000,  1.00000000,  0.00000000,
          0.00000000, -1.00000000,  0.00000000], dtype=np.float32),
        'z_axis' : np.array(
        [ 0.00000000,  0.79999977,  0.60000038,
          0.56568539,  0.56568539,  0.60000008,
          0.79999977,  0.00000000,  0.60000038,
          0.56568539, -0.56568539,  0.60000008,
          0.00000000, -0.80000049,  0.59999949,
         -0.56568539, -0.56568539,  0.60000008,
         -0.80000049,  0.00000000,  0.59999949,
         -0.56568539,  0.56568539,  0.60000008,
          0.00000000,  0.00000000, -1.00000000,
          0.00000000,  0.00000000,  1.00000000], dtype=np.float32)}
        self.lines_vertices = np.array(
            [-0.90000000, -0.90000000,  0.00000000,
             -0.82500000, -0.90000000,  0.00000000,
             -0.90000000, -0.90000000,  0.00000000,
             -0.90000000, -0.82500000,  0.00000000,
             -0.90000000, -0.90000000,  0.00000000,
             -0.90000000, -0.90000000, -0.07500000], dtype=np.float32)
        self.lines_colors = np.array(
            [1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
             0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
             0.0, 0.0, 1.0, 0.0, 0.0, 1.0], dtype=np.float32)
        self.axis_indexes = np.array([0, 1, 8, 1, 2, 8, 2, 3, 8, 3, 4, 8,
                                      4, 5, 8, 5, 6, 8, 6, 7, 8, 7, 0, 8,
                                      0, 1, 9, 1, 2, 9, 2, 3, 9, 3, 4, 9,
                                      4, 5, 9, 5, 6, 9, 6, 7, 9, 7, 0, 9], dtype=np.uint32)
        self.axis_colors = {'x_axis' : [1.0, 0.0, 0.0],
                            'y_axis' : [0.0, 1.0, 0.0],
                            'z_axis' : [0.0, 0.0, 1.0]}
        self.model_mat = np.identity(4, dtype=np.float32)
        self.gizmo_axis_program = None
        self.gl_lines_program = None
        self.x_vao = None
        self.y_vao = None
        self.z_vao = None
        self.lines_vao = None
        self.zrp = np.array([-0.9, -0.9, 0.0],dtype=np.float32)
        self.camera_position = np.array(cam_pos, dtype=np.float32)
        self.light_position = np.array([1.5, 1.5, -2.5],dtype=np.float32)
        self.light_color = np.array([1.0, 1.0, 1.0, 1.0],dtype=np.float32)
        self.light_ambient_coef = 0.2
        self.light_specular_coef = 0.7
        self.light_shininess = 32.0
        self.vertex_shader_axis = """
#version 330

uniform mat4 model_mat;

in vec3 vert_coord;
in vec3 vert_color;
in vec3 vert_norm;

out vec3 frag_color;
out vec3 frag_norm;

void main(){
    vec3 frag_coord = vec3(model_mat * vec4(vert_coord, 1.0));
    frag_norm = mat3(transpose(inverse(model_mat))) * vert_norm;
    frag_color = vert_color;
    gl_Position = vec4(frag_coord, 1.0);
}
"""
        self.fragment_shader_axis = """
#version 330

struct Light {
   vec3 position;
   vec3 color;
   float ambient_coef;
   float specular_coef;
   float shininess;
};

uniform Light my_light;
uniform vec3 cam_pos;

in vec3 frag_color;
in vec3 frag_norm;

out vec4 final_color;

void main(){
    vec3 N = normalize(frag_norm);
    vec3 L = normalize(my_light.position);
    vec3 E = vec3(0, 0, 1);
    vec3 H = normalize(L + E);
    
    float df = max(0.0, dot(N, L));
    float sf = max(0.0, dot(N, H));
    sf = pow(sf, my_light.shininess);

    vec3 color = frag_color * 0.2 + df * frag_color + sf * vec3(.5);
    final_color = vec4(color, 1.0);
}
"""
        self.vertex_shader_lines = """
#version 330

uniform mat4 model_mat;

in vec3 vert_coord;
in vec3 vert_color;

out vec3 frag_color;

void main()
{
    gl_Position = model_mat * vec4(vert_coord, 1.0);
    frag_color = vert_color;
}
"""
        self.fragment_shader_lines = """
#version 330

in vec3 frag_color;

out vec4 final_color;

void main()
{
    final_color = vec4(frag_color, 1.0);
}
"""
    
    def initialize_gl(self):
        """ First function, called right after the object creation. Creates the
            OpenGL programs and Vertex Array Objects.
        """
        self._make_axis_program()
        self._make_lines_program()
        self._make_gl_gizmo_axis()
        return True
    
    def _make_gl_gizmo_axis(self):
        """ Creates the Vertex Array Objects for the XYZ axis. Initially creates
            the vaos for the cones of the axis and then for the lines.
        """
        self.x_vao = self._get_vao('x_axis')
        self.y_vao = self._get_vao('y_axis')
        self.z_vao = self._get_vao('z_axis')
        self.lines_vao = self._get_vao_lines()
        return True
    
    def _make_axis_program(self):
        """ Compiles the cone shaders. This function compiles only the cones
            of the gizmo axis.
        """
        v_shader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
        GL.glShaderSource(v_shader, self.vertex_shader_axis)
        GL.glCompileShader(v_shader)
        f_shader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
        GL.glShaderSource(f_shader, self.fragment_shader_axis)
        GL.glCompileShader(f_shader)
        self.gizmo_axis_program = GL.glCreateProgram()
        GL.glAttachShader(self.gizmo_axis_program, v_shader)
        GL.glAttachShader(self.gizmo_axis_program, f_shader)
        GL.glLinkProgram(self.gizmo_axis_program)
        if GL.glGetShaderiv(v_shader, GL.GL_COMPILE_STATUS) != GL.GL_TRUE:
            print("Error compiling the shader: ", "GL_VERTEX_SHADER")
            raise RuntimeError(GL.glGetShaderInfoLog(v_shader))
        if GL.glGetShaderiv(f_shader, GL.GL_COMPILE_STATUS) != GL.GL_TRUE:
            print("Error compiling the shader: ", "GL_FRAGMENT_SHADER")
            raise RuntimeError(GL.glGetShaderInfoLog(f_shader))
        return True
    
    def _make_lines_program(self):
        """ Compiles the lines shaders. This function compiles only the lines
            of the gizmo axis.
        """
        v_shader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
        GL.glShaderSource(v_shader, self.vertex_shader_lines)
        GL.glCompileShader(v_shader)
        f_shader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
        GL.glShaderSource(f_shader, self.fragment_shader_lines)
        GL.glCompileShader(f_shader)
        self.gl_lines_program = GL.glCreateProgram()
        GL.glAttachShader(self.gl_lines_program, v_shader)
        GL.glAttachShader(self.gl_lines_program, f_shader)
        GL.glLinkProgram(self.gl_lines_program)
        if GL.glGetShaderiv(v_shader, GL.GL_COMPILE_STATUS) != GL.GL_TRUE:
            print("Error compiling the shader: ", "GL_VERTEX_SHADER")
            raise RuntimeError(GL.glGetShaderInfoLog(v_shader))
        if GL.glGetShaderiv(f_shader, GL.GL_COMPILE_STATUS) != GL.GL_TRUE:
            print("Error compiling the shader: ", "GL_FRAGMENT_SHADER")
            raise RuntimeError(GL.glGetShaderInfoLog(f_shader))
        return True
    
    def _get_vao(self, axis):
        """ Creates the Vertex Array Object, Vertex Buffer Objects and fill the
            shaders with the data of the corresponding axis. The buffers are not
            stored anywhere since the data will be the same always, so does the
            drawing method is GL_STATIC_DRAW and not GL_DYNAMIC_DRAW.
            
            Input parameters:
            axis -- a string describing the corresponding axis, its values can
                    be x_axis, y_axis or z_axis.
        
            Returns:
                The Vertex Array Object of the corresponding axis.
        """
        colors = self.axis_colors[axis] * int(len(self.axis_vertices[axis]))
        colors = np.array(colors, dtype=np.float32)
        
        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)
        
        ind_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self.axis_indexes.itemsize*int(len(self.axis_indexes)), self.axis_indexes, GL.GL_STATIC_DRAW)
        
        vert_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vert_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.axis_vertices[axis].itemsize*int(len(self.axis_vertices[axis])), self.axis_vertices[axis], GL.GL_STATIC_DRAW)
        att_position = GL.glGetAttribLocation(self.gizmo_axis_program, 'vert_coord')
        GL.glEnableVertexAttribArray(att_position)
        GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*self.axis_vertices[axis].itemsize, ctypes.c_void_p(0))
        
        col_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
        att_colors = GL.glGetAttribLocation(self.gizmo_axis_program, 'vert_color')
        GL.glEnableVertexAttribArray(att_colors)
        GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
        
        norm_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, norm_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.axis_normals[axis].itemsize*len(self.axis_normals[axis]), self.axis_normals[axis], GL.GL_STATIC_DRAW)
        att_norm = GL.glGetAttribLocation(self.gizmo_axis_program, 'vert_norm')
        GL.glEnableVertexAttribArray(att_norm)
        GL.glVertexAttribPointer(att_norm, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*self.axis_normals[axis].itemsize, ctypes.c_void_p(0))
        
        GL.glBindVertexArray(0)
        GL.glDisableVertexAttribArray(att_position)
        GL.glDisableVertexAttribArray(att_colors)
        GL.glDisableVertexAttribArray(att_norm)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
        
        return vao
    
    def _get_vao_lines(self):
        """ Creates the Vertex Array Object, Vertex Buffer Objects and fill the
            shaders with the data of the gizmo's lines. It takes no arguments
            since the lines are taken as one entity
            
            Returns:
                The Vertex Array Object of the corresponding axis.
        """
        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)
        
        vert_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vert_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.lines_vertices.itemsize*int(len(self.lines_vertices)), self.lines_vertices, GL.GL_STATIC_DRAW)
        
        att_position = GL.glGetAttribLocation(self.gl_lines_program, 'vert_coord')
        GL.glEnableVertexAttribArray(att_position)
        GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*self.lines_vertices.itemsize, ctypes.c_void_p(0))
        
        col_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.lines_colors.itemsize*int(len(self.lines_colors)), self.lines_colors, GL.GL_STATIC_DRAW)
        
        att_colors = GL.glGetAttribLocation(self.gl_lines_program, 'vert_color')
        GL.glEnableVertexAttribArray(att_colors)
        GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*self.lines_colors.itemsize, ctypes.c_void_p(0))
        
        GL.glBindVertexArray(0)
        GL.glDisableVertexAttribArray(att_position)
        GL.glDisableVertexAttribArray(att_colors)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        
        return vao
    
    def load_params(self):
        """ This function load the model matrix of the gizmo, the camera
            position and the light parameters in the cones OpenGL program.
        """
        model = GL.glGetUniformLocation(self.gizmo_axis_program, 'model_mat')
        GL.glUniformMatrix4fv(model, 1, GL.GL_FALSE, self.model_mat)
        cam_pos = GL.glGetUniformLocation(self.gizmo_axis_program, 'cam_pos')
        GL.glUniform3fv(cam_pos, 1, self.camera_position)
        light_pos = GL.glGetUniformLocation(self.gizmo_axis_program, 'my_light.position')
        GL.glUniform3fv(light_pos, 1, self.light_position)
        light_col = GL.glGetUniformLocation(self.gizmo_axis_program, 'my_light.color')
        GL.glUniform3fv(light_col, 1, self.light_color)
        amb_coef = GL.glGetUniformLocation(self.gizmo_axis_program, 'my_light.ambient_coef')
        GL.glUniform1fv(amb_coef, 1, self.light_ambient_coef)
        spec_coef = GL.glGetUniformLocation(self.gizmo_axis_program, 'my_light.specular_coef')
        GL.glUniform1fv(spec_coef, 1, self.light_specular_coef)
        shiny = GL.glGetUniformLocation(self.gizmo_axis_program, 'my_light.shininess')
        GL.glUniform1fv(shiny, 1, self.light_shininess)
        return True
    
    def load_lines_params(self):
        """ Load the model matrix of the gizmo's lines in the lines OpenGL
            program.
        """
        model = GL.glGetUniformLocation(self.gl_lines_program, 'model_mat')
        GL.glUniformMatrix4fv(model, 1, GL.GL_FALSE, self.model_mat)
        return True
    
    def _draw_gizmo_axis(self, flag):
        """ Function called to draw the gizmo axis in an OpenGL window.
            To drawing method is inside the class to make the class completely
            independent.
            
            Input parameters:
            flag -- a boolean to determine if the cones or the lines are going
                    to be drawed up. True for draw the cones, False to draw
                    the lines.
            
            IMPORTANT!!!
            THIS FUNCTION MUST BE CALLED ONLY WHEN AN OPENGL CONTEXT WINDOW HAS
            BEEN CREATED AND INITIALIZED, OTHERWISE WILL RAISE AN ERROR IN THE
            OPENGL WRAPPER!!!
            YOU HAVE BEEN WARNED
        """
        GL.glEnable(GL.GL_DEPTH_TEST)
        if flag:
            GL.glUseProgram(self.gizmo_axis_program)
            self.load_params()
            GL.glBindVertexArray(self.x_vao)
            GL.glDrawElements(GL.GL_TRIANGLES, len(self.axis_indexes), GL.GL_UNSIGNED_INT, None)
            GL.glBindVertexArray(0)
            GL.glBindVertexArray(self.y_vao)
            GL.glDrawElements(GL.GL_TRIANGLES, len(self.axis_indexes), GL.GL_UNSIGNED_INT, None)
            GL.glBindVertexArray(0)
            GL.glBindVertexArray(self.z_vao)
            GL.glDrawElements(GL.GL_TRIANGLES, len(self.axis_indexes), GL.GL_UNSIGNED_INT, None)
            GL.glBindVertexArray(0)
            GL.glUseProgram(0)
        else:
            GL.glUseProgram(self.gl_lines_program)
            GL.glLineWidth(3)
            self.load_lines_params()
            GL.glBindVertexArray(self.lines_vao)
            GL.glDrawArrays(GL.GL_LINES, 0, len(self.lines_vertices))
            GL.glBindVertexArray(0)
            GL.glLineWidth(1)
            GL.glUseProgram(0)
        GL.glDisable(GL.GL_DEPTH_TEST)
        return True
    
