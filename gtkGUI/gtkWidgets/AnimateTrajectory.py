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



class AnimatedWindow:
    """ Class doc """
    
    def __init__ (self, main_window):
        """ Class initialiser """
        self.actived =  False
        self.main_window = main_window
        #self.EMSession =  GTKSession.EMSession
    def open_window (self, text = None):
        """ Function doc """
        if self.actived  ==  False:
            self.builder = Gtk.Builder()
            self.builder.add_from_file('gtkGUI/gtkWidgets/AnimateTrajectory.glade')
            
            self.window = self.builder.get_object('animate_window')
            self.builder.connect_signals(self)
            
            self.window.show_all()
            self.window.set_keep_above (self.window)

            scale = self.builder.get_object("scale1")  
            scale.set_range(1, 1000)                               
            scale.set_increments(1, 10)                           
            actual_frame = int(self.main_window.vismolSession.get_frame())
            scale.set_digits(1)

            scale.set_digits(actual_frame)                        
            #gtk.main()
    def on_TrajectoryTool_HSCALE_update (self, MIN = 1, MAX = 100):
        """ Function doc """
        #MAX  = int(self.builder.get_object('trajectory_max_entrey').get_text())
        #MIN  = int(self.builder.get_object('trajectory_min_entrey').get_text())

        scale = self.builder.get_object("scale1")
        scale.set_range(MIN, MAX)
        scale.set_increments(1, 10)
        scale.set_digits(1)
    
    def on_TrajectoryTool_BarSetFrame(self, hscale, text= None,  data=None):            # SETUP  trajectory window
        valor = hscale.get_value()
	
        if self.main_window.vismolSession != None:
            self.main_window.vismolSession.set_frame(int(valor-1))
            #self.main_window.vismolSession.glwidget.queue_draw()
        else:
            print (valor)

    def on_animate_trajectory_window_destroy(self, widget):
        """ Function doc """
        self.actived  =  False
        self.main_window.builder.get_object('toolbutton_trajectory_tool').set_active(False)

