#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  __main__.py
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

import gi, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import os
VISMOL_HOME        = os.environ.get('VISMOL_HOME')

#import os

#w = Gtk.Window()
#f = Gtk.Image()
#f.set_from_file("/home/fernando/Pictures/Screenshot from 2021-06-12 09-49-19.png")
#w.add(f)
#w.show_all()
#Gtk.main()

from vCore.VismolSession  import VisMolSession
#from GTKGUI               import VismolMain 
from easyhybrid.GUI       import EasyHybridMainWindow
#from easyhybrid.GUI       import LabelWindow
from vModel.Representations   import LinesRepresentation
from vModel.Representations   import NonBondedRepresentation
from vModel.Representations   import SticksRepresentation
from vModel.Representations   import DotsRepresentation
from vModel.Representations   import SpheresRepresentation
from vModel.Representations   import GlumpyRepresentation
from vModel.Representations   import RibbonsRepresentation
from vModel.Representations   import SurfaceRepresentation
from vModel.Representations   import WiresRepresentation
from vModel.Representations   import LabelRepresentation

from vModel.Representations   import DynamicBonds
from vModel.Representations   import CartoonRepresentation

from easyhybrid.Serialization import LoadAndSaveFiles

from vModel import VismolObject
import pickle

class EasyHybridDialogPrune:
    """ Class doc """

    def __init__ (self, num_of_atoms,  name, tag):
        """ Class initialiser """
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.join(VISMOL_HOME,'easyhybrid/gui/easyhybrid_prune_dialog.glade'))
        self.builder.connect_signals(self)
        
        self.dialog       = self.builder.get_object('dialog_prune')

        self.builder.get_object('entry_number_of_atoms').set_text(str(num_of_atoms))
        self.builder.get_object('entry_name').set_text(name + '_pruned')
        self.builder.get_object('entry_tag').set_text(tag)
        

        
        self.prune = False
        self.name  = None
        self.tag   = None
        answer = self.dialog.run()
        print ('answer', answer)
    def on_click_button_prune (self, widget):
        """ Function doc """
        num_of_atoms = self.builder.get_object('entry_number_of_atoms').get_text( )
        self.name    = self.builder.get_object('entry_name').get_text( )
        self.tag     = self.builder.get_object('entry_tag').get_text( )
        self.prune   = True

        self.dialog.destroy()

    

    def on_click_button_cancel (self, widget):
        """ Function doc """
        self.dialog.destroy()
        self.prune   = False

class EasyHybridVismolSession(VisMolSession, LoadAndSaveFiles):
    """ Class doc """
   
    #ef __init__ (self, glwidget = False, toolkit = 'gtk3', main_session = None):
    #   """ Function doc """
    #   super().__init__( glwidget = False, toolkit = 'gtk3', main_session = None)
    #   self.treestore = Gtk.TreeStore(
    #                                   str , # Name
    #                                   
    #                                   bool, # toggle active=1
    #                                   bool, # radio  active=2
    #                                   
    #                                   bool, # toggle visible = 3
    #                                   bool, # radio  visible = 4
    #                                   
    #                                   int , # vobject index
    #                                   bool, # is vobject index visible?
    #                                   int , # pdynamo system index 
    #                                   bool, # is pdynamo system index visible?
    #
    #                                   
    #                                   )
    #   
    def save_serialization_file (self, filename = 'session.easy'):
        """ Function doc """
        #serialization = LoadAndSaveFiles(self, self.main_session.p_session)
        self.save_session(filename)


    def build_index_list_from_atom_selection (self):
        """  
        returns the index_list and residue_list
        """
        selection         = self.selections[self.current_selection]
        
        index_list = []                
        
        residue_list = {} 
        
        for atom in selection.selected_atoms:
            #print(atom.vobject.easyhybrid_system_id , pdmsys_active)
            true_or_false = self.check_selected_atom (atom)
            if true_or_false:
                index_list.append(atom.index -1)
                
                if atom.resi in residue_list.keys():
                    residue_list[atom.resi].append(atom.index -1)
                else:
                    residue_list[atom.resi] = [atom.index -1]

                
            else:
                return False
        return index_list, residue_list


    def check_selected_atom(self, atom, dialog = True):
        '''checks if selected atoms belong to the dynamo system in memory'''
        if atom.vobject.easyhybrid_system_id != self.main_session.p_session.active_id:
            #print(atom.index-1, atom.name, atom.resn)
            
            name = self.main_session.p_session.systems[self.main_session.p_session.active_id]['name']
            
            dialog = Gtk.MessageDialog(
                        transient_for = self.main_session.window,
                        flags=0,
                        message_type=Gtk.MessageType.INFO,
                        buttons=Gtk.ButtonsType.OK,
                        text="Invalid Atom Selection",
                        )
            dialog.format_secondary_text(
"""Your atom selection does not belong to the active pDynamo system:
 
{} ({}) 

You can choose the active pDynamo system by changing the radio 
button position in the main treeview (active column).""".format(name,self.main_session.p_session.active_id)
            )
            dialog.run()
            print("INFO dialog closed")
            dialog.destroy()
            return False
        else:
            return True
        
    
    def set_color (self, color = [0.5 , 0.5 , 0.5]):
        """ Function doc """
        selection         = self.selections[self.current_selection]

        vobject_list = []

        for atom in selection.selected_atoms:
            if atom.symbol == 'C':
                atom.color = color
                if atom.vobject in vobject_list:
                    pass
                else:
                    vobject_list.append(atom.vobject)

        for vobject in vobject_list:
            vobject._generate_color_vectors ( do_colors         = True,
                                              do_colors_idx     = False,
                                              do_colors_raindow = False,
                                              do_vdw_dot_sizes  = False,
                                              do_cov_dot_sizes  = False,
                                              )

            
            for rep  in vobject.representations.keys():
                if vobject.representations[rep]:
                    #try:
                    vobject.representations[rep]._set_colors_to_buffer()
                    #except:
                    #    print("VisMol/vModel/Representations.py, line 123, in _set_colors_to_buffer GL.glBindBuffer(GL.GL_ARRAY_BUFFER, ctypes.ArgumentError: argument 2: <class 'TypeError'>: wrong type'")

            self.main_session.p_session.refresh_vobject_qc_and_fixed_representations (
                                                                      vobject = vobject,    
                                                                 fixed_atoms = True         , 
                                                                    QC_atoms = True         ,
                                                                metal_bonds  = True         ,
                                                                      static = True         )
        self.glwidget.vm_widget.queue_draw()
        return True
    
    
    def load_easyhybrid_serialization_file (self, filename):
        """ Function doc """
        #new_session = self.restart_session(filename)
        #serialization = LoadAndSaveFiles(self, self.main_session.p_session)
        '''
        #--------------------------------------------------------------------------
        self.vobjects     = [] # old vobjects - include molecules
        self.vobjects_dic = {} # old vobjects dic - include molecules
        self.vobj_counter       = 0  # Each vismol object has a unique access key (int), which is generated in the method: add_vobject_to_vismol_session.
        self.vismol_geometric_object     = []
        
        self.vismol_geometric_object_dic = {
                                           'pk1pk2' :  None,
                                           'pk2pk3' :  None,
                                           'pk3pk4' :  None,
                                           }
        
        self.atom_id_counter  = 0  # 
        self.atom_dic_id      = {
                                # atom_id : obj_atom 
                                 }
        
        #--------------------------------------------------------------------------
        '''

        
        #print('loading easyhybrid session')
        for key , vobject in self.vobjects_dic.items():
            for key, rep in vobject.representations.items():
                if rep:
                    rep.delete_buffers()
            
            vobject.active =  False
            self.glwidget.queue_draw()
            del vobject
        
        
        self.vobjects_dic      = {} # old vobjects dic - include molecules
        self.vobj_counter            = 0  # Each vismol object has a unique access key (int), which is generated in the method: add_vobject_to_vismol_session.
        self.vismol_geometric_object = []
        self.vm_session_vbos         = []

        self.vismol_geometric_object_dic = {
                                           'pk1pk2' :  None,
                                           'pk2pk3' :  None,
                                           'pk3pk4' :  None,
                                           }
        self.atom_id_counter  = 0  # 
        self.atom_dic_id      = {
                                # atom_id : obj_atom 
                                 }
                                 
                                 
        self.treestore.clear()
        self.parents = {}
        self.main_session.p_session.restart_pdynamo2vismol_session()
        
        
        
        
        self.load_session(filename)
        self.main_session.treeview.expand_all()
    
    def build_treeview_from_pdynamo_session_data (self, pdynamo_session):
        """ Function doc """
        
        
        #vobject.active = active_original

        for sys_index in pdynamo_session.systems.keys():
            '''        T R E E S T O R E           '''
            if sys_index in self.parents.keys():
                pass
            else:          
                # Creates a new "parent" when a new system is loaded into memory. 
                for row in self.treestore:
                    row[3] =  False
                vobject = pdynamo_session.systems[sys_index]['vobject']
                
                if  pdynamo_session.systems[sys_index] == pdynamo_session.systems[pdynamo_session.active_id]:
                    is_active = True
                else:
                    is_active = False
                print('is_active:', is_active)
                self.parents[sys_index] = self.treestore.append(None,                                                
                                                               
                                                               [pdynamo_session.systems[sys_index]['name'], # Name
                                                                False,                                      # toggle active=1
                                                                False,                                      # toggle visible = 3
                                                                
                                                                is_active ,                                      # radio  active  = 2
                                                                True ,                                      # radio  visible = 4

                                                                False,                                      # traj radio  active = 5
                                                                False,                                      # is trajectory radio visible?
                                                                
                                                                vobject.index,                        #
                                                                vobject.easyhybrid_system_id,         # pdynamo system index
                                                                0])                                     # is pdynamo system index visible?
                
                self.gtk_treeview_iters.append(self.parents[sys_index])

            #n = 0
            #for treeview_iter in self.gtk_treeview_iters:
            #    self.treestore[treeview_iter][5] = False
            #    n+=1
            for key , vobject in pdynamo_session.systems[sys_index]['vobjects'].items():
                treeview_iter = self.treestore.append(self.parents[vobject.easyhybrid_system_id]      ,        #parent
                                                  
                                                  [vobject.name, 
                                                   vobject.active ,   # toggle active   =1       
                                                   True ,                   # toggle visible  = 2                  
                                                   
                                                   False ,                  # radio  active  = 3                       
                                                   False ,                  # radio  visible = 4                      
                                                   
                                                   True  ,                  # traj radio  active = 5                     
                                                   True  ,                  # is trajectory radio visible?  6                   
                                                   
                                                   vobject.index,     # 7
                                                   vobject.easyhybrid_system_id,   # pdynamo system index  8    
                                                   len(vobject.frames)] # is pdynamo system index visible?  9 
                                                    )
                self.gtk_treeview_iters.append(treeview_iter)
                self.gtk_widgets_update ()







    
    
    def add_vobject_to_vismol_session (self, pdynamo_session    = None, 
                                                   rep                = {'lines': [], 'nonbonded': []}, 
                                                   vobject      = None, 
                                                   vobj_count         = True,
                                                   autocenter         = True,
                                                   find_dynamic_bonds = True):
        """ Function doc """
       
        if vobj_count:
            vobject.index = self.vobj_counter
        else:
            pass
        
        #self.vobjects.append(vobject)
        self.vobjects_dic[vobject.index] = vobject
        
        #self.append_vobject_to_vobjects_listStore(vobject)
        
        if vobj_count:
            self.vobj_counter += 1
        
            
        vobj_index = vobject.index
        sys_index  = vobject.easyhybrid_system_id
        
        if 'vobjects' in pdynamo_session.systems[sys_index].keys():
            pdynamo_session.systems[sys_index]['vobjects'][vobj_index] = vobject
        else:
            pdynamo_session.systems[sys_index]['vobjects'] = {}
            pdynamo_session.systems[sys_index]['vobjects'][vobj_index] = vobject
        
        
        '''
        We have to do a preliminary render for all objects before building 
        the treewview (even for those inactive objects coming from the 
        serialization file). This is necessary because it is necessary to 
        create the VBOs and VAOs of the sphere representations, otherwise, 
        we may have problems when associating a new QC region () for example) 
        for a system that has inactive objects and without the VBOs and VAOs 
        already created .
        '''

        #            Saving the object's active/inactive condition 
        active_original  = vobject.active
        
        #---------------------------------------------------------------------#
        vobject.active =  True        
        
        #vobject.create_new_representation (rtype = 'spheresInstace')
        if rep:
            #print('\n\nrep.keys()', rep.keys())
            #try:
            for key in rep.keys():
                if rep[key]:
                    self.show_or_hide_by_object (_type = key, 
                                               vobject = vobject,  
                                       selection_table = rep[key], 
                                                  show = True,
                                    find_dynamic_bonds = find_dynamic_bonds,     
                                                  )     
                else:
                    
                    if key == 'lines':
                        self.show_or_hide_by_object (_type = 'lines', 
                                                   vobject = vobject,  
                                           selection_table = range(0, len(vobject.atoms)), 
                                                      show = True)
                        
                        #self.show_or_hide_by_object (_type = 'dotted_lines', 
                        #                       vobject = vobject,  
                        #               selection_table = vobject.metal_bonded_atoms, 
                        #                          show = True,
                        #           #find_dynamic_bonds = find_dynamic_bonds,     
                        #                          )

                    if key == 'nonbonded':
                            self.show_or_hide_by_object (_type = 'nonbonded', 
                                                        vobject = vobject,  
                                                selection_table = vobject.non_bonded_atoms , 
                                                            show = True)
                    
                    pass

            #except:
            #    
            #    print( 'except: rep:',rep )
               #
               #
               #if key == 'lines':
               #    if rep[key] == []:
               #        self.show_or_hide_by_object (_type = 'lines', 
               #                                   vobject = vobject,  
               #                           selection_table = range(0, len(vobject.atoms)), 
               #                                      show = True)
               #    else:
               #        self.show_or_hide_by_object (_type = 'lines', 
               #                                   vobject = vobject,  
               #                           selection_table = rep[key], 
               #                                      show = True)
               #if key == 'nonbonded':
               #    if rep[key] == []:
               #        self.show_or_hide_by_object (_type = 'nonbonded', 
               #                                   vobject = vobject,  
               #                           selection_table = range(0, len(vobject.atoms)), 
               #                                      show = True)
               #    else:
               #        self.show_or_hide_by_object (_type = 'nonbonded', 
               #                                   vobject = vobject,  
               #                           selection_table = rep[key], 
               #                                      show = True)
               #    
               #    
               #    
               #    
               #    
               #    #if rep[key] == []:
               #    #    vobject.create_new_representation (rtype = 'lines')
               #    #else:
               #    #    
               #    #    vobject.create_new_representation (rtype = 'lines', indexes = rep[key])
               #
               #if key == 'nonbonded':
               #    if rep[key] == []:
               #        vobject.create_new_representation (rtype = 'nonbonded')
               #    else:
               #        vobject.create_new_representation (rtype = 'nonbonded', indexes = rep[key])
               #    
               #if key == 'sticks':
               #    if rep[key] == []:
               #        vobject.create_new_representation (rtype = 'sticks')
               #    else:
               #        vobject.create_new_representation (rtype = 'sticks', indexes = rep[key])
               #
               ##if key == 'dynamic_bonds':
               ##    if rep[key] == []:
               ##        vobject.create_new_representation (rtype = 'dynamic_bonds')
               ##    else:
               ##        vobject.create_new_representation (rtype = 'dynamic_bonds', indexes = rep[key])
               #
               #if key == 'spheres':
               #    
               #    if rep[key] == []:
               #        vobject.create_new_representation (rtype = 'spheres')
               #    else:
               #        vobject.create_new_representation (rtype = 'spheres', indexes = rep[key])
        else:
            print('no representation')
        #rep =  RibbonsRepresentation(name = 'ribbons', active = True, _type = 'mol', vobject = vobject, glCore = self.glwidget.vm_widget)
        #vobject.representations[rep.name] = rep
    

        #'''
        if autocenter:
            #print(self.vobjects[-1].mass_center)
            self.glwidget.vm_widget.center_on_coordinates(vobject, vobject.mass_center, sleep_time = 0.0000001)
        else:
            self.glwidget.vm_widget.queue_draw()
        #---------------------------------------------------------------------#
        
        
        
        
        
        #  Loading the object's active/inactive condition 
        vobject.active = active_original
                
        '''        T R E E S T O R E           '''
        if sys_index in self.parents.keys():
            pass
        else:          
            # Creates a new "parent" when a new system is loaded into memory. 
            for row in self.treestore:
                #row[2] = row.path == selected_path
                row[3] =  False
                #row[5] = False 
                #for i,j in enumerate(row):
                #    print(i, j,)           
                
            #if  pdynamo_session.systems[sys_index] == pdynamo_session.systems[pdynamo_session.active_id]:
            #    is_active = True
            #else:
            #    is_active = False
            #print('is_active:', is_active)
            
            self.parents[sys_index] = self.treestore.append(None,                                                
                                                           
                                                           [pdynamo_session.systems[sys_index]['name'], # Name
                                                            False,                                      # toggle active=1
                                                            False,                                      # toggle visible = 3
                                                            
                                                            True ,                                      # radio  active  = 2
                                                            True ,                                      # radio  visible = 4

                                                            False,                                      # traj radio  active = 5
                                                            False,                                      # is trajectory radio visible?
                                                            
                                                            vobject.index,                        #
                                                            vobject.easyhybrid_system_id,         # pdynamo system index
                                                            0])                                     # is pdynamo system index visible?
            
            self.gtk_treeview_iters.append(self.parents[sys_index])

        n = 0
        for treeview_iter in self.gtk_treeview_iters:
            self.treestore[treeview_iter][5] = False
            #print(self.treestore[treeview_iter][0])
            #print ('\ntreeview_iter', treeview_iter, n)
            n+=1
            
        treeview_iter = self.treestore.append(self.parents[vobject.easyhybrid_system_id]      ,        #parent
                                          
                                          [vobject.name, 
                                           vobject.active ,   # toggle active   =1       
                                           True ,                   # toggle visible  = 2                  
                                           
                                           False ,                  # radio  active  = 3                       
                                           False ,                  # radio  visible = 4                      
                                           
                                           True  ,                  # traj radio  active = 5                     
                                           True  ,                  # is trajectory radio visible?  6                   
                                           
                                           vobject.index,     # 7
                                           vobject.easyhybrid_system_id,   # pdynamo system index  8    
                                           len(vobject.frames)] # is pdynamo system index visible?  9 
                                            )
        self.gtk_treeview_iters.append(treeview_iter)
        
        #print('\n\n\n')
        #for vobj in self.vobjects:
        #    print(vobj.name, vobj.easyhybrid_system_id)
        #print('\n\n\n')
        #print(vobject.index)
        self.gtk_widgets_update ()
        if self.main_session.selection_list_window.visible:
            self.main_session.selection_list_window.update_window(system_names = False, 
                                                                  coordinates  = True,  
                                                                  selections   = False )
        
        #print('vobjects_dic', self.vobjects_dic)




    
    def insert_glmenu (self, bg_menu  = None, 
                            sele_menu = None, 
                             obj_menu = None, 
                            pick_menu = None):
        """ Function doc """
        



        def _viewing_selection_mode_atom (_):
            """ Function doc """
            self.viewing_selection_mode(sel_type = 'atom')
        def _viewing_selection_mode_residue (_):
            """ Function doc """
            self.viewing_selection_mode(sel_type = 'residue')
        def _viewing_selection_mode_chain (_):
            """ Function doc """
            self.viewing_selection_mode(sel_type = 'chain')

        def _selection_type_picking(_):
            
            if self.selection_box_frane:
                self.selection_box_frane.change_toggle_button_selecting_mode_status(True)
            else:
                self._picking_selection_mode = True
            self.glwidget.queue_draw()
        
        def _selection_type_viewing(_):
            if self.selection_box_frane:
                self.selection_box_frane.change_toggle_button_selecting_mode_status(False)
            else:
                self._picking_selection_mode = False
            self.glwidget.queue_draw()

        if sele_menu is None:
            ''' Standard Sele Menu '''
            
            def menu_show_dynamic_bonds (_):
                """ Function doc """
               #print('dynamic_test')
                self.show_or_hide( _type = 'dynamic_bonds', show = True)
            def menu_hide_dynamic_bonds (_):
                """ Function doc """
               #print('dynamic_test')
                self.show_or_hide( _type = 'dynamic_bonds', show = False)
            
            def menu_show_ribbons (_):
                """ Function doc """
               #print('dynamic_test')
                self.show_or_hide( _type = 'ribbons', show = True)
            def menu_hide_ribbons (_):
                """ Function doc """
               #print('dynamic_test')
                self.show_or_hide( _type = 'ribbons', show = False)
            
            def select_test (_):
                """ Function doc """
                self.select(indexes = 'all')
            
            def menu_show_lines (_):
                """ Function doc """
                self.show_or_hide( _type = 'lines', show = True)
            
            def menu_show_dotted_lines (_):
                """ Function doc """
                self.show_or_hide( _type = 'dotted_lines', show = True)

            def menu_hide_lines (_):
                """ Function doc """
                #print('hide')
                self.show_or_hide( _type = 'lines', show = False)
            
            def menu_hide_dotted_lines (_):
                """ Function doc """
                self.show_or_hide( _type = 'dotted_lines', show = False)
            
            def menu_show_sticks (_):
                """ Function doc """
                self.show_or_hide( _type = 'sticks', show = True)
            
            def menu_show_nonbonded (_):
                """ Function doc """
                self.show_or_hide( _type = 'nonbonded', show = True)
            
            def menu_hide_nonbonded (_):
                """ Function doc """
                self.show_or_hide( _type = 'nonbonded', show = False)

            def menu_hide_sticks (_):
                """ Function doc """
                self.show_or_hide( _type = 'sticks', show = False)

            def menu_show_spheres (_):
                """ Function doc """
                self.show_or_hide( _type = 'spheres', show = True)

            def menu_hide_spheres (_):
                """ Function doc """
                self.show_or_hide( _type = 'spheres', show = False)
            
            def menu_show_dots (_):
                """ Function doc """
                self.show_or_hide( _type = 'dots', show = True)

            def menu_hide_dots (_):
                """ Function doc """
                self.show_or_hide( _type = 'dots', show = False)
            
            
            
            def menu_set_color_grey (_):
                """ Function doc """
                self.set_color(color = [0.3     , 0.3     , 0.5 ] )
            
            def menu_set_color_green (_):
                """ Function doc """
                self.set_color(color = [0.0     , 1.0     , 0.0 ] )
            
            def menu_set_color_yellow (_):
                """ Function doc """
                self.set_color(color = [1.0     , 1.0     , 0.0 ] )
            
            def menu_set_color_light_blue (_):
                """ Function doc """
                self.set_color(color = [0.5     , 0.5     , 1.0 ] )
            
            def menu_set_color_light_red (_):
                """ Function doc """
                self.set_color(color = [1.0     , 0.5     , 0.5 ] )
            
            def menu_set_color_purple (_):
                """ Function doc """
                self.set_color(color = [1.0     , 0.0     , 1.0 ] )
            
            def menu_set_color_orange (_):
                """ Function doc """
                self.set_color(color = [1.0     , 0.5     , 0.0 ] )


            def menu_set_color_magenta (_):
                """ Function doc """

            
            
            def menu_color_change (_):
                """ Function doc """
                selection               = self.selections[self.current_selection]
                self.colorchooserdialog = Gtk.ColorChooserDialog()
                
                if self.colorchooserdialog.run() == Gtk.ResponseType.OK:
                    color = self.colorchooserdialog.get_rgba()
                    print(color.red,color.green, color.blue )
                    new_color = [color.red, color.green, color.blue]

                self.colorchooserdialog.destroy()
                self.set_color(new_color)

            
            def set_as_qc_atoms (_):
                """ Function doc """
                #selection = self.selections[self.current_selection]
                pdmsys_active = self.main_session.p_session.active_id
                qc_list, residue_list = self.build_index_list_from_atom_selection()
                
                #print('residue_list:', residue_list)
                
                if qc_list:
                    
                    self.main_session.p_session.systems[pdmsys_active]['qc_residue_table'] = residue_list
                    self.main_session.p_session.systems[pdmsys_active]['qc_table'] = qc_list
                    self.main_session.run_dialog_set_QC_atoms()

            def set_as_free_atoms (_):
                """ Function doc """
                selection         = self.selections[self.current_selection]
                
                freelist = []                
                for atom in selection.selected_atoms:
                    #print(atom.index, atom.name, atom.color) 
                    
                    '''checks if the selected atoms belong to the active project'''
                    true_or_false = self.check_selected_atom(atom, dialog = True)
                    if true_or_false:
                        freelist.append(atom.index -1)
                        #index = atom.index -1
                        

                        #atom.color = atom.init_color(atom.symbol) 
                        #true_or_false = self.check_selected_atom( atom, dialog = True)
                    else:
                        return False
                    
                
                
                '''here we are returning the original color of the selected atoms'''
                for key, vobject in self.vobjects_dic.items():
                    if vobject.easyhybrid_system_id == self.main_session.p_session.active_id:
                        #print('key',key, vobject.name, vobject.easyhybrid_system_id, vobject.active)
                        for index in freelist:
                           #print(index,vobject. atoms[index])
                            atom = vobject.atoms[index]
                            atom.color = atom.init_color(atom.symbol)
                            #vobject.atoms[index]
                            #vobject.atoms[index].init_color(atom.symbol) 
                
                
                
                
                
                #print(atom.index, atom.name, atom.color) 
                #----------------------------------------------
                pdmsys_active =   self.main_session.p_session.active_id
                #fixedlist = fixedlist + self.main_session.p_session.systems[pdmsys_active]['fixed_table']
                a = set(self.main_session.p_session.systems[pdmsys_active]['fixed_table'])
                b = set(freelist)
                
                c = a - b
                
                #print (a)
                #print (b)
                
                #Combining with list that the already exists  
                fixedlist =  set(self.main_session.p_session.systems[pdmsys_active]['fixed_table']) -set(freelist)
                #guarantee that the atom index appears only once in the list
                fixedlist = list(c) 
                
                #print ('fixedlist',fixedlist)
                #sending to pDynamo
                refresh = self.main_session.p_session.define_free_or_fixed_atoms_from_iterable (fixedlist)
                if refresh:
                    #self.main_session.p_session.refresh_qc_and_fixed_representations()
                    self.glwidget.vm_widget.queue_draw()
                #self.main_session.p_session.vismol_selection_qc = selection.copy()
            
            def prune_atoms (_):
                """ Function doc """
                

                builder = Gtk.Builder()
                builder.add_from_file(os.path.join(VISMOL_HOME,'easyhybrid/gui/easyhybrid_prune_dialog.glade'))
                


                atomlist, resi_table = self.build_index_list_from_atom_selection()
                if atomlist:
                    atomlist = list(set(atomlist))
                    
                    num_of_atoms = len(atomlist)
                    name = self.main_session.p_session.systems[self.main_session.p_session.active_id]['name']
                    tag  = self.main_session.p_session.systems[self.main_session.p_session.active_id]['tag']
                    dialog =  EasyHybridDialogPrune(num_of_atoms, name, tag)
                    
       

                    if dialog.prune:
                        print ("Prune")
                        name         = dialog.name        
                        tag          = dialog.tag  
                        
                        for row in self.treestore:
                            #row[2] = row.path == selected_path
                            row[3] =  False

                        self.main_session.p_session.prune_system (selection = atomlist, name = name, summary = True, tag = tag)
            
            def set_as_fixed_atoms (_):
                """ Function doc """
                
                fixedlist, sel_resi_table = self.build_index_list_from_atom_selection()
                
                if fixedlist:
                    pdmsys_active = self.main_session.p_session.active_id
                    fixedlist = list(fixedlist) + list(self.main_session.p_session.systems[pdmsys_active]['fixed_table'])
                    #guarantee that the atom index appears only once in the list
                    fixedlist = list(set(fixedlist)) 
                    #print ('fixedlist',fixedlist)
                    #sending to pDynamo
                    refresh = self.main_session.p_session.define_free_or_fixed_atoms_from_iterable (fixedlist)
                    if refresh:
                        self.glwidget.vm_widget.queue_draw()
                    #self.main_session.p_session.vismol_selection_qc = selection.copy()
            
            
            def add_selection_to_sel_list (_):
                """ Function doc """
                #print('self.selections[self.current_selection].invert_selection()')
                sel_list, sel_resi_table = self.build_index_list_from_atom_selection()
                if sel_list:
                    
                    self.main_session.p_session.add_a_new_item_to_selection_list (system_id = self.main_session.p_session.active_id, 
                                                                                       indexes = sel_list, 
                                                                                        )

                
                #self.selections[self.current_selection].invert_selection()
            
            def invert_selection (_):
                """ Function doc """
                #print('self.selections[self.current_selection].invert_selection()')
                self.selections[self.current_selection].invert_selection()
            
            
            sele_menu = { 
                    #'header' : ['MenuItem', None],
                    
                    'separator0':['separator', None],
                    
                    'Send to Selection List':['MenuItem', add_selection_to_sel_list],
                    
                    'separator1':['separator', None],
                    
                    
                    'show'   : [
                                'submenu' ,{
                                            
                                            'lines'         : ['MenuItem', menu_show_lines],
                                            #'dotted_lines'  : ['MenuItem', menu_show_dotted_lines],
                                            'sticks'        : ['MenuItem', menu_show_sticks],
                                            'spheres'       : ['MenuItem', menu_show_spheres],
                                            #'dots'          : ['MenuItem', menu_show_dots],
                                            'dynamic bonds' : ['MenuItem', menu_show_dynamic_bonds],
                                            'ribbons'       : ['MenuItem', menu_show_ribbons],
                                            'separator2'    : ['separator', None],
                                            'nonbonded'     : ['MenuItem', menu_show_nonbonded],
                    
                                           }
                               ],
                    
                    
                    'hide'   : [
                                'submenu',  {
                                            'lines'         : ['MenuItem', menu_hide_lines],
                                            #'dotted_lines'  : ['MenuItem', menu_hide_dotted_lines],
                                            'sticks'        : ['MenuItem', menu_hide_sticks],
                                            'spheres'       : ['MenuItem', menu_hide_spheres],
                                            #'dots'          : ['MenuItem', menu_hide_dots],
                                            'dynamic bonds' : ['MenuItem', menu_hide_dynamic_bonds],
                                            'ribbons' : ['MenuItem', menu_hide_ribbons],

                                            'separator2'    : ['separator', None],
                                            'nonbonded'     : ['MenuItem', menu_hide_nonbonded],
                                            }
                                ],
                    
                    'color'   : [
                                'submenu',  {
                                            'grey'          : ['MenuItem', menu_set_color_grey],
                                            'yellow'        : ['MenuItem', menu_set_color_yellow],
                                            'green'         : ['MenuItem', menu_set_color_green],
                                            'light_blue'    : ['MenuItem', menu_set_color_light_blue],
                                            'light_red'     : ['MenuItem', menu_set_color_light_red],
                                            'purple'        : ['MenuItem', menu_set_color_purple],
                                            'orange'        : ['MenuItem', menu_set_color_orange],
                                            'custon'        : ['MenuItem', menu_color_change],
                                            #'dotted_lines'  : ['MenuItem', menu_hide_dotted_lines],
                                            }
                                ],
                    
                    'Invert Selection':['MenuItem', invert_selection],
                    
                    

                    
                    'separator2':['separator', None],

                    
                    
                    'Selection type'   : [
                                'submenu' ,{
                                            
                                            'viewing'   :  ['MenuItem', _selection_type_viewing],
                                            'picking'   :  ['MenuItem', _selection_type_picking],
                                            #'separator2':['separator', None],
                                            #'nonbonded' : ['MenuItem', None],
                    
                                           }
                                        ],
                    
                    'Selection Mode'   : [
                                'submenu' ,{
                                            
                                            'Atoms'     :  ['MenuItem', _viewing_selection_mode_atom],
                                            'Residue'   :  ['MenuItem', _viewing_selection_mode_residue],
                                            'Chain'     :  ['MenuItem', _viewing_selection_mode_chain],
                                            #'separator2':['separator', None],
                                            #'nonbonded' : ['MenuItem', None],
                    
                                           }
                               ],
                    
                    'separator3':['separator', None],
                    
                    'Set as QC atoms'      :  ['MenuItem', set_as_qc_atoms],
                    
                    'separator4':['separator', None],

                    'Set as fixed atoms'   :  ['MenuItem', set_as_fixed_atoms],
                    'Set as free atoms'   :  ['MenuItem', set_as_free_atoms],
                    
                    'separator5':['separator', None],
                    'prune to selection'  :  ['MenuItem', prune_atoms],

                    'separator6':['separator', None],

                    
                    #'Label Mode':  ['submenu' , {
                    #                        'Atom'         : [
                    #                                           'submenu', {
                    #                                                       'lines'    : ['MenuItem', None],
                    #                                                       'sticks'   : ['MenuItem', None],
                    #                                                       'spheres'  : ['MenuItem', None],
                    #                                                       'nonbonded': ['MenuItem', None],
                    #                                                       }
                    #                                          ],
                    #                        
                    #                        'Atom index'   : ['MenuItem', None],
                    #                        'residue name' : ['MenuItem', None],
                    #                        'residue_index': ['MenuItem', None],
                    #                       },
                    #          ]
                    }
      
        if bg_menu is None:
            ''' Standard Bg Menu'''
            
            def open_structure_data (_):
                """ Function doc """
                #print('ebaaaa')
                #self.filechooser   = FileChooser()
                #filename = self.filechooser.open()
                #self.load (filename, widget = None, autocenter = True)
                self.main_session.selection_list_window.OpenWindow()
            
            def import_system_menu (_):
                """ Function doc """
                self.main_session.NewSystemWindow.OpenWindow()
            
            def active_selection (_):
                """ Function doc """
                self.selections[self.current_selection].active = True
                self.glwidget.vm_widget.queue_draw()
                
            bg_menu = { 

                    'separator3'       : ['separator', None],
                    'Active Selection' : ['MenuItem', active_selection],

                    
                    'separator0'          : ['separator', None],
                    'Show Selection list' : ['MenuItem', open_structure_data],
                    
                    
                    #'funcao teste' : ['MenuItem', self.teste],                  
                    #'funcao teste2': ['MenuItem', self.teste2], 

                    'separator1':['separator', None],
                    'Selection type'   : [
                                'submenu' ,{
                                            
                                            'viewing'   :  ['MenuItem', _selection_type_viewing],
                                            'picking'   :  ['MenuItem', _selection_type_picking],
                                            #'separator2':['separator', None],
                                            #'nonbonded' : ['MenuItem', None],
                    
                                           }
                                        ],
                    
                    'Selection Mode'   : [
                                'submenu' ,{
                                            
                                            'atoms'     :  ['MenuItem', _viewing_selection_mode_atom],
                                            'residue'   :  ['MenuItem', _viewing_selection_mode_residue],
                                            'chain'     :  ['MenuItem', _viewing_selection_mode_chain],
                                            #'separator2':['separator', None],
                                            #'nonbonded' : ['MenuItem', None],
                    
                                           }
                               ],
                    
                    
                    #'hide'   : [
                    #            'submenu',  {
                    #                        'lines'    : ['MenuItem', menu_hide_lines],
                    #                        'sticks'   : ['MenuItem', menu_hide_sticks],
                    #                        'spheres'  : ['MenuItem', menu_hide_spheres],
                    #                        'nonbonded': ['MenuItem', None],
                    #                        }
                    #            ],
                    
                    
                    'separator2':['separator', None],
                    'Import System' : ['MenuItem', import_system_menu],
                    'separator3':['separator', None],

                    
                    
                    #'label':  ['submenu' , {
                    #                        'Atom'         : [
                    #                                           'submenu', {
                    #                                                       'lines'    : ['MenuItem', None],
                    #                                                       'sticks'   : ['MenuItem', None],
                    #                                                       'spheres'  : ['MenuItem', None],
                    #                                                       'nonbonded': ['MenuItem', None],
                    #                                                       }
                    #                                          ],
                    #                        
                    #                        'Atom index'   : ['MenuItem', None],
                    #                        'residue name' : ['MenuItem', None],
                    #                        'residue_index': ['MenuItem', None],
                    #                       },
                    #           ]
                    }

        if obj_menu is None:
            ''' Standard Obj Menu'''
            obj_menu = { 
                    'OBJ menu' : ['MenuItem', None],
                    
                    
                    'separator1':['separator', None],
                    
                    
                    'show'   : [
                                'submenu' ,{
                                            
                                            'lines'    : ['MenuItem', menu_show_lines],
                                            'sticks'   : ['MenuItem', menu_show_sticks],
                                            'spheres'  : ['MenuItem', menu_show_spheres],
                                            'separator2':['separator', None],
                                            'nonbonded': ['MenuItem', None],
                    
                                           }
                               ],
                    
                    
                    'hide'   : [
                                'submenu',  {
                                            'lines'    : ['MenuItem', menu_hide_lines],
                                            'sticks'   : ['MenuItem', menu_hide_sticks],
                                            'spheres'  : ['MenuItem', menu_hide_spheres],
                                            'nonbonded': ['MenuItem', None],
                                            }
                                ],
                    
                    
                    'separator2':['separator', None],

                    
                    
                    'label':  ['submenu' , {
                                            'Atom'         : [
                                                               'submenu', {
                                                                           'lines'    : ['MenuItem', None],
                                                                           'sticks'   : ['MenuItem', None],
                                                                           'spheres'  : ['MenuItem', None],
                                                                           'nonbonded': ['MenuItem', None],
                                                                           }
                                                              ],
                                            
                                            'atomic index' : ['MenuItem', None],
                                            'residue name' : ['MenuItem', None],
                                            'residue_index': ['MenuItem', None],
                                           },
                               ]
                    }



        if pick_menu is None:
            ''' Standard Sele Menu '''
            pick_menu = { 
                    'header' : ['MenuItem', None],
                    
                    
                    
                    'separator1':['separator', None],
                    
                    
                    'show'   : [
                                'submenu' ,{
                                            
                                            'lines'         : ['MenuItem', menu_show_lines],
                                            'sticks'        : ['MenuItem', menu_show_sticks],
                                            'spheres'       : ['MenuItem', menu_show_spheres],
                                            'dynamic bonds' : ['MenuItem', menu_show_dynamic_bonds],
                                            'separator2'    : ['separator', None],
                                            'nonbonded'     : ['MenuItem', None],
                    
                                           }
                               ],
                    
                    
                    'hide'   : [
                                'submenu',  {
                                            'lines'    : ['MenuItem', menu_hide_lines],
                                            'sticks'   : ['MenuItem', menu_hide_sticks],
                                            'spheres'  : ['MenuItem', menu_hide_spheres],
                                            'dynamic bonds' : ['MenuItem', menu_hide_dynamic_bonds],

                                            'nonbonded': ['MenuItem', None],
                                            }
                                ],
                    
                    
                    'separator2':['separator', None],

                    }




        self.glwidget.build_glmenu(bg_menu   = bg_menu, 
                                   sele_menu = sele_menu, 
                                   obj_menu  = obj_menu,
                                   pick_menu = pick_menu )

    



    def restart_session (self, filename = None):
        """ Function doc """
        
        self.main_session.window.destroy()
        self.main_session = None
        self.__init__(glwidget = True, toolkit = 'gtk3')
        self.treestore = Gtk.TreeStore(
                                                str , # Name
                                                
                                                bool, # toggle active=1
                                                bool, # radio  active=2
                                                
                                                bool, # toggle visible = 3
                                                bool, # radio  visible = 4
                                                
                                                int , # vobject index
                                                bool, # is vobject index visible?
                                                int , # pdynamo system index 
                                                bool, # is pdynamo system index visible?
                                                )
        self.parents = {}
        self.insert_glmenu()

        #self.main_session.window.destroy()
        window = EasyHybridMainWindow(self)


        #Gtk.main()

    def load_easyhybrid_data_to_session (self, easyhybrid_session_data):
        """ Function doc """
        
    
    def pDynamo_selections (self):
        """ Function doc """
        
        #atomref = AtomSelection.FromAtomPattern( self.cSystem, _centerAtom )
        #core    = AtomSelection.Within(self.cSystem,atomref,_radius)
        #core2   = AtomSelection.ByComponent(self.cSystem,core)
        #self.cSystem = PruneByAtom( self.cSystem , Selection(core2) )
        ##---------------------------------------------------
        #self.cSystem.label = self.baseName + "#{} Pruned System ".format(self.systemCoutCurr) 
        #self.cSystem.DefineNBModel( self.nbModel )
        #self.cSystem.Energy()





def main():
    
    #vm_session  =  VisMolSession(glwidget = True, toolkit = 'gtk3')
    vm_session  =  EasyHybridVismolSession(glwidget = True, toolkit = 'gtk3')
    
    vm_session.treestore = Gtk.TreeStore(
                                            str  ,   #                                   # 0
                                            bool ,   # toggle active=1                   # 1
                                            bool ,   # toggle visible = 3                # 2 
                                                                                         
                                            bool ,   # radio  active  = 2                # 3      
                                            bool ,   # radio  visible = 4                # 4     
                                                                                         
                                            bool  ,  # traj radio  active = 5            # 5        
                                            bool  ,  # is trajectory radio visible?      # 6          
                                                                                         
                                            int,     #                                   # 7
                                            int,     # pdynamo system index              # 8
                                            int,)    # frames  # 9
    
    
    
    vm_session.combobox_starting_coordinates = Gtk.ComboBox()
    vm_session.filechooser_working_folder    = Gtk.FileChooserButton()
    vm_session.starting_coords_liststore     = Gtk.ListStore(str, int)
    
    
    
    
    
    
    
    
    
    '''
    vm_session.treestore = Gtk.TreeStore(
                                        str , # Name
                                        
                                        bool, # toggle active=1
                                        bool, # radio  active=2
                                        
                                        bool, # toggle visible = 3
                                        bool, # radio  visible = 4
                                        
                                        bool, # radio  active = 5 
                                        #int , # vobject index
                                        bool, # is trajectory toogle visible?
                                        int , # pdynamo system index 
                                        bool, # is pdynamo system index visible?
                                        )
    '''
    vm_session.parents = {}
    vm_session.insert_glmenu()
    window = EasyHybridMainWindow(vm_session)
    Gtk.main()
 

if __name__ == '__main__':
    main()

