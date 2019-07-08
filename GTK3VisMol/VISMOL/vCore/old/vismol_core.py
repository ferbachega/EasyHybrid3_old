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
from VISMOL.vModel  import VismolObject
from VISMOL.vBabel import PDBFiles
import os

class ShowHideVisMol:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        pass
    
    def _hide_dots (self, Vobjects ):
        for Vobject in Vobjects:
            Vobject.flat_sphere_representation.actived = False
            #self.flat_sphere_representation.update()

    def _show_dots (self, Vobjects = []):
        """ Function doc """
        for Vobject in Vobjects:
            Vobject.flat_sphere_representation.actived = True
            Vobject.flat_sphere_representation.update()
            
            #self.glwidget.draw_dots(Vobject)

    #def _hide_flat_spheres (self, Vobjects ):
    #    for Vobject in Vobjects:
    #        Vobject.show_dots = False
    #
    #def _show_flat_spheres (self, Vobjects = []):
    #    """ Function doc """
    #    for Vobject in Vobjects:
    #        Vobject.show_dots = True
    #        #self.glwidget.draw_dots(Vobject)

    def _hide_ribbons (self, Vobjects ):
        """ Function doc """
        for Vobject in Vobjects:
            pass
            #self.flat_sphere_representation.actived = False
            #self.flat_sphere_representation.update()
    
    def _show_ribbons (self, Vobjects ):
        """ Function doc """
        for Vobject in Vobjects:
            Vobject.show_ribbons = True
            #self.glwidget.draw_ribbon(Vobject)
        
    def _hide_lines (self, Vobjects ):
        """ Function doc """
        for Vobject in Vobjects:
            #Vobject.show_lines = False
            Vobject.line_representation.actived = False

    def _show_lines (self, Vobjects ):
        """ Function doc """
        for Vobject in Vobjects:
            #Vobject.show_lines = True
            Vobject.line_representation.actived = True
            Vobject.line_representation.update()

    def _hide_ball_and_stick (self, Vobjects ):
        """ Function doc """
        for Vobject in Vobjects:
            Vobject.show_ball_and_stick = False
        
    def _show_ball_and_stick(self, Vobjects):
        """ Function doc """
        for Vobject in Vobjects:
            Vobject.show_ball_and_stick = True
            #self.glwidget.draw_ball_and_stick(Vobject)
    
    def _hide_spheres (self, Vobjects ):
        """ Function doc """
        for Vobject in Vobjects:
            Vobject.show_spheres = False
        
    def _show_spheres (self, Vobjects):
        """ Function doc """
        for Vobject in Vobjects:
            Vobject.show_spheres = True
            #self.glwidget.draw_spheres(Vobject)
    
    def hide (self, _type = 'lines', Vobjects =  []):
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

    def show (self, _type = 'lines', Vobjects =  []):
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
    
        self.glwidget.updateGL()


class VisMolPickingSelection:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        self.picking_selections = [None]*4
        #self.picking_selection_coordinates = []
    
    def _generate_picking_selection_coordinates (self):
        """ Function doc """
        pass
        #for i,atom in enumerate(self.picking_selections):
        #    if atom is not None:
        #        coord = [atom.Vobject.frames[frame][(atom.index-1)*3  ],
        #                 atom.Vobject.frames[frame][(atom.index-1)*3+1],
        #                 atom.Vobject.frames[frame][(atom.index-1)*3+2],]
        #                
        #        rep.draw_selected(atom, coord, [0.83, 0.48, 1])
        #        rep.draw_numbers(atom, i+1, coord)
    
    def selection_function_picking (self, selected):
        """ Function doc """
        if selected is None:
            self.picking_selections = [None]*len(self.picking_selections)
            #self.selected_residues = []
        else:
            if selected not in self.picking_selections:
                for i in range(len(self.picking_selections)):
                    if self.picking_selections[i] == None:
                        self.picking_selections[i] = selected
                        selected = None
                        break
                if selected is not None:
                    self.picking_selections[len(self.picking_selections)-1] = selected
            else:
                for i in range(len(self.picking_selections)):
                    if self.picking_selections[i] == selected:
                        self.picking_selections[i] = None
    

class VisMolViewingSelection:
    """ Class doc """
    
    def __init__ (self):
        #---------------------------------------------------------------
        #                S E L E C T I O N S
        #---------------------------------------------------------------
        self.actived = True
        
        self._selection_mode    = 'residue'
        
        self.viewing_selections = []
        
        self.selected_residues  = []
        
        """ Class initialiser """
        self.selected_atoms = []
        self.selected_frames= []
	
    def _generate_viewing_selection_coordinates (self):
        """ Function doc """
        pass
        
        #for i,atom in enumerate(self.EMSession.selections[self.EMSession.current_selection].viewing_selections):
        #    #print (atom, atom.index, frame, atom.Vobject_id, self.EMSession.Vobjects[atom.Vobject_id].frames, self.EMSession.Vobjects[atom.Vobject_id].coords  )
        #    #rep.draw_picked(atom)
        #    coord = atom.Vobject.frames[frame][atom.index-1]
        #    #glVertex3f(coord1[0], coord1[1], coord1[2])
        #    rep.draw_selected(atom, coord)
        ##'''
    
    def selecting_by_atom (self, selected):
        """ Function doc """
        if selected not in self.viewing_selections:
            self.viewing_selections.append(selected)
            
        else:
            index = self.viewing_selections.index(selected)
            self.viewing_selections.pop(index)
    
    def selecting_by_residue (self, selected):
        """ Function doc """
        # if the selected atoms is not on the selected list
        if selected not in self.viewing_selections:
            
            for atom in selected.residue.atoms:
                print (len(selected.residue.atoms), atom.name, atom.index)
                
        # the atom is not on the list -  add atom by atom
                if atom not in self.viewing_selections:
                    self.viewing_selections.append(atom)
                
                # the atom IS on the list - do nothing 
                else:
                    pass
    
        # else: if the selected atoms IS on the selected list
        else:
            # So, add all atoms  - selected residue <- selected.resi
            for atom in selected.residue.atoms:
                
                # the atom is not on the list -  add atom by atom
                if atom in self.viewing_selections:
                    index = self.viewing_selections.index(atom)
                    self.viewing_selections.pop(index)                            
                # the atom IS on the list - do nothing 
                else:
                    pass   

    def selecting_by_chain (self, selected):
        
        # if the selected atoms is not on the selected list
        if selected not in self.viewing_selections:
            # So, add all atoms  - selected residue <- selected.resi
            for residue in selected.Vobject.chains[selected.chain].residues:
                for atom in residue.atoms:
                    # the atom is not on the list -  add atom by atom
                    if atom not in self.viewing_selections:
                        self.viewing_selections.append(atom)
                    
                    # the atom IS on the list - do nothing 
                    else:
                        pass

        # if the selected atoms IS on the selected list
        else:
            for residue in selected.Vobject.chains[selected.chain].residues:
                #for residue in chain.residues:
                for atom in residue.atoms:
                    # the atom is not on the list -  add atom by atom
                    if atom in self.viewing_selections:
                        index = self.viewing_selections.index(atom)
                        self.viewing_selections.pop(index)                            
                    # the atom IS on the list - do nothing 
                    else:
                        pass          

        print ('selected atoms: ',len(self.viewing_selections))

    def selection_function_viewing (self, selected):
        
        if selected is None:
            self.viewing_selections = []
            self.selected_residues  = []
        
        else:
            if self._selection_mode == 'atom':
                self.selecting_by_atom (selected)
                '''
                #if selected not in self.viewing_selections:
                #    self.viewing_selections.append(selected)
                #    
                #else:
                #    index = self.viewing_selections.index(selected)
                #    self.viewing_selections.pop(index)
                '''
            
            elif self._selection_mode == 'residue':
                self.selecting_by_residue (selected)
                '''
                #if selected not in self.viewing_selections:
                #    
                #    for atom in selected.residue.atoms:
                #        print (len(selected.residue.atoms), atom.name, atom.index)
                #        
                ## the atom is not on the list -  add atom by atom
                #        if atom not in self.viewing_selections:
                #            self.viewing_selections.append(atom)
                #        
                #        # the atom IS on the list - do nothing 
                #        else:
                #            pass
                #
                ## if the selected atoms IS on the selected list
                #else:
                #    # So, add all atoms  - selected residue <- selected.resi
                #    for atom in selected.residue.atoms:
                #        
                #        # the atom is not on the list -  add atom by atom
                #        if atom in self.viewing_selections:
                #            index = self.viewing_selections.index(atom)
                #            self.viewing_selections.pop(index)                            
                #        # the atom IS on the list - do nothing 
                #        else:
                #            pass                    
                '''
                
            elif self._selection_mode == 'chain':
                self.selecting_by_chain (selected)
                '''
                ## if the selected atoms is not on the selected list
                #if selected not in self.viewing_selections:
                #    # So, add all atoms  - selected residue <- selected.resi
                #    for residue in selected.Vobject.chains[selected.chain].residues:
                #        for atom in residue.atoms:
                #            # the atom is not on the list -  add atom by atom
                #            if atom not in self.viewing_selections:
                #                self.viewing_selections.append(atom)
                #            
                #            # the atom IS on the list - do nothing 
                #            else:
                #                pass
                #
                ## if the selected atoms IS on the selected list
                #else:
                #    for residue in selected.Vobject.chains[selected.chain].residues:
                #        #for residue in chain.residues:
                #        for atom in residue.atoms:
                #            # the atom is not on the list -  add atom by atom
                #            if atom in self.viewing_selections:
                #                index = self.viewing_selections.index(atom)
                #                self.viewing_selections.pop(index)                            
                #            # the atom IS on the list - do nothing 
                #            else:
                #                pass          
                #
                #print ('selected atoms: ',len(self.viewing_selections))
                '''
        

class VisMolSession (ShowHideVisMol):
    """ Class doc """

    def __init__ (self, glwidget = False, backend = 'gtk3'):
        """ Class initialiser """
        #self.vismol_objects         = [] # self.vismol_objects
        #self.vismol_objects_dic     = {} # self.vismol_objects_dic   
        
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
                                      
                                      'dot_size'                   : 5      ,
                                      'line_width'                 : 3      ,
                                      'sphere_scale'               : 0.85    ,
                                      'stick_scale'                : 1.5    ,
                                      'ball_and_sick_sphere_scale' : 1      ,
                                      'antialias'                  : False  ,
                                      'bg_color'                   : [0,0,0,1],
                                      }
        
        

        if glwidget:
            if backend == 'gtk3':
                from VISMOL.glWidget import gtk3 as VisMolGLWidget
                self.glwidget   = VisMolGLWidget.GtkGLWidget (self)
            
            if backend == 'qt4':
                self.glwidget   = VisMolGLWidget.QtGLWidget (self)
        else:
            self.glwidget = None
        #---------------------------------------------------------------------------
        
        
        
        
        
        self._picking_selection_mode = False # True/False  - interchange between viewing  and picking mode
        #---------------------------------------------------------------
        #  VIEWING SELECTIONS
        #---------------------------------------------------------------
        selection = VisMolViewingSelection()
        self.selections = {
                          'sel01' : selection
                          }
        self.current_selection = 'sel01'
        
        #---------------------------------------------------------------
        #  PICKING SELECTIONS
        #---------------------------------------------------------------
        self.picking_selections =  VisMolPickingSelection()
        


    def load (self, infile):
        """ Function doc """
        #Vobject_id = len(self.vismol_objects)

        
        if infile[-3:] == 'pdb':
            self._load_pdb_file(infile = infile)
            
        #if infile[-3:] == 'xyz':
        #
        #    Vobject, self.atom_dic_id = parse_xyz(infile     = infile,  
        #                     counter     = self.atom_id_counter,  
        #                     atom_dic_id = self.atom_dic_id,
        #                     Vobject_id  = Vobject_id
        #                     )
        
        #self.atom_id_counter += len(Vobject.atoms)
        
        self.vismol_objects[-1].actived = True
        #self.center_by_index (index =  -1)
        #return True
        
    def _load_pdb_file (self, infile):
        """ Function doc """
        print(infile)
        atoms, frames  = PDBFiles.load_pdb_files (infile = infile)
        name = os.path.basename(infile)
        vismol_object  = VismolObject.VismolObject(name        = name, 
                                                   atoms       = atoms, 
                                                   EMSession   = self, 
                                                   trajectory  = frames)
			      
        self.vismol_objects.append(vismol_object)
        
    def delete_by_index(self, index = None):
        """ Function doc """
        self.viewing_selections = []
        self.picking_selections = [None]*4        
        self.vismol_objects.pop(index)
        #self.glwidget.updateGL()
        
    def select (self, obj =  None):
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
        self.glwidget.updateGL()
            
    def enable_by_index (self, index = 0):
        """ Function doc """
        self.vismol_objects[index].actived = True
        #self.glwidget.draw()
        self.glwidget.updateGL()
        
    def set_frame (self, frame = 0):
        """ Function doc """
        #self.glwidget.frame = frame
        #self.glwidget.updateGL()
    
    def get_frame (self):
        """ Function doc """
        #""" Function doc """
        #frame = self.glwidget.frame
        #return frame
        
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

       
