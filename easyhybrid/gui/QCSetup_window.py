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


class EasyHybridSetupQCModelWindow:
    """ Class doc """
    
    def __init__(self, main = None):
        """ Class initialiser """
        self.easyhybrid_main     = main
        self.Visible             =  False        
        
        self.methods_liststore = Gtk.ListStore(str, str, str)
        
        self.method_id    = 0    # 0 for am1, 1 for pm3  and...
        self.charge       = 0
        self.multiplicity = 1
        self.restricted   = True
        
        self.adjustment_charge = Gtk.Adjustment(value=0,
                                           lower=-100,
                                           upper=100,
                                           step_increment=1,
                                           page_increment=1,
                                           page_size=0)
        
        self.adjustment_multiplicity = Gtk.Adjustment(value=1,
                                           lower=1,
                                           upper=100,
                                           step_increment=1,
                                           page_increment=1,
                                           page_size=0)
        
        self.methods_id_dictionary = {
                                      0 : 'am1'     ,
                                      1 : 'am1dphot',
                                      2 : 'pm3'     ,
                                      3 : 'pm6'     ,
                                      4 : 'mndo'    ,
                                
                                      }
        
        
        
    def OpenWindow (self):
        """ Function doc """
        if self.Visible  ==  False:
            self.builder = Gtk.Builder()
            self.builder.add_from_file(os.path.join(VISMOL_HOME,'easyhybrid/gui/easyhybrid_QCSetup_window.glade'))
            self.builder.connect_signals(self)
            
            self.window = self.builder.get_object('SetupQCModelWindow')
            self.window.set_keep_above(True)


            
            '''--------------------------------------------------------------------------------------------'''
            self.methods_type_store = Gtk.ListStore(str)
            methods_types = [
                "am1",
                "am1dphot",
                "pm3",
                "pm6",
                "mndo",
                "ab initio - ORCA",
                "DFT / DFTB",
                ]
            for method_type in methods_types:
                self.methods_type_store.append([method_type])
                #print (method_type)
            
            self.methods_combo = self.builder.get_object('QCModel_methods_combobox')
            self.methods_combo.connect("changed", self.on_name_combo_changed)
            self.methods_combo.set_model(self.methods_type_store)
            renderer_text = Gtk.CellRendererText()
            self.methods_combo.pack_start(renderer_text, True)
            self.methods_combo.add_attribute(renderer_text, "text", 0)
            self.methods_combo.set_active(self.method_id)
            '''--------------------------------------------------------------------------------------------'''


            self.spinbutton_charge       = self.builder.get_object('spinbutton_charge'      )
            self.spinbutton_multiplicity = self.builder.get_object('spinbutton_multiplicity')
            self.spinbutton_charge      .set_adjustment(self.adjustment_charge)
            self.spinbutton_multiplicity.set_adjustment(self.adjustment_multiplicity)
            
            self.window.show_all()                                               
            self.builder.connect_signals(self)                                   
            
            
            ''' Updating the number of atoms '''
            self.update_number_of_qc_atoms ()
            
            self.Visible  =  True

        else:
            ''' Updating the number of atoms '''
            self.update_number_of_qc_atoms ()

            
    def update_number_of_qc_atoms (self):
        """ Function doc """
        self.entry_number_of_qc_atoms = self.builder.get_object('entry_number_of_qc_atoms')
        
        '''   Estiamting the QC charge  '''
        '''----------------------------------------------------------------------------------------------'''
        psystem          = self.easyhybrid_main.p_session.systems [self.easyhybrid_main.p_session.active_id]
        estimated_charge = 0.0
        for index in psystem['qc_table']:
            estimated_charge += psystem['system'].mmState.charges[index]
        
        estimated_charge = int(round(estimated_charge))
        self.spinbutton_charge.set_value (estimated_charge)
        '''----------------------------------------------------------------------------------------------'''

        
        if self.easyhybrid_main.p_session.systems[self.easyhybrid_main.p_session.active_id]['qc_table']:
            number_of_qc_atoms = len(self.easyhybrid_main.p_session.systems[self.easyhybrid_main.p_session.active_id]['qc_table'])
            self.entry_number_of_qc_atoms.set_text(str(number_of_qc_atoms))
        else:
            number_of_qc_atoms = len(self.easyhybrid_main.p_session.systems[self.easyhybrid_main.p_session.active_id]['system'].atoms)
            self.entry_number_of_qc_atoms.set_text(str(number_of_qc_atoms)+ ' (all)')
    
    
    def CloseWindow (self, button, data  = None):
        """ Function doc """
        self.window.destroy()
        self.Visible    =  False
    
    #----------------------------------------------------------------
    def on_spian_button_change (self, widget):
        """ Function doc """
        self.charge       = self.spinbutton_charge.get_value_as_int()
        self.multiplicity = self.spinbutton_multiplicity.get_value_as_int()
        
        
    def on_name_combo_changed (self, combobox):
        """ Function doc """
        self.method_id = self.builder.get_object('QCModel_methods_combobox').get_active()
    
    def on_button_ok (self, button):
        """ Function doc """
        #print(button)
        #charge         = self.spinbutton_charge.get_value_as_int()
        #multiplicity   = self.spinbutton_multiplicity.get_value_as_int()
        #print('\n\ncharge'  , self.charge      )
        #print('multiplicity', self.multiplicity)
        #print('method_id'   , self.method_id   )
        
        if self.builder.get_object('radio_button_restricted').get_active():
            #print("%s is active" % (self.builder.get_object('radio_button_restricted').get_label()))
            self.restricted = True
        else:
            #print("%s is not active" % (self.builder.get_object('radio_button_restricted').get_label()))
            self.restricted = False
        

        
        parameters = {
                    'charge'       : self.charge      ,
                    'multiplicity' : self.multiplicity,
                    'method'       : self.methods_id_dictionary[self.method_id]   ,
                    'restricted'   : self.restricted  ,
                     }


        parameters['energyTolerance'  ] = float(self.builder.get_object('entry_energyTolerance').get_text())
        parameters['densityTolerance' ] = float(self.builder.get_object('entry_densityTolerance').get_text())
        parameters['maximumIterations'] = int(self.builder.get_object('entry_maximumIterations').get_text())



        self.easyhybrid_main.p_session.define_a_new_QCModel(parameters =parameters)
        self.easyhybrid_main.update_gui_widgets ()
        self.window.destroy()
        self.Visible    =  False

