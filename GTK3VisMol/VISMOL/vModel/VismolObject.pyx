#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  VismolObject.py
#  
#  Copyright 2017 
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
import time
import os
import multiprocessing
#import threading

import VISMOL.glCore.vismol_font as vmf

from VISMOL.vModel.Atom       import Atom
from VISMOL.vModel.Chain      import Chain
from VISMOL.vModel.Residue    import Residue






class VismolObject:
    """ Class doc 
    
    
    Visual Object contains the information necessary for openGL to draw 
    a model on the screen. Everything that is represented in the graphical 
    form is stored in the form of a VismolObject.
    
    Arguments
    
    name       = string  - Label that describes the object  
    atoms      = list of atoms  - [index, at_name, cov_rad,  at_pos, at_res_i, at_res_n, at_ch]
    VMSession  = Vismol Session - Necessary to build the "atomtree_structure"
                 VMSession contains the atom_id_counter (self.vismol_session.atom_id_counter)
    
    trajectory = A list of coordinates - eg [ [x1,y1,z1, x2,y2,z2...], [x1,y1,z1, x2,y2,z2...]...]
                 One frame is is required at last.
    
    
    Attributes 
    
    self.actived            = False
    self.editing            = False
    self.Type               = 'molecule'
    self.name               = name #self._get_name(name)
    self.mass_center        = Center of mass <- necessary to center the object on the screen
                              calculated on _generate_atomtree_structure
    
    self.atoms2             = [[index, at_name, cov_rad,  at_pos, at_res_i, at_res_n, at_ch], ...]
    self.atoms              = [Atom1, atom2, ...] <--- Atom objects (from VISMOL.vModel.Atom       import Atom)
    
    self.residues           = []
    self.chains             = {}
    self.frames             = trajectory    
    self.atom_unique_id_dic = {}    
    
    
    #-----------------------#
    #         Bonds         #
    #-----------------------#
    
    self.index_bonds        = []
    self.index_bonds_rep    = []
    self.index_bonds_pairs  = [] 
    
    self.non_bonded_atoms   = None    
    """
    
    def __init__ (self, 
                  name       = 'UNK', 
                  atoms      = []   ,
                  VMSession  = None , 
                  trajectory = None):
        
        """ Class initialiser """
        #-----------------------------------------------------------------
        #                V I S M O L   a t t r i b u t e s
        #----------------------------------------------------------------- 
        self.vismol_session = VMSession     #
        self.actived        = False         # for "show and hide"   enable/disable
        self.editing        = False         # for translate and rotate  xyz coords 
        self.Type           = 'molecule'    # Not used yet
        self.name           = name          # 
        self.vm_font        = vmf.VisMolFont()
        
        #-----------------------------------------------------------------
        self.mass_center = None
        #-----------------------------------------------------------------

       
        #-----------------------------------------------------------------
        self.atoms2             = atoms
        self.atoms              = []
        self.residues           = []
        self.chains             = {}
        #self.chains             = []
                                
        
        self.frames             = trajectory
        self.atom_unique_id_dic = {}
        
        #-----------------------#
        #         Bonds         #
        #-----------------------#
        self.index_bonds        = []
        self.index_bonds_rep    = []
        self.index_bonds_pairs  = []
        
        #-----------------------#
        #       Nonbonded       #
        #-----------------------#
        self.non_bonded_atoms   = []
        
        #-----------------------#
        #    Calpha  Ribbons    #
        #-----------------------#
        self.ribbons_Calpha_pairs_full  = []
        self.ribbons_Calpha_pairs_rep   = []
        self.ribbons_Calpha_indexes_rep = []
        #-----------------------------------------------------------------
        
        #-----------------------#
        #      True Spheres     #
        #-----------------------#
        self.sphere_vertices_full  = []
        self.sphere_triangles_full = []
        self.sphere_rep = None


        self.sel_sphere_rep = None

        #-----------------------------------------------------------------
        #                O p e n G L   a t t r i b u t e s
        #-----------------------------------------------------------------                
        """   L I N E S   """
        self.lines_actived       = True
        self.lines_show_list     = False

        """   D O T S   """
        self.dots_actived = False

        """   R I B B O N S   """
        self.ribbons_actived = False
        
        """   N O N  B O N D E D   """
        self.non_bonded_actived = True
        
        """   S T I C K S   """
        self.sticks_actived = False
        
        """   S P H E R E S   """
        self.spheres_actived = False
        
        """   D O T S  S U R F A C E   """
        self.dots_surface_actived = False
        
        """   T E X T   """
        self.text_activated = True
        
        """   S E L E C T I O N   """
        self._sel_lines_actived = False
        self._sel_dots_actived = False
        self._sel_ribbons_actived = False
        self._sel_non_bonded_actived = False
        self._sel_sticks_actived = True
        self._sel_spheres_actived = True
        self._sel_dots_surface_actived = False
        
        #print ('frames:     ', len(self.frames))
        #print ('frame size: ', len(self.frames[0]))
        #-----------------------------------------------------------------
        self.dots_vao        = None
        self.lines_vao       = None
        self.ribbons_vao     = None
        self.non_bonded_vao  = None
        self.sticks_vao   = None
        self.spheres_vao     = None
        self.dots_surface_vao = None
    
        self.dot_buffers        = None
        self.lines_buffers      = None
        self.ribbons_buffers    = None
        self.non_bonded_buffers = None
        self.sticks_buffers  = None
        self.spheres_buffers    = None
        self.dots_surface_buffers = None
        
        """   S E L E C T I O N   """
        self.sel_dots_vao = None
        self.sel_lines_vao = None
        self.sel_ribbons_vao = None
        self.sel_non_bonded_vao = None
        self.sel_sticks_vao = None
        self.sel_spheres_vao = None
        self.sel_dots_surface_vao = None
        
        self.sel_dot_buffers = None
        self.sel_lines_buffers = None
        self.sel_ribbons_buffers = None
        self.sel_non_bonded_buffers = None
        self.sel_sticks_buffers = None
        self.sel_spheres_buffers = None
        self.sel_dots_surface_buffers = None
        
        
        self.dot_indexes     = None
        
        self.selection_dots_vao      = None
        self.selection_dot_buffers   = None
        
        self.model_mat = np.identity(4, dtype=np.float32)
        self.trans_mat = np.identity(4, dtype=np.float32)
        self.target    = None
        self.unit_vec  = None
        self.distance  = None
        self.step      = None

        self.picking_dots_vao      = None
        self.picking_dot_buffers   = None
        #-----------------------------------------------------------------
    
    def generate_dot_indexes(self):
        """ Function doc
        """
        self.dot_indexes = []
        for i in range(int(len(self.atoms))):
            self.dot_indexes.append(i)
        self.dot_indexes = np.array(self.dot_indexes, dtype=np.uint32)
    
    def _generate_atomtree_structure (self):
        """ Function doc """
        
        print ('\ngenerate_chain_structure starting')
        initial          = time.time()
        
        parser_chi   = None
        parser_chn   = None

        parser_resi  = None
        parser_resn  = None
        chains_m     = {}
        frame        = []
        #index        = 1
        
        self.atoms   = [] 
            
        sum_x = 0.0 
        sum_y = 0.0 
        sum_z = 0.0 
        
        for atom2 in self.atoms2:
            #[index, at_name, cov_rad,  at_pos], at_res_i, at_res_n, at_ch]
            index    = atom2[0]
            at_name  = atom2[1]
            cov_rad  = atom2[2]
            at_pos   = atom2[3]
            at_res_i = atom2[4]
            at_res_n = atom2[5]
            at_ch    = atom2[6]
            
            atom      = Atom(name      =  at_name, 
                             index     =  index+1, 
                             pos       =  at_pos, 
                             resi      =  at_res_i, 
                             resn      =  at_res_n, 
                             chain     =  at_ch, 
                             #atom_id  =  counter, 
                             )
            
            atom.atom_id = self.vismol_session.atom_id_counter
            atom.Vobject = self
            '''
            if atom.chain == parser_chn:# and at_res_n == parser_resn:
                atom.residue = ch.residues[-1]
                ch.residues[-1].atoms.append(atom)
                #frame.append([atom.pos[0].,atom.pos[1],atom.pos[2]])

            else:
                residue = Residue(name=atom.resn, index=atom.resi, chain=atom.chain)
                atom.residue     = residue
                residue.atoms.append(atom)
                
                ch.residues.append(residue)
                #frame.append([atom.pos[0],atom.pos[1],atom.pos[2]])
                parser_resi  = atom.resi
                parser_resn  = atom.resn
            '''
            
            if atom.chain in self.chains.keys():
                ch = self.chains[atom.chain]
            
            else:
                ch = Chain(name = atom.chain, label = 'UNK')
                self.chains[atom.chain] = ch
            
            if atom.resi == parser_resi:# and at_res_n == parser_resn:
                atom.residue = ch.residues[-1]
                ch.residues[-1].atoms.append(atom)
                #frame.append([atom.pos[0].,atom.pos[1],atom.pos[2]])

            else:
                residue = Residue(name=atom.resn, index=atom.resi, chain=atom.chain)
                atom.residue     = residue
                residue.atoms.append(atom)
                
                ch.residues.append(residue)
                #frame.append([atom.pos[0],atom.pos[1],atom.pos[2]])
                parser_resi  = atom.resi
                parser_resn  = atom.resn


            if atom.name == 'CA':
                ch.backbone.append(atom)
            
            self.atoms.append(atom)
            
            sum_x += atom.pos[0]
            sum_y += atom.pos[1]
            sum_z += atom.pos[2]
            
            self.vismol_session.atom_dic_id[self.vismol_session.atom_id_counter] = atom
            #index +=1
            self.vismol_session.atom_id_counter +=1
        

        total = len(self.atoms2)        
        self.mass_center = np.array([sum_x / total,
                                     sum_y / total, 
                                     sum_z / total])

        final = time.time() 
        print ('_generate_atomtree_structure end -  total time: ', final - initial, '\n')
        self.get_backbone_indexes()
        return True


    def _get_name (self, name):
        """ Function doc """
        self.name  = os.path.basename(name)

    def _generate_non_bonded_list (self):
        """ Function doc """
        self.non_bonded_atoms   =  []
        initial = time.time()
        #
        ##for i in range(0, len(self.atoms)):
        ##    if i in self.index_bonds:
        ##        pass
        ##    else:
        ##        self.non_bonded_atoms.append(i)
        #
        #for atom in self.atoms:
        #    if atom.connected != []:
        #        pass
        #    else:
        #        self.non_bonded_atoms.append(atom.index -1)
        self.non_bonded_atoms = np.array(self.non_bonded_atoms, dtype=np.uint32)
        final = time.time()    
        print ('Cython PARALLEL _generate_non_bonded_list total time: ', final - initial, '\n') 
        
    def _generate_atom_unique_color_id (self):
        """ Function doc 
        
        (1) This method assigns to each atom of the system a 
        unique identifier based on the RGB color standard. 
        This identifier will be used in the selection function. 
        There are no two atoms with the same color ID in the 
        vismol.
        
        
        (2) This method builds the "colors" np array that will 
        be sent to the GPU and which contains the RGB values 
        for each atom of the system.
        
        
        """
        self.color_indexes  = []
        self.colors         = []        
        self.vdw_dot_sizes  = []
        self.cov_dot_sizes  = []
        for atom in self.atoms:
            #-------------------------------------------------------
            # (1)                  ID Colors
            #-------------------------------------------------------
            i = atom.atom_id
            r = (i & 0x000000FF) >>  0
            g = (i & 0x0000FF00) >>  8
            b = (i & 0x00FF0000) >> 16
           
            self.color_indexes.append(r/255.0)
            self.color_indexes.append(g/255.0)
            self.color_indexes.append(b/255.0)
            
            pickedID = r + g * 256 + b * 256*256
            atom.color_id = [r/255.0, g/255.0, b/255.0]
            #print (pickedID)
            self.vismol_session.atom_dic_id[pickedID] = atom
            
            #-------------------------------------------------------
            # (2)                   Colors
            #-------------------------------------------------------
            self.colors.append(atom.color[0])        
            self.colors.append(atom.color[1])        
            self.colors.append(atom.color[2])   

            #-------------------------------------------------------
            # (3)                  VdW list
            #-------------------------------------------------------
            self.vdw_dot_sizes.append(atom.vdw_rad)
            self.cov_dot_sizes.append(atom.cov_rad)

        self.color_indexes = np.array(self.color_indexes, dtype=np.float32)
        self.colors        = np.array(self.colors       , dtype=np.float32)    
        self.vdw_dot_sizes = np.array(self.vdw_dot_sizes, dtype=np.float32)
        self.cov_dot_sizes = np.array(self.cov_dot_sizes, dtype=np.float32)

    def set_model_matrix(self, mat):
        """ Function doc
        """
        self.model_mat = np.copy(mat)
        return True
    

    def get_backbone_indexes (self):
        """ Function doc """
        chains_list   = []
        bonds_pairs   = [] 
        bonds_indexes = [] 
        
        for chain in self.chains.values():
            #bonds_indexes = [] 
            chain_list    = []

            resi       = None
            atomi      = None
            
            for atom in chain.backbone:
                
                if resi is None:
                    resi  = atom.resi
                    atomi = atom.index
                    chain_list.append([atom.resi, atom.index])
                
                else:
                    
                    if resi == atom.resi-1:
                        
                        bonds_pairs.append([atomi,atom.index])
                        bonds_indexes.append(atomi)
                        bonds_indexes.append(atom.index)

                        chain_list.append([atom.resi, atom.index])
                        
                        resi  = atom.resi
                        atomi = atom.index
                    
                    else:
                        
                        chain_list.append([atom.resi, atom.index])
                        resi  = atom.resi
                        atomi = atom.index
                
                chains_list.append(chain_list)

        
        bonds_indexes = np.array(bonds_indexes, dtype=np.uint32)
        self.ribbons_Calpha_pairs_full  = bonds_pairs
        self.ribbons_Calpha_pairs_rep   = bonds_pairs
        self.ribbons_Calpha_indexes_rep = bonds_indexes
        

'''
def determine_the_paired_atomic_grid_elements_parallel(atomic_grid):
    """
    There is also an array vOff that specifies the offsets of each of the 14 neighbor
    cells. The array covers half the neighboring cells, together with the cell itself; its
    size and contents are specified as
    
    {{0,0,0}, {1,0,0}, {1,1,0}, {0,1,0}, {-1,1,0}, {0,0,1},
    {1,0,1}, {1,1,1}, {0,1,1}, {-1,1,1}, {-1,0,1},
    {-1,-1,1}, {0,-1,1}, {1,-1,1}}
    
    """
    initial = time.time()
    pair_of_sectors2 = []
    grid_offset = [[ 0, 0, 0], 
                   [ 1, 0, 0], 
                   [ 1, 1, 0], 
                   [ 0, 1, 0], 
                   [-1, 1, 0], 
                   [ 0, 0, 1],
                   [ 1, 0, 1], 
                   [ 1, 1, 1], 
                   [ 0, 1, 1], 
                   [-1, 1, 1], 
                   [-1, 0, 1],
                   [-1,-1, 1], 
                   [ 0,-1, 1], 
                   [ 1,-1, 1]
                   ]
    
    for element in atomic_grid.keys():
        for offset_element in  grid_offset:              
            
            element1  = (element[0]                  , element[1]                  , element[2]                  ) 
            element2  = (element[0]+offset_element[0], element[1]+offset_element[1], element[2]+offset_element[2]) 
                    
            if element2 in atomic_grid:                        
                pair_of_sectors2.append([self.atomic_grid[element1],
                                         self.atomic_grid[element2]])

    
    final = time.time()    
    print ('Pairwise grid elements time : ', final - initial, '\n')  
    return pair_of_sectors2
'''



'''
Contains all pairs of neighboring sectors that will be used to 
calculate distances between atoms from  different sectors (this 
list does not contain any pairs of repeated sectors)
#--------------------------------------------------------------


#-----------------------------------------------------------------
self.full_grid_offset = [
                       [ 1, 1, 1], # top level
                       [ 0, 1, 1], # top level
                       [-1, 1, 1], # top level
                       [-1, 0, 1], # top level
                       [ 0, 0, 1], # top level
                       [ 1, 0, 1], # top level
                       [-1,-1, 1], # top level
                       [ 0,-1, 1], # top level
                       [ 1,-1, 1], # top level
                       
                       #-------------------------
                       [ 1, 1, 0], # middle level 
                       [ 0, 1, 0], # middle level 
                       [-1, 0, 0], # middle level 
                       [-1, 1, 0], # middle level 
                      #[ 0, 0, 0], # middle level 
                       [ 1, 0, 0], # middle level 
                       [-1,-1, 0], # middle level 
                       [ 0,-1, 0], # middle level 
                       [ 1,-1, 0], # middle level 
                       #-------------------------
                       
                       [ 1, 1,-1], # ground level
                       [ 0, 1,-1], # ground level
                       [-1, 1,-1], # ground level
                       [-1, 0,-1], # ground level
                       [ 0, 0,-1], # ground level
                       [ 1, 0,-1], # ground level
                       [-1,-1,-1], # ground level
                       [ 0,-1,-1], # ground level
                       [ 1,-1,-1], # ground level
                       ]
#-----------------------------------------------------------------
'''
