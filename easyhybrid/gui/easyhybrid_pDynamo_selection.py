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



#from GTKGUI.gtkWidgets.main_treeview import GtkMainTreeView
class PDynamoSelectionWindow:
    """ Class doc """
    def OpenWindow (self):
        """ Function doc """
        if self.Visible  ==  False:
            self.builder = Gtk.Builder()
            self.builder.add_from_file(os.path.join(VISMOL_HOME,'easyhybrid/gui/easyhybrid_pDynamo_selection.glade'))
            self.builder.connect_signals(self)
            
            self.window = self.builder.get_object('pdynamo_selection_window')
            self.window.set_title('pDynamo Selection Window')
            self.window.set_keep_above(True)
            
            #self.chain_entry  = self.builder.get_object('chain_entry')
            #self.resn_entry   = self.builder.get_object('resn_entry' )
            #self.resi_entry   = self.builder.get_object('resi_entry' )
            #self.atom_entry   = self.builder.get_object('atom_entry' )
            self.builder.get_object('chain_entry').set_text(str(self.chain) )
            self.builder.get_object('resn_entry' ).set_text(str(self.resn ) )
            self.builder.get_object('resi_entry' ).set_text(str(self.resi ) )
            self.builder.get_object('atom_entry' ).set_text(str(self.atom ) )
            
            
            self.box_combo_methods = self.builder.get_object('box_combo_methods')
            
            #self.self.method_combobox   = self.builder.get_object('self.method_combobox'   )
            #self.radius_spinbutton = self.builder.get_object('radius_spinbutton' )
            #self.action_combobox   = self.builder.get_object('action_combobox'   )

            method_store = Gtk.ListStore(str)
            method_store.append(["ByComponent"])
            method_store.append(["Complement"])
            method_store.append(["ByAtom"])


            #------------------------------------------------------------------
            self.method_combo = Gtk.ComboBox.new_with_model(method_store)
            renderer_text = Gtk.CellRendererText()
            self.method_combo.pack_start(renderer_text, True)
            self.method_combo.add_attribute(renderer_text, "text", 0)            
            
            self.method_combo.set_entry_text_column(0)
            self.method_combo.set_active(0)
            self.box_combo_methods.pack_start(self.method_combo, False, False, 0)
            #------------------------------------------------------------------

            
            
            
            
            self.radius_spinbutton  = self.builder.get_object('radius_spinbutton' )
            #------------------------------------------------------------------
            self.fps_adjustment = Gtk.Adjustment(value          = 24 , 
                                                 upper          = 100, 
                                                 step_increment = 1  , 
                                                 page_increment = 10 )

            self.radius_spinbutton.set_adjustment ( self.fps_adjustment)
            #------------------------------------------------------------------




            '''
            self.box_combo_action = self.builder.get_object('box_combo_action' )
            
            action_store = Gtk.ListStore(str)
            action_store.append(["ByComponent"])
            action_store.append(["Complement"])
            action_store.append(["ByLinearPolymer"])
            #------------------------------------------------------------------
            self.action_combo = Gtk.ComboBox.new_with_model(action_store)
            renderer_text = Gtk.CellRendererText()
            self.action_combo.pack_start(renderer_text, True)
            self.action_combo.add_attribute(renderer_text, "text", 0)            
            
            self.action_combo.set_entry_text_column(0)
            self.action_combo.set_active(0)
            
            self.box_combo_action.pack_start(self.action_combo, False, False, 0)
            #------------------------------------------------------------------
            '''
                
                
                

            self.window.show_all()
            self.Visible  = True
    
    def import_data (self, button):
        """ Function doc """
        entry_name    = None
        idnum     = self.combobox_pdynamo_system.get_active()
        text      = self.combobox_pdynamo_system.get_active_text()
        
        print(idnum, text )

    
    def CloseWindow (self, button, data  = None):
        """ Function doc """
        self.window.destroy()
        self.Visible    =  False
    
    
    def __init__(self, main = None):
        """ Class initialiser """
        self.easyhybrid_main     = main
        self.vm_session       = main.vm_session
        self.Visible             =  False        

        self.chain = ''
        self.resn  = ''
        self.resi  = ''
        self.atom  = ''

    def run_selection (self, button):
        """ Function doc """
        #print('run_selection', self.method_combo.get_active(), self.radius_spinbutton.get_value ())
        self.chain = self.builder.get_object('chain_entry').get_text()
        self.resn  = self.builder.get_object('resn_entry' ).get_text()
        self.resi  = self.builder.get_object('resi_entry' ).get_text()
        self.atom  = self.builder.get_object('atom_entry' ).get_text()
        
        #print(chain,resn,resi, atom)
        #'''
        #atom1 = self.vm_session.picking_selections.picking_selections_list[0]
        #print (atom1.chain, atom1.resn, atom1.resi, atom1.name)
        #print ("%s:%s.%s:%s" %(chain,resn,resi,atom))
        
        _centerAtom = "%s:%s.%s:%s" %(self.chain, 
                                      self.resn,
                                      self.resi,
                                      self.atom)
        _radius     =  self.radius_spinbutton.get_value ()
        _method     =  self.method_combo.get_active()
        
        self.easyhybrid_main.p_session.selections (_centerAtom, _radius, _method )

        if self.easyhybrid_main.vm_session.selection_box_frane:
            self.easyhybrid_main.vm_session.selection_box_frane.change_toggle_button_selecting_mode_status(False)
        else:
            self.easyhybrid_main.vm_session._picking_selection_mode = False
        
        self.easyhybrid_main.vm_session.selections[self.easyhybrid_main.vm_session.current_selection].active = True
        self.easyhybrid_main.vm_session.glwidget.vm_widget.queue_draw()
        
        
          
    def get_info_from_selection (self, button):
        """ Function doc """
        #chain = self.builder.get_object('chain_entry').get_text()
        #resn  = self.builder.get_object('resn_entry' ).get_text()
        #resi  = self.builder.get_object('resi_entry' ).get_text()
        #atom  = self.builder.get_object('atom_entry' ).get_text()
        
        atom1 = self.vm_session.picking_selections.picking_selections_list[0]
        if atom1:
            #atom1.chain, atom1.resn, atom1.resi, atom1.name
            
            if atom1.chain =='':
                chain = '*'
            else:
                chain = atom1.chain
            
            self.builder.get_object('chain_entry').set_text(str(chain)      )
            self.builder.get_object('resn_entry' ).set_text(str(atom1.resn) )
            self.builder.get_object('resi_entry' ).set_text(str(atom1.resi) )
            self.builder.get_object('atom_entry' ).set_text(str(atom1.name) )
        else:
            print('use picking selection to chose the central atom')
            
            
            
            
        
