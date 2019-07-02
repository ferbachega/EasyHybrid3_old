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



class ConsoleWindow:
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
            self.builder.add_from_file('gtkGUI/gtkWidgets/console.glade')
            self.window = self.builder.get_object('console_window')
            
            textarea = self.builder.get_object('textview1')
            textarea.connect('key-press-event', self.on_key_pressed)
            self.textbuffer = textarea.get_buffer()
            self.textbuffer.set_text('>>>')
            
            
            
            self.builder.connect_signals(self)
            self.window.show_all()
            self.window.set_keep_above (self.window)
    
    def on_console_window_destroy(self, widget):
        """ Function doc """
        self.actived  =  False
        self.main_window.builder.get_object('toolbutton1').set_active(False)

    def on_key_pressed (self,  widget, event):
        """ Function doc """
        if event.keyval == Gdk.keyval_from_name('Return'):
            start = self.textbuffer.get_iter_at_line(0)
            lineend = start.get_chars_in_line()
            end = self.textbuffer.get_end_iter()
            source = self.textbuffer.get_text(start, end, False)
            print (source)
