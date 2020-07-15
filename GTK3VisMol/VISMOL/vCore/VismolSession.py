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

from VISMOL.vBabel import MOL2Files
from VISMOL.vBabel import XYZFiles

from VISMOL.vCore.VismolSelections  import VisMolPickingSelection as vPick
from VISMOL.vCore.VismolSelections  import VisMolViewingSelection as vSele
from VISMOL.vCore.vConfig           import VisMolConfig 

import VISMOL.glCore.shapes as shapes





from VISMOL.vModel.Representations   import LinesRepresentation
from VISMOL.vModel.Representations   import NonBondedRepresentation
from VISMOL.vModel.Representations   import SticksRepresentation
from VISMOL.vModel.Representations   import DotsRepresentation
from VISMOL.vModel.Representations   import SpheresRepresentation
from VISMOL.vModel.Representations   import GlumpyRepresentation
from VISMOL.vModel.Representations   import RibbonsRepresentation
from VISMOL.vModel.Representations   import SurfaceRepresentation










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
        '''
        for atom in self.selections[self.current_selection].selected_atoms:

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
                
        '''
        
        
        '''
        if _type in ['lines','sticks','ribbons']:
            for atom in self.selections[self.current_selection].selected_atoms:
                for bond in atom.bonds:
                    if bond.atom_i in self.selections[self.current_selection].selected_atoms and bond.atom_j in self.selections[self.current_selection].selected_atoms:

                        if _type == 'lines':
                            if show:
                                bond.line_active  = True
                            else:
                                bond.line_active  = False

                        if _type == 'sticks':
                            if show:
                                bond.stick_active = True        
                            else:
                                bond.stick_active = False        
        '''
        
        
        
        
        
        
        
        
        for vobject in selection.selected_objects:
            #print("Vobject.name:",vobject.name)

            if _type in ['lines','sticks','ribbons']:
                #----------------------------------------------------------------   
                
                indices_bonds = []
                
                for bond in vobject.bonds:
                    
                    if _type == 'lines':
                        
                        if bond.atom_i.lines  and  bond.atom_j.lines:
                            indices_bonds.append(bond.atom_index_i)
                            indices_bonds.append(bond.atom_index_j)
                        else:
                            pass
                    
                    if _type == 'sticks':
                        if bond.atom_i.sticks  and  bond.atom_j.sticks:
                            indices_bonds.append(bond.atom_index_i)
                            indices_bonds.append(bond.atom_index_j)
                        else:
                            pass
                #----------------------------------------------------------------   
                
                if vobject.representations[_type] is None:
                    #print(vobject.representations[_type])
                    #if indices_bonds == []:
                    #    pass
                    #
                    #
                    #else:
                    #print(indices_bonds)
                    rep  = SticksRepresentation    (name    = _type, 
                                                    active  = True, 
                                                    _type   = 'mol', 
                                                    visObj  = vobject, 
                                                    glCore  = self.glwidget.vm_widget,
                                                    indices = indices_bonds)
                                                    
                    vobject.representations[rep.name] = rep 
                    #print(vobject.representations[_type])
                
                else:

                    if indices_bonds == []:
                        vobject.representations[_type].active = False
                        pass
                    
                    else:
                        indices_bonds = np.array(indices_bonds, dtype=np.uint32)
                        #print (indices_bonds)
                        vobject.representations[_type].define_new_indices_to_VBO ( indices_bonds)
                        vobject.representations[_type].active = True
                


            #           nonbond  spheres  dots
            else:   
                
                indices = []
                if _type == 'dots':
                    indices = []
                    
                    for atom in vobject.atoms:
                        
                        if atom.dots:
                            index = vobject.atoms.index(atom)
                            indices.append(index)
                        else:
                            pass

                    if vobject.representations[_type] is None:
                        #print(vobject.representations[_type])
                        rep  = DotsRepresentation    (name    = _type, 
                                                      active  = True, 
                                                      _type   = 'mol', 
                                                      visObj  = vobject, 
                                                      glCore  = self.glwidget.vm_widget,
                                                      indices = indices)
                                                        
                        vobject.representations[rep.name] = rep 
                    
                    else:

                        if indices  == []:
                            vobject.representations[_type].active = False
                            pass
                        
                        else:
                            indices = np.array(indices, dtype=np.uint32)
                            #print (indices)
                            vobject.representations[_type].define_new_indices_to_VBO ( indices)
                            vobject.representations[_type].active = True


                if _type == 'nonbonded':
                    pass
                
                if  _type == 'spheres':
                    
                    atoms2spheres = []
                    for atom in vobject.atoms:
                        if atom.spheres:
                            atoms2spheres.append(atom)
                            index = vobject.atoms.index(atom)
                            #indices.append(atom.index-1)
                            indices.append(index)
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
        selection = vSele()
        #selection._selection_mode ='chain' # 'atom'
        self.selections = {
                          'sel01' : selection
                          }
        self.current_selection = 'sel01'
        
        #---------------------------------------------------------------
        #  PICKING SELECTIONS
        #---------------------------------------------------------------
        self.picking_selections =  vPick()
        
    
    
    
    
    
    
    
        def menu_show_lines (_):
            """ Function doc """
            self.show_or_hide( _type = 'lines', show = True)
        
        def menu_hide_lines (_):
            """ Function doc """
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
        

            
    
    
    
     
        menu = { 
                'header' : ['MenuItem', None],
                
                
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

        self.insert_glmenu(menu)

























        self.default_rep = {'nonbonded' : False,
                              'lines'   : True,
                              'spheres' : False,
                              'sticks'  : False,
                              'ribbons' : False,
                              'surface' : False,
                              }

    def insert_glmenu (self, menu  = None):
	    """ Function doc """
	    self.glwidget.build_glmenu(menu  = menu )

    def command_line (self, entry = None):
        """ Function doc """
        cmd = entry.split()
        print (cmd)
        
        obj     = int(cmd[1]            )
        _indices = cmd[2].split('+')
        indices = []
        
        
        for index in _indices:
            indices.append(int(index))
        
        if cmd[0] == 'show':
            self._show_lines (visObj = self.vismol_objects[obj], 
                                       indices = indices)       
        
        if cmd[0] == 'hide':
            self._hide_lines (visObj = self.vismol_objects[obj], 
                                       indices = indices)  
        
        self.ctrl = True
        
        
        print (entry)

    def load (self, infile, widget = None, autocenter = True):
        """ Function doc """
        #Vobject_id = len(self.vismol_objects)
        print ('load')
        
        if infile[-3:] == 'pdb':
            self._load_pdb_file(infile = infile)
        
        if infile[-4:] == 'mol2':
            self._load_mol2_file(infile = infile)
        
        if infile[-3:] == 'xyz':
            self._load_xyz_file(infile = infile)

        self.vismol_objects[-1].active = True
        
        if self.toolkit == 'gtk':
            
            print(self.vismol_objects)
        
        
        #self.vismol_objects[-1].generate_default_representations (reps_list = self.default_rep)
        #print (self.vismol_objects[-1].representations)

        rep  = LinesRepresentation (name = 'lines', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
        self.vismol_objects[-1].representations[rep.name] = rep

        rep  = NonBondedRepresentation (name = 'nonbonded', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
        self.vismol_objects[-1].representations[rep.name] = rep
        
        #rep  = SticksRepresentation (name = 'sticks', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
        #self.vismol_objects[-1].representations[rep.name] = rep
        
        #rep  = GlumpyRepresentation (name = 'glumpy', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
        #self.vismol_objects[-1].representations[rep.name] = rep
        
        #rep  = DotsRepresentation (name = 'dots', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
        #self.vismol_objects[-1].representations[rep.name] = rep
        
        #rep  = SpheresRepresentation (name = 'spheres', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
        #self.vismol_objects[-1].representations[rep.name] = rep
        
        #rep =  RibbonsRepresentation(name = 'ribbons', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
        #self.vismol_objects[-1].representations[rep.name] = rep
        
        #rep =  SurfaceRepresentation(name = 'surface', active = True, _type = 'mol', visObj = self.vismol_objects[-1], glCore = self.glwidget.vm_widget)
        #self.vismol_objects[-1].representations[rep.name] = rep

        #self.glwidget.queue_draw()
       
        #if self.toolkit == 'gtk3':
        #    self.refresh_gtk(widget)
        #visObj = vismolSession.vismol_objects[-1]
        if autocenter:
            self.glwidget.vm_widget.center_on_coordinates(self.vismol_objects[-1], self.vismol_objects[-1].mass_center)

        
        

        
    def _load_pdb_file (self, infile):
        """ Function doc """      
        print(infile)
        vismol_object  = PDBFiles.load_pdb_file (infile = infile, VMSession = self)     
        vismol_object.set_model_matrix(self.glwidget.vm_widget.model_mat)        
        self.vismol_objects.append(vismol_object)
     

    def _load_mol2_file (self, infile):
        """ Function doc """
        print(infile)
        vismol_object  = MOL2Files.load_mol2_files (infile = infile, VMSession = self)
        vismol_object.set_model_matrix(self.glwidget.vm_widget.model_mat)        
        self.vismol_objects.append(vismol_object)
        
    
    def _load_xyz_file (self, infile):
        """ Function doc """
        #load_xyz_file
        print(infile)
        vismol_object  = XYZFiles.load_xyz_file (infile = infile, VMSession = self)
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
    
    def select (self, obj =  None, indices = []):
        """ Function doc """

    def orient (self, obj =  None):
        """ Function doc """  
    
    def center (self, visObj):
        """ Function doc """
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

    def selection_mode(self, selmode = 'atom'):
        """ Function doc """        
        self.selections[self.current_selection]._selection_mode = selmode
    
    def selection_function (self, pickedID):
        """ Function doc """
        if pickedID is None:
            selected = None
        else:
            selected = self.atom_dic_id[pickedID]
        
        #"""     P I C K I N G     S E L E C T I O N S     """
        if self._picking_selection_mode:
            self.picking_selections.selection_function_picking(selected)
        
        else:
            self.selections[self.current_selection].selection_function_viewing(selected)

    def _selection_function (self, selected):
        #"""     P I C K I N G     S E L E C T I O N S     """
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
