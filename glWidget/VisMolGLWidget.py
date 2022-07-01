#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  gtk3.py
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

import math
import numpy as np
import ctypes
import glCore.VisMolGLCore as vismol_widget
#import glCore.shapes as shapes
#import glCore.glaxis as glaxis
#import glCore.glcamera as cam
#import glCore.operations as op
#import glCore.sphere_data as sph_d
#import glCore.vismol_shaders as vm_shader
#import glCore.matrix_operations as mop

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import OpenGL
from OpenGL import GLU
from OpenGL import GL
from OpenGL.GL import shaders


class GLMenus2 :
    """ Class doc """
    def __init__ (self, glWidget, menu_items):
        
        
        #---------------------------------------------------------
        self.menu1 = Gtk.Menu()
        self.menu1_item_label          = Gtk.MenuItem('label'       )
        self.menu1_separator1         = Gtk.SeparatorMenuItem()
        self.menu1_item_eneble        = Gtk.MenuItem('enable'       )
        self.menu1_item_disable       = Gtk.MenuItem('disable'      )
        self.menu1_separator2         = Gtk.SeparatorMenuItem()
        self.menu1_item_delete_all    = Gtk.MenuItem('delete all'   )
        self.menu1_item_reinitialize  = Gtk.MenuItem('reinitialize' )
        #---------------------------------------------------------
        self.menu1.append(self.menu1_item_label       )
        self.menu1.append(self.menu1_separator1       )
        self.menu1.append(self.menu1_item_eneble      )
        self.menu1.append(self.menu1_item_disable     )
        self.menu1.append(self.menu1_separator2       )
        self.menu1.append(self.menu1_item_delete_all  )
        self.menu1.append(self.menu1_item_reinitialize)
        #---------------------------------------------------------
        
    
               
        



        #---------------------------------------------------------
        self.menu2 = Gtk.Menu()
        self.menu2_item_label         = Gtk.MenuItem('label')
        self.menu2_separator1         = Gtk.SeparatorMenuItem()
        self.menu2_item_atom          = Gtk.MenuItem('atom')
        self.menu2_item_residue       = Gtk.MenuItem('residue')
        self.menu2_item_chain         = Gtk.MenuItem('chain')
        self.menu2_separator2         = Gtk.SeparatorMenuItem()
        self.menu2_item_molecule      = Gtk.MenuItem('molecule')
        self.menu2_separator3         = Gtk.SeparatorMenuItem()
        #---------------------------------------------------------
        self.menu2.append(self.menu2_item_label   )
        self.menu2.append(self.menu2_separator1   )
        self.menu2.append(self.menu2_item_atom    )
        self.menu2.append(self.menu2_item_residue )
        self.menu2.append(self.menu2_item_chain   )
        self.menu2.append(self.menu2_separator2   )
        self.menu2.append(self.menu2_item_molecule)
        self.menu2.append(self.menu2_separator3   )
        #---------------------------------------------------------



        self.menu3 = Gtk.Menu()
        self.menu3_item_label = Gtk.MenuItem('label')
        for label in menu_items:
            mitem = Gtk.MenuItem(label)
            mitem.connect('activate', menu_items[label])
            self.glMenu.append(mitem)

   
        
    
    def build_glmenu (self, menu_items = None):
        """ Function doc """
        self.glMenu = Gtk.Menu()
        
        self.menu_header = Gtk.MenuItem('')
        #mitem.connect('activate', menu_items[label])
        self.glMenu.append(self.menu_header)
        
        for label in menu_items:
            mitem = Gtk.MenuItem(label)
            mitem.connect('activate', menu_items[label])
            self.glMenu.append(mitem)
			
        self.glMenu.show_all()
     


class GLMenu3:
    """ Class doc """
    def __init__ (self, glWidget):
        """ Class initialiser """
        xml = '''
<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated with glade 3.18.3 -->
<interface>
  <requires lib="gtk+" version="3.12"/>
  <object class="GtkMenu" id="menu1">
    <property name="visible">True</property>
    <property name="can_focus">False</property>
    <child>
      <object class="GtkMenuItem" id="menuitem1">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="label" translatable="yes">menuitem1</property>
        <property name="use_underline">True</property>
        <signal name="button-release-event" handler="menuItem_function" swapped="no"/>
      </object>
    </child>
    <child>
      <object class="GtkMenuItem" id="menuitem2">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="label" translatable="yes">menuitem2</property>
        <property name="use_underline">True</property>
        <child type="submenu">
          <object class="GtkMenu" id="menu2">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <child>
              <object class="GtkMenuItem" id="menuitem5">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">menuitem5</property>
                <property name="use_underline">True</property>
                <signal name="button-release-event" handler="menuItem_function" swapped="no"/>
              </object>
            </child>
          </object>
        </child>
      </object>
    </child>
    <child>
      <object class="GtkMenuItem" id="menuitem3">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="label" translatable="yes">menuitem3</property>
        <property name="use_underline">True</property>
        <child type="submenu">
          <object class="GtkMenu" id="menu3">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <child>
              <object class="GtkMenuItem" id="menuitem4">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">menuitem4</property>
                <property name="use_underline">True</property>
                <signal name="button-release-event" handler="menuItem_function" swapped="no"/>
              </object>
            </child>
          </object>
        </child>
      </object>
    </child>
    <child>
      <object class="GtkMenuItem" id="menuitem6">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="label" translatable="yes">menuitem6</property>
        <property name="use_underline">True</property>
        <signal name="button-release-event" handler="menuItem_function" swapped="no"/>
      </object>
    </child>
    <child>
      <object class="GtkMenuItem" id="menuitem7">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="label" translatable="yes">menuitem7</property>
        <property name="use_underline">True</property>
        <signal name="button-release-event" handler="menuItem_function" swapped="no"/>
      </object>
    </child>
    <child>
      <object class="GtkMenuItem" id="menuitem8">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="label" translatable="yes">menuitem8</property>
        <property name="use_underline">True</property>
        <signal name="button-release-event" handler="menuItem_function" swapped="no"/>
      </object>
    </child>
    <child>
      <object class="GtkMenuItem" id="menuitem9">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="label" translatable="yes">El Diablo</property>
        <property name="use_underline">True</property>
        <signal name="button-release-event" handler="menuItem_function" swapped="no"/>
      </object>
    </child>
  </object>
</interface>
        '''

        self.builder = Gtk.Builder()
        self.builder.add_from_string(xml)
        self.builder.connect_signals(self)
        self.glWidget = glWidget
    
    def open_gl_menu(self, event = None):
        """ Function doc """
        
        # Check if right mouse button was preseed
        if event.button == 3:
        
        #self.popup.popup(None, None, None, None, event.button, event.time)
        #return True # event has been handled        
            print('clickei no menu')
            widget = self.builder.get_object('menu1')
            widget.popup(None, None, None, None, event.button, event.time)        
            pass
    
    def menuItem_function (self, widget, data):
        """ Function doc """
        #print ('Charlitos, seu lindo')
        if widget == self.builder.get_object('menuitem1'):
            self.glWidget.test_hide()
        
        if widget == self.builder.get_object('menuitem4'):
            self.glWidget.test_show()
        
        if widget == self.builder.get_object('menuitem5'):
        
            print ('Charlitos, el diablo')
        
        if widget == self.builder.get_object('menuitem6'):
            print ('Charlitos, el locotto del Andes')
        
        if widget == self.builder.get_object('menuitem7'):
            print ('Charlitos, seu lindo2')
        
        if widget == self.builder.get_object('menuitem8'):
            print ('Charlitos, seu lindo3')
        
        if widget == self.builder.get_object('menuitem9'):
            print ('Charlitos, seu lindo4')
            

class GtkGLAreaWidget(Gtk.GLArea):
    """ Object that contains the GLArea from GTK3+.
        It needs a vertex and shader to be created, maybe later I'll
        add a function to change the shaders.
    """
    
    def __init__(self, vm_session = None, width=640, height=420):
        """ Constructor of the class, needs two String objects,
            the vertex and fragment shaders.
            
            Keyword arguments:
            vertex -- The vertex shader to be used (REQUIRED)
            fragment -- The fragment shader to be used (REQUIRED)
            
            Returns:
            A MyGLProgram object.
        """
        super(GtkGLAreaWidget, self).__init__()
        self.connect("realize", self.initialize)
        self.connect("render", self.render)
        self.connect("resize", self.reshape)
        self.connect("key-press-event", self.key_pressed)
        self.connect("key-release-event", self.key_released)
        self.connect("button-press-event", self.mouse_pressed)
        self.connect("button-release-event", self.mouse_released)
        self.connect("motion-notify-event", self.mouse_motion)
        self.connect("scroll-event", self.mouse_scroll)
        #self.set_size_request(600, 600)
        self.grab_focus()
        self.set_events( self.get_events() | Gdk.EventMask.SCROLL_MASK
                       | Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON_RELEASE_MASK
                       | Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.POINTER_MOTION_HINT_MASK
                       | Gdk.EventMask.KEY_PRESS_MASK | Gdk.EventMask.KEY_RELEASE_MASK )
        
        
        self.Vismol_Objects_ListStore         = Gtk.ListStore(bool,  # visible? 
                                                               str,  # id
                                                               str,  # name
                                                               str,  # num of atoms
                                                               str)  # num of frames
                                                               
        self.Vismol_selection_modes_ListStore = Gtk.ListStore(str)
        
        self.vm_widget = vismol_widget.VisMolGLCore(self, vm_session, np.float32(width), np.float32(height))
        self.vm_session = vm_session
        
        
        self.glMenu_sele = None
        self.glMenu_bg = None
        self.glMenu_obj = None
        #self.glMenu = GLMenu(self)

    
    def _ (_):
        """ Function doc """
        
    
    def build_submenus_from_dicts (self, menu_dict):
        """ Function doc """
        menu = Gtk.Menu()
        
        for key in menu_dict:
            mitem = Gtk.MenuItem(key)
            
            if menu_dict[key][0] == 'submenu':
                #print(key)
                menu2 = self.build_submenus_from_dicts (menu_dict[key][1])
                mitem.set_submenu(menu2)
            
            
            elif menu_dict[key][0] == 'separator':
                mitem = Gtk.SeparatorMenuItem()
                #menu2 = self.build_submenus_from_dicts (menu_dict[key][1])
                #mitem.set_submenu(menu2)
                #print(key)

            
            else:
                if menu_dict[key][1] != None:
                    mitem.connect('activate', menu_dict[key][1])
                else:
                    pass
            menu.append(mitem)
        
        return menu
        #menu.show_all()

    def build_glmenu_from_dicts (self, menu_dict, glMenu):
        """ Function doc """
        for key in menu_dict:
            mitem = Gtk.MenuItem(label = key)
            
            if menu_dict[key][0] == 'submenu':
                menu2 = self.build_submenus_from_dicts (menu_dict[key][1])
                mitem.set_submenu(menu2)
            
            elif menu_dict[key][0] == 'separator':
                mitem = Gtk.SeparatorMenuItem()
          
            else:
                if menu_dict[key][1] != None:
                    mitem.connect('activate', menu_dict[key][1])
                else:
                    pass
            glMenu.append(mitem) 

    def build_glmenu (self,  bg_menu  = None, sele_menu = None, obj_menu = None , pick_menu =  None):
        """ Function doc """

        #self.glMenu = Gtk.Menu()
        #
        #self.menu_header = Gtk.MenuItem('')
        ##mitem.connect('activate', menu_items[label])
        #self.glMenu.append(self.menu_header)
        #
        #for label in menu_items:
        #    mitem = Gtk.MenuItem(label)
        #    mitem.connect('activate', menu_items[label])
        #    self.glMenu.append(mitem)
		#	
        #
        #self.glMenu_show = Gtk.Menu()
        #self.menu_item1 = Gtk.MenuItem('test')
        #self.glMenu_show.append(self.menu_item1)
        #
        #
        #
        #self.menu_show = Gtk.MenuItem('show')
        #self.menu_show.set_submenu(self.glMenu_show)
        ##mitem.connect('activate', menu_items[label])
        #self.glMenu.append(self.menu_show)
        #    
        #    
        #self.glMenu.show_all()

        
        ''' Selection Menu '''
        # --------------------------------------------------------------- #
        if sele_menu:
            self.glMenu_sele           = Gtk.Menu()
            self.glMenu_sele_toplabel =  Gtk.MenuItem(label = 'selection')
            self.glMenu_sele.append (self.glMenu_sele_toplabel)
            
            self.build_glmenu_from_dicts( sele_menu, self.glMenu_sele)
           
            self.glMenu_sele.show_all()

        else:
            self.glMenu_sele = None
        # --------------------------------------------------------------- #
        
        ''' Picking Menu '''
        # --------------------------------------------------------------- #
        if pick_menu:
            self.glMenu_pick           = Gtk.Menu()
            self.glMenu_pick_toplabel =  Gtk.MenuItem(label = 'picking')
            self.glMenu_pick.append (self.glMenu_pick_toplabel)
            
            self.build_glmenu_from_dicts( pick_menu, self.glMenu_pick)
           
            self.glMenu_pick.show_all()

        else:
            self.glMenu_pick = None
        # --------------------------------------------------------------- #

        ''' Background Menu '''
        # --------------------------------------------------------------- #
        if bg_menu:
            self.glMenu_bg  = Gtk.Menu()
            self.glMenu_bg_toplabel =  Gtk.MenuItem(label = 'background')
            self.glMenu_bg.append (self.glMenu_bg_toplabel)

            self.build_glmenu_from_dicts( bg_menu, self.glMenu_bg)
            #self.glMenu_bg = self.build_submenus_from_dicts (bg_menu)
            self.glMenu_bg.show_all()
        else:
            self.glMenu_bg = None
        
        
        if obj_menu:
            self.glMenu_obj  = Gtk.Menu()
            self.glMenu_obj_toplabel =  Gtk.MenuItem(label = 'atom')
            self.glMenu_obj.append (self.glMenu_obj_toplabel)

            self.build_glmenu_from_dicts( obj_menu, self.glMenu_obj)
            self.glMenu_obj.show_all()
        else:
            self.glMenu_obj = None
            
     
    def show_gl_menu (self, signals = None, menu_type = None, info = None):
        """ Function doc """
        
        if menu_type == 'bg_menu':
            if self.glMenu_bg:
                self.glMenu_bg.popup(None, None, None, None, 0, 0)
        
        
        if menu_type == 'sele_menu':
            if self.glMenu_sele:
                self.glMenu_sele.popup(None, None, None, None, 0, 0)
        
        if menu_type == 'pick_menu':
            if self.glMenu_pick:
                self.glMenu_pick.popup(None, None, None, None, 0, 0)
        
        
        if menu_type == 'obj_menu':
            if self.glMenu_obj:
                self.glMenu_obj_toplabel.set_label(info)
                self.glMenu_obj.popup(None, None, None, None, 0, 0)
        
            
    def initialize(self, widget):
        """ Enables the buffers and other charasteristics of the OpenGL context.
            sets the initial projection and view matrix
            
            self.flag -- Needed to only create one OpenGL program, otherwise a bunch of
                         programs will be created and use system resources. If the OpenGL
                         program will be changed change this value to True
        """
        if self.get_error()!=None:
            print(self.get_error().args)
            print(self.get_error().code)
            print(self.get_error().domain)
            print(self.get_error().message)
            Gtk.main_quit()
        self.vm_widget.initialize()
    
    def reshape(self, widget, width, height):
        """ Resizing function, takes the widht and height of the widget
            and modifies the view in the camera acording to the new values
        
            Keyword arguments:
            widget -- The widget that is performing resizing
            width -- Actual width of the window
            height -- Actual height of the window
        """
        w = float(width)
        h = float(height)
        self.vm_widget.resize_window(w, h)
        self.queue_draw()
    
    def render(self, area, context):
        """ This is the function that will be called everytime the window
            needs to be re-drawed.
        """
        self.vm_widget.render()
    
    def key_pressed(self, widget, event):
        """ The mouse_button function serves, as the names states, to catch
        events in the keyboard, e.g. letter 'l' pressed, 'backslash'
        pressed. Note that there is a difference between 'A' and 'a'.
        Here I use a specific handler for each key pressed after
        discarding the CONTROL, ALT and SHIFT keys pressed (usefull
        for customized actions) and maintained, i.e. it's the same as
        using Ctrl+Z to undo an action.
        """
        k_name = Gdk.keyval_name(event.keyval)

        print(k_name)

        self.vm_widget.key_pressed(k_name)

        if k_name == 'l':
            filename = self.vm_session.main_session.filechooser.open()
            self.vm_session.load(filename)
            #self.main_treeview.refresh_gtk_main_treeview()
            vobject = self.vm_session.vobjects[-1]
            self.vm_session.glwidget.vm_widget.center_on_coordinates(vobject, vobject.mass_center)

        #if k_name == 'r':
        #    #self.vm_session.show(_type = 'ball_and_stick', vobjects =  [self.vm_session.vobjects[-1]])
        #    vobject = self.vm_session.vobjects[0]
        #    #vobject.ribbons_active =  True
        #    if vobject.ribbons_active:
        #        vobject.ribbons_active =  False
        #    else:
        #        vobject.ribbons_active =  True





        #if k_name == 'f':
        #    #self.vm_session.show(_type = 'ball_and_stick', vobjects =  [self.vm_session.vobjects[-1]])
        #    vobject = self.vm_session.vobjects[0]
        #    
        #    if vobject.spheres_ON_THE_FLY_active:
        #        vobject.spheres_ON_THE_FLY_active =  False
        #    else:
        #        vobject.spheres_ON_THE_FLY_active =  True
        #    #self.vm_session.show (_type = 'lines', vobjects =  [])




        #if k_name == 't':
        #    #self.vm_session.show(_type = 'ball_and_stick', vobjects =  [self.vm_session.vobjects[-1]])
        #    for vobject in self.vm_session.vobjects:
        #        
        #        if vobject.sticks_active:
        #            print (vobject.sticks_active)
        #            print("vobject.representations['sticks'].active =  True")
        #            vobject.representations['sticks'].active =  False
        #        else:
        #            print (vobject.sticks_active)
        #            indexes = np.array([0,1,0,2,1,2], dtype=np.uint32)
        #            vobject.representations['sticks'].indexes = indexes
        #            
        #            print("vobject.representations['sticks'].active =  False")
        #            vobject.representations['sticks'].active =  True

        #if k_name == 'd':
        #    self.vm_session.show(_type = 'dots', vobjects =  [self.vm_session.vobjects[-1]])
        #    #vobject = self.vm_session.vobjects[0]
        #    #vobject.dots_active =  True
        
        if k_name == 'v':
            #self.vm_session.show(_type = 'dots', vobjects =  [self.vm_session.vobjects[-1]])
            vobject = self.vm_session.vobjects[0]
            if vobject.dots_surface_active:
                vobject.dots_surface_active =  False
            else:
                vobject.dots_surface_active =  True


        if k_name == 'e':                             
            self.vm_session.show_or_hide( _type = 'spheres', show = True)
        if k_name == 'd':
            self.vm_session.show_or_hide( _type = 'spheres', show = False) 


        if k_name == 'w':                             
            self.vm_session.show_or_hide( _type = 'sticks', show = True)
        if k_name == 's':
            self.vm_session.show_or_hide( _type = 'sticks', show = False)     
        
        
        if k_name == 'q':
            self.vm_session.show_or_hide( _type = 'lines', show = True)    
        if k_name == 'a':
            self.vm_session.show_or_hide( _type = 'lines', show = False)


        if k_name == 'r':
            self.vm_session.show_or_hide( _type = 'dots', show = True)    
        if k_name == 'f':
            self.vm_session.show_or_hide( _type = 'dots', show = False)


       
        if k_name == 'z':
            #self.vm_session.glwidget._set_draw_dots_indexes (vobject = self.vm_session.vobjects[0],  indexes = False)

            # Associates selected bonds as false / true
            for atom in self.vm_session.selections[self.vm_session.current_selection].selected_atoms:
                #print (atom.name)
                for bond in atom.bonds:
                    bond.line_active = False

            # Build a list of the connections that are active -> this list will be sent to the openGL buffer
            for vobject in self.vm_session.selections[self.vm_session.current_selection].selected_objects:
                indexes_bonds = []
                
                for bonds in vobject.bonds:
                    if bonds.line_active:
                        indexes_bonds.append(bonds.atom_index_i)
                        indexes_bonds.append(bonds.atom_index_j)
                    else:
                        pass

                # When the list is [] we simply have to disable the display of the representation type
                if indexes_bonds == []:
                    #print('indexes_bonds == []')
                    vobject.lines_active  = False
                else:
                    #print('indexes_bonds ==', indexes_bonds)
                    vobject.representations['lines'].define_new_indexes_to_VBO(indexes_bonds)
                    #self.vm_widget.set_draw_lines_indexes (vobject = vobject,  show = False, input_indexes = indexes_bonds)

        if k_name == 'x':
            #self.vm_session.glwidget._set_draw_dots_indexes (vobject = self.vm_session.vobjects[0],  indexes = False)
            
            # Associates selected bonds as false / true
            for atom in self.vm_session.selections[self.vm_session.current_selection].selected_atoms:
                #print (atom.name)
                for bond in atom.bonds:
                    bond.stick_active = False

            # Build a list of the connections that are active -> this list will be sent to the openGL buffer
            for vobject in self.vm_session.selections[self.vm_session.current_selection].selected_objects:
                indexes_bonds = []
                
                for bond in vobject.bonds:
                    if bond.stick_active:
                        indexes_bonds.append(bond.atom_index_i)
                        indexes_bonds.append(bond.atom_index_j)
                    else:
                        pass
                
                # When the list is [] we simply have to disable the display of the representation type
                if indexes_bonds == []:
                    #print('indexes_bonds == []')
                    vobject.sticks_active  = False
                else:
                    #print('indexes_bonds ==', indexes_bonds)
                    vobject.representations['sticks'].define_new_indexes_to_VBO(indexes_bonds)





        if k_name == 'c':
            #self.vm_session.glwidget._set_draw_dots_indexes (vobject = self.vm_session.vobjects[0],  indexes = False)
            
            # Associates selected bonds as false / true
            for atom in self.vm_session.selections[self.vm_session.current_selection].selected_atoms:
                atom.nonbonded = False
                #print (atom.name)
                
            for vobject in self.vm_session.selections[self.vm_session.current_selection].selected_objects:
                indexes = []
                
                for atom in vobject.atoms:
                    if atom.nonbonded:
                        indexes.append(atom.index-1)
                    else:                   
                        pass
                
                # When the list is [] we simply have to disable the display of the representation type
                if indexes == []:
                    #print('indexes_bonds == []')
                    vobject.representations['nonbonded'].active = False
                else:
                    #print('indexes_bonds ==', indexes_bonds)
                    vobject.representations['nonbonded'].define_new_indexes_to_VBO(indexes)

        if k_name == 'b':
            #self.vm_session.glwidget._set_draw_dots_indexes (vobject = self.vm_session.vobjects[0],  indexes = False)
            
            # Associates selected bonds as false / true
            for atom in self.vm_session.selections[self.vm_session.current_selection].selected_atoms:
                atom.spheres = False
                #print (atom.name)
                
            for vobject in self.vm_session.selections[self.vm_session.current_selection].selected_objects:
                indexes = []
                
                for atom in vobject.atoms:
                    if atom.spheres:
                        indexes.append(atom.index-1)
                    else:                   
                        pass
                
                # When the list is [] we simply have to disable the display of the representation type
                if indexes == []:
                    #print('indexes_bonds == []')
                    vobject.representations['dots'].active = False
                else:
                    #print('indexes_bonds ==', indexes_bonds)
                    vobject.representations['dots'].define_new_indexes_to_VBO(indexes)
                    vobject.representations['spheres'].define_new_indexes_to_VBO(indexes)







        if k_name == 'period':
            #self.vm_session.get_frame()
            frame = self.vm_session.get_frame()+1
            self.vm_session.set_frame(frame)
            print (frame)
        if k_name == 'comma':
            frame = self.vm_session.get_frame()-1
            self.vm_session.set_frame(frame)
            print (frame)	
            
    def key_released(self, widget, event):
        """ Used to indicates a key has been released.
        """
        k_name = Gdk.keyval_name(event.keyval)
        self.vm_widget.key_released(k_name)
    
    def mouse_pressed(self, widget, event):
        """ Function doc
        """
        self.vm_widget.mouse_pressed(int(event.button), event.x, event.y)
        
    def mouse_released(self, widget, event):
        """ Function doc
        """
        #self.vm_widget.mouse_released(int(event.button), event.x, event.y)
        self.vm_widget.mouse_released(event, event.x, event.y)
        
    def mouse_motion(self, widget, event):
        """ Function doc
        """
        self.vm_widget.mouse_motion(event.x, event.y)
        #print('764', event.x, event.y)
        
        #GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)
        #pos = [event.x, event.y -  self.vm_widget.picking_y]
        ##print(self.mouse_x, self.mouse_y, pos)
        #data = GL.glReadPixels(pos[0], pos[1], 1, 1, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE)
        #
        ##converting RGB values to atoms address (unique id)
        #pickedID = data[0] + data[1] * 256 + data[2] * 256*256;
        #if self.vm_session._picking_selection_mode:
        #    print('_picking_selection_mode = True',data, pickedID)




    def mouse_scroll(self, widget, event):
        """ Function doc
        """
        if event.direction == Gdk.ScrollDirection.UP:
            self.vm_widget.mouse_scroll(1)
        if event.direction == Gdk.ScrollDirection.DOWN:
            self.vm_widget.mouse_scroll(-1)
    
