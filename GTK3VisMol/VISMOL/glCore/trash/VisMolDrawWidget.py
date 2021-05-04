#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  VisMolDrawWidget.py
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

import numpy as np
import math
import matrix_operations as mop
import operations as op
import vismol_shaders as sh
import vaos
import time

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from OpenGL import GL

class VisMolDrawWidget(Gtk.GLArea):
    
    def __init__(self, widget, vismolSession = None, width=640.0, height=420.0):
        """ Function doc """
        self.parent_widget = widget
        self.vismolSession = vismolSession
        self.width = np.float32(width)
        self.height = np.float32(height)
    
    def initialize(self):
        """ Function doc """
        self.parent_widget.set_has_depth_buffer(True)
        self.parent_widget.set_has_alpha(True)
        self.z_near = 1.0
        self.z_far = 9.0
        self.min_znear = 0.1
        self.min_zfar = 1.1
        self.model_mat = np.identity(4, dtype=np.float32)
        self.view_mat = mop.my_glTranslatef(np.identity(4, dtype=np.float32), [0, 0, -5])
        self.cam_pos = self.get_cam_pos()
        self.fov = 20.0 # Field Of View = fov
        self.var = self.width/self.height # Viewport Aspect Ratio
        self.proj_mat = mop.my_glPerspectivef(self.fov, self.var, self.z_near, self.z_far)
        self.gl_programs = True
        self.right = self.width / self.height
        self.left = -self.right
        self.top = 1.0
        self.bottom = -1.0
        self.scroll = 0.3
        self.edit_points = []
        self.editing = True
        self.mouse_rotate = False
        self.mouse_pan = False
        self.mouse_zoom = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.drag_pos_x = 0
        self.drag_pos_y = 0
        self.drag_pos_z = 0
        self.dx = 0.0
        self.dy = 0.0
        self.start_time = time.perf_counter()
        self.ctrl = False
        self.shift = False
        self.light_position = np.array([-2.5, 2.5, 3.0],dtype=np.float32)
        self.light_color = np.array([1.0, 1.0, 1.0, 1.0],dtype=np.float32)
        self.light_ambient_coef = 0.5
        self.light_shininess = 5.5
        self.light_intensity = np.array([0.6, 0.6, 0.6],dtype=np.float32)
        self.light_specular_color = np.array([1.0, 1.0, 1.0],dtype=np.float32)
        # Here are the test programs and flags
        self.gl_program_edit_mode = None
        self.edit_mode_vao = None
        self.edit_mode_vbos = None
        self.edit_mode_elemns = None
        self.modified_points = False
        return True
    
    def resize_window(self, width, height):
        """ Function doc """
        self.width = np.float32(width)
        self.height = np.float32(height)
        self.right = self.width / self.height
        self.left = -self.right
        self.var = self.width/self.height # Viewport Aspect Ratio
        self.proj_mat = mop.my_glPerspectivef(self.fov, self.var, self.z_near, self.z_far)
        return True
    
    def create_gl_programs(self):
        """ Function doc """
        print('OpenGL version: ',GL.glGetString(GL.GL_VERSION))
        try:
            print('OpenGL major version: ',GL.glGetDoublev(GL.GL_MAJOR_VERSION))
            print('OpenGL minor version: ',GL.glGetDoublev(GL.GL_MINOR_VERSION))
        except:
            print('OpenGL major version not found')
        self.gl_program_edit_mode = self.load_shaders(sh.v_shader_spheres, sh.f_shader_spheres)
        return True
    
    def load_shaders(self, vertex, fragment, geometry=None):
        """ Here the shaders are loaded and compiled to an OpenGL program. By default
            the constructor shaders will be used, if you want to change the shaders
            use this function. The flag is used to create only one OpenGL program.
            
            Keyword arguments:
            vertex -- The vertex shader to be used
            fragment -- The fragment shader to be used
        """
        my_vertex_shader = self.create_shader(vertex, GL.GL_VERTEX_SHADER)
        my_fragment_shader = self.create_shader(fragment, GL.GL_FRAGMENT_SHADER)
        if geometry is not None:
            my_geometry_shader = self.create_shader(geometry, GL.GL_GEOMETRY_SHADER)
        program = GL.glCreateProgram()
        GL.glAttachShader(program, my_vertex_shader)
        GL.glAttachShader(program, my_fragment_shader)
        if geometry is not None:
            GL.glAttachShader(program, my_geometry_shader)
        GL.glLinkProgram(program)
        return program
        
    def create_shader(self, shader_prog, shader_type):
        """ Creates, links to a source, compiles and returns a shader.
            
            Keyword arguments:
            shader -- The shader text to use
            shader_type -- The OpenGL enum type of shader, it can be:
                           GL.GL_VERTEX_SHADER, GL.GL_GEOMETRY_SHADER or GL.GL_FRAGMENT_SHADER
            
            Returns:
            A shader object identifier or pops out an error
        """
        shader = GL.glCreateShader(shader_type)
        GL.glShaderSource(shader, shader_prog)
        GL.glCompileShader(shader)
        if GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS) != GL.GL_TRUE:
            print("Error compiling the shader: ", shader_type)
            raise RuntimeError(GL.glGetShaderInfoLog(shader))
        return shader
    
    def load_matrices(self, program):
        """ Function doc """
        model = GL.glGetUniformLocation(program, 'model_mat')
        GL.glUniformMatrix4fv(model, 1, GL.GL_FALSE, self.model_mat)
        view = GL.glGetUniformLocation(program, 'view_mat')
        GL.glUniformMatrix4fv(view, 1, GL.GL_FALSE, self.view_mat)
        proj = GL.glGetUniformLocation(program, 'proj_mat')
        GL.glUniformMatrix4fv(proj, 1, GL.GL_FALSE, self.proj_mat)
        return True
    
    def load_lights(self, program):
        """ Function doc
        """
        light_pos = GL.glGetUniformLocation(program, 'my_light.position')
        GL.glUniform3fv(light_pos, 1, self.light_position)
        #light_col = GL.glGetUniformLocation(program, 'my_light.color')
        #GL.glUniform3fv(light_col, 1, self.light_color)
        amb_coef = GL.glGetUniformLocation(program, 'my_light.ambient_coef')
        GL.glUniform1fv(amb_coef, 1, self.light_ambient_coef)
        shiny = GL.glGetUniformLocation(program, 'my_light.shininess')
        GL.glUniform1fv(shiny, 1, self.light_shininess)
        intensity = GL.glGetUniformLocation(program, 'my_light.intensity')
        GL.glUniform3fv(intensity, 1, self.light_intensity)
        #spec_col = GL.glGetUniformLocation(program, 'my_light.specular_color')
        #GL.glUniform3fv(spec_col, 1, self.light_specular_color)
        return True
    
    def get_viewport_pos(self, x, y):
        """ Function doc """
        px = (2.0*x - self.width)/self.width
        py = (self.height - 2.0*y)/self.height
        return [px, py, self.z_near]
    
    def get_cam_pos(self):
        """ Returns the position of the camera in XYZ coordinates
            The type of data returned is 'numpy.ndarray'.
        """
        modelview = mop.my_glMultiplyMatricesf(self.model_mat, self.view_mat)
        crd_xyz = -1 * np.mat(modelview[:3,:3]) * np.mat(modelview[3,:3]).T
        return crd_xyz.A1
    
    def _update_cam_pos(self):
        """ Function doc """
        self.cam_pos = self.get_cam_pos()
        return True
    
    def render(self):
        """ Function doc """
        if self.gl_programs:
            self.create_gl_programs()
            self.gl_programs = False
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        if len(self.edit_points) > 0:
            if self.modified_points:
                self.edit_mode_vao, self.edit_mode_vbos, self.edit_mode_elemns = vaos.make_spheres(self.gl_program_edit_mode, self.edit_points)
                self.modified_points = False
            self._draw_edit_mode()
    
    def _draw_edit_mode(self):
        """ Function doc """
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.gl_program_edit_mode)
        self.load_matrices(self.gl_program_edit_mode)
        self.load_lights(self.gl_program_edit_mode)
        GL.glBindVertexArray(self.edit_mode_vao)
        GL.glDrawElements(GL.GL_TRIANGLES, self.edit_mode_elemns, GL.GL_UNSIGNED_INT, None)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
    
    def mouse_pressed(self, button_number, mouse_x, mouse_y):
        """ Function doc """
        left = button_number == 1
        middle = button_number == 2
        right = button_number == 3
        self.mouse_rotate = left and not (middle or right)
        self.mouse_zoom = right and not (middle or left)
        self.mouse_pan = middle and not (right  or left)
        self.mouse_x = float(mouse_x)
        self.mouse_y = float(mouse_y)
        self.drag_pos_x, self.drag_pos_y, self.drag_pos_z = self.get_viewport_pos(self.mouse_x, self.mouse_y)
        self.dragging = False
        if left:
            self.dx = 0.0
            self.dy = 0.0
        if middle:
            pass
        if right:
            pass
    
    def mouse_released(self, button_number, mouse_x, mouse_y):
        """ Function doc """
        left = int(button_number) == 1
        middle = int(button_number) == 2
        right = int(button_number) == 3
        self.mouse_rotate = False
        self.mouse_zoom = False
        self.mouse_pan = False
        if left:
            if self.dragging:
                pass
                #if (time.perf_counter()-self.start_time) <= 0.01:
                    #for i in range(10):
                        #self._rotate_view(self.dx, self.dy, self.mouse_x, self.mouse_y)
                        #self.parent_widget.get_window().invalidate_rect(None, False)
                        #self.parent_widget.get_window().process_updates(False)
                        #time.sleep(0.02)
                    #for i in range(1, 18):
                        #self._rotate_view(self.dx/i, self.dy/i, self.mouse_x, self.mouse_y)
                        #self.parent_widget.get_window().invalidate_rect(None, False)
                        #self.parent_widget.get_window().process_updates(False)
                        #time.sleep(0.02)
            else:
                if self.editing:
                    self.edit_draw(mouse_x, mouse_y)
                self.dragging = False
        if middle:
            pass
        if right:
            if not self.dragging:
                if self.editing:
                    self.edit_points = []
                    self.parent_widget.queue_draw()
    
    def mouse_motion(self, mouse_x, mouse_y):
        """ Function doc """
        x = float(mouse_x)
        y = float(mouse_y)
        dx = x - self.mouse_x
        dy = y - self.mouse_y
        if (dx==0 and dy==0):
            return
        self.mouse_x, self.mouse_y = x, y
        changed = False
        if self.mouse_rotate:
            changed = self._rotate_view(dx, dy, x, y)
        elif self.mouse_pan:
            changed = self._pan_view(x, y)
        elif self.mouse_zoom:
            changed = self._zoom_view(dy)
        if changed:
            self._update_cam_pos()
            self.start_time = time.perf_counter()
            self.dx = dx
            self.dy = dy
            self.dragging = True
            self.parent_widget.queue_draw()
        return True
    
    def mouse_scroll(self, direction):
        """ Function doc """
        up = int(direction) == 1
        down = int(direction) == -1
        if self.ctrl:
            if up:
                self.model_mat = mop.my_glTranslatef(self.model_mat, [0.0, 0.0, -self.scroll])
            if down:
                self.model_mat = mop.my_glTranslatef(self.model_mat, [0.0, 0.0, self.scroll])
        else:
            pos_z = self.cam_pos[2]
            if up:
                self.z_near -= self.scroll
                self.z_far += self.scroll
            if down:
                if (self.z_far-self.scroll) >= (self.min_zfar):
                    if (self.z_far-self.scroll) > (self.z_near+self.scroll):
                        self.z_near += self.scroll
                        self.z_far -= self.scroll
            if (self.z_near >= self.min_znear):
                self.proj_mat = mop.my_glPerspectivef(self.fov, self.var, self.z_near, self.z_far)
            else:
                if self.z_far < (self.min_zfar+self.min_znear):
                    self.z_near -= self.scroll
                    self.z_far = self.min_znear + self.min_zfar
                self.proj_mat = mop.my_glPerspectivef(self.fov, self.var, self.min_znear, self.z_far)
        self.parent_widget.queue_draw()
    
    def _rotate_view(self, dx, dy, x, y):
        """ Function doc """
        dist = np.linalg.norm(self.cam_pos)
        if dist < 25:
            factor = 36.0
        elif dist < 50:
            factor = 18.0
        else:
            factor = 12.0
        angle = math.sqrt(dx**2+dy**2)/float(self.width+1)*factor*dist
        if self.ctrl:
            if abs(dx) >= abs(dy):
                if (y-self.height/2.0) < 0:
                    rot_mat = mop.my_glRotatef(np.identity(4), angle, [0.0, 0.0, dx])
                else:
                    rot_mat = mop.my_glRotatef(np.identity(4), angle, [0.0, 0.0, -dx])
            else:
                if (x-self.width/2.0) < 0:
                    rot_mat = mop.my_glRotatef(np.identity(4), angle, [0.0, 0.0, -dy])
                else:
                    rot_mat = mop.my_glRotatef(np.identity(4), angle, [0.0, 0.0, dy])
        else:
            rot_mat = mop.my_glRotatef(np.identity(4), angle, [-dy, -dx, 0.0])
        self.model_mat = mop.my_glMultiplyMatricesf(self.model_mat, rot_mat)
        return True
    
    def _pan_view(self, x, y):
        """ Function doc """
        px, py, pz = self.get_viewport_pos(x, y)
        pan_mat = mop.my_glTranslatef(np.identity(4, dtype=np.float32),
            [(px-self.drag_pos_x)*self.z_far/10.0, 
             (py-self.drag_pos_y)*self.z_far/10.0, 
             (pz-self.drag_pos_z)*self.z_far/10.0])
        self.model_mat = mop.my_glMultiplyMatricesf(self.model_mat, pan_mat)
        self.drag_pos_x = px
        self.drag_pos_y = py
        self.drag_pos_z = pz
        return True
    
    def _zoom_view(self, dy):
        """ Function doc """
        delta = (((self.z_far-self.z_near)/2.0)+self.z_near)/200.0
        move_z = dy * delta
        moved_mat = mop.my_glTranslatef(self.view_mat, [0.0, 0.0, move_z])
        moved_pos = mop.get_xyz_coords(moved_mat)
        if moved_pos[2] > 0.101:
            self.view_mat = moved_mat
            self.z_near -= move_z
            self.z_far -= move_z
            if self.z_near >= self.min_znear:
                self.proj_mat = mop.my_glPerspectivef(self.fov, self.var, self.z_near, self.z_far)
            else:
                if self.z_far < (self.min_zfar+self.min_znear):
                    self.z_near += move_z
                    self.z_far = self.min_zfar+self.min_znear
                self.proj_mat = mop.my_glPerspectivef(self.fov, self.var, self.min_znear, self.z_far)
        else:
            pass
        return True
    
    def edit_draw(self, mouse_x, mouse_y):
        """ Function doc """
        proj = np.matrix(self.proj_mat)
        view = np.matrix(self.view_mat)
        model = np.matrix(self.model_mat)
        i_proj = proj.I
        i_view = view.I
        i_model = model.I
        i_mvp = i_proj * i_view * i_model
        mod = self.get_viewport_pos(mouse_x, mouse_y)
        mod.append(1)
        mod = np.matrix(mod)
        mod = (mod*i_mvp).A1
        mod /= mod[3]
        u_vec = op.unit_vector(mod[:3] - self.cam_pos)
        v_vec = op.unit_vector(-self.cam_pos)
        angle = np.radians(op.get_angle(v_vec, u_vec))
        hypo = op.get_euclidean(self.cam_pos, [0,0,0]) / np.cos(angle)
        test = u_vec * hypo
        mod = self.cam_pos + test
        self.add_points(mod[:3])
        self.parent_widget.queue_draw()
    
    def add_points(self, point):
        """ Function doc """
        for i in point:
            self.edit_points.append(i)
        self.modified_points = True
        print("Point added")
    
    def key_pressed(self, k_name):
        """ Function doc """
        func = getattr(self, '_pressed_' + k_name, None)
        if func:
            func()
        return True
    
    def key_released(self, k_name):
        """ Function doc """
        func = getattr(self, '_released_' + k_name, None)
        if func:
            func()
        return True
    
    def _pressed_e(self):
        self.editing = not self.editing
        print("Editing mode:", self.editing)
    
    def _pressed_Control_L(self):
        self.ctrl = True
    
    def _released_Control_L(self):
        self.ctrl = False
    
    def _pressed_Shift_L(self):
        """ Function doc
        """
        self.shift = True
        return True
    
    def _released_Shift_L(self):
        """ Function doc
        """
        self.shift = False
        return True
    
    def _pressed_i(self):
        print("------------------------------------")
        print(self.edit_points,"<- points")
    
    def _pressed_o(self):
        print("------------------------------------")
        print(self.cam_pos,"<- camera position")
        print(np.linalg.norm(self.cam_pos),"<- camera dist to 0")
    
    def _pressed_m(self):
        print("------------------------------------")
        print(self.model_mat,"<- model matrix")
        print("------------------------------------")
        print(self.view_mat,"<- view matrix")
        print("------------------------------------")
        print(self.proj_mat,"<- projection matrix")
    
    
