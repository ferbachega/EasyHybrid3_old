#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  molecular_model.py
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
#from visual import gl_draw_area as gda, vis_parser

#from   GLarea.vis_parser import load_pdb_files, parse_xyz
#import GLarea.molecular_model as mm

#from vis_parser import load_pdb_files

#from pprint import pprint
#from GLarea.GLWidget   import GLWidget
from vModel import VismolObject
#from vModel import VismolGeometricObject
#from vBabel import PDBFiles
from vBabel import PDBFiles
from vBabel import GROFiles

from vBabel import MOL2Files
from vBabel import XYZFiles
from vBabel import NewObj
from vBabel import AUXFiles
from vBabel import AMBERFiles
from vBabel import PSFFiles

from vCore.VismolSelections  import VisMolPickingSelection as vPick
from vCore.VismolSelections  import VisMolViewingSelection as vSele
from vCore.vConfig           import VisMolConfig 

import glCore.shapes as shapes
import time
import ctypes
from OpenGL import GL





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


from GTKGUI.gtkWidgets.VismolTools import VismolGoToAtomWindow2
from GTKGUI.gtkWidgets.VismolTools import VismolStatusBar
from GTKGUI.gtkWidgets.VismolTools import VismolTrajectoryFrame
from GTKGUI.gtkWidgets.VismolTools import VismolSelectionTypeBox

from GTKGUI.gtkWidgets.filechooser import FileChooser
from GTKGUI.gtkWidgets.player import PlayerFrame


from pprint import pprint




#from gtkWidgets.main_treeview import GtkMainTreeView, FileChooser
import numpy as np

import os

class ShowHideVisMol:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        pass
#'''
    def change_attributes_for_selected_atoms(self, _type = 'lines', atoms = [], show = True ):
        for atom in atoms:

            #               B O N D S
            if _type in ['lines', 'dotted_lines', 'sticks','ribbons']:
                if _type == 'lines':
                    if show:
                        atom.lines = True        
                    else:         
                        atom.lines = False 
                
                if _type == 'dotted_lines':
                    if show:
                        atom.dotted_lines = True        
                    else:         
                        atom.dotted_lines = False 

                if _type == 'sticks':
                    if show:
                        atom.sticks = True        
                    else:         
                        atom.sticks = False 
                        ##print(atom.index, atom.name, atom.sticks)
                
                if _type == 'ribbons':
                    if show:
                        atom.ribbons = True        
                    else:         
                        atom.ribbons = False 
                        ##print(atom.index, atom.name, atom.sticks)
           
            #               A T O M S 
            else:
                if _type == 'nonbonded':
                    
                    if len(atom.bonds) != 0:
                        pass
                    else:
                        if show:
                            atom.nonbonded = True
                        else:
                            atom.nonbonded = False
                    #else:
                    #    atom.nonbonded = True
                    #print(atom.name, atom.nonbonded)
                
                if _type == 'dots':
                    if show:
                        atom.dots = True
                    else:
                        atom.dots = False

                if _type == 'spheres':
                    #print (atom.name, atom.index, atom.vobject.name)
                    if show:
                        atom.spheres = True
                    else:
                        atom.spheres = False

                if _type == 'dynamic_bonds':
                    #print (atom.name, atom.index, atom.vobject.name)
                    if show:
                        atom.dynamic_bonds = True
                    else:
                        atom.dynamic_bonds = False

    def _dots_show_or_hide (self, vobject):
        """ Function doc """
        pass
        #indexes = []
        #for atom in vobject.atoms:
        #    if atom.dots:
        #        index = vobject.atoms.index(atom)
        #        indexes.append(index)
        #    else:
        #        pass
        #
        #
        #
        #if vobject.representations['dots'] is None:            
        #    rep  = DotsRepresentation    (name    = 'dots', 
        #                                  active  = True, 
        #                                  _type   = 'mol', 
        #                                  vobject  = vobject, 
        #                                  glCore  = self.glwidget.vm_widget,
        #                                  indexes = indexes)
        #                                    
        #    vobject.representations['dots'] = rep 
        #else:
        #
        #    if indexes  == []:
        #        vobject.representations[_type].active = False
        #        pass
        #    
        #    else:
        #        indexes = np.array(indexes, dtype=np.uint32)
        #        vobject.representations[_type].define_new_indexes_to_VBO ( indexes)
        #        vobject.representations[_type].active = True

    def _nonbonded_show_or_hide (self, vobject):
        """ Function doc """
        indexes = []
        for atom in vobject.atoms:
            if atom.nonbonded:
                index = vobject.atoms.index(atom)
                indexes.append(index)
            else:
                pass

        if vobject.representations['nonbonded'] is None:
            ##print(vobject.representations[_type])
            rep  = NonBondedRepresentation    (name    = 'nonbonded', 
                                               active  = True, 
                                               _type   = 'mol', 
                                               vobject  = vobject, 
                                               glCore  = self.glwidget.vm_widget,
                                               indexes = indexes)
                                            
            vobject.representations['nonbonded'] = rep 
        
        else:

            if indexes  == []:
                vobject.representations['nonbonded'].active = False
                pass
            
            else:
                indexes = np.array(indexes, dtype=np.uint32)
                #print (indexes)
                vobject.representations['nonbonded'].define_new_indexes_to_VBO ( indexes)
                vobject.representations['nonbonded'].active = True                

    def _spheres_show_or_hide (self, vobject):
        """ Function doc """
        #_type = 'spheres_instance'
        indexes = []
        atoms2spheres = []
        for atom in vobject.atoms:
            if atom.spheres:
                atoms2spheres.append(atom)
                index = vobject.atoms.index(atom)
                indexes.append(index)
            else:                   
                pass



        if vobject.representations['spheres'] is None:
            if atoms2spheres !=[]:
                rep  = SpheresRepresentation    (name    = 'spheres', 
                                                        active  = True, 
                                                        _type   = 'mol', 
                                                        vobject  = vobject, 
                                                        glCore  = self.glwidget.vm_widget,
                                                       indexes  = indexes
                                                        )
                
                #rep._create_sphere_data()                                
                vobject.representations['spheres'] = rep 
            else:
                #print ('494 pass')
                pass
        else:
            if atoms2spheres == []:
                #print ('498 active = False')
                vobject.representations['spheres'].active = False
                pass

            else:
                #print ('503 update_atomic_indexes')
                vobject.representations['spheres'].update_atomic_indexes(indexes = indexes)
                vobject.representations['spheres'].active = True

    def _dynamic_bonds_show_or_hide (self, vobject, selection, show = True, find_dynamic_bonds = True):
        """ Function doc """
        
        if show:
            atom_list = selection
            if find_dynamic_bonds:
                vobject.find_dynamic_bonds (atom_list = atom_list, 
                                       index_list = None     , 
                                           update = False    )
            else:
                pass
            
            if vobject.representations['dynamic_bonds']:
                vobject.representations['dynamic_bonds'].active = True
            
            else:
                rep  = DynamicBonds (name  = 'dynamic', 
                            active = True, 
                            _type  = 'mol', 
                            vobject = vobject, 
                            glCore = self.glwidget.vm_widget)
                vobject.representations['dynamic_bonds'] = rep

        else:
            atom_list = []
            if vobject.representations['dynamic_bonds']:
                vobject.representations['dynamic_bonds'].active = False
            else:
                return None

    def _ribbons_show_or_hide (self, vobject):
        """ Function doc """
        indexes_bonds = []
        
        if vobject.c_alpha_bonds == []:
            vobject.get_backbone_indexes ()
            
            if vobject.c_alpha_bonds == []:
                return None
                #self.active =  False
            else:
                pass

        
        for bond in vobject.c_alpha_bonds:
            if bond.atom_i.ribbons  and  bond.atom_j.ribbons:
                indexes_bonds.append(bond.atom_index_i)
                indexes_bonds.append(bond.atom_index_j)
            else:
                pass



        if vobject.representations['ribbons']:

            if indexes_bonds == []:
                vobject.representations['ribbons'].active = False
            else:
                vobject.representations['ribbons'].active = False
                #vobject.representations['sticks'].define_new_indexes_to_VBO ( indexes_bonds)
                rep  = RibbonsRepresentation   (name    = 'ribbons', 
                                                active  = True, 
                                                _type   = 'mol', 
                                                vobject  = vobject, 
                                                glCore  = self.glwidget.vm_widget,
                                                indexes = indexes_bonds)
                vobject.representations['ribbons'] = rep
                
        
        else:
            rep  = RibbonsRepresentation   (name    = 'ribbons', 
                                            active  = True, 
                                            _type   = 'mol', 
                                            vobject  = vobject, 
                                            glCore  = self.glwidget.vm_widget,
                                            indexes = indexes_bonds)
            vobject.representations['ribbons'] = rep 

    def _sticks_show_or_hide (self, vobject):
        """ Function doc """
        indexes_bonds = []
        metal_indexes_bonds = []
        for bond in vobject.bonds:
            if bond.atom_i.sticks  and  bond.atom_j.sticks:
                if bond.has_metal:
                    metal_indexes_bonds.append(bond.atom_index_i)
                    metal_indexes_bonds.append(bond.atom_index_j)
                else:
                    indexes_bonds.append(bond.atom_index_i)
                    indexes_bonds.append(bond.atom_index_j)
            else:
                pass



        if vobject.representations['sticks']:

            if indexes_bonds == []:
                vobject.representations['sticks'].active = False
            else:
                vobject.representations['sticks'].active = False
                #vobject.representations['sticks'].define_new_indexes_to_VBO ( indexes_bonds)
                rep  = SticksRepresentation     (name    = 'sticks', 
                                                active  = True, 
                                                _type   = 'mol', 
                                                vobject  = vobject, 
                                                glCore  = self.glwidget.vm_widget,
                                                indexes = indexes_bonds)
                vobject.representations['sticks'] = rep
                
        
        else:
            rep  = SticksRepresentation     (name    = 'sticks', 
                                            active  = True, 
                                            _type   = 'mol', 
                                            vobject  = vobject, 
                                            glCore  = self.glwidget.vm_widget,
                                            indexes = indexes_bonds)
            vobject.representations['sticks'] = rep 

    def _lines_show_or_hide (self, vobject):
        """ Function doc """
        indexes_bonds       = []
        metal_indexes_bonds = []
        #print('UHUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU')
        for bond in vobject.bonds:
            if bond.atom_i.lines  and  bond.atom_j.lines:
                if bond.has_metal:
                    metal_indexes_bonds.append(bond.atom_index_i)
                    metal_indexes_bonds.append(bond.atom_index_j)
                else:
                    indexes_bonds.append(bond.atom_index_i)
                    indexes_bonds.append(bond.atom_index_j)
            else:
                pass


        '''-----------------------------------------------------------------------------------'''
        if vobject.representations['lines']:
        
            if indexes_bonds == []:
                vobject.representations['lines'].active = False
            else:
                vobject.representations['lines'].define_new_indexes_to_VBO ( indexes_bonds)
                #vobject.representations['lines'].active = False
                #rep  = LinesRepresentation     (name    = 'lines', 
                #                            active  = True, 
                #                            _type   = 'mol', 
                #                            vobject  = vobject, 
                #                            glCore  = self.glwidget.vm_widget,
                #                            indexes = indexes_bonds)
                #vobject.representations['lines'] = rep
                
        
        else:
            rep  = LinesRepresentation     (name    = 'lines', 
                                            active  = True, 
                                            _type   = 'mol', 
                                            vobject  = vobject, 
                                            glCore  = self.glwidget.vm_widget,
                                            indexes = indexes_bonds)
            vobject.representations['lines'] = rep 
        '''-----------------------------------------------------------------------------------'''
        
    def _dotted_lines_show_or_hide (self, vobject):

        #indexes_bonds       = []
        metal_indexes_bonds = []
        for bond in vobject.bonds:
            #if bond.atom_i.dotted_lines  and  bond.atom_j.dotted_lines:
            if bond.has_metal:
                #print(bond.atom_i.name, bond.atom_j.name)
                #if bond.has_metal:
                metal_indexes_bonds.append(bond.atom_index_i)
                metal_indexes_bonds.append(bond.atom_index_j)
                #else:
                #    indexes_bonds.append(bond.atom_index_i)
                #    indexes_bonds.append(bond.atom_index_j)
            else:
                pass

        '''-----------------------------------------------------------------------------------'''
        print ('metal_indexes_bonds', metal_indexes_bonds, vobject.metal_bonded_atoms)
        if vobject.representations['dotted_lines']:
            #print('AQUIII   1')
            if metal_indexes_bonds == []:
                vobject.representations['dotted_lines'].active = False
            else:
                vobject.representations['dotted_lines'].define_new_indexes_to_VBO ( metal_indexes_bonds)
        
        else:
            #print('AQUIII   2')
            rep  = LinesRepresentation     (name    = 'dotted_lines', 
                                            active  = True, 
                                            _type   = 'mol', 
                                            vobject  = vobject, 
                                            glCore  = self.glwidget.vm_widget,
                                            indexes = metal_indexes_bonds)
            vobject.representations['dotted_lines'] = rep

        '''-----------------------------------------------------------------------------------'''
            




    def show_or_hide (self, _type = 'lines', selection = None,  show = True ):
        """ Function doc """

        if selection:
            pass
        else:
            selection = self.selections[self.current_selection]
        
        self.change_attributes_for_selected_atoms (_type = _type , 
                                                   atoms = selection.selected_atoms,  
                                                    show = show)
      
        
        for vobject in selection.selected_objects:

            if _type == 'lines':
                self._lines_show_or_hide (vobject)
            
            elif _type == 'dotted_lines':
                self._dotted_lines_show_or_hide (vobject)
            
            elif _type == 'sticks':
                self._sticks_show_or_hide (vobject)
                
            elif _type == 'dynamic_bonds':
                self._dynamic_bonds_show_or_hide(vobject, selection.selected_atoms, show = show)

            elif _type == 'dots':
                self._dots_show_or_hide (vobject)

            elif _type == 'nonbonded':
                self._nonbonded_show_or_hide(vobject)

            elif  _type == 'spheres':
                self._spheres_show_or_hide(vobject)
            
            elif  _type == 'ribbons':
                self._ribbons_show_or_hide(vobject)
            else:
                pass
        self.glwidget.queue_draw()

    def show_or_hide_by_object (self, _type = 'lines', vobject = None,  selection_table = [], show = True, find_dynamic_bonds = True):
        """ Function doc """
        atoms = []
        
        for atom_index in selection_table:
            atoms.append(vobject.atoms[atom_index])
        self.change_attributes_for_selected_atoms (_type = _type , 
                                                   atoms = atoms,  
                                                    show = show)
        if _type == 'lines':
            self._lines_show_or_hide (vobject)

        elif _type == 'dotted_lines':
            self._dotted_lines_show_or_hide (vobject)

        elif _type == 'sticks':
            self._sticks_show_or_hide (vobject)
            
        elif _type == 'dynamic_bonds':
            self._dynamic_bonds_show_or_hide(vobject, atoms, show = show, find_dynamic_bonds = find_dynamic_bonds)

        elif _type == 'dots':
            self._dots_show_or_hide (vobject)

        elif _type == 'nonbonded':
            self._nonbonded_show_or_hide(vobject)

        elif  _type == 'spheres':
            self._spheres_show_or_hide(vobject)
        
        elif  _type == 'ribbons':
            self._ribbons_show_or_hide(vobject)
        else:
            pass
        self.glwidget.queue_draw()

class VisMolSession (ShowHideVisMol):
    """ Class doc """

    def __init__ (self, glwidget = False, toolkit = 'gtk3', main_session = None):
        """ Class initialiser """
        #self.vobjects     = [] # self.vobjects
        #self.vobjects_dic = {} # self.vobjects_dic   
        self.main_session = None
        self.toolkit      = toolkit
        self.vConfig      = VisMolConfig(self)

        self.vobjects     = [] # old vobjects - include molecules
        self.vobjects_dic = {} # old vobjects dic - include molecules
        self.vobj_counter       = 0  # Each vismol object has a unique access key (int), which is generated in the method: add_vobject_to_vismol_session.
        self.vismol_geometric_object     = []
        self.vm_session_vbos = []

        self.vismol_geometric_object_dic = {
                                           'pk1pk2' :  None,
                                           'pk2pk3' :  None,
                                           'pk3pk4' :  None,
                                           }
        
        self.atom_id_counter  = 0  # 
        self.atom_dic_id      = {
                                # atom_id : obj_atom 
                                 }
        
        self._picking_selection_mode = False # True/False  - interchange between viewing  and picking mode
        #---------------------------------------------------------------
        #  VIEWING SELECTIONS
        #---------------------------------------------------------------
        selection = vSele(self)
        #selection._selection_mode ='chain' # 'atom'
        self.selections = {
                          'sel01' : selection
                          }
        self.current_selection = 'sel01'
        #---------------------------------------------------------------------------
        
        #---------------------------------------------------------------
        #  PICKING SELECTIONS
        #---------------------------------------------------------------
        self.picking_selections =  vPick(self)
        
        
        
        #---------------------------------------------------------------------------
        # F R A M E
        self.frame = 0
        #---------------------------------------------------------------------------
        

        #---------------------------------------------------------------------------
        # gl stuffs
        #---------------------------------------------------------------------------
        
        '''
        self.gl_parameters      =     {
                                      
                                      'dot_size'                   : 5        ,
                                      'line_width'                 : 1        ,
                                      'sphere_scale'               : 0.85     ,
                                      'stick_scale'                : 1.5      ,
                                      'ball_and_sick_sphere_scale' : 1        ,
                                      'antialias'                  : False    ,
                                      'bg_color'                   : [255,255,255,1],
                                      'center_on_coord_sleep_time' : 0.001    ,
                      }
        '''
        #---------------------------------------------------------------------------
        # GTK WIDGETS
        #---------------------------------------------------------------------------
         
        self.toolkit = toolkit
        if glwidget:
            if toolkit == 'gtk3':
                self.selection_box_frane = None
                #from glWidget import gtk3 as VisMolGLWidget
                from glWidget import VisMolGLWidget
                self.glwidget   = VisMolGLWidget.GtkGLAreaWidget(self)
                self.glwidget.vm_widget.queue_draw()
                
                self.gtk_widgets_update_list = []
                
                '''This gtk list is declared in the VismolGLWidget file 
                   (it does not depend on the creation of Treeview)'''
                self.Vismol_Objects_ListStore = self.glwidget.Vismol_Objects_ListStore
                
                
                self.Vismol_selection_modes_ListStore = self.glwidget.Vismol_selection_modes_ListStore
                data = ['atom'   , 
                        'residue',
                        'chain'  , 
                        'protein', 
                        'C alpha',
                        'solvent',
                        'atom name',
                        'element',
                        #'segment' 
                        ]
                for i in data:
                    self.Vismol_selection_modes_ListStore.append([i])
                
                #self.player = PlayerFrame(self)
                #self.player_frame = self.player.main_frame
                #self.player.show_player_main_window ()
                statusbar             = VismolStatusBar(vm_session = self)
                self.statusbar         = statusbar.statusbar
                self.go_to_atom_window = VismolGoToAtomWindow2( vm_session = self)
                self.TrajectoryFrame        = VismolTrajectoryFrame( vm_session = self)
                self.trajectory_frame  = self.TrajectoryFrame.get_box()
                
                self.selection_box_frane = VismolSelectionTypeBox( vm_session = self)
                self.selection_box       = self.selection_box_frane.box
                #self.go_to_atom_window.show_window()
                
                self.gtk_widgets_update_list.append(self.go_to_atom_window)
                self.gtk_widgets_update_list.append(self.TrajectoryFrame)
                self.gtk_widgets_update_list.append(self.selection_box_frane)
                
            if toolkit == 'qt4':
                self.glwidget   = VisMolGLWidget.QtGLWidget(self)
        else:
            self.glwidget = None
        
        self.gtk_treeview_iters = []


    def gtk_widgets_update (self):
        """ Function doc """
        for widget in self.gtk_widgets_update_list:
            widget.update()
            
            

    def teste2 (self, teste = None):
        """ Function doc """
        
        #vobject = self.vobjects[-1]
        #
        ##print('  funcao teste 2  ', len(vobject.atoms))
        #
        #vobject._add_new_atom_to_vobj (name          = 'O',  
        #                                     index         =  3 ,
        #                                     pos           =  [3,0,4] ,
        #                                     resi          =  1       ,
        #                                     resn          =  'UNK'   ,
        #                                     chain         =   "A"    ,
        #                                     atom_id       =  self.atom_id_counter ,
        #                                     occupancy     =   0 ,
        #                                     bfactor       =   0 ,
        #                                     charge        =   0 ,
        #                                     bonds_indexes =   [] ,
        #                                     vobject       =   vobject )
        #
        #frame = []
        #for atom in vobject.atoms:
        #    vobject.non_bonded_atoms.append(atom.index-1)
        #    for coord  in atom.pos:
        #        print (coord)
        #        #print (atom.pos)
        #        frame.append(coord)
        ##print('len', len(frame))
        #frame =    np.array(frame, dtype=np.float32)
        #vobject.frames = [frame]
        
        ##-----------------------------------------------------------------------
        ## Modifying an existing atom 
        #vobject.atoms[0].name = "N" 
        #vobject.atoms[0].define_atom_symbol ( vobject.atoms[0].name)
        #vobject.atoms[0].get_color()
        #vobject._generate_color_vectors()
        ##self.vobjects.append(vobject)
        #vobject._get_center_of_mass()
        ##-----------------------------------------------------------------------
        ##index_bonds = [0,1, 2,3, 3,4 , 0,4, 1,3]
        #
        #
        #
        ##----------------------------------------------------------------------
        #vobject.index_bonds.append(2) #bonds_full_indexes
        #vobject.index_bonds.append(1) #bonds_full_indexes
        #bonds_pair_of_indexes      = [[2,1]]
        #vobject.import_bonds(bonds_pair_of_indexes)

        #----------------------------------------------------------------------
        vobject0 = self.vobjects[0]
        #print('before',vobject0.index_bonds)

        vobject0.index_bonds.append(0)
        vobject0.index_bonds.append(24)
        #print('after',vobject0.index_bonds)
        vobject0.representations['lines'].define_new_indexes_to_VBO ( vobject0.index_bonds)
        #-----------------------------------------------------------------------
        
        #vobject = self.vobjects[-1]
        #vobject.index_bonds.append(0)
        #vobject.index_bonds.append(1) #bonds_full_indexes
        #bonds_pair_of_indexes = [[0,1]] 
        #vobject.import_bonds(bonds_pair_of_indexes)
        
            
        #rep  = LinesRepresentation (name = 'lines', active = True, _type = 'mol', vobject = self.vobjects[-1], glCore = self.glwidget.vm_widget)
        #self.vobjects[-1].representations[rep.name] = rep
        #
        #rep  = NonBondedRepresentation (name = 'nonbonded', active = True, _type = 'mol', vobject = self.vobjects[-1], glCore = self.glwidget.vm_widget)
        #self.vobjects[-1].representations[rep.name] = rep
        ##self.append_vobject_to_vobjects_listStore(self.vobjects[-1])
        #
        #from pprint import pprint
        #p#print(vobject.chains)
    
    def teste (self, teste = None):
        """ Function doc """
        from vModel.Atom              import Atom
        from vModel.Chain             import Chain
        from vModel.Residue           import Residue
        #print('  funcao teste   ')
        vobject  = NewObj.create_empty_vismol_obj (infile = None, vm_session = self, gridsize = 3)
        vobject.set_model_matrix(self.glwidget.vm_widget.model_mat)        
        vobject.active = True
        
        for i in range(1,3):
            vobject._add_new_atom_to_vobj (name          = 'C',  
                                                 index         =  i ,
                                                 pos           =  [i,i,i] ,
                                                 resi          =  1       ,
                                                 resn          =  'UNK'   ,
                                                 chain         =   "A"    ,
                                                 atom_id       =  self.atom_id_counter ,
                                                 occupancy     =   0 ,
                                                 bfactor       =   0 ,
                                                 charge        =   0 ,
                                                 bonds_indexes =   [] ,
                                                 vobject       =   vobject )
            
            
        
        frame = []
        for atom in vobject.atoms:
            vobject.non_bonded_atoms.append(atom.index-1)
            for coord  in atom.pos:
                frame.append(coord)
        
        
        frame =    np.array(frame, dtype=np.float32)
        
        vobject.frames = [frame]
        vobject._generate_color_vectors()
        self.vobjects.append(vobject)
        vobject._get_center_of_mass()

        
        
        vobject.index_bonds  = [0,1] #bonds_full_indexes
        bonds_pair_of_indexes      = [[0,1]]
        vobject.import_bonds(bonds_pair_of_indexes)
        
            
        rep  = LinesRepresentation (name = 'lines', active = True, _type = 'mol', vobject = self.vobjects[-1], glCore = self.glwidget.vm_widget)
        self.vobjects[-1].representations[rep.name] = rep

        rep  = NonBondedRepresentation (name = 'nonbonded', active = True, _type = 'mol', vobject = self.vobjects[-1], glCore = self.glwidget.vm_widget)
        self.vobjects[-1].representations[rep.name] = rep
        self.append_vobject_to_vobjects_listStore(self.vobjects[-1])

    
    def _get_distance_atom1_atom2 (self, atom1, atom2, frame = None):
        """ Function doc """
        if frame:
            pass
        else:
            frame = self.get_frame()
        
        coords1 =  atom1.coords(frame)
        coords2 =  atom2.coords(frame)
        
        x1 = coords1[0]
        y1 = coords1[1]
        z1 = coords1[2]
        
        x2 = coords2[0]
        y2 = coords2[1]
        z2 = coords2[2]
        
        dx = x1 - x2
        dy = y1 - y2
        dz = z1 - z2
        
        dist = (dx**2 + dy**2+ dz**2)**0.5
        return dist
    
    def teste3 (self,  selection = None):
        """ Function doc """
        selection = self.selections[self.current_selection]
        #initial       = time.time()
        vobject = selection.selected_atoms[0].vobject
        vobject.find_dynamic_bonds (atom_list = selection.selected_atoms, index_list = None, update = True )
        #final = time.time()                                            #
        rep  = DynamicBonds (name = 'dynamic', active = True, _type = 'mol', vobject = vobject, glCore = self.glwidget.vm_widget)
        vobject.representations[rep.name] = rep
        #print ('Bonds calcultation time : ', final - initial, '\n')    #
        
        '''
        initial       = time.time()
        if selection:
            pass
        else:
            selection = self.selections[self.current_selection]
        
        #print(selection)
        vobject = selection.selected_atoms[0].vobject
        
        index_bonds_dynamic = []
        
        
        parameters = []
        
        for i in range (0, len(vobject.frames)):
            
            
            
            indexes = []

            
            bonds_by_pairs = vobject.find_bonded_and_nonbonded_by_selection(selection = selection.selected_atoms, 
                                                                                frame = i,  
                                                                             gridsize = self.vConfig.gl_parameters['gridsize'],
                                                                            tolerance = self.vConfig.gl_parameters['bond_tolerance'])
            #print(bonds_by_pairs)
            
            #for i in range(0,len(bonds_by_pairs), 2 )#pair_of_indexes  in bonds_by_pairs:
            #    indexes.append(pair_of_indexes[0])
            #    indexes.append(pair_of_indexes[1])

            indexes = np.array(bonds_by_pairs,dtype=np.uint32)
            #indexes = np.array(indexes,dtype=np.uint32)
            index_bonds_dynamic.append(indexes)        
        
        vobject.dynamic_bonds = index_bonds_dynamic
        final = time.time()                                            #
        
        
        rep  = DynamicBonds (name = 'dynamic', active = True, _type = 'mol', vobject = vobject, glCore = self.glwidget.vm_widget)
        vobject.representations[rep.name] = rep
        
        print ('Bonds calcultation time : ', final - initial, '\n')    #
        '''

    def calculate_secondary_structure(self, vobject):
        '''
            First, the distances d2i, d3i and d4i between the (i - 1)th
            residue and the (i + 1)th, the (i + 2)th and the (i + 3)th,
            respectively, are computed from the cartesian coordinates
            of the Ca carbons, as well as the angle ti and dihedral angle
            ai defined by the Ca carbon triplet (i - 1, i , i + 1) and
            quadruplet (i - 1, i, i + 1, i + 2), respectively.
            
            
            Assignment parameters
                                       Secondary structure
                                       
                                       Helix        Strand
                                       
            Angle T (°)               89 ± 12       124 ± 14
            Dihedral angle a (°)      50 ± 20      -170 ± 4 5
                                                   
            Distance d2 (A)           5.5 ± 0.5    6.7 ± 0.6
            Distance d3 (A)           5.3 ± 0.5    9.9 ± 0.9
            Distance d4 (A)           6.4 ± 0.6    12.4 ± 1.1

 
        '''
        if vobject.c_alpha_bonds == [] or vobject.c_alpha_atoms == []:
            vobject.get_backbone_indexes()
        
        #for atom in vobject.c_alpha_atoms:
            #print(atom.index, atom.name, atom.bonds_indexes, atom.bonds)
        

        size = len(vobject.c_alpha_bonds)
        SSE_list  = ['C']
        SSE_list2 = []
        
        
        block     = [0,0,1]
        SS_before = 1
        for i in range(1,size -3):
            
            CA0 = vobject.c_alpha_bonds[i-1].atom_i # i - 1
            CA1 = vobject.c_alpha_bonds[i-1].atom_j # i
            
            CA2 = vobject.c_alpha_bonds[i].atom_i   # i
            CA3 = vobject.c_alpha_bonds[i].atom_j   # i + 1
                                                   
            CA4 = vobject.c_alpha_bonds[i+1].atom_i # i + 1
            CA5 = vobject.c_alpha_bonds[i+1].atom_j # i + 2
                                                   
            CA6 = vobject.c_alpha_bonds[i+2].atom_i # i + 2
            CA7 = vobject.c_alpha_bonds[i+2].atom_j # i + 3
                                                   
            CA8 = vobject.c_alpha_bonds[i+3].atom_i # i + 3 
            CA9 = vobject.c_alpha_bonds[i+3].atom_j #


            if CA1 == CA2 and CA3 == CA4 and CA5 == CA6 and CA7 == CA8:
                #print ('CA1 = CA2')
                
                # distances
                d2i  = LA.subtract(CA0.coords(), CA3.coords()) 
                d2i  = LA.length(d2i)
                
                d3i  = LA.subtract(CA1.coords(), CA5.coords()) 
                d3i  = LA.length(d3i)
                
                d4i  = LA.subtract(CA3.coords(), CA7.coords()) 
                d4i  = LA.length(d4i)
                
                # angle
                v0   = LA.subtract(CA0.coords(), CA1.coords())
                v1   = LA.subtract(CA1.coords(), CA3.coords())
                
                ti   = 57.295779513*(LA.angle(v0, v1))
                
                # dihedral 
                ai   = 57.295779513*(LA.dihedral(CA0.coords(), CA1.coords(), CA3.coords(), CA5.coords()))
                
                
                
                SS = None
                
                if 77.0 <= ti <= 101 and 30 <= ai <= 70:
                    ##print(CA1.resi, CA1.name, CA1.resn, CA1.name, 'H', d2i, d3i, d4i, ti,  ai)
                    SS = 1
                
                if 110.0 <= ti <= 138 and -215 <= ai <= -125:
                    ##print(CA1.resi, CA1.name, CA1.resn, CA1.name, 'S', d2i, d3i, d4i, ti,  ai)
                    SS = 2
                
                '''
                if 5.0 <= d2i <= 6.0:
                    ##print('d2i', d2i)
                    
                    if 4.8 <= d3i <= 5.8:
                        ##print('d3i', d3i)

                        if 5.8 <= d4i <= 7.0:
                            ##print('d4i', d4i)

                            if 77.0 <= ti <= 101:
                                
                                if 30 <= ai <= 70:
                                    #print(CA1.resi, CA1.name, CA1.resn, CA1.name, 'H', d2i, d3i, d4i, ti,  ai)
                                    SS = 'H'
          
                         
                if 6.1 <= d2i <= 7.3:
                    ##print('d2i', d2i)
                    
                    if 9.0 <= d3i <= 10.8:
                        ##print('d3i', d3i)

                        if 11.3 <= d4i <= 13.5:
                            ##print('d4i', d4i)

                            if 110.0 <= ti <= 138:
                                if -215 <= ai <= -125:
                                    #print(CA1.resi, CA1.name, CA1.resn, CA1.name, 'S', d2i, d3i, d4i, ti,  ai)
                                    SS = 'S'
                '''
                
                if SS:
                    pass
                else:
                    SS = 0 
                #print(CA1.resi, CA1.name, CA1.resn, CA1.name, SS, d2i, d3i, d4i, ti,  ai)
                
                SSE_list.append(SS)
                
                
                if SS == SS_before:
                    block[2] += 1
                
                else:
                    SSE_list2.append(block)
                    SS_before = SS
                    
                    block = [SS, CA1.resi-1, CA1.resi]
                
            
        #print(SSE_list2)
        return SSE_list2 
    
    
    def import_player_widget (self):
        """ Function doc """
        
    
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
            
            def select_test (_):
                """ Function doc """
                self.select(indexes = 'all')
            
            def menu_show_lines (_):
                """ Function doc """
                self.show_or_hide( _type = 'lines', show = True)

            def menu_hide_lines (_):
                """ Function doc """
                ##print('hide')
                self.show_or_hide( _type = 'lines', show = False)

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
            
            def set_as_qc_atoms (_):
                """ Function doc """
                selection         = self.selections[self.current_selection]

                pdmsys_active =   self.main_session.p_session.active_id
                self.main_session.p_session.systems[pdmsys_active]['qc_table'] = []
                
                for atom in selection.selected_atoms:
                    #print(atom.index-1, atom.name, atom.resn)
                    self.main_session.p_session.systems[pdmsys_active]['qc_table'].append(atom.index -1)
                #print('selection_qc',self.main_session.p_session.systems[pdmsys_active]['qc_table'] )
                self.main_session.run_dialog_set_QC_atoms()

            def set_as_free_atoms (_):
                """ Function doc """
                selection         = self.selections[self.current_selection]
                
                # these are the new atoms to bet set as fixed
                freelist = []                
                for atom in selection.selected_atoms:
                    #print(atom.index-1, atom.name, atom.resn)
                    freelist.append(atom.index -1)
                    atom.get_color()  
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
                    self.glwidget.vm_widget.queue_draw()
                #self.main_session.p_session.vismol_selection_qc = selection.copy()

            def set_as_fixed_atoms (_):
                """ Function doc """
                selection         = self.selections[self.current_selection]
                
                # these are the new atoms to bet set as fixed
                fixedlist = []                
                for atom in selection.selected_atoms:
                    #print(atom.index-1, atom.name, atom.resn)
                    fixedlist.append(atom.index -1)
                ##print('selection_free',fixedlist )
                #----------------------------------------------
                
                #Combining with list that the already exists
                pdmsys_active =   self.main_session.p_session.active_id
                
                fixedlist = fixedlist + self.main_session.p_session.systems[pdmsys_active]['fixed_table']
                #guarantee that the atom index appears only once in the list
                fixedlist = list(set(fixedlist)) 
                #print ('fixedlist',fixedlist)
                #sending to pDynamo
                
                refresh = self.main_session.p_session.define_free_or_fixed_atoms_from_iterable (fixedlist)
                #vobject = selection.selected_atoms[0].vobject
                
                if refresh:
                    #self.main_session.p_session.refresh_vobject_qc_and_fixed_representations (
                    #                                                                      vobject = vobject,    
                    #                                                                 fixed_atoms = True         , 
                    #                                                                    QC_atoms = True         ,
                    #                                                                metal_bonds  = True         ,
                    #                                                                      static = True         )
                    
                    
                    self.glwidget.vm_widget.queue_draw()
                #self.main_session.p_session.vismol_selection_qc = selection.copy()
            
            def invert_selection (_):
                """ Function doc """
                #print('self.selections[self.current_selection].invert_selection()')
                self.selections[self.current_selection].invert_selection()
            
            
            sele_menu = { 
                    'header' : ['MenuItem', None],
                    
                    
                    
                    'separator1':['separator', None],
                    
                    
                    'show'   : [
                                'submenu' ,{
                                            
                                            'lines'         : ['MenuItem' , menu_show_lines],
                                            'sticks'        : ['MenuItem' , menu_show_sticks],
                                            'spheres'       : ['MenuItem' , menu_show_spheres],
                                            'dots'          : ['MenuItem' , menu_show_dots],
                                            'dynamic bonds' : ['MenuItem' , menu_show_dynamic_bonds],
                                            'separator2'    : ['separator', None],
                                            'nonbonded'     : ['MenuItem' , menu_show_nonbonded],
                    
                                           }
                               ],
                    
                    
                    'hide'   : [
                                'submenu',  {
                                            'lines'         : ['MenuItem' , menu_hide_lines],
                                            'sticks'        : ['MenuItem' , menu_hide_sticks],
                                            'spheres'       : ['MenuItem' , menu_hide_spheres],
                                            'dots'          : ['MenuItem' , menu_hide_dots],
                                            'dynamic bonds' : ['MenuItem' , menu_hide_dynamic_bonds],
                                            'separator2'    : ['separator', None],
                                            'nonbonded'     : ['MenuItem' , menu_hide_nonbonded],
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

                    
                    'Label Mode':  ['submenu' , {
                                            'Atom'         : [
                                                               'submenu', {
                                                                           'lines'    : ['MenuItem', None],
                                                                           'sticks'   : ['MenuItem', None],
                                                                           'spheres'  : ['MenuItem', None],
                                                                           'nonbonded': ['MenuItem', None],
                                                                           }
                                                              ],
                                            
                                            'Atom index'   : ['MenuItem', None],
                                            'residue name' : ['MenuItem', None],
                                            'residue_index': ['MenuItem', None],
                                           },
                               ]
                    }
      
        if bg_menu is None:
            ''' Standard Bg Menu'''
            
            def open_structure_data (_):
                """ Function doc """
                #print('ebaaaa')
                self.filechooser   = FileChooser()
                filename = self.filechooser.open()
                self.load (filename, widget = None, autocenter = True)


                
            bg_menu = { 
                    'separator0'   :['separator', None],

                    'Open File'    : ['MenuItem', open_structure_data],
                    
                    'select' : ['MenuItem', select_test],

                    'funcao teste' : ['MenuItem', self.teste],                  
                    'funcao teste2': ['MenuItem', self.teste2], 

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
                                            
                                            'Atom index'   : ['MenuItem', None],
                                            'residue name' : ['MenuItem', None],
                                            'residue_index': ['MenuItem', None],
                                           },
                               ]
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

    
    def command_line (self, entry = None):
        """ Function doc """
        cmd = entry.split()
        print (cmd)
        
        obj     = int(cmd[1]            )
        _indexes = cmd[2].split('+')
        indexes = []
        
        
        for index in _indexes:
            indexes.append(int(index))
        
        if cmd[0] == 'show':
            self._show_lines (vobject = self.vobjects[obj], 
                                       indexes = indexes)       
        
        if cmd[0] == 'hide':
            self._hide_lines (vobject = self.vobjects[obj], 
                                       indexes = indexes)  
        
        self.ctrl = True
        
        
        #print (entry)


    def add_vobject_to_vismol_session (self, rep = True, vobject = None, autocenter =  True):
        """ Function doc """
        vobject.index = self.vobj_counter
        #self.vobjects.append(vobject)
        self.vobjects_dic[self.vobj_counter] = vobject
        self.vobj_counter += 1
        
        self.append_vobject_to_vobjects_listStore(vobject)
        
        if rep:
            #self.vobjects[-1].generate_indexesresentations (reps_list = self.indexes)
            #print (self.vobjects[-1].representations)

            #rep =  CartoonRepresentation(name = 'cartoon', active = True, _type = 'mol', vobject = vobject, glCore = self.glwidget.vm_widget)
            #vobject.representations[rep.name] = rep
            
            #rep =  RibbonsRepresentation(name = 'ribbons', active = True, _type = 'mol', vobject = vobject, glCore = self.glwidget.vm_widget)
            #vobject.representations[rep.name] = rep
            
            vobject.create_new_representation (rtype = 'lines')
            vobject.create_new_representation (rtype = 'nonbonded')
            #vobject.create_new_representation (rtype = 'spheresInstace')
            #rep  = LinesRepresentation (name = 'lines', active = True, _type = 'mol', vobject = self.vobjects[-1], glCore = self.glwidget.vm_widget)
            #self.vobjects[-1].representations[rep.name] = rep
            #
            #rep  = NonBondedRepresentation (name = 'nonbonded', active = True, _type = 'mol', vobject = self.vobjects[-1], glCore = self.glwidget.vm_widget)
            #self.vobjects[-1].representations[rep.name] = rep
        
            if autocenter:
                #print(self.vobjects[-1].mass_center)
                self.glwidget.vm_widget.center_on_coordinates(vobject, vobject.mass_center)
            else:
                self.glwidget.vm_widget.queue_draw()
            self.gtk_widgets_update ()


    def load (self, infile, widget = None, autocenter = True):
        """ Function doc """
        #vobject_id = len(self.vobjects)
        #print ('load')
        
        rep1 = True
        
        if infile[-3:] == 'gro':
            vobject = self._load_gro_file(infile = infile)
        
        if infile[-3:] == 'top' or infile[-6:] == 'prmtop':
            vobject = self._load_amber_top_file(infile = infile)
            rep1 = False
        
        if infile[-3:] == 'psf':
            vobject = self._load_psf_file(infile = infile)
            rep1 = False
            
        if infile[-3:] == 'pdb':
            vobject = self._load_pdb_file(infile = infile)
        
        if infile[-4:] == 'mol2':
            vobject = self._load_mol2_file(infile = infile)
        
        if infile[-3:] == 'xyz':
            vobject = self._load_xyz_file(infile = infile)
        
        if infile[-3:] == 'aux':
            vobject = self._load_aux_file(infile = infile)
        
        vobject.active = True
        self.add_vobject_to_vismol_session (
                                                  rep           = rep1, 
                                                  vobject = vobject, 
                                                  autocenter    = True)
        


    
    
    def load_xyz_coords_to_vobject (self, infile, vobject, autocenter = True):
        """ Function doc """
        if infile[-3:] == 'gro':
            frames = self._load_gro_coords_to_vobject(infile, vobject)
                                                                   
        if infile[-3:] == 'pdb':                                  
            frames = self._load_pdb_coords_to_vobject(infile, vobject)
        
        if infile[-4:] == 'mol2':
            frames = self._load_mol2_coords_to_vobject(infile , vobject)
        
        if infile[-3:] == 'xyz':
            frames = self._load_xyz_coords_to_vobject(infile , vobject)
        
        if infile[-3:] == 'crd':
            frames = self._load_crd_coords_to_vobject(infile , vobject)
        
        if infile[-3:] == 'net' or infile[-2:] == 'nc' or infile[-6:] == 'netcdf' or infile[-6:] == 'rst7f':
            frames = self._load_netcdf4_coords_to_vobject(infile , vobject)
            
        if infile[-3:] == 'aux':
            frames = self._load_aux_coords_to_vobject(infile , vobject)

        if autocenter:
            vobject._get_center_of_mass(frame = 0)
            #print(vobject.mass_center)
            self.glwidget.vm_widget.center_on_coordinates(vobject, vobject.mass_center)

            rep  = LinesRepresentation (name = 'lines', active = True, _type = 'mol', vobject = vobject, glCore = self.glwidget.vm_widget)
            vobject.representations[rep.name] = rep

            rep  = NonBondedRepresentation (name = 'nonbonded', active = True, _type = 'mol', vobject = vobject, glCore = self.glwidget.vm_widget)
            vobject.representations[rep.name] = rep



    
    def append_vobject_to_vobjects_listStore(self, vobject):
        """ This function adds new structures to "Vismol_Objects_ListStore". 
        The Vismol_Objects_ListStore is created in the VisMolGLWidget 
        file and does not depend on the maintreeview of the main window. """


        
        if vobject.Type == 'molecule':
            #i = self.vobjects.index(vobject)
            i = vobject.index 
            
            data = [vobject.active           , 
                    str(i)                  ,
                    vobject.name             , 
                    str(len(vobject.atoms))  , 
                    str(len(vobject.frames)) ,
                    ]
            #print (data)
            self.Vismol_Objects_ListStore.append(data)
        else:
            pass
    
    def _load_gro_coords_to_vobject(self, infile , vobject = None):
        """ Function doc """
        pass
        
        
    def _load_netcdf4_coords_to_vobject(self, infile , vobject = None):
        #print( infile , vobject)
        frames = AMBERFiles.load_netcdf4_file(infile, vobject)
        #vobject.frames+=frames
        #print ('system size: ', len(vobject.atoms),'frame size: ',len(frames[0])/3)
        
        for frame in frames:
            vobject.frames.append(frame) 
            
    def _load_crd_coords_to_vobject(self, infile , vobject = None):
        #print( infile , vobject)
        frames = AMBERFiles.load_amber_crd_file(infile, vobject)
        #print ('system size: ', len(vobject.atoms),'frame size: ',len(frames[0])/3)
        for frame in frames:
            vobject.frames.append(frame) 
    
    def _load_pdb_coords_to_vobject(self, infile , vobject = None):
        """ Function doc """
        frames = PDBFiles.load_pdb_file (infile = infile, vm_session = self, frames_only = True) 
        
        #print ('system size: ', len(vobject.atoms),'frame size: ',len(frames[0])/3)
        for frame in frames:
            vobject.frames.append(frame)    
        #print (vobject.mass_center)
        #if vobject.mass_center == None:
        
        #vobject._get_center_of_mass(vobject.frames[-1])
        #print (vobject.mass_center)

    def _load_gro_file (self, infile):
        ##print(infile)
        vobject  = GROFiles.load_gro_file (infile = infile, vm_session = self)     
        vobject.set_model_matrix(self.glwidget.vm_widget.model_mat)        
        return vobject
        #self.vobjects.append(vobject)        
    
    def _load_amber_top_file (self, infile):
        ##print(infile)
        vobject  = AMBERFiles.load_amber_topology_file (infile = infile, vm_session = self)     
        vobject.set_model_matrix(self.glwidget.vm_widget.model_mat)        
        return vobject
        #self.vobjects.append(vobject)    
    def _load_psf_file (self, infile):
        ##print(infile)
        vobject  = PSFFiles.load_PSF_topology_file (infile = infile, vm_session = self)     
        vobject.set_model_matrix(self.glwidget.vm_widget.model_mat)        
        return vobject
        #self.vobjects.append(vobject)    
    def _load_pdb_file (self, infile):
        """ Function doc """      
        #print(infile)
        vobject  = PDBFiles.load_pdb_file (infile = infile, vm_session = self)     
        
        #self._load_pdb_coords_to_vobject(infile , vobject)
        
        vobject.set_model_matrix(self.glwidget.vm_widget.model_mat)        
        return vobject


    def _load_aux_file (self, infile):
        """ Function doc """
        #print(infile)
        vobject  = AUXFiles.load_aux_file (infile = infile, vm_session = self)
        vobject.set_model_matrix(self.glwidget.vm_widget.model_mat)        
        return vobject
        #self.vobjects.append(vobject)

    def _load_mol2_file (self, infile):
        """ Function doc """
        #print(infile)
        vobject  = MOL2Files.load_mol2_files (infile = infile, vm_session = self)
        vobject.set_model_matrix(self.glwidget.vm_widget.model_mat)        
        return vobject
        #self.vobjects.append(vobject)        
    
    def _load_xyz_file (self, infile):
        """ Function doc """
        #load_xyz_file
        #print(infile)
        vobject  = XYZFiles.load_xyz_file (infile = infile, vm_session = self)
        vobject.set_model_matrix(self.glwidget.vm_widget.model_mat)        
        return vobject
        #self.vobjects.append(vobject)
    
    '''
    def delete_by_index(self, index = None):
        """ Function doc """
        self.viewing_selections = []
        self.picking_selections = [None]*4        
        self.vobjects.pop(index)
        #self.glwidget.updateGL()
    #''' 
    
    def select (self, vobject =  None, indexes = [], sele = None):
        """  
        not being used - check later
        """
        #print('select',vobject, indexes, sele )
        
        self.get_distance()
        
        if vobject:
            pass
        else:
            vobject = self.vobjects[-1]
            
        #p#print(vobject.atoms_by_chains)
        
        if sele == None:
            sele = self.current_selection
        else:
            pass
            
        if indexes == 'all':
            self.selections[sele].selecting_by_indexes (vobject = vobject, 
                                                              indexes = range(0, int(len(vobject.atoms)/2)) 
                                                              )
            
            #for atom in vobject.atoms:
            #    atom.selected = True
            
            #self.selections[sele].build_selected_atoms_coords_and_selected_objects_from_selected_atoms()
        
        
        #for index in  
        
        self.glwidget.queue_draw()
        
    def orient (self, obj =  None):
        """ Function doc """  
    
    def center (self, vobject):
        """ Function doc """
        #print ('center', vobject)
        frame = self.get_frame ()
        vobject._get_center_of_mass (frame)
        self.glwidget.vm_widget.center_on_coordinates(vobject, vobject.mass_center)

    def center_by_atomlist (self, atoms = []):
        """ Function doc """
        
        x = 0
        y = 0
        z = 0
        size = len(atoms)
        atom = atoms[0]
        for atom in atoms:
            
            frame = self.get_frame ()
            if frame > len(atom.vobject.frames)-1:
                frame = len(atom.vobject.frames)-1
            else:
                pass
            
            xyz = atom.coords( frame)
            x += xyz[0]
            y += xyz[1]
            z += xyz[2]

        x = x /size
        y = y /size
        z = z /size
        xyz = [x,y,z]
        
        self.glwidget.vm_widget.center_on_coordinates(atom.vobject, xyz)
        

    def center_by_index(self, vobject =  None, index = None):
        """ Function doc """  
        #mass_center = self.vobjects[index].mass_center
        #self.glwidget.center_on_atom(mass_center)
        mass_center = self.vobjects_dic[index].mass_center
        
    def disable_by_index (self, index = 0 ):#, dictionary = False):
        """When the variable "dictionary" is active, the function accesses 
        a vismol object through the dictionary "self.vobjects_dic". 
        Each vismol object has a unique access key (int), which, in 
        easyhybrid, is generated in the method: add_vobject_to_vismol_session.

        In the vismol interface the enable_by_index/disable_by_index methods
        access the vismol objects by their position in the "self.vobjects" 
        list (this is because when an object is deleted in the vismol 
        interface, the treeview's liststore is rewritten) """
        #if dictionary:
        #    self.vobjects_dic[index].active = False
        #else:
        #    self.vobjects[index].active = False
        #self.glwidget.queue_draw()
        
        self.vobjects_dic[index].active = False
        self.glwidget.queue_draw()

    def enable_by_index (self, index = 0):#, dictionary = True):
        """When the variable "dictionary" is active, the function accesses 
        a vismol object through the dictionary "self.vobjects_dic". 
        Each vismol object has a unique access key (int), which, in 
        easyhybrid, is generated in the method: add_vobject_to_vismol_session.

        In the vismol interface the enable_by_index/disable_by_index methods
        access the vismol objects by their position in the "self.vobjects" 
        list (this is because when an object is deleted in the vismol 
        interface, the treeview's liststore is rewritten) """
        
        #if dictionary:
        #    self.vobjects_dic[index].active = True
        #else:
        #    self.vobjects[index].active = True
        #self.glwidget.queue_draw()
        self.vobjects_dic[index].active = True
        self.glwidget.queue_draw()
        
        
    def edit_by_index(self, index = 0):
        """ Function doc """
        #self.vobjects[index].editing = not self.vobjects[index].editing
        self.vobjects_dic[index].editing = not self.vobjects_dic[index].editing
        #self.glwidget.queue_draw()
    

    
    
    def set_color_by_index (self, vobject = None, indexes = [ ], color = [0.9, 0.9, 0.9] ):
        """ Function doc """
        #selection         = self.selections[self.current_selection]
        
        #fixedlist = []
        #if len(indexes) > 0:
        #print ('\n\n\n\n\n\n COLOR')
        for atom_index in indexes:
            vobject.atoms[atom_index].color = color    
            #print(atom_index, color)
        #print(vobject.colors)
        vobject._generate_color_vectors ( do_colors         = True,
                                                do_colors_idx     = False,
                                                do_colors_raindow = False,
                                                do_vdw_dot_sizes  = False,
                                                do_cov_dot_sizes  = False,
                                               )
        #print(vobject.colors)

        self.glwidget.vm_widget.queue_draw()
        for rep  in vobject.representations.keys():
            if vobject.representations[rep]:
                #try:
                vobject.representations[rep]._set_colors_to_buffer()
                #except:
                #    print("VisMol/vModel/Representations.py, line 123, in _set_colors_to_buffer GL.glBindBuffer(GL.GL_ARRAY_BUFFER, ctypes.ArgumentError: argument 2: <class 'TypeError'>: wrong type'")
                    
        return True


        #refresh = self.main_session.p_session.define_free_or_fixed_atoms_from_iterable (fixedlist)
    
    def set_frame (self, frame = 0):
        """ Function doc """
        self.glwidget.vm_widget.frame = frame
        self.glwidget.queue_draw()

        #self.glwidget.updateGL()
    
    def get_distance (self):
        """ Function doc """
        if self._picking_selection_mode:
            print(self.picking_selections.picking_selections_list)
    
    def get_frame (self):
        """ Function doc """
        #""" Function doc """
        frame = self.glwidget.vm_widget.frame
        return frame
    
    '''   
    def get_vobject_dict (self):
        """ Function doc """
        vobjects_dic = {}
    
        for vobj_id, vobject in self.vobjects_dic.items():
            #print ('----------------------- > get_vobject_list ', vobject.label)
            index = self.vobjects.index(vobject)
            name = vobject.label
            ##print( '\n label get_vobject_list:', name, index, len(vobject.atoms) )
            vobjects_dic[index] = name
    
        return vobjects_dic
    '''
   
    def viewing_selection_mode(self, sel_type = 'atom'):
        """ Function doc """        
        
        if self.selection_box_frane:
            self.selection_box_frane.change_sel_type_in_combobox(sel_type)
            
        #print(sel_type)
        self.selections[self.current_selection]._selection_mode = sel_type
    
    '''
    def selection_function (self, pickedID):
        """ Function doc """
        #print('selection_function')

        if pickedID is None:
            selected = None
        else:
            selected = self.atom_dic_id[pickedID]
        
        #"""     P I C K I N G     S E L E C T I O N S     """
        if self._picking_selection_mode:
            self.picking_selections.selection_function_picking(selected)
        
        else:
            self.selections[self.current_selection].selection_function_viewing(selected)
    '''
    
    def _selection_function (self, selected, _type = None, disable = True):
        #"""     P I C K I N G     S E L E C T I O N S     """
        #print('_selection_function')
        if self._picking_selection_mode:
            self.picking_selections.selection_function_picking(selected)
        
        #"""     V I E W I N G     S E L E C T I O N S     """
        else:
            self.selections[self.current_selection].selection_function_viewing(selected, _type, disable)

       

    def start_viewer (self):
        """ Function doc """
        import gi, sys
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk, Gdk
        #----------------------------------------------------------------------------#
        # - - - - - - - - -  GTK STUFFS  - - - - - - - - -               
        self.window = Gtk.Window(title="VisMol window")                  
        #filechooser = FileChooser()                                     
                                         
        self.container = Gtk.Box (orientation = Gtk.Orientation.VERTICAL)
        # - - - - - - - - - - - -  - - - - - - - - - - - -               
                                       
        #---------------------------------------------------------------------------  
        #self.vm_session  =  VisMolSession(glwidget = True, toolkit = 'gtk3')       
        self.container.pack_start(self.glwidget, True, True, 0)         
                                         
        self.window.connect("key-press-event"  , self.glwidget.key_pressed)  
        self.window.connect("key-release-event", self.glwidget.key_released) 
        self.window.add(self.container)                                                    
        #--------------------------------------------------------------------------- #
                                         
        #--------------------------------------------------------------------------- #
        self.window.connect("delete-event",    Gtk.main_quit)                             #
        self.window.show_all()                                                            #
        #----------------------------------------------------------------------------#
        #x = threading.Thread(target = Gtk.main(), args=(1,))
        #x.start()

        Gtk.main()
        
        return None
