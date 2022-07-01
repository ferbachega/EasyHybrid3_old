#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  easyhybrid_pDynamo_selection.py
#  
#  Copyright 2022 Fernando <fernando@winter>
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
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
#from GTKGUI.gtkWidgets.filechooser import FileChooser
#from easyhybrid.pDynamoMethods.pDynamo2Vismol import *
import gc
import os

VISMOL_HOME = os.environ.get('VISMOL_HOME')
HOME        = os.environ.get('HOME')





class MergeSystemsWindow(Gtk.Window):
    """ Class doc """
    
    def OpenWindow (self):
        """ Function doc """
        if self.Visible  ==  False:
            self.builder = Gtk.Builder()
            self.builder.add_from_file(os.path.join(VISMOL_HOME,'easyhybrid/gui/merge_systems.glade'))
            self.builder.connect_signals(self)
            
            self.window = self.builder.get_object('Merge_systems_window')
            self.box1   = self.builder.get_object('box1')
            self.box2   = self.builder.get_object('box2')
            self.entry  = self.builder.get_object('merge_entry')
            '''--------------------------------------------------------------------------------------------'''
            self.system_type_store = Gtk.ListStore(int, str)
            
            for index, system in self.easyhybrid_main.p_session.systems.items():
                
                name  = "{} {}".format(index, system['name'] )
                print(name)
                #name = 'teste'
                self.system_type_store.append([index, name])
           
            
            self.combo1 = Gtk.ComboBox.new_with_model(self.system_type_store)
            self.combo2 = Gtk.ComboBox.new_with_model(self.system_type_store)
            
            self.box1.pack_start(self.combo1, True, True, 0)
            self.box2.pack_start(self.combo2, True, True, 0)

            
            renderer_text = Gtk.CellRendererText()
            self.combo1.pack_start(renderer_text, True)
            self.combo1.add_attribute(renderer_text, "text", 1)
            
            renderer_text = Gtk.CellRendererText()
            self.combo2.pack_start(renderer_text, True)
            self.combo2.add_attribute(renderer_text, "text", 1)
            '''--------------------------------------------------------------------------------------------'''

            
            self.window.show_all()                                               
            self.builder.connect_signals(self)                                   

            self.Visible  =  True
            #----------------------------------------------------------------
    
    def ok_button (self, button):
        """ Function doc """
        print(button)
        print(self.combo1.get_active())
        print(self.combo1.get_active_id())
        print(self.combo1.get_active_iter())
        print(self.combo2.get_active())
        
        name1 = None
        name2 = None
        
        tree_iter = self.combo1.get_active_iter()
        if tree_iter is not None:
            model    = self.combo1.get_model()
            name1    = model[tree_iter][1]
            index1   = model[tree_iter][0]
            print("Selected: system =%s" % index1, name1)
        
        tree_iter = self.combo2.get_active_iter()
        if tree_iter is not None:
            model    = self.combo2.get_model()
            name2    = model[tree_iter][1]
            index2   = model[tree_iter][0]
            print("Selected: system =%s" % index2, name2)
        
        
        new_system_label = self.entry.get_text()
        
        
        if index2 != index1 and name1 is not None and name2 is not None:
            
            
            system1 = self.easyhybrid_main.p_session.systems[index1]['system']
            system2 = self.easyhybrid_main.p_session.systems[index2]['system']
            system1.Summary()
            system2.Summary()
            print(system1)
            print(system2)
            self.easyhybrid_main.p_session.merge_systems (system1 = system1, 
                                                                system2 = system2, 
                                                                label   = 'Merged System', 
                                                                summary = True)
            
            
            
            
            
        
        
        
    
    
    
    def CloseWindow (self, button, data  = None):
        """ Function doc """
        self.window.destroy()
        self.Visible    =  False
    
    def __init__(self, main = None):
        """ Class initialiser """
        self.easyhybrid_main     = main
        self.Visible             =  False        
        

