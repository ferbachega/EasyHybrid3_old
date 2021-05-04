#!/usr/bin/env python
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
#import multiprocessing as mp


#from multiprocessing import Pool
import multiprocessing


import threading

from VISMOL.vModel.Atom       import Atom
from VISMOL.vModel.Chain      import Chain
from VISMOL.vModel.Residue    import Residue
#from VISMOL.vModel.cfunctions import * #calculate_distances, calculate_distances_offset#, C_generate_bonds #C_generate_bonds, C_generate_bonds2, C_generate_bonds_between_sectors



class VismolObject:
    """ Class doc """
    
    def __init__ (self, 
                  name       = 'UNK', 
                  atoms      = []   ,
                  #coords     = None ,
                  VMSession  = None , 
                  trajectory = None):
        
        """ Class initialiser """
        #-----------------------------------------------------------------
        self.vismol_session = VMSession
        self.actived        = False
        self.editing        = False
        self.Type           = 'molecule'
        self.name           = name #self._get_name(name)
        
        #-----------------------------------------------------------------
        self.mass_center= None
        #-----------------------------------------------------------------

       
        #-----------------------------------------------------------------
        self.atoms2             = atoms
        
        self.residues           = []
        self.chains             = {}
                                
        self.bonds              = []
        self.frames             = trajectory

        self.atom_unique_id_dic = {}
        self.index_bonds        = []
        self.index_bonds_rep    = []
        self.non_bonded_atoms   = None
        #-----------------------------------------------------------------
                
        """   L I N E S   """
        self.lines_actived       = True
        self.lines_show_list     = True

        """   D O T S   """
        self.dots_actived = False

        """   C I R C L E S   """
        self.circles_actived = False

        print ('frames:     ', len(self.frames))
        print ('frame size: ', len(self.frames[0]))
        #-----------------------------------------------------------------
        
        #-----------------------------------------------------------------
        # OpenGL attributes
        #-----------------------------------------------------------------
        self.dots_vao        = None
        self.lines_vao       = None
        self.circles_vao     = None
        self.dot_buffers     = None
        self.line_buffers    = None
        self.circles_buffers = None
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

            if atom.chain in self.chains.keys():
                ch = self.chains[atom.chain]
           
            else:
                ch = Chain(name = atom.chain, label = 'UNK')
                self.chains[atom.chain] = ch
            
            if atom.resi == parser_resi:# and at_res_n == parser_resn:
                atom.residue = ch.residues[-1]
                ch.residues[-1].atoms.append(atom)
                frame.append([atom.pos[0],atom.pos[1],atom.pos[2]])

            else:
                residue = Residue(name=atom.resn, index=atom.resi, chain=atom.chain)
                atom.residue     = residue
                residue.atoms.append(atom)
                
                ch.residues.append(residue)
                frame.append([atom.pos[0],atom.pos[1],atom.pos[2]])
                parser_resi  = atom.resi
                parser_resn  = atom.resn


            if atom.name == 'CA':
                ch.backbone.append(atom)
            
            self.atoms.append(atom)
            
            sum_x += atom.pos[0]
            sum_y += atom.pos[1]
            sum_z += atom.pos[2]
            
            self.vismol_session.atom_dic_id[self.vismol_session.atom_id_counter] = atom
            index +=1
            self.vismol_session.atom_id_counter +=1
        

        total = len(self.atoms2)        
        self.mass_center = np.array([sum_x / total,
                                     sum_y / total, 
                                     sum_z / total])

        final = time.time() 
        print ('_generate_atomtree_structure end -  total time: ', final - initial, '\n')
    
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
    

class VismolObjectOld:
    """ Class doc """
    
    def __init__ (self, 
                  name       = 'UNK', 
                  atoms      = []   ,
                  #coords     = None ,
                  VMSession  = None , 
                  trajectory = None):
        
        """ Class initialiser """
        self.vismol_session = VMSession
        self.actived        = False
        self.editing        = False
        self.Type           = 'molecule'
        self.name           = name #self._get_name(name)
        
        #-----------------------------------------------------------------
        self.mass_center= None
        #-----------------------------------------------------------------
        
        # ------------------------------------ Model size and cell --------------------------------------------        
        self.grid_size   = 3  # It's the size of each grid element - size of a sector (A) angtrons 
        self.atomic_grid = {}
        #------------------------------------------------------------------------------------------------------


        
        
        
        
        
        #-----------------------------------------------------------------
        # 
        #-----------------------------------------------------------------
        self.atoms              = atoms
        self.residues           = []
        self.chains             = {}
                                
        self.bonds              = []
        self.frames             = trajectory

        self.atom_unique_id_dic = {}
        self.index_bonds        = []
        self.index_bonds_rep    = []
        self.non_bonded_atoms   = None
		
		
        #self._generate_atomtree_structure()
        #self._generate_atom_unique_color_id()
        #self._generate_bonds()
        #self._generate_non_bonded_list()
                
        """   L I N E S   """
        self.lines_actived       = True
        self.lines_show_list     = True

        """   D O T S   """
        self.dots_actived = False

        """   C I R C L E S   """
        self.circles_actived = False

        print ('frames:     ', len(self.frames))
        print ('frame size: ', len(self.frames[0]))
        
        
    
        # OpenGL attributes
        self.dots_vao        = None
        self.lines_vao       = None
        self.circles_vao     = None
        self.dot_buffers     = None
        self.line_buffers    = None
        self.circles_buffers = None
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
        
        parser_resi  = None
        parser_resn  = None
        chains_m     = {}
        frame        = []
        index        = 1
        
        self.atoms2  = [] 

        sum_x = 0.0 
        sum_y = 0.0 
        sum_z = 0.0 
        
        for atom in self.atoms:
            atom.index   = index
            atom.atom_id = self.vismol_session.atom_id_counter
            atom.Vobject = self
            
            if atom.chain in self.chains.keys():
                ch = self.chains[atom.chain]
           
            else:
                ch = Chain(name = atom.chain, label = 'UNK')
                self.chains[atom.chain] = ch
            
            if atom.resi == parser_resi:# and at_res_n == parser_resn:
                atom.residue = ch.residues[-1]
                ch.residues[-1].atoms.append(atom)
                frame.append([atom.pos[0],atom.pos[1],atom.pos[2]])

            else:
                residue = Residue(name=atom.resn, index=atom.resi, chain=atom.chain)
                atom.residue     = residue
                residue.atoms.append(atom)
                
                ch.residues.append(residue)
                frame.append([atom.pos[0],atom.pos[1],atom.pos[2]])
                parser_resi  = atom.resi
                parser_resn  = atom.resn


            if atom.name == 'CA':
                ch.backbone.append(atom)
            
            self.atoms2.append([atom.index-1, atom.name, atom.cov_rad,  atom.pos])
            sum_x += atom.pos[0]
            sum_y += atom.pos[1]
            sum_z += atom.pos[2]
            
            self.vismol_session.atom_dic_id[self.vismol_session.atom_id_counter] = atom
            index +=1
            self.vismol_session.atom_id_counter +=1
        

        total = len(self.atoms2)        
        self.mass_center = np.array([sum_x / total,
                                     sum_y / total, 
                                     sum_z / total])

        final = time.time() 
        print ('_generate_atomtree_structure end -  total time: ', final - initial, '\n')
    
        return True

    def _get_name (self, name):
        """ Function doc """
        self.name  = os.path.basename(name)
        #self.name  = name.split('.')
        #self.name  = self.name[0]
    
    def _generate_bonds (self):
        """ Function doc 

        (1)Calculate the distances and bonds 
        between atoms within a single element 
        of the atomic grid
        |-------|-------|-------|
        |       |       |       |
        |       |       |       |
        |       |       |       |
        |-------|-------|-------|
        |       |       |       |
        |       | i<->j |       |
        |       |       |       |
        |-------|-------|-------|
        |       |       |       |
        |       |       |       |
        |       |       |       |
        |-------|-------|-------|
        
        (2)Calculate the distances and connections 
        between atoms between different elements 
        of the atomic grid
        |-------|-------|-------|
        |       |       |       |
        |       |       |       |
        |       |       |       |
        |-------|-------|-------|
        |       |   i   |       |
        |       |    \  |       |
        |       |     \ |       |
        |-------|------\|-------|
        |       |       \       |
        |       |       |\      |
        |       |       | j     |
        |-------|-------|-------|
        
        """
               
        if self.atomic_grid == {}:
            #-----------------------------------------------------------------
            #                 distribute_atoms_by_sectors
            #-----------------------------------------------------------------
            initial          = time.time()
            self.build_atomic_grid()
            final = time.time() 
            print ('build_atomic_grid end -  total time: ', final - initial, '\n')
        
        
        self.index_bonds_pairs = []
        self.index_bonds       = []
        nCPUs  =  multiprocessing.cpu_count()
        
        
        print ('Delta compression using up to', nCPUs ,'threads.')
        #'''
        #--------------------------------------------------------------------------------------------------
        #  (1)      P A R A L L E L        Calculate distances between atoms in a sector
        #--------------------------------------------------------------------------------------------------
        initial       = time.time()
        pool          = multiprocessing.Pool(nCPUs)        
        grid_elements = self.atomic_grid.values()
        
        pool_of_index_bonds = (pool.map(C_generate_bonds2, grid_elements))
        
        for index_bonds in pool_of_index_bonds:
            for pair_of_indexes in index_bonds:
                self.index_bonds.append(pair_of_indexes[0])
                self.index_bonds.append(pair_of_indexes[1]) 
                self.index_bonds_pairs.append(pair_of_indexes)      
        final = time.time()    
        print ('Cython PARALLEL C_generate connections between atoms within a single element of the atomic grid total time: ', final - initial, '\n')
        #--------------------------------------------------------------------------------------------------
        #'''
        
        #--------------------------------------------------------------------------------------------------
        #  (2)      P A R A L L E L        Calculate distances between atoms in neighboring sectors  
        #--------------------------------------------------------------------------------------------------
        pair_of_sectors2 = self.determine_the_paired_atomic_grid_elements()
        #-----------------------------------------------------------------------------------------
        initial = time.time()
        pool_of_index_bonds = (pool.map(calculate_distances_between_sectors_parallel2, pair_of_sectors2))
        for index_bonds in pool_of_index_bonds:
            for pair_of_indexes in index_bonds:
                self.index_bonds.append(pair_of_indexes[0])
                self.index_bonds.append(pair_of_indexes[1]) 
                self.index_bonds_pairs.append(pair_of_indexes)
        final = time.time()    
        print ('Cython PARALLEL C_generate connections between atoms between different elements of the atomic grid total time: ', final - initial, '\n')  
        #--------------------------------------------------------------------------------------------------

    
    def determine_the_paired_atomic_grid_elements(self):
        '''
        There is also an array vOff that specifies the offsets of each of the 14 neighbor
        cells. The array covers half the neighboring cells, together with the cell itself; its
        size and contents are specified as
        
        {{0,0,0}, {1,0,0}, {1,1,0}, {0,1,0}, {-1,1,0}, {0,0,1},
        {1,0,1}, {1,1,1}, {0,1,1}, {-1,1,1}, {-1,0,1},
        {-1,-1,1}, {0,-1,1}, {1,-1,1}}
        
        '''
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
        
        for element in self.atomic_grid.keys():
            for offset_element in  grid_offset:              
                
                element1  = (element[0], 
                             element[1], 
                             element[2])
                              
                element2  = (element[0]+offset_element[0], 
                             element[1]+offset_element[1], 
                             element[2]+offset_element[2]) 
                        
                if element2 in self.atomic_grid:                        
                    pair_of_sectors2.append([self.atomic_grid[element1],
                                             self.atomic_grid[element2]])

        final = time.time()    
        print ('Pairwise grid elements time : ', final - initial, '\n')  
        return pair_of_sectors2
    
    
    
    
    
    
    
    
    
    
    
    
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
    
    def build_atomic_grid (self, log= True):
        """  fucntion build_atomic_grid
        
        This function organizes the atoms in their respective position 
        of the grid (atomic grid) - Nescessary to calculate distances between 
        atoms in different elements of the grid
        
        self.grid_size = is the size of a grid element - size of a sector
        
        """
        initial = time.time() 
        self.atomic_grid == {}
        '''
        for atom in self.atoms:
            a = int((atom.pos[0]) / self.grid_size)
            b = int((atom.pos[1]) / self.grid_size)
            c = int((atom.pos[2]) / self.grid_size)
            
            if (a,b,c) in self.sectors:
                #self.sectors[(a,b,c)].append(atom.index-1)
                self.sectors [(a,b,c)].append(atom)
            else:
                self.sectors [(a,b,c)] = []
                #self.sectors[(a,b,c)].append(atom.index-1) 
                self.sectors [(a,b,c)].append(atom)
        '''
        for atom in self.atoms2:
            a = int((atom[3][0]) / self.grid_size)
            b = int((atom[3][1]) / self.grid_size)
            c = int((atom[3][2]) / self.grid_size)
            
            if (a,b,c) in self.atomic_grid:
                #self.sectors[(a,b,c)].append(atom.index-1)
                self.atomic_grid[(a,b,c)].append(atom)
            else:
                self.atomic_grid[(a,b,c)] = []
                #self.sectors[(a,b,c)].append(atom.index-1) 
                self.atomic_grid[(a,b,c)].append(atom)

        final = time.time() 
        print ('building atomic grid total time: ', final - initial, '\n')
        
        if log:
            print (
'''
-----------------------------------------------------------------        
          V I S M O L   G R I D   P A R A M E T E R S
-----------------------------------------------------------------        
''')           
            print ('grid size          = ', self.grid_size)
            print ('Number of elements = ', len(self.atomic_grid))
            #print (self.atomic_grid)
            print ('''-----------------------------------------------------------------''')
        


def calculate_distances_between_sectors_parallel2(pair_of_sectors):
    index_bonds = C_generate_bonds_between_sectors2(pair_of_sectors[0], 
                                                    pair_of_sectors[1])
    return index_bonds

def calculate_distances_per_sectors_parallel2 (sector):
    index_bonds = C_generate_bonds2(sector)
    return index_bonds

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
