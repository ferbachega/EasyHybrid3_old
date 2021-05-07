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

import numpy as np


class VisMolPickingSelection:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        self.picking_selections_list = [None]*4
        self.picking_selections_list_index = []

        #self.picking_selection_coordinates = []
        #self.selected_atoms_coords   = []
        #self.selected_objects        = {}


    def _generate_picking_selection_coordinates (self):
        """ Function doc """
        pass
        #for i,atom in enumerate(self.picking_selections_list):
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
            self.picking_selections_list = [None]*len(self.picking_selections_list)
            #self.selected_residues = []
        else:
            if selected not in self.picking_selections_list:
                for i in range(len(self.picking_selections_list)):
                    if self.picking_selections_list[i] == None:
                        self.picking_selections_list[i] = selected
                        selected = None
                        break
                if selected is not None:
                    self.picking_selections_list[len(self.picking_selections_list)-1] = selected
            else:
                for i in range(len(self.picking_selections_list)):
                    if self.picking_selections_list[i] == selected:
                        self.picking_selections_list[i] = None
        print(self.picking_selections_list)

        
        
        #self.picking_selections_list_index=[]
        #for atom in self.picking_selections_list:  #selections[self.vismolSession.current_selection].selected_objects:
        #    if atom != None:
        #        self.picking_selections_list_index.append(atom.index-1)
        #        #print(atom.index-1)
        #self.picking_selections_list_index = np.array(self.selected_objects[vobject], dtype=np.uint32)





class VisMolViewingSelection:
    """ Class doc """
    
    def __init__ (self):
        #---------------------------------------------------------------
        #                S E L E C T I O N S
        #---------------------------------------------------------------
        self.active = True
        
        self._selection_mode    = 'residue'
        self.selected_objects          = {} #dic of VisMol objects (obj)
        self.selected_atoms        = [] #List of atoms objects (obj)
        self.selected_atoms_coords = [] #coordinate (floats) x y z
    
    def get_selection_info (self):
        """ Function doc """
        #print('self._selection_mode          ',self._selection_mode           )
        #print('self.selected_objects         ',self.selected_objects          )
        #
        #print('self.selected_atoms       ',self.selected_atoms        )
        print('Selection defiend with  ',len(self.selected_atoms), 'atom(s)')
        #print('self.selected_atoms_coords',self.selected_atoms_coords )
        
        '''
        for atom in self.selected_atoms:
            print(atom.name,                             # nome
                  atom.resi,                             # residue index
                  atom.Vobject.residues[atom.resi].resn, # residue name  taken from residues dic
                  atom.residue)                          # residue obj
        '''
            
        #print(atom.name, atom.resi, atom.Vobject.residues) 
        #print('self.selected_residues        ',self.selected_residues         )
        #print('self.selected_atoms           ',self.selected_atoms            )
        #print('self.selected_frames          ',self.selected_frames           )
        return len(self.selected_atoms)
    
    def selecting_by_atom (self, selected):
        """ Function doc """
        if selected not in self.selected_atoms:
            self.selected_atoms.append(selected)
            
        else:
            index = self.selected_atoms.index(selected)
            self.selected_atoms.pop(index)
    
    def selecting_by_residue (self, selected):
        """ Function doc """
        # if the selected atoms is not on the selected list
        if selected not in self.selected_atoms:
            
            for atom in selected.residue.atoms:
                '''print (len(selected.residue.atoms), atom.name, atom.index)'''
                
                # the atom is not on the list -  add atom by atom
                if atom not in self.selected_atoms:
                    self.selected_atoms.append(atom)
                
                # the atom IS on the list - do nothing 
                else:
                    pass
    
        # else: if the selected atoms IS on the selected list
        else:
            # So, add all atoms  - selected residue <- selected.resi
            for atom in selected.residue.atoms:
                
                # the atom is not on the list -  add atom by atom
                if atom in self.selected_atoms:
                    index = self.selected_atoms.index(atom)
                    self.selected_atoms.pop(index)                            
                # the atom IS on the list - do nothing 
                else:
                    pass   

    def selecting_by_chain (self, selected):
        
        # if the selected atoms is not on the selected list
        if selected not in self.selected_atoms:
            # So, add all atoms  - selected residue <- selected.resi
            for residue in selected.Vobject.chains[selected.chain].residues:
                for atom in residue.atoms:
                    # the atom is not on the list -  add atom by atom
                    if atom not in self.selected_atoms:
                        self.selected_atoms.append(atom)
                    
                    # the atom IS on the list - do nothing 
                    else:
                        pass

        # if the selected atoms IS on the selected list
        else:
            for residue in selected.Vobject.chains[selected.chain].residues:
                #for residue in chain.residues:
                for atom in residue.atoms:
                    # the atom is not on the list -  add atom by atom
                    if atom in self.selected_atoms:
                        index = self.selected_atoms.index(atom)
                        self.selected_atoms.pop(index)                            
                    # the atom IS on the list - do nothing 
                    else:
                        pass          

        print ('selected atoms: ',len(self.selected_atoms))

    def selection_function_viewing (self, selected):
        
        if selected is None:
            self.selected_atoms = []
            self.selected_residues  = []
        
        else:
            if self._selection_mode == 'atom':
                self.selecting_by_atom (selected)
            
            elif self._selection_mode == 'residue':
                self.selecting_by_residue (selected)

            elif self._selection_mode == 'chain':
                self.selecting_by_chain (selected)
        
        
        self.selected_atoms_coords = []
        self.selected_objects          = {}
        for atom in self.selected_atoms:
            
            if atom.Vobject in self.selected_objects:
                self.selected_objects[atom.Vobject] += [atom.index-1]
            else:
                self.selected_objects[atom.Vobject] = [atom.index-1]
            
            #coords =  atom.coords()
            #self.selected_atoms_coords = self.selected_atoms_coords + coords
        
        
        for vobject in self.selected_objects:
            self.selected_objects[vobject] =  np.array(self.selected_objects[vobject], dtype=np.uint32)         
        
        #print  (self.selected_atoms_coords)      
        #for vobject in     self.selected_objects:
            #print(vobject.name,self.selected_objects[vobject], 'selection_function_viewing' )
            print('Selection defiend with  ',len(self.selected_atoms), 'atom(s)')
        
            
