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

import VISMOL.glCore.shapes as shapes

#from VISMOL.gtkWidgets.main_treeview import GtkMainTreeView, FileChooser


import os

class ShowHideVisMol:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        pass
#'''
    def _hide_dots (self, Vobjects ):
        for Vobject in Vobjects:
            Vobject.flat_sphere_representation.actived = False
            #self.flat_sphere_representation.update()

    def _show_dots (self, Vobjects = []):
        """ Function doc """
        for Vobject in Vobjects:
            Vobject.dots_actived = True
            
            
            #Vobject.dots_actived.update()
            
    def _hide_ribbons (self, Vobjects ):
        """ Function doc """
        for Vobject in Vobjects:
            pass
    
    def _show_ribbons (self, Vobjects ):
        """ Function doc """
        for Vobject in Vobjects:
            Vobject.show_ribbons = True
        
    def _hide_lines (self, visObj = None, indexes = []):
        """ Function doc 
        
        _hide_lines
        visObj  = object
        indexes = [] list
        
        """
        if indexes == []:
            for atom in visObj.atoms:
                atom.lines =  False        
        else:
            for index in indexes:
                visObj.atoms[index].lines = False

        visObj.index_bonds = []
        
        for bond_pairs in visObj.index_bonds_pairs:
            if visObj.atoms[bond_pairs[0]].lines and  visObj.atoms[bond_pairs[1]].lines:
                visObj.index_bonds.append(visObj.atoms[bond_pairs[0]].index-1)
                visObj.index_bonds.append(visObj.atoms[bond_pairs[1]].index-1)

        shapes.change_vbo_indexes (ind_vbo = visObj.lines_buffers[0], indexes = visObj.index_bonds)
    
    def _show_lines (self, visObj = None, indexes = [] ):
        """ Function doc 
        
        visObj  = object
        indexes = [] list
        
        
        """
        
        if indexes == []:
            for atom in visObj.atoms:
                atom.lines =  True        
        else:
            for index in indexes:
                visObj.atoms[index].lines = True

        visObj.index_bonds = []
        
        for bond_pairs in visObj.index_bonds_pairs:
            if visObj.atoms[bond_pairs[0]].lines and  visObj.atoms[bond_pairs[1]].lines:
                visObj.index_bonds.append(visObj.atoms[bond_pairs[0]].index-1)
                visObj.index_bonds.append(visObj.atoms[bond_pairs[1]].index-1)

        shapes.change_vbo_indexes (ind_vbo = visObj.lines_buffers[0], indexes = visObj.index_bonds)
    
    def hide (self, Vobjects =  [], _type = 'lines', indexes = [] ):
        """ Function doc """    
        if _type == 'dots':
            self._hide_dots (Vobjects )

        if _type == 'lines':
            self._hide_lines (Vobjects )

        if _type == 'ribbons':
            self._hide_ribbons (Vobjects )
        
        if _type == 'ball_and_stick':
            self._hide_ball_and_stick(Vobjects )
        
        if _type == 'spheres':
            self._hide_spheres (Vobjects )            
        
        self.glwidget.updateGL()

    def show (self, _type = 'lines', Vobjects =  [], indexes = [] ):
        """ Function doc """
        if _type == 'dots':
            self._show_dots (Vobjects )

        if _type == 'lines':
            self._show_lines (Vobjects )

        if _type == 'ribbons':
            self._show_ribbons (Vobjects )
        
        if _type == 'ball_and_stick':
            self._show_ball_and_stick(Vobjects)
        
        if _type == 'spheres':
            self._show_spheres(Vobjects ) 
    
        #self.glwidget.updateGL()


class VisMolSession (ShowHideVisMol):
    """ Class doc """

    def __init__ (self, glwidget = False, backend = 'gtk3', main_session = None):
        """ Class initialiser """
        #self.vismol_objects         = [] # self.vismol_objects
        #self.vismol_objects_dic     = {} # self.vismol_objects_dic   
        self.main_session = None
        
        
        self.vismol_objects     = [] # old Vobjects
        self.vismol_objects_dic = {}
        
        self.atom_id_counter  = 0  # 
        self.atom_dic_id      = {
                                # atom_id : obj_atom 
                                 }
        

        #---------------------------------------------------------------------------
        # gl stuffs
        #---------------------------------------------------------------------------
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
        
        
        self.backend = backend
        if glwidget:
            if backend == 'gtk3':
                #from VISMOL.glWidget import gtk3 as VisMolGLWidget
                from VISMOL.glWidget import VisMolGLWidget
                self.glwidget   = VisMolGLWidget.GtkGLAreaWidget(self)
            
            if backend == 'qt4':
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
        self.selections = {
                          'sel01' : selection
                          }
        self.current_selection = 'sel01'
        
        #---------------------------------------------------------------
        #  PICKING SELECTIONS
        #---------------------------------------------------------------
        self.picking_selections =  vPick()
        
        self.insert_glmenu()
    
    #def get_gtk_main_treeview (self):
    #    """ Function doc """
    #    self.main_treeview = GtkMainTreeView(vismolSession = self) 
    #    self.main_treeview.treeView
    #    return self.main_session.vismolSession.main_treeview.treeView


    #def refresh_gtk (self, 
    #                 maintreeview = True
    #                 ):
    #    """ Function doc """
    #    if maintreeview:
    #        #self.main_treeview.refresh_gtk_main_treeview()
    #        self.main_session.vismolSession.main_treeview.treeView.refresh_gtk_main_treeview()
    def insert_glmenu (self, menu_items = None):
	    """ Function doc """
	    self.glwidget.build_glmenu(menu_items = menu_items)

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

        
        if infile[-3:] == 'pdb':
            self._load_pdb_file(infile = infile)
        
        if infile[-4:] == 'mol2':
            self._load_mol2_file(infile = infile)
        
        if infile[-3:] == 'xyz':
            self._load_xyz_file(infile = infile)


        self.vismol_objects[-1].actived = True
        self.glwidget.queue_draw()
       
        #if self.backend == 'gtk3':
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
    
    def delete_by_index(self, index = None):
        """ Function doc """
        self.viewing_selections = []
        self.picking_selections = [None]*4        
        self.vismol_objects.pop(index)
        #self.glwidget.updateGL()
        
    def select (self, obj =  None, indexes = []):
        """ Function doc """

    def orient (self, obj =  None):
        """ Function doc """  

    def center_by_index(self, Vobject =  None, index = None):
        """ Function doc """  
        mass_center = self.vismol_objects[index].mass_center
        #self.glwidget.center_on_atom(mass_center)

    def disable_by_index (self, index = 0):
        self.vismol_objects[index].actived = False
        #self.glwidget.draw()
        self.glwidget.queue_draw()
            
    def enable_by_index (self, index = 0):
        """ Function doc """
        self.vismol_objects[index].actived = True
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
        #self.vismolSession  =  VisMolSession(glwidget = True, backend = 'gtk3')       
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
