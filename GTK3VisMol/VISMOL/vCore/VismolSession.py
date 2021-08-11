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
from VISMOL.vModel import VismolObject
#from VISMOL.vBabel import PDBFiles
from VISMOL.vBabel import PDBFiles
from VISMOL.vBabel import GROFiles

from VISMOL.vBabel import MOL2Files
from VISMOL.vBabel import XYZFiles
from VISMOL.vBabel import NewObj
from VISMOL.vBabel import AUXFiles
from VISMOL.vBabel import AMBERFiles
from VISMOL.vBabel import PSFFiles

from VISMOL.vCore.VismolSelections  import VisMolPickingSelection as vPick
from VISMOL.vCore.VismolSelections  import VisMolViewingSelection as vSele
from VISMOL.vCore.vConfig           import VisMolConfig 

import VISMOL.glCore.shapes as shapes
import time






from VISMOL.vModel.Representations   import LinesRepresentation
from VISMOL.vModel.Representations   import NonBondedRepresentation
from VISMOL.vModel.Representations   import SticksRepresentation
from VISMOL.vModel.Representations   import DotsRepresentation
from VISMOL.vModel.Representations   import SpheresRepresentation
from VISMOL.vModel.Representations   import GlumpyRepresentation
from VISMOL.vModel.Representations   import RibbonsRepresentation
from VISMOL.vModel.Representations   import SurfaceRepresentation
from VISMOL.vModel.Representations   import WiresRepresentation
from VISMOL.vModel.Representations   import LabelRepresentation

from VISMOL.vModel.Representations   import DynamicBonds
from VISMOL.vModel.Representations   import CartoonRepresentation


from GTKGUI.gtkWidgets.VismolTools import VismolGoToAtomWindow2
from GTKGUI.gtkWidgets.VismolTools import VismolTrajectoryFrame
from GTKGUI.gtkWidgets.filechooser import FileChooser
from GTKGUI.gtkWidgets.player import PlayerFrame


from pprint import pprint




#from VISMOL.gtkWidgets.main_treeview import GtkMainTreeView, FileChooser
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
            if _type in ['lines','sticks','ribbons']:
                if _type == 'lines':
                    if show:
                        atom.lines = True        
                    else:         
                        atom.lines = False 

                if _type == 'sticks':
                    if show:
                        atom.sticks = True        
                    else:         
                        atom.sticks = False 

           
            #               A T O M S 
            else:
                if _type == 'nonbonded':
                    if show:
                        atom.nonbonded = True
                    else:
                        atom.nonbonded = False

                if _type == 'dots':
                    if show:
                        atom.dots = True
                    else:
                        atom.dots = False

                if _type == 'spheres':
                    #print (atom.name, atom.index, atom.Vobject.name)
                    if show:
                        atom.spheres = True
                    else:
                        atom.spheres = False










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
            #print("Vobject.name:",vobject.name)

            if _type in ['lines','sticks','ribbons']:
                #----------------------------------------------------------------   
                
                indexes_bonds = []
                
                for bond in vobject.bonds:
                    
                    if _type == 'lines':
                        
                        if bond.atom_i.lines  and  bond.atom_j.lines:
                            indexes_bonds.append(bond.atom_index_i)
                            indexes_bonds.append(bond.atom_index_j)
                        else:
                            pass
                    
                    if _type == 'sticks':
                        if bond.atom_i.sticks  and  bond.atom_j.sticks:
                            indexes_bonds.append(bond.atom_index_i)
                            indexes_bonds.append(bond.atom_index_j)
                        else:
                            pass
                #----------------------------------------------------------------   
                
                if vobject.representations[_type] is None:
                    #print(vobject.representations[_type])
                    #if indexes_bonds == []:
                    #    pass
                    #
                    #
                    #else:
                    #print(indexes_bonds)
                    rep  = SticksRepresentation    (name    = _type, 
                                                    active  = True, 
                                                    _type   = 'mol', 
                                                    visObj  = vobject, 
                                                    glCore  = self.glwidget.vm_widget,
                                                    indexes = indexes_bonds)
                                                    
                    vobject.representations[rep.name] = rep 
                    #print(vobject.representations[_type])
                
                else:

                    if indexes_bonds == []:
                        vobject.representations[_type].active = False
                        pass
                    
                    else:
                        indexes_bonds = np.array(indexes_bonds, dtype=np.uint32)
                        #print (indexes_bonds)
                        vobject.representations[_type].define_new_indexes_to_VBO ( indexes_bonds)
                        vobject.representations[_type].active = True
                


            #           nonbond  spheres  dots
            else:   
                
                indexes = []
                if _type == 'dots':
                    indexes = []
                    
                    for atom in vobject.atoms:
                        
                        if atom.dots:
                            index = vobject.atoms.index(atom)
                            indexes.append(index)
                        else:
                            pass

                    if vobject.representations[_type] is None:
                        #print(vobject.representations[_type])
                        rep  = DotsRepresentation    (name    = _type, 
                                                      active  = True, 
                                                      _type   = 'mol', 
                                                      visObj  = vobject, 
                                                      glCore  = self.glwidget.vm_widget,
                                                      indexes = indexes)
                                                        
                        vobject.representations[rep.name] = rep 
                    
                    else:

                        if indexes  == []:
                            vobject.representations[_type].active = False
                            pass
                        
                        else:
                            indexes = np.array(indexes, dtype=np.uint32)
                            #print (indexes)
                            vobject.representations[_type].define_new_indexes_to_VBO ( indexes)
                            vobject.representations[_type].active = True


                if _type == 'nonbonded':
                    pass
                
                if  _type == 'spheres':
                    
                    atoms2spheres = []
                    for atom in vobject.atoms:
                        if atom.spheres:
                            atoms2spheres.append(atom)
                            index = vobject.atoms.index(atom)
                            #indexes.append(atom.index-1)
                            indexes.append(index)
                        else:                   
                            pass



                    if vobject.representations['spheres'] is None:
                        #print(vobject.representations[_type])
 
                        rep  = SpheresRepresentation    (name    = _type, 
                                                         active  = True, 
                                                         _type   = 'mol', 
                                                         visObj  = vobject, 
                                                         glCore  = self.glwidget.vm_widget,
                                                         atoms   = atoms2spheres
                                                         )
                        
                        #print ('len', len(atoms2spheres))
                        rep._create_sphere_data()                                
                        vobject.representations[rep.name] = rep 
                        
                        #print(vobject.representations[_type])
                    else:
                        if atoms2spheres == []:
                            vobject.representations[_type].active = False
                            #self.glwidget.queue_draw()
                            pass

                        else:
                            vobject.representations[_type].atoms = atoms2spheres
                            vobject.representations[_type]._create_sphere_data() 
                            vobject.representations[_type]._update_sphere_data_to_VBOs ()                               
                            vobject.representations[_type].active = True
                            #self.glwidget.queue_draw()
                    #self.glwidget.queue_draw()
        self.glwidget.queue_draw()



class VisMolSession (ShowHideVisMol):
    """ Class doc """

    def __init__ (self, glwidget = False, toolkit = 'gtk3', main_session = None):
        """ Class initialiser """
        #self.vismol_objects         = [] # self.vismol_objects
        #self.vismol_objects_dic     = {} # self.vismol_objects_dic   
        self.main_session = None
        self.toolkit = toolkit
        
        self.vismol_objects     = [] # old Vobjects
        self.vismol_objects_dic = {}
        
        self.atom_id_counter  = 0  # 
        self.atom_dic_id      = {
                                # atom_id : obj_atom 
                                 }
        

        #---------------------------------------------------------------------------
        # gl stuffs
        #---------------------------------------------------------------------------
        
        self.vConfig =  VisMolConfig(self)
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
        
        self.toolkit = toolkit
        if glwidget:
            if toolkit == 'gtk3':
                #from VISMOL.glWidget import gtk3 as VisMolGLWidget
                from VISMOL.glWidget import VisMolGLWidget
                self.glwidget   = VisMolGLWidget.GtkGLAreaWidget(self)
                self.glwidget.vm_widget.queue_draw()
                
                '''This gtk list is declared in the VismolGLWidget file 
                   (it does not depend on the creation of Treeview)'''
                self.Vismol_Objects_ListStore = self.glwidget.Vismol_Objects_ListStore
                
                
                self.Vismol_selection_modes_ListStore = self.glwidget.Vismol_selection_modes_ListStore
                data = ['atom'   , 
                        'residue',
                        'chain'  , 
                        'segment' 
                        ]
                for i in data:
                    self.Vismol_selection_modes_ListStore.append([i])
                
                #self.player = PlayerFrame(self)
                #self.player_frame = self.player.main_frame
                #self.player.show_player_main_window ()
                
                self.go_to_atom_window = VismolGoToAtomWindow2( vismolSession = self)
                TrajectoryFrame        = VismolTrajectoryFrame( vismolSession = self)
                self.trajectory_frame  = TrajectoryFrame.get_box()
                #self.go_to_atom_window.show_window()
                
            
            if toolkit == 'qt4':
                self.glwidget   = VisMolGLWidget.QtGLWidget(self)
        else:
            self.glwidget = None
        #---------------------------------------------------------------------------
        
        # GTK WIDGETS 

        
        
        
        
        
        # F R A M E
        self.frame = 0
        
        
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
        
        #---------------------------------------------------------------
        #  PICKING SELECTIONS
        #---------------------------------------------------------------
        self.picking_selections =  vPick(self)
        
    
    
    
    
    
    

        #self.insert_glmenu()
























        # not used yet
        self.indexes = {'nonbonded' : False,
                              'lines'   : True,
                              'spheres' : False,
                              'sticks'  : False,
                              'ribbons' : True,
                              'surface' : False,
                              }

    def teste2 (self, teste = None):
        """ Function doc """
        
        #vismol_object = self.vismol_objects[-1]
        #
        #print('  funcao teste 2  ', len(vismol_object.atoms))
        #
        #vismol_object._add_new_atom_to_vobj (name          = 'O',  
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
        #                                     Vobject       =   vismol_object )
        #
        #frame = []
        #for atom in vismol_object.atoms:
        #    vismol_object.non_bonded_atoms.append(atom.index-1)
        #    for coord  in atom.pos:
        #        print (coord)
        #        #print (atom.pos)
        #        frame.append(coord)
        #print('len', len(frame))
        #frame =    np.array(frame, dtype=np.float32)
        #vismol_object.frames = [frame]
        
        ##-----------------------------------------------------------------------
        ## Modifying an existing atom 
        #vismol_object.atoms[0].name = "N" 
        #vismol_object.atoms[0].define_atom_symbol ( vismol_object.atoms[0].name)
        #vismol_object.atoms[0].get_color()
        #vismol_object._generate_color_vectors()
        ##self.vismol_objects.append(vismol_object)
        #vismol_object._get_center_of_mass()
        ##-----------------------------------------------------------------------
        ##index_bonds = [0,1, 2,3, 3,4 , 0,4, 1,3]
        #
        #
        #
        ##----------------------------------------------------------------------
        #vismol_object.index_bonds.append(2) #bonds_full_indexes
        #vismol_object.index_bonds.append(1) #bonds_full_indexes
        #bonds_pair_of_indexes      = [[2,1]]
        #vismol_object.import_bonds(bonds_pair_of_indexes)

        #----------------------------------------------------------------------
        vismol_object0 = self.vismol_objects[0]
        print('before',vismol_object0.index_bonds)

        vismol_object0.index_bonds.append(0)
        vismol_object0.index_bonds.append(24)
        print('after',vismol_object0.index_bonds)
        vismol_object0.representations['lines'].define_new_indexes_to_VBO ( vismol_object0.index_bonds)
        #-----------------------------------------------------------------------
        
        #vismol_object = self.vismol_objects[-1]
        #vismol_object.index_bonds.append(0)
        #vismol_object.index_bonds.append(1) #bonds_full_indexes
        #bonds_pair_of_indexes = [[0,1]] 
        #vismol_object.import_bonds(bonds_pair_of_indexes)
        
            
        #rep  = LinesRepresentation (name = 'lines', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
        #self.vismol_objects[-1].representations[rep.name] = rep
        #
        #rep  = NonBondedRepresentation (name = 'nonbonded', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
        #self.vismol_objects[-1].representations[rep.name] = rep
        ##self.append_vismol_object_to_vismol_objects_listStore(self.vismol_objects[-1])
        #
        #from pprint import pprint
        #pprint(vismol_object.chains)
    
    def teste (self, teste = None):
        """ Function doc """
        from VISMOL.vModel.Atom              import Atom
        from VISMOL.vModel.Chain             import Chain
        from VISMOL.vModel.Residue           import Residue
        print('  funcao teste   ')
        vismol_object  = NewObj.create_empty_vismol_obj (infile = None, vismolSession = self, gridsize = 3)
        vismol_object.set_model_matrix(self.glwidget.vm_widget.model_mat)        
        vismol_object.active = True
        
        for i in range(1,3):
            vismol_object._add_new_atom_to_vobj (name          = 'C',  
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
                                                 Vobject       =   vismol_object )
            
            
        
        frame = []
        for atom in vismol_object.atoms:
            vismol_object.non_bonded_atoms.append(atom.index-1)
            for coord  in atom.pos:
                frame.append(coord)
        
        
        frame =    np.array(frame, dtype=np.float32)
        
        vismol_object.frames = [frame]
        vismol_object._generate_color_vectors()
        self.vismol_objects.append(vismol_object)
        vismol_object._get_center_of_mass()

        
        
        vismol_object.index_bonds  = [0,1] #bonds_full_indexes
        bonds_pair_of_indexes      = [[0,1]]
        vismol_object.import_bonds(bonds_pair_of_indexes)
        
            
        rep  = LinesRepresentation (name = 'lines', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
        self.vismol_objects[-1].representations[rep.name] = rep

        rep  = NonBondedRepresentation (name = 'nonbonded', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
        self.vismol_objects[-1].representations[rep.name] = rep
        self.append_vismol_object_to_vismol_objects_listStore(self.vismol_objects[-1])

    
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
        initial       = time.time()
        if selection:
            pass
        else:
            selection = self.selections[self.current_selection]
        
        Vobject = selection.selected_atoms[0].Vobject
        
        index_bonds_dynamic = []
        
        for i in range (0, len(Vobject.frames)):
            
            indexes = []
            
            n = 1
            for atom1 in selection.selected_atoms:
            
                for atom2 in selection.selected_atoms[n:]:
            
                    dist = self._get_distance_atom1_atom2 (  atom1, atom2, i)
                    if dist <= (atom1.cov_rad + atom2.cov_rad)*1.1 :
                        #print ( atom1.name, atom2.name,atom1.index, atom2.index, dist, atom1.cov_rad + atom2.cov_rad, atom1.index, atom2.index, True)
                        indexes.append(atom1.index-1)
                        indexes.append(atom2.index-1)
    
                    else:
                        pass#print ( atom1.name, atom2.name, dist, atom1.cov_rad + atom2.cov_rad, atom1.index, atom2.index, False)
                n += 1

            indexes = np.array(indexes,dtype=np.uint32)
            index_bonds_dynamic.append(indexes)        
        
        Vobject.dynamic_bons = index_bonds_dynamic
        final = time.time()                                            #
        
        
        rep  = DynamicBonds (name = 'dynamic', active = True, _type = 'mol', visObj = Vobject, glCore = self.glwidget.vm_widget)
        Vobject.representations[rep.name] = rep
        
        print ('Bonds calcultation time : ', final - initial, '\n')    #

    def import_player_widget (self):
        """ Function doc """
        
    
    def insert_glmenu (self, bg_menu  = None, 
                            sele_menu = None, 
                             obj_menu = None, 
                            pick_menu = None):
        """ Function doc """
        



        def _viewing_selection_mode_atom (_):
            """ Function doc """
            self.viewing_selection_mode(selmode = 'atom')
        def _viewing_selection_mode_residue (_):
            """ Function doc """
            self.viewing_selection_mode(selmode = 'residue')
        def _viewing_selection_mode_chain (_):
            """ Function doc """
            self.viewing_selection_mode(selmode = 'chain')

        def _selection_type_picking(_):
            
            self._picking_selection_mode = True
            self.glwidget.queue_draw()
        
        def _selection_type_viewing(_):
            self._picking_selection_mode = False
            self.glwidget.queue_draw()

        if sele_menu is None:
            ''' Standard Sele Menu '''
            
            def dynamic_test (_):
                """ Function doc """
                self.teste3()
            
            def select_test (_):
                """ Function doc """
                self.select(indexes = 'all')
            
            def menu_show_lines (_):
                """ Function doc """
                self.show_or_hide( _type = 'lines', show = True)

            def menu_hide_lines (_):
                """ Function doc """
                print('hide')
                self.show_or_hide( _type = 'lines', show = False)

            def menu_show_sticks (_):
                """ Function doc """
                self.show_or_hide( _type = 'sticks', show = True)

            def menu_hide_sticks (_):
                """ Function doc """
                self.show_or_hide( _type = 'sticks', show = False)

            def menu_show_spheres (_):
                """ Function doc """
                self.show_or_hide( _type = 'spheres', show = True)

            def menu_hide_spheres (_):
                """ Function doc """
                self.show_or_hide( _type = 'spheres', show = False)


            sele_menu = { 
                    'header' : ['MenuItem', None],
                    
                    
                    
                    'separator1':['separator', None],
                    
                    
                    'show'   : [
                                'submenu' ,{
                                            
                                            'lines'         : ['MenuItem', menu_show_lines],
                                            'sticks'        : ['MenuItem', menu_show_sticks],
                                            'spheres'       : ['MenuItem', menu_show_spheres],
                                            'dynamic bonds' : ['MenuItem', dynamic_test],
                                            'separator2'    : ['separator', None],
                                            'nonbonded'     : ['MenuItem', None],
                    
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
                print('ebaaaa')
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
                                            
                                            'Atoms'     :  ['MenuItem', _viewing_selection_mode_atom],
                                            'Residue'   :  ['MenuItem', _viewing_selection_mode_residue],
                                            'Chain'     :  ['MenuItem', _viewing_selection_mode_chain],
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
                                            
                                            'Atom index'   : ['MenuItem', None],
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
                                            'dynamic bonds' : ['MenuItem', dynamic_test],
                                            'separator2'    : ['separator', None],
                                            'nonbonded'     : ['MenuItem', None],
                    
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
            self._show_lines (visObj = self.vismol_objects[obj], 
                                       indexes = indexes)       
        
        if cmd[0] == 'hide':
            self._hide_lines (visObj = self.vismol_objects[obj], 
                                       indexes = indexes)  
        
        self.ctrl = True
        
        
        print (entry)

    def load (self, infile, widget = None, autocenter = True):
        """ Function doc """
        #Vobject_id = len(self.vismol_objects)
        print ('load')
        
        rep1 = True
        
        if infile[-3:] == 'gro':
            self._load_gro_file(infile = infile)
        
        if infile[-3:] == 'top' or infile[-6:] == 'prmtop':
            self._load_amber_top_file(infile = infile)
            rep1 = False
        
        if infile[-3:] == 'psf':
            self._load_psf_file(infile = infile)
            rep1 = False
            
        if infile[-3:] == 'pdb':
            self._load_pdb_file(infile = infile)
        
        if infile[-4:] == 'mol2':
            self._load_mol2_file(infile = infile)
        
        if infile[-3:] == 'xyz':
            self._load_xyz_file(infile = infile)
        
        if infile[-3:] == 'aux':
            self._load_aux_file(infile = infile)
        
        self.vismol_objects[-1].active = True
        
        if self.toolkit == 'gtk':
            print(self.vismol_objects)
        
        #This function adds new structures to "Vismol_Objects_ListStore"
        self.append_vismol_object_to_vismol_objects_listStore(self.vismol_objects[-1])
        
        
        
        
        if rep1:
            #self.vismol_objects[-1].generate_indexesresentations (reps_list = self.indexes)
            #print (self.vismol_objects[-1].representations)

            #rep =  RibbonsRepresentation(name = 'ribbons', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
            #self.vismol_objects[-1].representations[rep.name] = rep
            
            rep  = LinesRepresentation (name = 'lines', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
            self.vismol_objects[-1].representations[rep.name] = rep
            #
            rep  = NonBondedRepresentation (name = 'nonbonded', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
            self.vismol_objects[-1].representations[rep.name] = rep
            
            #rep  = SticksRepresentation (name = 'sticks', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
            #self.vismol_objects[-1].representations[rep.name] = rep
            
            #rep  = DynamicBonds (name = 'dynamic', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
            #self.vismol_objects[-1].representations[rep.name] = rep
            
            #self.vismol_objects[-1]
            
            
            
            '''Representation of fake spheres using shaders. Each sphere is actually a point'''
            #rep  = GlumpyRepresentation (name = 'glumpy', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
            #self.vismol_objects[-1].representations[rep.name] = rep

            '''Simple dot representation'''
            #rep  = DotsRepresentation (name = 'dots', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
            #self.vismol_objects[-1].representations[rep.name] = rep
            
            #rep  = SpheresRepresentation (name = 'spheres', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
            #self.vismol_objects[-1].representations[rep.name] = rep
            
            #rep =  RibbonsRepresentation(name = 'ribbons', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
            #self.vismol_objects[-1].representations[rep.name] = rep
            
            #rep =  CartoonRepresentation(name = 'cartoon', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
            #self.vismol_objects[-1].representations[rep.name] = rep
            
            rep =  LabelRepresentation(name = 'label', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
            self.vismol_objects[-1].representations[rep.name] = rep
            
            #rep =  SurfaceRepresentation(name = 'surface', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
            #self.vismol_objects[-1].representations[rep.name] = rep

            #rep =  WiresRepresentation(name = 'wires', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
            #self.vismol_objects[-1].representations[rep.name] = rep

            #self.glwidget.queue_draw()
           
            #if self.toolkit == 'gtk3':
            #    self.refresh_gtk(widget)
            #visObj = vismolSession.vismol_objects[-1]
            
            
            # after opening a new object, center the camera on this new object
            if autocenter:
                print(self.vismol_objects[-1].mass_center)
                self.glwidget.vm_widget.center_on_coordinates(self.vismol_objects[-1], self.vismol_objects[-1].mass_center)
            

            
            '''
            print(self.vismol_objects[-1].c_alpha_atoms)
            self.vismol_objects[-1].get_backbone_indexes()
            
            
            
            for atom in self.vismol_objects[-1].c_alpha_atoms:
                print(atom.index, atom.name, atom.resn, atom.resi, atom.coords())
            '''
            

    
    
    def load_xyz_coords_to_vismol_obejct (self, infile, visObj, autocenter = True):
        """ Function doc """
        if infile[-3:] == 'gro':
            frames = self._load_gro_coords_to_vismol_object(infile, visObj)
                                                                   
        if infile[-3:] == 'pdb':                                  
            frames = self._load_pdb_coords_to_vismol_object(infile, visObj)
        
        if infile[-4:] == 'mol2':
            frames = self._load_mol2_coords_to_vismol_object(infile , visObj)
        
        if infile[-3:] == 'xyz':
            frames = self._load_xyz_coords_to_vismol_object(infile , visObj)
        
        if infile[-3:] == 'crd':
            frames = self._load_crd_coords_to_vismol_object(infile , visObj)
        
        if infile[-3:] == 'net' or infile[-2:] == 'nc' or infile[-6:] == 'netcdf' or infile[-6:] == 'rst7f':
            frames = self._load_netcdf4_coords_to_vismol_object(infile , visObj)
            
        if infile[-3:] == 'aux':
            frames = self._load_aux_coords_to_vismol_object(infile , visObj)

        if autocenter:
            visObj._get_center_of_mass(frame = 0)
            print(visObj.mass_center)
            self.glwidget.vm_widget.center_on_coordinates(visObj, visObj.mass_center)

            rep  = LinesRepresentation (name = 'lines', active = True, _type = 'mol', visObj = visObj, glCore = self.glwidget.vm_widget)
            visObj.representations[rep.name] = rep

            rep  = NonBondedRepresentation (name = 'nonbonded', active = True, _type = 'mol', visObj = visObj, glCore = self.glwidget.vm_widget)
            visObj.representations[rep.name] = rep



    
    def append_vismol_object_to_vismol_objects_listStore(self, visObj):
        """ This function adds new structures to "Vismol_Objects_ListStore". 
        The Vismol_Objects_ListStore is created in the VisMolGLWidget 
        file and does not depend on the maintreeview of the main window. """
        
        i = self.vismol_objects.index(visObj)

        data = [visObj.active          , 
                str(i)                 ,
                visObj.name            , 
                str(len(visObj.atoms)) , 
                str(len(visObj.frames)),
                ]
        #print (data)
        self.Vismol_Objects_ListStore.append(data)
      
    
    def _load_gro_coords_to_vismol_object(self, infile , visObj = None):
        """ Function doc """
        pass
        
        
    def _load_netcdf4_coords_to_vismol_object(self, infile , visObj = None):
        print( infile , visObj)
        frames = AMBERFiles.load_netcdf4_file(infile, visObj)
        #visObj.frames+=frames
        #print ('system size: ', len(visObj.atoms),'frame size: ',len(frames[0])/3)
        
        for frame in frames:
            visObj.frames.append(frame) 
            
    def _load_crd_coords_to_vismol_object(self, infile , visObj = None):
        print( infile , visObj)
        frames = AMBERFiles.load_amber_crd_file(infile, visObj)
        print ('system size: ', len(visObj.atoms),'frame size: ',len(frames[0])/3)
        for frame in frames:
            visObj.frames.append(frame) 
    
    def _load_pdb_coords_to_vismol_object(self, infile , visObj = None):
        """ Function doc """
        frames = PDBFiles.load_pdb_file (infile = infile, vismolSession = self, frames_only = True) 
        
        print ('system size: ', len(visObj.atoms),'frame size: ',len(frames[0])/3)
        for frame in frames:
            visObj.frames.append(frame)    
        #print (visObj.mass_center)
        #if visObj.mass_center == None:
        
        #visObj._get_center_of_mass(visObj.frames[-1])
        #print (visObj.mass_center)

    def _load_gro_file (self, infile):
        #print(infile)
        vismol_object  = GROFiles.load_gro_file (infile = infile, vismolSession = self)     
        vismol_object.set_model_matrix(self.glwidget.vm_widget.model_mat)        
        self.vismol_objects.append(vismol_object)
        
    
    def _load_amber_top_file (self, infile):
        #print(infile)
        vismol_object  = AMBERFiles.load_amber_topology_file (infile = infile, vismolSession = self)     
        vismol_object.set_model_matrix(self.glwidget.vm_widget.model_mat)        
        self.vismol_objects.append(vismol_object)
    
    def _load_psf_file (self, infile):
        #print(infile)
        vismol_object  = PSFFiles.load_PSF_topology_file (infile = infile, vismolSession = self)     
        vismol_object.set_model_matrix(self.glwidget.vm_widget.model_mat)        
        self.vismol_objects.append(vismol_object)
    
    def _load_pdb_file (self, infile):
        """ Function doc """      
        print(infile)
        vismol_object  = PDBFiles.load_pdb_file (infile = infile, vismolSession = self)     
        
        #self._load_pdb_coords_to_vismol_object(infile , vismol_object)
        
        vismol_object.set_model_matrix(self.glwidget.vm_widget.model_mat)        
        self.vismol_objects.append(vismol_object)
        
        #print(vismol_object.atoms)
        #print(vismol_object.atoms2)
        '''
        vismol_object.atoms2             = atoms # this is a raw list : [0, 'C5', 0.77, array([ 0.295,  2.928, -0.407]), 1, 'GLC', ' ', 'C ', [1, 12, 8, 10], [0, 0, 0]]
        #-----------------------------------------------------------------

        vismol_object.atoms              = []    # this a list ao atom objects!
        vismol_object.residues           = {}
        vismol_object.chains             = {}
        vismol_object.frames             = trajectory
        vismol_object.atom_unique_id_dic = {}



        #-----------------------#
        #         Bonds         #
        #-----------------------#
        vismol_object.index_bonds        = []
        vismol_object.bonds              = []                        

        #-----------------------#
        #    Calpha  Ribbons    #
        #-----------------------#
        vismol_object.c_alpha_bonds      = []           
        
        #-----------------------#
        #       Nonbonded       #
        #-----------------------#
        vismol_object.non_bonded_atoms   = []
        
        vismol_object.residues_in_protein = []
        vismol_object.residues_in_solvent = []
        vismol_object.residues_ligands    = []

        vismol_object.atoms_in_protein = [] # a list of atoms belonging to a protein
        vismol_object.atoms_in_solvent = []
        '''


    def _load_aux_file (self, infile):
        """ Function doc """
        print(infile)
        vismol_object  = AUXFiles.load_aux_file (infile = infile, vismolSession = self)
        vismol_object.set_model_matrix(self.glwidget.vm_widget.model_mat)        
        self.vismol_objects.append(vismol_object)


    def _load_mol2_file (self, infile):
        """ Function doc """
        print(infile)
        vismol_object  = MOL2Files.load_mol2_files (infile = infile, vismolSession = self)
        vismol_object.set_model_matrix(self.glwidget.vm_widget.model_mat)        
        self.vismol_objects.append(vismol_object)
        
    
    def _load_xyz_file (self, infile):
        """ Function doc """
        #load_xyz_file
        print(infile)
        vismol_object  = XYZFiles.load_xyz_file (infile = infile, vismolSession = self)
        vismol_object.set_model_matrix(self.glwidget.vm_widget.model_mat)        
        self.vismol_objects.append(vismol_object)
    
    '''
    def delete_by_index(self, index = None):
        """ Function doc """
        self.viewing_selections = []
        self.picking_selections = [None]*4        
        self.vismol_objects.pop(index)
        #self.glwidget.updateGL()
    #''' 
    
    def select (self, vismol_object =  None, indexes = [], sele = None):
        """ Function doc """
        print('select',vismol_object, indexes, sele )
        
        self.get_distance()
        
        if vismol_object:
            pass
        else:
            vismol_object = self.vismol_objects[-1]
            
        #pprint(vismol_object.atoms_by_chains)
        
        if sele == None:
            sele = self.current_selection
        else:
            pass
            
        if indexes == 'all':
            self.selections[sele].selecting_by_indexes (vismol_object = vismol_object, 
                                                              indexes = range(0, int(len(vismol_object.atoms)/2)) 
                                                              )
            
            #for atom in vismol_object.atoms:
            #    atom.selected = True
            
            #self.selections[sele].build_selected_atoms_coords_and_selected_objects_from_selected_atoms()
        
        
        #for index in  
        
        self.glwidget.queue_draw()
        
    def orient (self, obj =  None):
        """ Function doc """  
    
    def center (self, visObj):
        """ Function doc """
        print ('center', visObj)
        frame = self.get_frame ()
        visObj._get_center_of_mass (frame)
        self.glwidget.vm_widget.center_on_coordinates(visObj, visObj.mass_center)


    def center_by_index(self, Vobject =  None, index = None):
        """ Function doc """  
        mass_center = self.vismol_objects[index].mass_center
        #self.glwidget.center_on_atom(mass_center)

    def disable_by_index (self, index = 0):
        self.vismol_objects[index].active = False
        #self.glwidget.draw()
        self.glwidget.queue_draw()
            
    def enable_by_index (self, index = 0):
        """ Function doc """
        self.vismol_objects[index].active = True
        #self.glwidget.draw()
        self.glwidget.queue_draw()
    
    def edit_by_index(self, index = 0):
        """ Function doc """
        self.vismol_objects[index].editing = not self.vismol_objects[index].editing
        #self.glwidget.queue_draw()
    
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
        
    def get_vobject_list (self):
        """ Function doc """
        Vobjects_dic = {}
    
        for Vobject in self.vismol_objects:
            #print ('----------------------- > get_vobject_list ', Vobject.label)
            index = self.vismol_objects.index(Vobject)
            name = Vobject.label
            #print( '\n label get_vobject_list:', name, index, len(Vobject.atoms) )
            Vobjects_dic[index] = name
    
        return Vobjects_dic

   
    def viewing_selection_mode(self, selmode = 'atom'):
        """ Function doc """        
        print(selmode)
        self.selections[self.current_selection]._selection_mode = selmode
    
    '''
    def selection_function (self, pickedID):
        """ Function doc """
        print('selection_function')

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
    
    def _selection_function (self, selected):
        #"""     P I C K I N G     S E L E C T I O N S     """
        print('_selection_function')
        if self._picking_selection_mode:
            self.picking_selections.selection_function_picking(selected)
        
        #"""     V I E W I N G     S E L E C T I O N S     """
        else:
            self.selections[self.current_selection].selection_function_viewing(selected)

       

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
        #self.vismolSession  =  VisMolSession(glwidget = True, toolkit = 'gtk3')       
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
