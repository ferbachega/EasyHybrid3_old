#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  VisMolGLCore.py
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

import math
import numpy as np
import ctypes
from OpenGL import GL

import VISMOL.glCore.shapes as shapes
import VISMOL.glCore.glaxis as glaxis
import VISMOL.glCore.glcamera as cam
import VISMOL.glCore.operations as op
import VISMOL.glCore.sphere_data as sph_d
#import VISMOL.glCore.vismol_shaders as vm_shader
import VISMOL.glCore.matrix_operations as mop
import VISMOL.glCore.selection_box as sb
import VISMOL.glCore.sphere_representation as sph_r

import VISMOL.glCore.shaders.sticks             as sticksShaders
#import VISMOL.glCore.shaders.new_lines          as linesShaders
import VISMOL.glCore.shaders.lines              as linesShaders
import VISMOL.glCore.shaders.spheres            as spheresShaders
import VISMOL.glCore.shaders.surface            as surfacesShaders
import VISMOL.glCore.shaders.wires              as wiresShaders

import VISMOL.glCore.shaders.dots               as dotsShaders
import VISMOL.glCore.shaders.freetype           as freetypeShaders
import VISMOL.glCore.shaders.picked_and_picking as pickedShaders
import VISMOL.glCore.shaders.nonbond            as nonbondShaders
import VISMOL.glCore.shaders.glumpy             as glumpyShaders

class ShaderConfigObj:
	""" Class doc """
	
	def __init__ (self, vismol_glCore):
		""" Class initialiser """
		pass

	def define_line_shaders (self):
		""" Function doc """
		
	def define_dot_shaders (self):
		""" Function doc """
	
	def define_stick_shaders (self):
		""" Function doc """

	def define_sphere_shaders (self):
		""" Function doc """
		



class VisMolGLCore():
    
    def __init__(self, widget, vismolSession = None, width=640.0, height=420.0):
        """ Constructor of the class.
            
            Keyword arguments:
            vismolSession - 
        """
        self.parent_widget = widget
        self.vismolSession = vismolSession
        self.vConfig = self.vismolSession.vConfig
        self.width = np.float32(width)
        self.height = np.float32(height)
        self.sel_lines_buffers = None # this is not permanent - should be removed after some bug fixing 
        self.shader_programs = {}

    def initialize(self):
        """ Enables the buffers and other charasteristics of the OpenGL context.
            sets the initial projection, view and model matrices
            
            self.flag -- Needed to only create one OpenGL program, otherwise a bunch of
                         programs will be created and use system resources. If the OpenGL
                         program will be changed change this value to True
        """
        self.model_mat = np.identity(4, dtype=np.float32)
        self.normal_mat = np.identity(3, dtype=np.float32)
        self.zero_reference_point = np.array([0.0, 0.0, 0.0],dtype=np.float32)
        
        self.glcamera = cam.GLCamera(self.vConfig.gl_parameters['field_of_view'],  # int
                                     self.width/self.height                     , 
                                     np.array([0,0,10],dtype=np.float32)        , 
                                     self.zero_reference_point)
        
        
        
        self.axis = glaxis.GLAxis()
        self.parent_widget.set_has_depth_buffer(True)
        self.parent_widget.set_has_alpha(True)
        self.frame = 0
        self.scroll = self.vConfig.gl_parameters['scroll_step'] # 0.9 - float
        self.right = self.width/self.height
        self.left = -self.right
        self.top = 1.0
        self.bottom = -1.0
        self.button = None
        self.mouse_x = 0.0
        self.mouse_y = 0.0
        self.selection_box = sb.SelectionBox()
        self.bckgrnd_color = self.vConfig.gl_parameters['background_color'] # list of floats = [1.0,1.0,1.0,1.0]#[78/255, 78/255, 78/255, 1.0]#[0.0,0.0,0.0,1.0]#[0.5,0.5,0.5,1.0] #[0.0,0.0,0.0,1.0] #[1.0,1.0,1.0,1.0] or [0.0,0.0,0.0,1.0]
        
        #light
        self.light_position       =np.array(self.vConfig.gl_parameters['light_position'] ,dtype=np.float32)        #np.array([-2.5,2.5,3.0]   ,dtype=np.float32)
        self.light_color          =np.array(self.vConfig.gl_parameters['light_color']    ,dtype=np.float32)        #np.array([1.0,1.0,1.0,1.0],dtype=np.float32)
        
        self.light_ambient_coef   = self.vConfig.gl_parameters['light_ambient_coef']                               #0.4
        self.light_shininess      = self.vConfig.gl_parameters['light_shininess']                                  #5.5
        
        self.light_intensity      =np.array(self.vConfig.gl_parameters['light_intensity']      ,dtype=np.float32)  #np.array([0.6,0.6,0.6],dtype=np.float32)
        self.light_specular_color =np.array(self.vConfig.gl_parameters['light_specular_color'] ,dtype=np.float32)  #np.array([1.0,1.0,1.0],dtype=np.float32)
        
        
        
        self.dist_cam_zrp = np.linalg.norm(self.glcamera.get_position()-self.zero_reference_point)
        self.shader_flag = True
        self.modified_data = False
        self.modified_view = False
        self.mouse_rotate = False
        self.mouse_zoom = False
        self.mouse_pan = False
        self.dragging = False
        self.editing_mols = False
        self.show_axis = True
        self.ctrl = False
        self.shift = False
        self.atom_picked = None
        self.picking = False
        self.show_selection_box = False
        return True
    
    def resize_window(self, width, height):
        """ Resizing function, takes the widht and height of the widget
            and modifies the view in the camera acording to the new values
        
            Keyword arguments:
            width -- Actual width of the window
            height -- Actual height of the window
        """
        w = float(width)
        h = float(height)
        self.left = -w/h
        self.right = -self.left
        self.width = w
        self.height = h
        self.center_x = w/2.0
        self.center_y = h/2.0
        self.glcamera.viewport_aspect_ratio = w/h
        self.glcamera.set_projection_matrix(mop.my_glPerspectivef(self.glcamera.field_of_view,
             self.glcamera.viewport_aspect_ratio, self.glcamera.z_near, self.glcamera.z_far))
        return True
    
    def key_pressed(self, k_name):
        """ The key_pressed function serves, as the names states, to catch
            events in the keyboard, e.g. letter 'l' pressed, 'backslash'
            pressed. Note that there is a difference between 'A' and 'a'.
            Here I use a specific handler for each key pressed after
            discarding the CONTROL, ALT and SHIFT keys pressed (usefull
            for customized actions) and maintained, i.e. it's the same as
            using Ctrl+Z to undo an action.
        """
        func = getattr(self, '_pressed_' + k_name, None)
        if func:
            func()
        return True
    
    def key_released(self, k_name):
        """ Used to indicates a key has been released.
        """
        func = getattr(self, '_released_' + k_name, None)
        if func:
            func()
        return True
    
    def mouse_pressed(self, button_number, mouse_x, mouse_y):
        """ Function doc
        """
        left   = int(button_number) == 1
        middle = int(button_number) == 2
        right  = int(button_number) == 3
        self.mouse_rotate = left   and not (middle or right)
        self.mouse_zoom   = right  and not (middle or left)
        self.mouse_pan    = middle and not (right  or left)
        self.mouse_x = float(mouse_x)
        self.mouse_y = float(mouse_y)
        self.drag_pos_x, self.drag_pos_y, self.drag_pos_z = self.pos(self.mouse_x, self.mouse_y)
        self.dragging = False
        if left:
            if self.shift:
                self.show_selection_box = True
                self.selection_box.start = self.get_viewport_pos(float(mouse_x), float(mouse_y))
                self.selection_box.end = self.get_viewport_pos(float(mouse_x), float(mouse_y))
                self.selection_box.update_points()
        if middle:
            self.picking_x = mouse_x
            self.picking_y = mouse_y
            self.picking = True
            self.queue_draw()
        if right:
            self.picking_x = mouse_x
            self.picking_y = mouse_y
            self.picking = True
            self.queue_draw()
            pass
        return True
    
    def mouse_released(self, event, mouse_x, mouse_y):
        """ Function doc
        int(event.button)
        
        """
        button_number = int(event.button)
        left   = int(button_number) == 1
        middle = int(button_number) == 2
        right  = int(button_number) == 3
        self.mouse_rotate = False
        self.mouse_zoom = False
        self.mouse_pan = False
        if self.dragging:
            if left:
                if self.shift:
                    self.show_selection_box = False
                    self.selection_box.start = None
                    self.selection_box.end = None
                    self.queue_draw()
        else:
            if left:
                self.picking_x = mouse_x
                self.picking_y = mouse_y
                self.picking = True
                self.button = 1
                self.queue_draw()
                #print (self.vismolSession.selections[self.vismolSession.current_selection].selected_objects)
                #for vobject in self.vismolSession.selections[self.vismolSession.current_selection].selected_objects:
                #    print (vobject.name, self.vismolSession.selections[self.vismolSession.current_selection].selected_objects[vobject], 'selection_function_viewing button1' )
            if middle:
                if self.atom_picked is not None:
                    self.button = 2
                    self.center_on_atom(self.atom_picked)
                    self.atom_picked = None
            if right:
                self.button = 3
                menu_type = None 
                # Checks if there is anything in the selection list
                # If {} means that there are no selection points on the screen
                if self.vismolSession.selections[self.vismolSession.current_selection].selected_objects == {}:
                    
                    print('selection is not active')
                    # There is no selection (blue dots) but an atom was identified in the click with the right button
                    if self.atom_picked is not None:

                        # Getting the information about the atom that was identified in the click
                        print(self.atom_picked.chain,self.atom_picked.resn, self.atom_picked.resi, self.atom_picked.name, self.atom_picked.index, self.atom_picked.bonds_indexes)
                        label = '{} / {} / {}({}) / {}({} / {})'.format( self.atom_picked.Vobject.name,
																    self.atom_picked.chain,
                                                                    self.atom_picked.resn, 
                                                                    self.atom_picked.resi, 
                                                                    self.atom_picked.name, 
                                                                    self.atom_picked.index,
                                                                    self.atom_picked.symbol)
                        #for bond in self.atom_picked.bonds:
                        #    print (bond.atom_index_i, bond.atom_index_j)
                        self.atom_picked = None
                        menu_type = 'obj_menu'
                        info = label
                    else:
                        
                        # When no atom is identified in the click (user clicked on a point in the background)
                        print ('self.atom_picked is None')
                        print ('selection is not active')
                        menu_type = 'bg_menu'
                        info = None
                else:
                    print('selection is  active')
                    info = self.vismolSession.selections[self.vismolSession.current_selection].get_selection_info()
                    menu_type = 'sele_menu'
                #self.parent_widget.glMenu.#open_gl_menu(event = event)
                #self.parent_widget.menu_header.set_label(label)
                #self.parent_widget.glMenu.popup(None, None, None, None, 0, 0)  
                self.parent_widget.show_gl_menu(menu_type = menu_type, info = info)
        return True
    
    def mouse_motion(self, mouse_x, mouse_y):
        """ Function doc
        """
        x = float(mouse_x)
        y = float(mouse_y)
        #state = event.state
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
            self.dragging = True
            self.queue_draw()
        return True
    
    def mouse_scroll(self, direction):
        """ Function doc
        """
        up = int(direction) == 1
        down = int(direction) == -1
        if self.ctrl:
            if not self.editing_mols:
                if up:
                    self.model_mat = mop.my_glTranslatef(self.model_mat, np.array([0.0, 0.0, -self.scroll]))
                if down:
                    self.model_mat = mop.my_glTranslatef(self.model_mat, np.array([0.0, 0.0, self.scroll]))
                for visObj in self.vismolSession.vismol_objects:
                    if up:
                        visObj.model_mat = mop.my_glTranslatef(visObj.model_mat, np.array([0.0, 0.0, -self.scroll]))
                    if down:
                        visObj.model_mat = mop.my_glTranslatef(visObj.model_mat, np.array([0.0, 0.0, self.scroll]))
            else:
                for visObj in self.vismolSession.vismol_objects:
                    if visObj.editing:
                        if up:
                            visObj.model_mat = mop.my_glTranslatef(visObj.model_mat, np.array([0.0, 0.0, -self.scroll]))
                        if down:
                            visObj.model_mat = mop.my_glTranslatef(visObj.model_mat, np.array([0.0, 0.0, self.scroll]))
        else:
            pos_z = self.glcamera.get_position()[2]
            if up:
                self.glcamera.z_near -= self.scroll
                self.glcamera.z_far += self.scroll
            if down:
                if (self.glcamera.z_far-self.scroll) >= (self.glcamera.min_zfar):
                    if (self.glcamera.z_far-self.scroll) > (self.glcamera.z_near+self.scroll+0.005):
                        self.glcamera.z_near += self.scroll
                        self.glcamera.z_far -= self.scroll
            if (self.glcamera.z_near >= self.glcamera.min_znear):
                self.glcamera.set_projection_matrix(mop.my_glPerspectivef(self.glcamera.field_of_view, 
                        self.glcamera.viewport_aspect_ratio, self.glcamera.z_near, self.glcamera.z_far))
            else:
                if self.glcamera.z_far < (self.glcamera.min_zfar+self.glcamera.min_znear):
                    self.glcamera.z_near -= self.scroll
                    self.glcamera.z_far = self.glcamera.min_clip+self.glcamera.min_znear
                self.glcamera.set_projection_matrix(mop.my_glPerspectivef(self.glcamera.field_of_view, 
                        self.glcamera.viewport_aspect_ratio, self.glcamera.min_znear, self.glcamera.z_far))
            self.glcamera.update_fog()
        self.queue_draw()
        return True
    
    def _rotate_view(self, dx, dy, x, y):
        """ Function doc """
        angle = math.sqrt(dx**2+dy**2)/float(self.width+1)*180.0
        if self.shift:
            self.selection_box.end = self.get_viewport_pos(float(self.mouse_x), float(self.mouse_y))
            self.selection_box.update_points()
        else:
            if self.ctrl:
                if abs(dx) >= abs(dy):
                    if (y-self.height/2.0) < 0:
                        rot_mat = mop.my_glRotatef(np.identity(4), angle, np.array([0.0, 0.0, dx]))
                    else:
                        rot_mat = mop.my_glRotatef(np.identity(4), angle, np.array([0.0, 0.0, -dx]))
                else:
                    if (x-self.width/2.0) < 0:
                        rot_mat = mop.my_glRotatef(np.identity(4), angle, np.array([0.0, 0.0, -dy]))
                    else:
                        rot_mat = mop.my_glRotatef(np.identity(4), angle, np.array([0.0, 0.0, dy]))
            else:
                rot_mat = mop.my_glRotatef(np.identity(4), angle, np.array([-dy, -dx, 0.0]))
            if self.editing_mols:
                for visObj in self.vismolSession.vismol_objects:
                    if visObj.editing:
                        visObj.model_mat = mop.my_glMultiplyMatricesf(visObj.model_mat, rot_mat)
            else:
                self.model_mat = mop.my_glMultiplyMatricesf(self.model_mat, rot_mat)
                for visObj in self.vismolSession.vismol_objects:
                    visObj.model_mat = mop.my_glMultiplyMatricesf(visObj.model_mat, rot_mat)
            # Axis operations, this code only affects the gizmo axis
            if not self.editing_mols:
                self.axis.model_mat = mop.my_glTranslatef(self.axis.model_mat, -self.axis.zrp)
                if self.ctrl:
                    if abs(dx) >= abs(dy):
                        if (y-self.height/2.0) < 0:
                            self.axis.model_mat = mop.my_glRotatef(self.axis.model_mat, angle, np.array([0.0, 0.0, dx]))
                        else:
                            self.axis.model_mat = mop.my_glRotatef(self.axis.model_mat, angle, np.array([0.0, 0.0, -dx]))
                    else:
                        if (x-self.width/2.0) < 0:
                            self.axis.model_mat = mop.my_glRotatef(self.axis.model_mat, angle, np.array([0.0, 0.0, -dy]))
                        else:
                            self.axis.model_mat = mop.my_glRotatef(self.axis.model_mat, angle, np.array([0.0, 0.0, dy]))
                else:
                    self.axis.model_mat = mop.my_glRotatef(self.axis.model_mat, angle, np.array([dy, dx, 0.0]))
                self.axis.model_mat = mop.my_glTranslatef(self.axis.model_mat, self.axis.zrp)
            # Axis operations, this code only affects the gizmo axis
        return True
    
    def _pan_view(self, x, y):
        """ Function doc """
        px, py, pz = self.pos(x, y)
        pan_mat = mop.my_glTranslatef(np.identity(4, dtype=np.float32),np.array(
            [(px-self.drag_pos_x)*self.glcamera.z_far/10.0, 
             (py-self.drag_pos_y)*self.glcamera.z_far/10.0, 
             (pz-self.drag_pos_z)*self.glcamera.z_far/10.0]))
        if not self.editing_mols:
            self.model_mat = mop.my_glMultiplyMatricesf(self.model_mat, pan_mat)
            for visObj in self.vismolSession.vismol_objects:
                visObj.model_mat = mop.my_glMultiplyMatricesf(visObj.model_mat, pan_mat)
            self.zero_reference_point = mop.get_xyz_coords(self.model_mat)
        else:
            for visObj in self.vismolSession.vismol_objects:
                if visObj.editing:
                    visObj.model_mat = mop.my_glMultiplyMatricesf(visObj.model_mat, pan_mat)
        self.drag_pos_x = px
        self.drag_pos_y = py
        self.drag_pos_z = pz
        return True
    
    def _zoom_view(self, dy):
        """ Function doc """
        delta = (((self.glcamera.z_far-self.glcamera.z_near)/2.0)+self.glcamera.z_near)/200.0
        move_z = dy * delta
        moved_mat = mop.my_glTranslatef(self.glcamera.view_matrix, np.array([0.0, 0.0, move_z]))
        moved_pos = mop.get_xyz_coords(moved_mat)
        if moved_pos[2] > 0.101:
            self.glcamera.set_view_matrix(moved_mat)
            self.glcamera.z_near -= move_z
            self.glcamera.z_far -= move_z
            if self.glcamera.z_near >= self.glcamera.min_znear:
                self.glcamera.set_projection_matrix(mop.my_glPerspectivef(self.glcamera.field_of_view, 
                        self.glcamera.viewport_aspect_ratio, self.glcamera.z_near, self.glcamera.z_far))
            else:
                if self.glcamera.z_far < (self.glcamera.min_zfar+self.glcamera.min_znear):
                    self.glcamera.z_near += move_z
                    self.glcamera.z_far = self.glcamera.min_zfar+self.glcamera.min_znear
                self.glcamera.set_projection_matrix(mop.my_glPerspectivef(self.glcamera.field_of_view, 
                        self.glcamera.viewport_aspect_ratio, self.glcamera.min_znear, self.glcamera.z_far))
            self.glcamera.update_fog()
            self.dist_cam_zrp += -move_z
            return True
        return False
        
    
    def render(self):
        """ This is the function that will be called everytime the window
            needs to be re-drawed.
        """
        if self.shader_flag:
            print ('self.create_gl_programs()')
            self.create_gl_programs()
            self.selection_box.initialize_gl()
            self.axis.initialize_gl()
            self.shader_flag = False
        
        if self.picking:
            #self._pick()
            self._pick2()
        
        GL.glClearColor(self.bckgrnd_color[0],self.bckgrnd_color[1], self.bckgrnd_color[2],self.bckgrnd_color[3])
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        
        for visObj in self.vismolSession.vismol_objects:
            # for all the visObj in all created visObjs  

            if visObj.active:
                # visObj.active = False means that nothing is showed 
                
                for rep_name in visObj.representations:
                    # if the representation doen't exists , ignore
                    if visObj.representations[rep_name] is None:
                        pass
                    
                    else:
                        # only shows the representation if representations[rep_name].active = True
                        if visObj.representations[rep_name].active:
                            #print(rep_name,visObj.representations[rep_name].active)
                            visObj.representations[rep_name].draw_representation()
                            #visObj.representations[rep_name].draw_background_sel_representation()
                        else:
                            pass


        for visObj in self.vismolSession.selections[self.vismolSession.current_selection].selected_objects:
            '''
            Here are represented the blue 
            dots referring to the atom's selections 
            '''
            if visObj.selection_dots_vao is None:
                shapes._make_gl_selection_dots(self.picking_dots_program, vismol_object = visObj)
            
            '''#Extracting the indexes for each vismol_object that was selected'''
            indexes = self.vismolSession.selections[self.vismolSession.current_selection].selected_objects[visObj]
            
            #print(indexes)
            #print(type(self.vismolSession.selections[self.vismolSession.current_selection].selected_objects[visObj]))
            #print(self.vismolSession.selections[self.vismolSession.current_selection].selected_objects)
            
            size =  self.vConfig.gl_parameters['dot_sel_size']
            GL.glPointSize(size*self.height/(abs(self.dist_cam_zrp))/2)
            #print (visObj, visObj.non_bonded_atoms)
            
            #print ('line 522')
            #GL.glPointSize(15)
            GL.glUseProgram(self.picking_dots_program)
            GL.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
            self.load_matrices(self.picking_dots_program, visObj.model_mat)
            #print ('line510')

            #self._draw_picking_dots(visObj = visObj, indexes = False)
            GL.glBindVertexArray(visObj.selection_dots_vao)
            
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, visObj.selection_dot_buffers[0])
            GL.glBufferData(GL.GL_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), 
                            indexes, GL.GL_STATIC_DRAW)
            
            frame = self._safe_frame_exchange(visObj)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, visObj.selection_dot_buffers[1])
            GL.glBufferData(GL.GL_ARRAY_BUFFER, frame.itemsize*int(len(frame)), 
                            frame, GL.GL_STATIC_DRAW)

            #GL.glDrawElements(GL.GL_POINTS, int(len(indexes)), GL.GL_UNSIGNED_INT, None)
            GL.glDrawElements(GL.GL_POINTS, int(len(indexes)), GL.GL_UNSIGNED_INT, None)
            GL.glBindVertexArray(0)
            
            GL.glDisable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
            GL.glPointSize(1)
            GL.glUseProgram(0)
            GL.glDisable(GL.GL_DEPTH_TEST)
        
        
        
        
        
        
        
        
        
        
        
        
        
        '''
        indexes = self.vismolSession.picking_selections.picking_selections_list
        
        #print(indexes)
        #print(type(self.vismolSession.selections[self.vismolSession.current_selection].selected_objects[visObj]))
        #print(self.vismolSession.selections[self.vismolSession.current_selection].selected_objects)
        
        size =  self.vConfig.gl_parameters['dot_sel_size']
        GL.glPointSize(size*self.height/(abs(self.dist_cam_zrp))/2)
        
        #print ('line 522')
        #GL.glPointSize(15)
        GL.glUseProgram(self.picking_dots_program)
        GL.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
        self.load_matrices(self.picking_dots_program, visObj.model_mat)
        #print ('line510')

        #self._draw_picking_dots(visObj = visObj, indexes = False)
        GL.glBindVertexArray(visObj.selection_dots_vao)
        
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, visObj.selection_dot_buffers[0])
        GL.glBufferData(GL.GL_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), 
                        indexes, GL.GL_STATIC_DRAW)
        
        frame = self._safe_frame_exchange(visObj)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, visObj.selection_dot_buffers[1])
        GL.glBufferData(GL.GL_ARRAY_BUFFER, frame.itemsize*int(len(frame)), 
                        frame, GL.GL_STATIC_DRAW)

        #GL.glDrawElements(GL.GL_POINTS, int(len(indexes)), GL.GL_UNSIGNED_INT, None)
        GL.glDrawElements(GL.GL_POINTS, int(len(indexes)), GL.GL_UNSIGNED_INT, None)
        GL.glBindVertexArray(0)
        
        GL.glDisable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
        GL.glPointSize(1)
        GL.glUseProgram(0)
        GL.glDisable(GL.GL_DEPTH_TEST)
        '''
        
        
        
        
        
        
        
        
        
        
        
        
        
        # picking 1 2 3 4 atoms -  special way to select atoms
        #for index in self.vismolSession.picking_selections.picking_selections_list:  #selections[self.vismolSession.current_selection].selected_objects:
        #    if index != None:
        #        pass
                #print(visObj.index)
            #index = visObj
        
        
        
        #'''
        if self.show_selection_box and self.shift:
            if self.selection_box.vao is None:
                self.selection_box._make_gl_selection_box()
            else:
                self._draw_selection_box()
        
        if self.show_axis:
            self._draw_gizmo_axis(True)
            self._draw_gizmo_axis(False)
        return True
    
    
    
    def _create_dot_shaders (self, _type = 0):
        """ Function doc """
        #self.shader_programs['dots']     = self.load_shaders(dotsShaders.vertex_shader_dot_sphere  ,
        #                                                     dotsShaders.fragment_shader_dot_sphere
        #                                                     )
        #
        #self.shader_programs['dots_sel'] = self.load_shaders(dotsShaders.vertex_shader_dot_sphere  ,
        #                                                     dotsShaders.fragment_shader_dot_sphere
        #                                                     )
        dot_type = self.vConfig.gl_parameters['dot_type']

        self.shader_programs['dots']     = self.load_shaders(dotsShaders.shader_type[dot_type]['vertex_shader'  ],
                                                             dotsShaders.shader_type[dot_type]['fragment_shader']
                                                             )
        
        self.shader_programs['dots_sel'] = self.load_shaders(dotsShaders.shader_type[dot_type]['sel_vertex_shader'  ],
                                                             dotsShaders.shader_type[dot_type]['sel_fragment_shader']
                                                             )
    
    
    def _create_line_shaders (self, _type = 0):
        # L I N E S 
        
        line_type = self.vConfig.gl_parameters['line_type']

        self.shader_programs['lines']      = self.load_shaders(linesShaders.shader_type[line_type]['vertex_shader'  ], 
                                                               linesShaders.shader_type[line_type]['fragment_shader'], 
                                                               linesShaders.shader_type[line_type]['geometry_shader'])
        
      

        self.shader_programs['lines_sel']  = self.load_shaders( linesShaders.shader_type[line_type]['sel_vertex_shader'  ],
                                                                linesShaders.shader_type[line_type]['sel_fragment_shader'],
                                                                linesShaders.shader_type[line_type]['sel_geometry_shader'])
                                                                      

    def _create_ribbon_shaders (self, _type = 0):
        # L I N E S 
        
        line_type = self.vConfig.gl_parameters['ribbon_type']

        self.shader_programs['ribbons']      = self.load_shaders(linesShaders.shader_type[line_type]['vertex_shader'  ], 
                                                                 linesShaders.shader_type[line_type]['fragment_shader'], 
                                                                 linesShaders.shader_type[line_type]['geometry_shader'])
        
      

        self.shader_programs['ribbons_sel']  = self.load_shaders( linesShaders.shader_type[line_type]['sel_vertex_shader'  ],
                                                                  linesShaders.shader_type[line_type]['sel_fragment_shader'],
                                                                  linesShaders.shader_type[line_type]['sel_geometry_shader'])
                                                                      



    def _create_nonbonded_shaders (self, _type = 0):
        # N O N  B O N D E D
        self.shader_programs['nonbonded']     = self.load_shaders(nonbondShaders.vertex_shader_non_bonded, 
                                                          nonbondShaders.fragment_shader_non_bonded, 
                                                          nonbondShaders.geometry_shader_non_bonded)
        
        self.shader_programs['nonbonded_sel'] = self.load_shaders(nonbondShaders.sel_vertex_shader_non_bonded, 
                                                          nonbondShaders.sel_fragment_shader_non_bonded, 
                                                          nonbondShaders.sel_geometry_shader_non_bonded)



    def _create_stick_shaders (self, _type = 0):
        # S T I C K S
        self.shader_programs['sticks']     = self.load_shaders(sticksShaders.vertex_shader_sticks, 
                                                               sticksShaders.fragment_shader_sticks, 
                                                               sticksShaders.geometry_shader_sticks)
        
        self.shader_programs['sticks_sel'] = self.load_shaders(sticksShaders.sel_vertex_shader_sticks, 
                                                               sticksShaders.sel_fragment_shader_sticks, 
                                                               sticksShaders.sel_geometry_shader_sticks)




    def _create_dynamic_bonds_shaders (self, _type = 0):
        # S T I C K S
        self.shader_programs['dynamic']     = self.load_shaders(sticksShaders.vertex_shader_sticks, 
                                                               sticksShaders.fragment_shader_sticks, 
                                                               sticksShaders.geometry_shader_sticks)
        
        self.shader_programs['dynamic_sel'] = self.load_shaders(sticksShaders.sel_vertex_shader_sticks, 
                                                               sticksShaders.sel_fragment_shader_sticks, 
                                                               sticksShaders.sel_geometry_shader_sticks)




    def _create_sphere_shaders (self, _type = 0):
        self.shader_programs['spheres']     = self.load_shaders(spheresShaders.vertex_shader_spheres, 
                                                                spheresShaders.fragment_shader_spheres)
        
        self.shader_programs['spheres_sel'] = self.load_shaders(spheresShaders.vertex_shader_spheres,  
                                                                spheresShaders.fragment_shader_spheres)


    def _create_impostor_shaders (self, _type = 0):
        """ Function doc """
        # G L U M P Y
        
        _type = self.vConfig.gl_parameters['impostor_type']
        
        self.shader_programs['glumpy']     = self.load_shaders(glumpyShaders.shader_type[_type]['sel_vertex_shader'  ],
                                                               glumpyShaders.shader_type[_type]['sel_fragment_shader'])
        self.shader_programs['glumpy_sel'] = self.load_shaders(glumpyShaders.shader_type[_type]['sel_vertex_shader'  ],
                                                               glumpyShaders.shader_type[_type]['sel_fragment_shader'])



    def _surface_dot_shaders (self, _type = 0):
        """ Function doc """
        #self.shader_programs['dots']     = self.load_shaders(dotsShaders.vertex_shader_dot_sphere  ,
        #                                                     dotsShaders.fragment_shader_dot_sphere
        #                                                     )
        #
        #self.shader_programs['dots_sel'] = self.load_shaders(dotsShaders.vertex_shader_dot_sphere  ,
        #                                                     dotsShaders.fragment_shader_dot_sphere
        #                                                     )
        #dot_type = self.vConfig.gl_parameters['dot_type']  vertex_shader_spheres 
        '''
        self.shader_programs['surface']     = self.load_shaders(dotsShaders.shader_type[0]['vertex_shader'  ],
                                                                dotsShaders.shader_type[0]['fragment_shader']
                                                                )
        
        self.shader_programs['surface_sel'] = self.load_shaders(dotsShaders.shader_type[0]['sel_vertex_shader'  ],
                                                                dotsShaders.shader_type[0]['sel_fragment_shader']
                                                                )
        '''

        # self.shader_programs['surface']     = self.load_shaders(spheresShaders.vertex_shader_spheres, 
        #                                                         spheresShaders.fragment_shader_spheres)
        self.shader_programs['surface']     = self.load_shaders(surfacesShaders.vertex_shader_surface,
                                                                surfacesShaders.fragment_shader_surface,
                                                                surfacesShaders.geometry_shader_surface)
        self.shader_programs['surface_sel'] = self.load_shaders(spheresShaders.vertex_shader_spheres,  
                                                                spheresShaders.fragment_shader_spheres)
        
    


    def _wires_dot_shaders (self, _type = 0):
        self.shader_programs['wires']     = self.load_shaders(wiresShaders.vertex_shader_wires,
                                                              wiresShaders.fragment_shader_wires,
                                                              wiresShaders.geometry_shader_wires)
        self.shader_programs['wires_sel'] = self.load_shaders(spheresShaders.vertex_shader_spheres,  
                                                              spheresShaders.fragment_shader_spheres)
                                              




    def create_gl_programs(self):
        """ Function doc
        """
        print('OpenGL version: ',GL.glGetString(GL.GL_VERSION))
        try:
            print('OpenGL major version: ',GL.glGetDoublev(GL.GL_MAJOR_VERSION))
            print('OpenGL minor version: ',GL.glGetDoublev(GL.GL_MINOR_VERSION))
        except:
            print('OpenGL major version not found')



        #-------------------------------------------------------------------------------------
        self._create_dot_shaders ()
        #-------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------
        self._create_line_shaders()
        self._create_nonbonded_shaders()
        self._create_ribbon_shaders ()
        #-------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------
        self._create_stick_shaders()
        self._create_sphere_shaders ()
        self._create_dynamic_bonds_shaders()
        self._create_impostor_shaders()
        #-------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------
        self._surface_dot_shaders ()
        self._wires_dot_shaders ()
        #-------------------------------------------------------------------------------------

        
        
        ## P I C K 
        #self.picked_program = self.load_shaders(pickedShaders.vertex_shader_picked, 
        #                                        pickedShaders.fragment_shader_picked)
        
        self.picking_dots_program = self.load_shaders(pickedShaders.vertex_shader_picking_dots, 
                                                      pickedShaders.fragment_shader_picking_dots)
                                                              
        # F R E E  T Y P E
        self.freetype_program = self.load_shaders(freetypeShaders.vertex_shader_freetype, 
                                                  freetypeShaders.fragment_shader_freetype, 
                                                  freetypeShaders.geometry_shader_freetype)
        

        

        #self.shader_programs['dots_surface']     = self.dots_surface_program
        #self.shader_programs['dots_surface_sel'] = self.sel_dots_surface_program
        #self.shader_programs['ribbons']          = self.ribbons_program


        #self.shader_programs['picked']           = self.picked_program
        self.shader_programs['picking_dots']     = self.picking_dots_program
        self.shader_programs['freetype']         = self.freetype_program

        
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
    
    '''
    def _pick_old(self):
        """ Function doc
        """
        GL.glClearColor(1,1,1,1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        for visObj in self.vismolSession.vismol_objects:
            if visObj.active:
                if visObj.picking_dots_vao is None:
                    shapes._make_gl_picking_dots(self.picking_dots_program,  vismol_object = visObj)
                GL.glEnable(GL.GL_DEPTH_TEST)
                GL.glUseProgram(self.picking_dots_program)
                GL.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
                self.load_matrices(self.picking_dots_program, visObj.model_mat)
                self._draw_picking_dots(visObj = visObj, indexes = False)
                GL.glDisable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
                GL.glUseProgram(0)
                GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)
        pos = [self.picking_x, self.height - self.picking_y]
        data = GL.glReadPixels(pos[0], (pos[1]), 1, 1, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE)
        pickedID = data[0] + data[1] * 256 + data[2] * 256*256;
        if pickedID == 16777215:
            self.atom_picked = None
            if self.button ==1:
                self.vismolSession._selection_function (self.atom_picked)
                print(self.atom_picked)
                self.button = None
        else:
            self.atom_picked = self.vismolSession.atom_dic_id[pickedID]
            if self.button ==1:
                self.vismolSession._selection_function (self.atom_picked)
                print(self.atom_picked)
                self.button = None
        self.picking = False
    '''
    
    def _pick2(self):
        """ Function doc """
        GL.glClearColor(1,1,1,1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        for visObj in self.vismolSession.vismol_objects:
            #if visObj.active:
            #    _draw_background_sel_representation

            if visObj.active:
                #visObj has few different types of representations
                
                for rep_name in visObj.representations:
                    # checking all the representations in visObj.representations dictionary
                    if visObj.representations[rep_name] is None:
                        pass
                    else:
                        
                        #  visObj.representations[rep_name] may be active or not  True/False
                        if visObj.representations[rep_name].active:
                            visObj.representations[rep_name].draw_background_sel_representation()
                        else:
                            pass

        GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)
        pos = [self.picking_x, self.height - self.picking_y]
        data = GL.glReadPixels(pos[0], (pos[1]), 1, 1, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE)
        pickedID = data[0] + data[1] * 256 + data[2] * 256*256;
        
        if pickedID == 16777215:
            self.atom_picked = None
            if self.button ==1:
                self.vismolSession._selection_function (self.atom_picked)
                #print('_selection_function 965', self.vismolSession.selections[self.vismolSession.current_selection].active )
                self.button = None
        else:
            try:
                '''
                
                Using antialias, in some rare cases, the pick function is not 
                identifying the right color of the selected atom. This event is 
                rare, but can impair viewing if it is not properly ignored
                
                '''
                self.atom_picked = self.vismolSession.atom_dic_id[pickedID]
                if self.button ==1:
                    #print('_selection_function 978', self.vismolSession.selections[self.vismolSession.current_selection].active )
                    self.vismolSession._selection_function (self.atom_picked)
                    #print('_selection_function 980', self.vismolSession.selections[self.vismolSession.current_selection].active )

                    self.button = None
            except:
                print('pickedID', pickedID, 'not found')
                self.button = None
        self.picking = False
        return True
    
    def load_fog(self, program):
        """ Load the fog parameters in the specified program
            
            fog_start -- The coordinates where the fog will begin (always
                         positive)
            fog_end -- The coordinates where the fog will begin (always positive
                       and greater than fog_start)
            fog_color -- The color for the fog (same as background)
        """
        fog_s = GL.glGetUniformLocation(program, 'fog_start')
        GL.glUniform1fv(fog_s, 1, self.glcamera.fog_start)
        fog_e = GL.glGetUniformLocation(program, 'fog_end')
        GL.glUniform1fv(fog_e, 1, self.glcamera.fog_end)
        fog_c = GL.glGetUniformLocation(program, 'fog_color')
        GL.glUniform4fv(fog_c, 1, self.bckgrnd_color)
        return True
        
    def load_matrices(self, program = None, model_mat = None, normal = None):
        """ Load the matrices to OpenGL.
            
            model_mat -- transformation matrix for the objects rendered
            view_mat -- transformation matrix for the camera used
            proj_mat -- matrix for the space to be visualized in the scene
        """
        model = GL.glGetUniformLocation(program, 'model_mat')
        GL.glUniformMatrix4fv(model, 1, GL.GL_FALSE, model_mat)
        view = GL.glGetUniformLocation(program, 'view_mat')
        GL.glUniformMatrix4fv(view, 1, GL.GL_FALSE, self.glcamera.view_matrix)
        proj = GL.glGetUniformLocation(program, 'proj_mat')
        GL.glUniformMatrix4fv(proj, 1, GL.GL_FALSE, self.glcamera.projection_matrix)
       
        # not sure if is necessary
        norm = GL.glGetUniformLocation(program, 'normal_mat')
        GL.glUniformMatrix3fv(norm, 1, GL.GL_FALSE, self.normal_mat)
        
        return True
    
    def load_dot_params(self, program):
        """ Function doc
        """
        # Extern line
        linewidth = float(80/abs(self.dist_cam_zrp))
        if linewidth > 3.73:
            linewidth = 3.73
        # Intern line
        antialias = float(80/abs(self.dist_cam_zrp))
        if antialias > 3.73:
            antialias = 3.73
        # Dot size factor
        dot_factor = float(500/abs(self.dist_cam_zrp))
        if dot_factor > 150.0:
            dot_factor = 150.0
        uni_vext_linewidth = GL.glGetUniformLocation(program, 'vert_ext_linewidth')
        GL.glUniform1fv(uni_vext_linewidth, 1, linewidth)
        uni_vint_antialias = GL.glGetUniformLocation(program, 'vert_int_antialias')
        GL.glUniform1fv(uni_vint_antialias, 1, antialias)
        uni_dot_size = GL.glGetUniformLocation(program, 'vert_dot_factor')
        GL.glUniform1fv(uni_dot_size, 1, dot_factor)
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
    
    def load_antialias_params(self, program):
        """ Function doc """
        a_length = GL.glGetUniformLocation(program, 'antialias_length')
        GL.glUniform1fv(a_length, 1, 0.05)
        bck_col = GL.glGetUniformLocation(program, 'alias_color')
        GL.glUniform3fv(bck_col, 1, self.bckgrnd_color[:3])
    
    def _safe_frame_exchange (self, visObj):
        """ Function doc 
        
        This function checks if the number of the called frame will not exceed 
        the limit of frames that each object has. Allowing two objects with 
        different trajectory sizes to be manipulated at the same time within the 
        glArea
        
        """
        if self.frame <  0:
            self.frame = 0
        else:
            pass
        
        if self.frame >= (len (visObj.frames)-1):
            #print (type(self.frame),self.frame,  type(len (visObj.frames)-1),len (visObj.frames)-1)
            frame = visObj.frames[len (visObj.frames)-2]
            #position = len (visObj.frames)-1
            #frame2 = visObj.frames[position-1]
            #print (type(frame), type(frame2), position)

        else:
            frame = visObj.frames[self.frame]
            #position = len (visObj.frames)-1
            #frame2 = visObj.frames[position-1]
            #print (type(frame), type(frame2), position)
        
        return frame

    def _get_visObj_frame (self, visObj):
        """ Function doc """
        if self.frame <  0:
            self.frame = 0
        else:
            pass
        
        if self.frame >= (len (visObj.frames)-1):
            frame = len (visObj.frames)-2
        else:
            frame = self.frame
        return frame
















    def _draw_picking_dots(self, visObj = None,  indexes = False):  # not used !!!
        """ Function doc
        """
        #print (100/abs(self.dist_cam_zrp))
        GL.glPointSize(100/abs(self.dist_cam_zrp))
        if visObj.picking_dots_vao is not None:
            GL.glBindVertexArray(visObj.picking_dots_vao)
            
            if self.modified_view:
                pass
            #    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, visObj.dot_buffers[0])
            #    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, visObj.dot_indexes.itemsize*int(len(visObj.dot_indexes)), visObj.dot_indexes, GL.GL_DYNAMIC_DRAW)
            #    GL.glDrawElements(GL.GL_POINTS, int(len(visObj.dot_indexes)), GL.GL_UNSIGNED_INT, None)
            #    GL.glBindVertexArray(0)
            #    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
            #    self.modified_view = False
            else:
                frame = self._safe_frame_exchange(visObj)

                GL.glBindBuffer(GL.GL_ARRAY_BUFFER, visObj.picking_dot_buffers[1])
                GL.glBufferData(GL.GL_ARRAY_BUFFER, frame.itemsize*int(len(frame)), 
                                frame, GL.GL_STATIC_DRAW)
                if indexes:
                    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, visObj.picking_dot_buffers[2])
                    GL.glBufferData(GL.GL_ARRAY_BUFFER, visObj.color_indexes.itemsize*int(len(visObj.color_indexes)), visObj.color_indexes, GL.GL_STATIC_DRAW)
                GL.glDrawElements(GL.GL_POINTS, int(len(visObj.index_bonds)), GL.GL_UNSIGNED_INT, None)
        GL.glBindVertexArray(0)
    

    
    def _draw_freetype(self, visObj = None):
        """ Function doc """
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glUseProgram(self.freetype_program)
        visObj.vm_font.load_matrices(self.freetype_program, self.glcamera.view_matrix, self.glcamera.projection_matrix)
        visObj.vm_font.load_font_params(self.freetype_program)
        GL.glBindVertexArray(visObj.vm_font.vao)
        texto = visObj.name
        point = np.array(visObj.mass_center,np.float32)
        point = np.array((point[0],point[1],point[2],1),np.float32)
        point = np.dot(point, visObj.model_mat)
        GL.glBindTexture(GL.GL_TEXTURE_2D, visObj.vm_font.texture_id)
        for i,c in enumerate(texto):
            c_id = ord(c)
            x = c_id%16
            y = c_id//16-2
            xyz_pos = np.array([point[0]+i*visObj.vm_font.char_width, point[1], point[2]],np.float32)
            uv_coords = np.array([x*visObj.vm_font.text_u, y*visObj.vm_font.text_v, (x+1)*visObj.vm_font.text_u, (y+1)*visObj.vm_font.text_v],np.float32)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, visObj.vm_font.vbos[0])
            GL.glBufferData(GL.GL_ARRAY_BUFFER, xyz_pos.itemsize*len(xyz_pos), xyz_pos, GL.GL_DYNAMIC_DRAW)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, visObj.vm_font.vbos[1])
            GL.glBufferData(GL.GL_ARRAY_BUFFER, uv_coords.itemsize*len(uv_coords), uv_coords, GL.GL_DYNAMIC_DRAW)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
            GL.glDrawArrays(GL.GL_POINTS, 0, 1)
        GL.glDisable(GL.GL_BLEND)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)

    
    
    
    def _draw_gizmo_axis(self, flag):
        """ Drawing method for the gizmo axis, see the glaxis.py documentation
            for more details about this function.
        """
        self.axis._draw_gizmo_axis(flag)
    
    def _draw_selection_box(self):
        """ Drawing method for the selection box, see the selection_box.py
            documentation for more details about this function.
        """
        self.selection_box._draw_selection_box()
    
    def _pressed_Control_L(self):
        """ Function doc
        """
        #self.vismolSession._hide_lines (visObj = self.vismolSession.vismol_objects[0], 
        #                               indexes = range(0,20))
        self.ctrl = True
        return True
    
    def _released_Control_L(self):
        """ Function doc
        """
        self.ctrl = False
        return True
    
    def _pressed_Shift_L(self):
        """ Function doc
        """
        #self.vismolSession._show_lines (visObj = self.vismolSession.vismol_objects[0], 
        #                               indexes = range(0,20))
        self.shift = True
        return True
    
    def _released_Shift_L(self):
        """ Function doc
        """
        self.shift = False
        return True
    
    def get_viewport_pos(self, x, y):
        """ Function doc """
        px = (2.0*x - self.width)/self.width
        py = (2.0*y - self.height)/self.height
        return [px, -py]
    
    def pos(self, x, y):
        """
        Use the ortho projection and viewport information
        to map from mouse co-ordinates back into world
        co-ordinates
        """
        px = x/self.width
        py = y/self.height
        px = self.left + px*(self.right-self.left)
        py = self.top + py*(self.bottom-self.top)
        pz = self.glcamera.z_near
        return px, py, pz
    
    def center_on_atom(self, atom):
        """ Function doc
        """
        frame_index  =  self._get_visObj_frame(atom.Vobject)
        self.center_on_coordinates(atom.Vobject, atom.coords(frame_index))
        return True
    
    def center_on_coordinates(self, vismol_object, atom_pos):
        """ Takes the coordinates of an atom in absolute coordinates and first
            transforms them in 4D world coordinates, then takes the unit vector
            of that atom position to generate the loop animation. To generate
            the animation, first obtains the distance from the zero reference
            point (always 0,0,0) to the atom, then divides this distance in a
            defined number of cycles, this result will be the step for
            translation. For the translation, the world will move a number of
            steps defined, and every new point will be finded by multiplying the
            unit vector by the step. As a final step, to avoid biases, the world
            will be translated to the atom position in world coordinates.
            The effects will be applied on the model matrices of every VisMol
            object and the model matrix of the window.
        """
        if self.zero_reference_point[0]!=atom_pos[0] or self.zero_reference_point[1]!=atom_pos[1] or self.zero_reference_point[2]!=atom_pos[2]:
            import time
            self.zero_reference_point = atom_pos
            pos = np.array([atom_pos[0],atom_pos[1],atom_pos[2],1],dtype=np.float32)
            model_pos = vismol_object.model_mat.T.dot(pos)[:3]
            self.model_mat = mop.my_glTranslatef(self.model_mat, -model_pos)
            unit_vec = op.unit_vector(model_pos)
            dist = op.get_euclidean(model_pos, [0.0,0.0,0.0])
            step = dist/15.0
            for i in range(15):
                to_move = unit_vec * step
                for visObj in self.vismolSession.vismol_objects:
                    visObj.model_mat = mop.my_glTranslatef(visObj.model_mat, -to_move)
                # WARNING: Method only works with GTK!!!
                self.parent_widget.get_window().invalidate_rect(None, False)
                self.parent_widget.get_window().process_updates(False)
                # WARNING: Method only works with GTK!!!
                time.sleep(self.vConfig.gl_parameters['center_on_coord_sleep_time'])
            for visObj in self.vismolSession.vismol_objects:
                model_pos = visObj.model_mat.T.dot(pos)[:3]
                visObj.model_mat = mop.my_glTranslatef(visObj.model_mat, -model_pos)
            self.queue_draw()
        return True
    
    def _print_matrices(self):
        """ Function doc
        """
        print(self.model_mat,"<== widget model_mat")
        for visObj in self.vismolSession.vismol_objects:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print(visObj.model_mat,"<== visObj model_mat")
    
    def queue_draw(self):
        """ Function doc """
        self.parent_widget.queue_draw()
    





#    def _draw_dots(self, visObj = None,  color_indexes = False):
#        """ Function doc"""
#        #indexes  = np.array(indexes, dtype=np.uint32)
#
#
#
#        GL.glPointSize(200/abs(self.dist_cam_zrp))
#
#        GL.glEnable(GL.GL_DEPTH_TEST)
#        GL.glUseProgram(self.dots_program)
#        GL.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
#        self.load_matrices(self.dots_program, visObj.model_mat)
#        self.load_fog(self.dots_program)
#        self.load_dot_params(self.dots_program)
#        
#        
#        if visObj.dots_vao is not None:
#            GL.glBindVertexArray(visObj.dots_vao)
#            if self.modified_view:
#                pass
#            #    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, visObj.dot_buffers[0])
#            #    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, visObj.dot_indexes.itemsize*int(len(visObj.dot_indexes)), visObj.dot_indexes, GL.GL_DYNAMIC_DRAW)
#            #    GL.glDrawElements(GL.GL_POINTS, int(len(visObj.dot_indexes)), GL.GL_UNSIGNED_INT, None)
#            #    GL.glBindVertexArray(0)
#            #    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
#            #    self.modified_view = False
#            else:
#                frame = self._safe_frame_exchange(visObj)
#
#                GL.glBindBuffer(GL.GL_ARRAY_BUFFER, visObj.dots_buffers[1])
#                GL.glBufferData(GL.GL_ARRAY_BUFFER,
#                    frame.nbytes,
#                    frame,
#                    GL.GL_STATIC_DRAW)
#
#                if  color_indexes:
#                    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, visObj.dots_buffers[2])
#                    GL.glBufferData(GL.GL_ARRAY_BUFFER, 
#                            visObj.color_indexes.itemsize*int(len(visObj.color_indexes)), 
#                            visObj.color_indexes, 
#                            GL.GL_STATIC_DRAW)
#            
#        GL.glDrawElements(GL.GL_POINTS, int(len(visObj.index_bonds)), GL.GL_UNSIGNED_INT, None)
#        GL.glBindVertexArray(0)
#        GL.glDisable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
#        GL.glUseProgram(0)
#        GL.glDisable(GL.GL_DEPTH_TEST)
#
#    def _draw_sphere_dots (self, visObj = None, indexes = False):
#        """ Function doc """
#        GL.glEnable(GL.GL_DEPTH_TEST)
#        GL.glUseProgram(self.spheres_dots_program)
#        #GL.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
#        self.load_matrices(self.spheres_dots_program, visObj.model_mat)
#        #self.load_fog(self.spheres_dots_program)
#        #self.load_dot_params(self.dots_program)
#        #print('linha1070')
#        
#        if visObj.sphere_dots_vao is not None:
#            GL.glBindVertexArray(visObj.sphere_dots_vao)
#            if self.modified_view:
#                pass
#            #    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, visObj.dot_buffers[0])
#            #    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, visObj.dot_indexes.itemsize*int(len(visObj.dot_indexes)), visObj.dot_indexes, GL.GL_DYNAMIC_DRAW)
#            #    GL.glDrawElements(GL.GL_POINTS, int(len(visObj.dot_indexes)), GL.GL_UNSIGNED_INT, None)
#            #    GL.glBindVertexArray(0)
#            #    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
#            #    self.modified_view = False
#            else:
#                frame = self._safe_frame_exchange(visObj)
#                print ('linha 1083')
#                GL.glBindBuffer(GL.GL_ARRAY_BUFFER, visObj.sphere_dots_buffers[1])
#                GL.glBufferData(GL.GL_ARRAY_BUFFER,
#                    frame.nbytes,
#                    frame,
#                    GL.GL_STATIC_DRAW)
#                    
#                GL.glDrawElements(GL.GL_POINTS, int(len(visObj.index_dots)), GL.GL_UNSIGNED_INT, None)
#                #GL.glDrawElements(GL.GL_POINTS, int(len(visObj.index_bonds)), GL.GL_UNSIGNED_INT, None)
#                #if  color_indexes:
#                #    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, sphere_dots_buffers.dot_buffers[2])
#                #    GL.glBufferData(GL.GL_ARRAY_BUFFER, 
#                #            visObj.color_indexes.itemsize*int(len(visObj.color_indexes)), 
#                #            visObj.color_indexes, 
#                #            GL.GL_STATIC_DRAW)
#            
#        #GL.glDrawElements(GL.GL_POINTS, int(len(visObj.index_bonds)), GL.GL_UNSIGNED_INT, None)
#        #GL.glBindVertexArray(0)
#        #GL.glDisable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
#        GL.glUseProgram(0)
#        GL.glDisable(GL.GL_DEPTH_TEST)


    
#    def _draw_sel_dots(self, visObj = None,  indexes = False):
#        """ Function doc
#        """
#        GL.glEnable(GL.GL_DEPTH_TEST)
#        GL.glUseProgram(self.sel_dots_program)
#        GL.glEnable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
#        self.load_matrices(self.sel_dots_program, visObj.model_mat)
#        self.load_dot_params(self.sel_dots_program)
#        if visObj.sel_dots_vao is not None:
#            GL.glBindVertexArray(visObj.sel_dots_vao)
#            if self.modified_view:
#                pass
#            else:
#                frame = self._safe_frame_exchange(visObj)
#                GL.glBindBuffer(GL.GL_ARRAY_BUFFER, visObj.sel_dots_buffers[1])
#                GL.glBufferData(GL.GL_ARRAY_BUFFER,
#                    frame.nbytes,
#                    frame,
#                    GL.GL_STATIC_DRAW)
#
#                GL.glDrawElements(GL.GL_POINTS, int(len(visObj.index_bonds)), GL.GL_UNSIGNED_INT, None)
#        GL.glBindVertexArray(0)
#        GL.glDisable(GL.GL_VERTEX_PROGRAM_POINT_SIZE)
#        GL.glUseProgram(0)
#        GL.glDisable(GL.GL_DEPTH_TEST)
#    
#   def _draw_sel_dots_surface(self, visObj = None,  indexes = False):
#       """ Function doc
#       """
#       GL.glEnable(GL.GL_DEPTH_TEST)
#       GL.glUseProgram(self.sel_dots_surface_program)
#       self.load_matrices(self.sel_dots_surface_program, visObj.model_mat)
#       GL.glPointSize(15)
#       if visObj.sel_dots_surface_vao is not None:
#           GL.glBindVertexArray(visObj.sel_dots_surface_vao)
#           if self.modified_view:
#               pass
#           else:
#               frame = self._safe_frame_exchange(visObj)
#               GL.glBindBuffer(GL.GL_ARRAY_BUFFER, visObj.sel_dots_surface_buffers[1])
#               GL.glBufferData(GL.GL_ARRAY_BUFFER, frame.nbytes, 
#                                                   frame, GL.GL_STATIC_DRAW)
#               GL.glDrawElements(GL.GL_POINTS, int(len(visObj.index_bonds)), GL.GL_UNSIGNED_INT, None)
#       GL.glPointSize(1)
#       GL.glBindVertexArray(0)
#       GL.glUseProgram(0)
#       GL.glDisable(GL.GL_DEPTH_TEST)
#   
#   def _draw_sel_spheres(self, visObj = None,  indexes = False):
#       """ Function doc
#       """
#       GL.glEnable(GL.GL_DEPTH_TEST)
#       GL.glUseProgram(self.sel_spheres_program)
#       self.load_matrices(self.sel_spheres_program, visObj.model_mat)
#       if visObj.sphere_rep.sel_spheres_vao is not None:
#           GL.glBindVertexArray(visObj.sphere_rep.sel_spheres_vao)
#           if self.modified_view:
#               pass
#           
#           else:
#               frame = self._safe_frame_exchange(visObj)
#               GL.glBindBuffer(GL.GL_ARRAY_BUFFER, visObj.sphere_rep.sel_spheres_buffers[1])
#               GL.glBufferData(GL.GL_ARRAY_BUFFER, visObj.sphere_rep.sel_coords.itemsize*int(len(visObj.sphere_rep.sel_coords)), 
#                                                   visObj.sphere_rep.sel_coords, GL.GL_STATIC_DRAW)
#               GL.glDrawElements(GL.GL_TRIANGLES, visObj.sphere_rep.sel_triangles, GL.GL_UNSIGNED_INT, None)
#       GL.glBindVertexArray(0)
#       GL.glUseProgram(0)
#       GL.glDisable(GL.GL_DEPTH_TEST)
#   
#   

#   def _draw_spheres(self, visObj = None,  indexes = False):
#       """ Function doc
#       """
#       GL.glEnable(GL.GL_DEPTH_TEST)
#       GL.glEnable(GL.GL_CULL_FACE)
#       GL.glCullFace(GL.GL_BACK)
#       GL.glUseProgram(self.spheres_program)
#       self.load_matrices(self.spheres_program, visObj.model_mat)
#       self.load_lights(self.spheres_program)
#       self.load_fog(self.spheres_program)
#       if visObj.sphere_rep.spheres_vao is not None:
#           GL.glBindVertexArray(visObj.sphere_rep.spheres_vao)
#           if self.modified_view:
#               pass
#           
#           else:
#               frame = self._safe_frame_exchange(visObj)
#
#               GL.glBindBuffer(GL.GL_ARRAY_BUFFER, visObj.sphere_rep.spheres_buffers[1])
#               GL.glBufferData(GL.GL_ARRAY_BUFFER, visObj.sphere_rep.coords.itemsize*int(len(visObj.sphere_rep.coords)), 
#                                                   visObj.sphere_rep.coords, GL.GL_STATIC_DRAW)
#               
#               #if  indexes:
#               #    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, visObj.spheres_buffers[2])
#               #    GL.glBufferData(GL.GL_ARRAY_BUFFER, visObj.color_indexes.itemsize*int(len(visObj.color_indexes)), visObj.color_indexes, GL.GL_STATIC_DRAW)
#               
#               GL.glDrawElements(GL.GL_TRIANGLES, visObj.sphere_rep.triangles, GL.GL_UNSIGNED_INT, None)
#       GL.glBindVertexArray(0)
#       GL.glUseProgram(0)
#       GL.glDisable(GL.GL_DEPTH_TEST)
#   
#   def _draw_dots_surface(self, visObj = None,  indexes = False):
#       """ Function doc
#       """
#       #'''
#       GL.glEnable(GL.GL_DEPTH_TEST)
#       GL.glUseProgram(self.dots_surface_program)
#       self.load_matrices(self.dots_surface_program, visObj.model_mat)
#       self.load_fog(self.dots_surface_program)
#       #self.load_lights(self.dots_surface_program)
#       GL.glPointSize(1)
#       if visObj.dots_surface_vao is not None:
#           GL.glBindVertexArray(visObj.dots_surface_vao)
#           if self.modified_view:
#               pass
#           else:
#               frame = self._safe_frame_exchange(visObj)
#               GL.glBindBuffer(GL.GL_ARRAY_BUFFER, visObj.dots_surface_buffers[1])
#               GL.glBufferData(GL.GL_ARRAY_BUFFER, frame.itemsize*int(len(frame)), 
#                                                   frame, GL.GL_STATIC_DRAW)
#               if  indexes:
#                   GL.glBindBuffer(GL.GL_ARRAY_BUFFER, visObj.dots_surface_buffers[2])
#                   GL.glBufferData(GL.GL_ARRAY_BUFFER, visObj.color_indexes.itemsize*int(len(visObj.color_indexes)), visObj.color_indexes, GL.GL_STATIC_DRAW)
#               GL.glDrawElements(GL.GL_POINTS, int(len(visObj.index_bonds)), GL.GL_UNSIGNED_INT, None)
#               #GL.glDrawElements(GL.GL_LINES, int(len(visObj.index_bonds)), GL.GL_UNSIGNED_INT, None)
#       GL.glPointSize(1)
#       GL.glBindVertexArray(0)
#       GL.glUseProgram(0)
#       GL.glDisable(GL.GL_DEPTH_TEST)
#
#
#
#    def _draw_ribbons(self, visObj = None):
#        """ Function doc
#        """
#        GL.glEnable(GL.GL_DEPTH_TEST)
#        #GL.glEnable(GL.GL_BLEND)
#        #GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
#        #GL.glEnable(GL.GL_LINE_SMOOTH)
#        #GL.glHint(GL.GL_LINE_SMOOTH_HINT, GL.GL_NICEST)
#        GL.glUseProgram(self.lines_program)
#        
#        
#        #GL.glLineWidth(self.vismolSession.gl_parameters['line_width']*80/abs(self.dist_cam_zrp))
#        GL.glLineWidth(800/abs(self.dist_cam_zrp))
#
#        
#        self.load_matrices(self.lines_program, visObj.model_mat)
#        self.load_fog(self.lines_program)
#        #self.load_antialias_params(self.lines_program)
#        if visObj.lines_vao is not None:
#            GL.glBindVertexArray(visObj.ribbons_vao)
#            if self.modified_view:
#                pass
#       
#            else:
#                #coord_vbo = GL.glGenBuffers(1)
#                frame = self._safe_frame_exchange(visObj)
#
#                GL.glBindBuffer(GL.GL_ARRAY_BUFFER, visObj.ribbons_buffers[1])
#                GL.glBufferData(GL.GL_ARRAY_BUFFER, frame.itemsize*int(len(frame)), 
#                                frame, 
#                                GL.GL_STATIC_DRAW)              
#                #GL.glDrawElements(GL.GL_LINES, int(len(visObj.index_bonds)*2), GL.GL_UNSIGNED_INT, None)
#                GL.glDrawElements(GL.GL_LINES, int(len(visObj.ribbons_Calpha_indexes_rep)*2), GL.GL_UNSIGNED_INT, None)
#        GL.glBindVertexArray(0)
#        GL.glLineWidth(1)
#        GL.glUseProgram(0)
#
#        GL.glDisable(GL.GL_DEPTH_TEST)#
#
#
#
#
#
#
