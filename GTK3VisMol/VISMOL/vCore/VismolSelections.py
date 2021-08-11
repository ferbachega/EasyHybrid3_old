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
import VISMOL.vModel.Vectors as LA

class VisMolPickingSelection:
    """ Class doc """
    
    def __init__ (self, VMSession):
        """ Class initialiser """
        self.picking_selections_list = [None]*4
        self.picking_selections_list_index = []
        self.VMSession = VMSession
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

        
        print('\n\nDistances:')
        c = 0
        for atom1 in self.picking_selections_list:
            for atom2 in self.picking_selections_list[c+1:]:
            
                if atom1 and atom2:
                    dist = self.VMSession._get_distance_atom1_atom2 ( atom1, atom2 )
                    name1 = atom1.name
                    name2 = atom2.name
                    print ('atom',name1, 'atom',name2,  dist)
            
            c += 1
        
        atom1 = self.picking_selections_list[0]
        atom2 = self.picking_selections_list[1]
        atom3 = self.picking_selections_list[2]
        atom4 = self.picking_selections_list[3]
        
        
        print('\n\nAngles:')
        if atom1 and atom2 and atom3:
            xyz1 = atom1.coords()
            xyz2 = atom2.coords()
            xyz3 = atom3.coords()
            print(
                  xyz1, 
                  xyz2, 
                  xyz3, 
                 )
            xyz1 = [ xyz1[0] - xyz2[0], xyz1[1] - xyz2[1],   xyz1[2] - xyz2[2]]
            xyz3 = [ xyz3[0] - xyz2[0], xyz3[1] - xyz2[1],   xyz3[2] - xyz2[2]]
            #print(
            #      xyz1, 
            #      xyz3, 
            #     )
            angle = LA.angle(xyz1, xyz3)
            print ('Angle: ', angle*57.297)
        

        print('\n\nDihedral:')
        if atom1 and atom2 and atom3:
            p0 = atom1.coords()
            p1 = atom2.coords()
            p2 = atom3.coords()
            p3 = atom4.coords()
            angle = LA.dihedral(p0, p1, p2, p3)
            print ('Angle: ', angle*57.297)






class VisMolViewingSelection:
    """ Class doc """
    
    def __init__ (self, VMSession):
        #---------------------------------------------------------------
        #                S E L E C T I O N S
        #---------------------------------------------------------------
        self.active = False
        
        self._selection_mode       = 'residue'
        self.selected_objects      = {} #dic of VisMol objects (obj)
        self.selected_atoms        = [] #List of atoms objects (obj)
        self.selected_atoms_coords = [] #coordinate (floats) x y z
        self.VMSession             = VMSession
    
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
    
    def selecting_by_atom (self, selected_atom):
        """ Function doc """
        
        self._clear_selection_buffer(selected_atom)

        if selected_atom not in self.selected_atoms:
            self.selected_atoms.append(selected_atom)
            selected_atom.selected = True
            
        else:
            index = self.selected_atoms.index(selected_atom)
            self.selected_atoms.pop(index)
            selected_atom.selected = False

    def selecting_by_residue (self, selected_atom):
        """ Function doc """
        
        self._clear_selection_buffer(selected_atom)

            
        #if selected
        
        # if the selected atoms is not in the selected list
        if selected_atom not in self.selected_atoms:
            
            for atom in selected_atom.residue.atoms:
                '''print (len(selected.residue.atoms), atom.name, atom.index)'''
                
                # the atom is not on the list -  add atom by atom
                if atom not in self.selected_atoms:
                    self.selected_atoms.append(atom)
                    atom.selected = True
                # the atom IS on the list - do nothing 
                else:
                    pass
    
        # else: if the selected atoms IS in the selected list
        else:
            # So, add all atoms  - selected residue <- selected.resi
            for atom in selected_atom.residue.atoms:
                
                # the atom is not on the list -  add atom by atom
                if atom in self.selected_atoms:
                    index = self.selected_atoms.index(atom)
                    self.selected_atoms.pop(index)
                    atom.selected = False

                # the atom IS in the list - do nothing 
                else:
                    pass   

    def selecting_by_chain (self, selected_atom):
        ''' If the object selection is disabled, all atoms in the system will be set to False '''
        #VMSession      = selected_atom.Vobject.VMSession
        self._clear_selection_buffer(selected_atom)
        
        '''
        VMSession      = selected_atom.Vobject.VMSession
        
        #------------------------------------------------
        # Clearing the selections buffer
        # assigning false to all atoms loaded into memory
        if self.active:
            pass
        else:
            for Vobject in VMSession.vismol_objects:
                for atom in Vobject.atoms:
                    atom.selected = False
        #------------------------------------------------
        '''
                    
        print ('selecting_by_chain', selected_atom )
        # if the selected atoms is not on the selected list
        
        if selected_atom.selected == False:
        
            chain = selected_atom.chain
            print (chain)
            
            for atom in selected_atom.Vobject.atoms_by_chains[chain]:
                atom.selected = True 
            
        else:
            chain = selected_atom.chain
            for atom in selected_atom.Vobject.atoms_by_chains[chain]:
                atom.selected = False 
        
        self._build_selection_buffer ()
        print ('selected atoms: ',len(self.selected_atoms))


    def selecting_by_indexes (self, vismol_object = None, indexes = []):
        """ Function doc """
        print (indexes)
        #for atom in vismol_object.atoms:
        for i in indexes:
            vismol_object.atoms[i-1].selected = True
        
        self._build_selection_buffer()
        #self.active = True
        self.build_selected_atoms_coords_and_selected_objects_from_selected_atoms ()
        
    def _build_selection_buffer (self):
        """ Function doc """
        self.selected_atoms = []
        
        for Vobject in self.VMSession.vismol_objects:
            for atom in Vobject.atoms:
                if atom.selected:
                    #print ('',atom )
                    self.selected_atoms.append(atom)
                else:
                    pass
        
        
    def _clear_selection_buffer (self,  selected_atom):
        ''' If the object selection is disabled, 
        all atoms in the system will be set to False '''

        #------------------------------------------------
        # Clearing the selections buffer
        # assigning false to all atoms loaded into memory
        if self.active:
            pass
        else:
            for Vobject in self.VMSession.vismol_objects:
                for atom in Vobject.atoms:
                    atom.selected = False
        #------------------------------------------------""

    def selection_function_viewing (self, selected):
        #print (selected)
        if selected is None:
            self.selected_atoms = []
            self.selected_residues  = []
            self.active = False
        
        else:
            if self._selection_mode == 'atom':
                self.selecting_by_atom (selected)
            
            elif self._selection_mode == 'residue':
                self.selecting_by_residue (selected)

            elif self._selection_mode == 'chain':
                self.selecting_by_chain (selected)
            else:
                pass
            
            self.active = True
        
        self.build_selected_atoms_coords_and_selected_objects_from_selected_atoms ()
    
    def build_selected_atoms_coords_and_selected_objects_from_selected_atoms (self):
        """ Function doc """
        

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
        
            
