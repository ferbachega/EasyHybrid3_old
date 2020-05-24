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
import VISMOL.glCore.VisMolWidget as vismol_widget
#import VISMOL.glCore.shapes as shapes
#import VISMOL.glCore.glaxis as glaxis
#import VISMOL.glCore.glcamera as cam
#import VISMOL.glCore.operations as op
#import VISMOL.glCore.sphere_data as sph_d
#import VISMOL.glCore.vismol_shaders as vm_shader
#import VISMOL.glCore.matrix_operations as mop

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import OpenGL
from OpenGL import GLU
from OpenGL import GL
from OpenGL.GL import shaders


class GLMenu:
    """ Class doc """
    def __init__ (self, glWidget):
        """ Class initialiser """
        xml = '''
<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated with glade 3.22.1 -->
<interface>
  <requires lib="gtk+" version="3.20"/>
  <object class="GtkMenu" id="menu1">
    <property name="visible">True</property>
    <property name="can_focus">False</property>
    <child>
      <object class="GtkMenuItem" id="menuItem1">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="label" translatable="yes">__glade_unnamed_2</property>
        <property name="use_underline">True</property>
      </object>
    </child>
  </object>
        '''
        self.builder = Gtk.Builder()
        self.builder.add_from_string(xml)
        #self.builder.connect_signals(self)
        #self.glWidget = glWidget

        #self.menuzao = Gtk.Menu()
        self.menuzao = self.builder.get_object('menu1')
        
        self.file_new  = Gtk.MenuItem("New")
        self.file_open = Gtk.MenuItem("Open")
        self.file_exit = Gtk.MenuItem("Exit")
        self.builder.get_object('menuItem1').set_label('Tche!!')
        
        #self.builder.get_object('menu1').append(self.file_new)
        self.menuzao.append(self.file_open)
        self.menuzao.append(Gtk.SeparatorMenuItem())
        self.menuzao.append(self.file_exit)
        

    
    def open_gl_menu(self, event = None):
        """ Function doc """
        
        # Check if right mouse button was preseed
        if event.button == 3:
        
        #self.popup.popup(None, None, None, None, event.button, event.time)
        #return True # event has been handled        
            print('clickei no menu2')
            widget = self.menuzao#.get_object('menu1')
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
            


class GLMenu2:
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
            

class GtkGLWidget(Gtk.GLArea):
    """ Object that contains the GLArea from GTK3+.
        It needs a vertex and shader to be created, maybe later I'll
        add a function to change the shaders.
    """
    
    def __init__(self, vismolSession = None, width=640, height=420):
        """ Constructor of the class, needs two String objects,
            the vertex and fragment shaders.
            
            Keyword arguments:
            vertex -- The vertex shader to be used (REQUIRED)
            fragment -- The fragment shader to be used (REQUIRED)
            
            Returns:
            A MyGLProgram object.
        """
        super(GtkGLWidget, self).__init__()
        self.connect("realize", self.initialize)
        self.connect("render", self.render)
        self.connect("resize", self.reshape)
        self.connect("key-press-event", self.key_pressed)
        self.connect("key-release-event", self.key_released)
        self.connect("button-press-event", self.mouse_pressed)
        self.connect("button-release-event", self.mouse_released)
        self.connect("motion-notify-event", self.mouse_motion)
        self.connect("scroll-event", self.mouse_scroll)
        #self.set_size_request(width, height)
        self.grab_focus()
        self.set_events( self.get_events() | Gdk.EventMask.SCROLL_MASK
                       | Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON_RELEASE_MASK
                       | Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.POINTER_MOTION_HINT_MASK
                       | Gdk.EventMask.KEY_PRESS_MASK | Gdk.EventMask.KEY_RELEASE_MASK )
        
        self.vm_widget = vismol_widget.VisMolWidget(self, vismolSession, np.float32(width), np.float32(height))
        self.vismolSession = vismolSession
        
        #self.glMenu = GLMenu(self)
    
    def build_glmenu (self, menu_items = None):
        """ Function doc """
        if menu_items:
            print('building a new glMenu, diferent from default')
        else:
            self.glMenu = GLMenu2(self)
            ##main_menu_bar = Gtk.MenuBar()
            ##self.gl_menu = self.glMenu.builder.get_object('menu1')
            ## Drop down menu
            #file_menu = Gtk.Menu()
            #file_menu_dropdown = Gtk.MenuItem("File")
            #
            ## File menu items
            #file_new = Gtk.MenuItem("New")
            #file_open = Gtk.MenuItem("Open")
            #file_exit = Gtk.MenuItem("Exit")
            #
            ## File button has dropdown
            ##self.gl_menu.set_submenu(file_menu)
            #
            ## Add menu items
            #self.gl_menu.append(file_new)
            #self.gl_menu.append(file_open)
            #self.gl_menu.append(Gtk.SeparatorMenuItem())
            #self.gl_menu.append(file_exit)
            #
            ## Add to main menu bar
            ##main_menu_bar.append(file_menu_dropdown)
            ##self.gl_menu.gl_menu.append()




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
            filename = self.vismolSession.main_session.filechooser.open()
            self.vismolSession.load(filename)
            #self.main_treeview.refresh_gtk_main_treeview()
            visObj = self.vismolSession.vismol_objects[-1]
            self.vismolSession.glwidget.vm_widget.center_on_coordinates(visObj, visObj.mass_center)

        if k_name == 'r':
            #self.vismolSession.show(_type = 'ball_and_stick', Vobjects =  [self.vismolSession.vismol_objects[-1]])
            visObj = self.vismolSession.vismol_objects[0]
            visObj.ribbons_actived =  True

        if k_name == 's':
            #self.vismolSession.show(_type = 'ball_and_stick', Vobjects =  [self.vismolSession.vismol_objects[-1]])
            visObj = self.vismolSession.vismol_objects[0]
            visObj.spheres_actived =  True

        if k_name == 't':
            #self.vismolSession.show(_type = 'ball_and_stick', Vobjects =  [self.vismolSession.vismol_objects[-1]])
            visObj = self.vismolSession.vismol_objects[0]
            visObj.sticks_actived =  True

        if k_name == 'period':
            #self.vismolSession.get_frame()
            frame = self.vismolSession.get_frame()+1
            self.vismolSession.set_frame(frame)
            print (frame)
        if k_name == 'comma':
            frame = self.vismolSession.get_frame()-1
            self.vismolSession.set_frame(frame)
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
    
    def mouse_scroll(self, widget, event):
        """ Function doc
        """
        if event.direction == Gdk.ScrollDirection.UP:
            self.vm_widget.mouse_scroll(1)
        if event.direction == Gdk.ScrollDirection.DOWN:
            self.vm_widget.mouse_scroll(-1)
    
