#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  vis_parser.py
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

import numpy as np
import time
import multiprocessing


#cpdef list C_generate_bonds2(atoms, coords):
#    #print (coords[0])
#    """
#        Calculate the distances and bonds 
#        between atoms within a single element 
#        of the atomic grid
#        
#                  |-------|-------|-------|
#                  |       |       |       |
#                  |       |       |       |
#                  |       |       |       |
#                  |-------|-atoms-|-------|
#                  |       |       |       |
#                  |       | i<->j |       |
#                  |       |       |       |
#                  |-------|-------|-------|
#                  |       |       |       |
#                  |       |       |       |
#                  |       |       |       |
#                  |-------|-------|-------|
#    
#    
#    
#    atoms = [[index, at_name, cov_rad,  at_pos, at_res_i, at_res_n, at_ch], ...]
#            each elemte is a list contain required data.
#    
#    
#    index_bonds2 [[a,b],[b,c], ...] where a and b are indexes. 
#    returns a list of pair of indexes "index_bonds2"
#    
#    """
#
#    index_bonds2 = []
#
#    cdef int i
#    cdef int j
#    cdef int size
#    cdef int index_i
#
#    cdef double atom_ix
#    cdef double atom_iy
#    cdef double atom_iz
#    cdef double cov_rad_i, cov_rad_j
#    
#    cdef double r_ij
#    cdef double dX
#    cdef double dY
#    cdef double dZ
#
#    size =  len(atoms)
#    
#    for i in range (0, size-1):
#        atom_ix   = coords[i*3    ]
#        atom_iy   = coords[i*3 + 1]  
#        atom_iz   = coords[i*3 + 2] 
#        cov_rad_i = atoms[i][2]
#        index_i   = atoms[i][0]
#        
#        for j in range (i+1, size):    
#            
#            dX              = (atom_ix - coords[j*3    ])**2
#            dY              = (atom_iy - coords[j*3 + 1])**2
#            dZ              = (atom_iz - coords[j*3 + 2])**2
#            
#            cov_rad_j       = atoms[j][2]
#            cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*1.2
#            
#            
#            if (dX > cov_rad_ij_sqrt or 
#                dY > cov_rad_ij_sqrt or 
#                dZ > cov_rad_ij_sqrt):
#                pass
#
#            else:
#                r_ij = (dX + dY + dZ)
#                if r_ij <= cov_rad_ij_sqrt:
#                    index_bonds2.append([index_i , atoms[j][0]])
#                    #index_bonds .append( index_i           )
#                    #index_bonds .append( atoms[j].index -1 )
#                    #atoms[i].connected.append(atoms[j])
#                    #atoms[j].connected.append(atoms[i])
#                else:
#                    pass
#
#    return index_bonds2#, index_bonds
#
#cpdef list C_generate_bonds_old(list atoms):
#    """
#        Calculate the distances and bonds 
#        between atoms within a single element 
#        of the atomic grid
#        
#                  |-------|-------|-------|
#                  |       |       |       |
#                  |       |       |       |
#                  |       |       |       |
#                  |-------|-atoms-|-------|
#                  |       |       |       |
#                  |       | i<->j |       |
#                  |       |       |       |
#                  |-------|-------|-------|
#                  |       |       |       |
#                  |       |       |       |
#                  |       |       |       |
#                  |-------|-------|-------|
#    
#    
#    
#    atoms = [[index, at_name, cov_rad,  at_pos, at_res_i, at_res_n, at_ch], ...]
#            each elemte is a list contain required data.
#    
#    
#    index_bonds2 [[a,b],[b,c], ...] where a and b are indexes. 
#    returns a list of pair of indexes "index_bonds2"
#    
#    """
#
#    index_bonds2 = []
#    index_bonds  = [] 
#    cdef int i
#    cdef int j
#    cdef int size
#    cdef int index_i
#
#    cdef double atom_ix
#    cdef double atom_iy
#    cdef double atom_iz
#    cdef double cov_rad_i, cov_rad_j
#    
#    cdef double r_ij
#    cdef double dX
#    cdef double dY
#    cdef double dZ
#
#    size =  len(atoms)
#    
#    for i in range (0, size-1):
#        atom_ix   = atoms[i][3][0]
#        atom_iy   = atoms[i][3][1]    
#        atom_iz   = atoms[i][3][2]
#        cov_rad_i = atoms[i][2]
#        index_i   = atoms[i][0]
#        
#        for j in range (i+1, size):    
#            #if atoms[i][9] == atoms[j][9]:
#            dX              = (atom_ix - atoms[j][3][0])**2
#            dY              = (atom_iy - atoms[j][3][1])**2
#            dZ              = (atom_iz - atoms[j][3][2])**2
#            
#            cov_rad_j       = atoms[j][2]
#            
#            cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*1.4
#            
#            
#            if (dX > cov_rad_ij_sqrt or 
#                dY > cov_rad_ij_sqrt or 
#                dZ > cov_rad_ij_sqrt):
#                pass
#
#            else:
#                r_ij = (dX + dY + dZ)
#                if r_ij <= cov_rad_ij_sqrt:
#                    pass
#                    index_bonds2.append([index_i , atoms[j][0]])
#                    
#                    index_bonds.append  (index_i               )
#                    index_bonds.append  (atoms[j][0]           )                 
#                    
#                    atoms[i][8].append  (atoms[j][0]           )
#                    atoms[j][8].append  (atoms[i][0]           )
#                else:
#                    pass
#
#    return atoms
#
##'''
#cpdef list C_generate_bonds_between_sectors_old(list atoms1, list atoms2):
#    """
#   
#    Calculate the distances and connections 
#    between atoms from different elements 
#    of the atomic grid
#    
#                |-------|-------|-------|
#                |       |       |       |
#                |       |       |       |
#                |       |       |       |
#                |-------|-atoms1|-------|
#                |       |   i   |       |
#                |       |    \  |       |
#                |       |     \ |       |
#                |-------|------\|-atoms2|
#                |       |       \       |
#                |       |       |\      |
#                |       |       | j     |
#                |-------|-------|-------|
#    
#    
#    atoms1 = [[index, at_name, cov_rad,  at_pos, at_res_i, at_res_n, at_ch], ...]
#    
#    atoms2 = [[index, at_name, cov_rad,  at_pos, at_res_i, at_res_n, at_ch], ...]
#
#    index_bonds2 [[a,b],[b,c], ...] where a and b are indexes. 
#    returns a list of pair of indexes "index_bonds2"
#    """
#    cdef list index_bonds2 = []
#    cdef list index_bonds  = [] 
#
#    cdef int i
#    cdef int j
#    cdef int size1, size2
#    cdef int index_i
#    cdef double atom_ix
#    cdef double atom_iy
#    cdef double atom_iz
#    cdef double cov_rad_i, cov_rad_j
#    cdef double r_ij
#    cdef double dX
#    cdef double dY
#    cdef double dZ
#    
#    
#    size1 =  len(atoms1)
#    size2 =  len(atoms2)
#
#    for i in range (0, size1):   
#        atom_ix   = atoms1[i][3][0]
#        atom_iy   = atoms1[i][3][1]    
#        atom_iz   = atoms1[i][3][2]
#        cov_rad_i = atoms1[i][2]
#        index_i   = atoms1[i][0]
#
#        for j in range (0, size2):    
#
#            dX              = (atom_ix - atoms2[j][3][0])**2
#            dY              = (atom_iy - atoms2[j][3][1])**2
#            dZ              = (atom_iz - atoms2[j][3][2])**2
#
#            cov_rad_j       = atoms2[j][2]
#            cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*1.4
#            
#            #if (dX > cov_rad_ij_sqrt or 
#            #    dY > cov_rad_ij_sqrt or 
#            #    dZ > cov_rad_ij_sqrt):
#            #    pass
#            #
#            #else:
#                
#            r_ij = (dX + dY + dZ)
#            
#            if r_ij <= cov_rad_ij_sqrt:
#                index_bonds2.append( [index_i , atoms2[j][0]] )
#                
#                index_bonds.append   (index_i                 )
#                index_bonds.append   (atoms2[j][0]            )                 
#                
#                atoms1[i][8].append  (atoms2[j][0]            )
#                atoms2[j][8].append  (atoms1[i][0]            )
#            else:
#                pass
#
#    return index_bonds2#, index_bonds
#
#
#



cpdef tuple C_generate_bonds (list list_of_atoms        , 
                              list atoms                , 
                              list bonds_pair_of_indexes,  #indexes of connected atoms
                              list bonds_full_indexes   ,
                              list non_bonded_list      ): #pairs_of_

    
    #list_of_atoms atoms bonds_full_indexes     bonds_pair_of_indexes    non_bonded_list      
    
    """
        Calculate the distances and bonds 
        between atoms within a single element 
        of the atomic grid
        
                  |-------|-------|-------|
                  |       |       |       |
                  |       |       |       |
                  |       |       |       |
                  |-------|-atoms-|-------|
                  |       |       |       |
                  |       | i<->j |       |
                  |       |       |       |
                  |-------|-------|-------|
                  |       |       |       |
                  |       |       |       |
                  |       |       |       |
                  |-------|-------|-------|
    
    
    
    atoms = [[index, at_name, cov_rad,  at_pos, at_res_i, at_res_n, at_ch], ...]
            each elemte is a list contain required data.
    
    
    bonds_pair_of_indexes [[a,b],[b,c], ...] where a and b are indexes. 
    returns a list of pair of indexes "bonds_pair_of_indexes"
    
    """

    cdef int i
    cdef int j
    cdef int size
    cdef int index_i

    cdef double atom_ix
    cdef double atom_iy
    cdef double atom_iz
    cdef double cov_rad_i, cov_rad_j
    
    cdef double r_ij
    cdef double dX
    cdef double dY
    cdef double dZ

    size =  len(list_of_atoms)
    
    cdef int list_index = 0 
    
    for i in range (0, size-1):
        atom_ix   = list_of_atoms[i][3][0]
        atom_iy   = list_of_atoms[i][3][1]    
        atom_iz   = list_of_atoms[i][3][2]
        cov_rad_i = list_of_atoms[i][2]
        index_i   = list_of_atoms[i][0]
        
        for j in range (i+1, size):    
            
            dX              = (atom_ix - list_of_atoms[j][3][0])**2
            dY              = (atom_iy - list_of_atoms[j][3][1])**2
            dZ              = (atom_iz - list_of_atoms[j][3][2])**2
            
            cov_rad_j       = atoms[j][2]
            
            cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*1.4
            
            
            if (dX > cov_rad_ij_sqrt or 
                dY > cov_rad_ij_sqrt or 
                dZ > cov_rad_ij_sqrt):
                pass

            else:
                r_ij = (dX + dY + dZ)
                if r_ij <= cov_rad_ij_sqrt:
                    index_j = list_of_atoms[j][0]
                    
                    print ([index_i,index_j])
                    
                    bonds_pair_of_indexes.append( [index_i, index_j])
                    
                    bonds_full_indexes.append(index_i  )
                    bonds_full_indexes.append(index_j  )                 
                    
                    atoms[index_i][8].append(index_j)
                    atoms[index_j][8].append(index_i)
                    
                    non_bonded_list[index_i] = False
                    non_bonded_list[index_j] = False
               
                else:
                    pass

    return atoms, bonds_full_indexes , bonds_pair_of_indexes, non_bonded_list
          #atoms, bonds_full_indexes, bonds_pair_of_indexes, non_bonded_list
          
          
          
cpdef tuple C_generate_bonds_between_sectors (list list_of_atoms1       , 
                                              list list_of_atoms2       , 
                                              list atoms                , 
                                              list bonds_pair_of_indexes,  #indexes of connected atoms
                                              list bonds_full_indexes   ,
                                              list non_bonded_list      ):
    """
   
    Calculate the distances and connections 
    between atoms from different elements 
    of the atomic grid
    
                |-------|-------|-------|
                |       |       |       |
                |       |       |       |
                |       |       |       |
                |-------|-atoms1|-------|
                |       |   i   |       |
                |       |    \  |       |
                |       |     \ |       |
                |-------|------\|-atoms2|
                |       |       \       |
                |       |       |\      |
                |       |       | j     |
                |-------|-------|-------|
    
    
    atoms1 = [[index, at_name, cov_rad,  at_pos, at_res_i, at_res_n, at_ch], ...]
    
    atoms2 = [[index, at_name, cov_rad,  at_pos, at_res_i, at_res_n, at_ch], ...]

    bonds_pair_of_indexes [[a,b],[b,c], ...] where a and b are indexes. 
    returns a list of pair of indexes "bonds_pair_of_indexes"
    """

    cdef int i
    cdef int j
    cdef int size1, size2
    cdef int index_i
    cdef double atom_ix
    cdef double atom_iy
    cdef double atom_iz
    cdef double cov_rad_i, cov_rad_j
    cdef double r_ij
    cdef double dX
    cdef double dY
    cdef double dZ
    
    
    size1 =  len(list_of_atoms1)
    size2 =  len(list_of_atoms2)

    for i in range (0, size1):   
        atom_ix   = list_of_atoms1[i][3][0]
        atom_iy   = list_of_atoms1[i][3][1]    
        atom_iz   = list_of_atoms1[i][3][2]
        cov_rad_i = list_of_atoms1[i][2]
        index_i   = list_of_atoms1[i][0]

        for j in range (0, size2):   
            
            index_j = list_of_atoms2[j][0]
            
            if index_j == index_i:
                pass
            
            else:
                
                dX              = (atom_ix - list_of_atoms2[j][3][0])**2
                dY              = (atom_iy - list_of_atoms2[j][3][1])**2
                dZ              = (atom_iz - list_of_atoms2[j][3][2])**2

                cov_rad_j       = list_of_atoms2[j][2]
                cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*1.4
                
                if (dX > cov_rad_ij_sqrt or 
                    dY > cov_rad_ij_sqrt or 
                    dZ > cov_rad_ij_sqrt):
                    pass

                else:
                    
                    r_ij = (dX + dY + dZ)
                    
                    if r_ij <= cov_rad_ij_sqrt:
                        
                        bonds_pair_of_indexes.append( [index_i, index_j])
                        
                        bonds_full_indexes.append(index_i  )
                        bonds_full_indexes.append(index_j  )                 
                        
                        atoms[index_i][8].append(index_j)
                        atoms[index_j][8].append(index_i)
                        
                        non_bonded_list[index_i] = False
                        non_bonded_list[index_j] = False
                    
                    else:
                        pass

    return atoms, bonds_full_indexes, bonds_pair_of_indexes, non_bonded_list

cpdef dict build_atomic_grid (list atoms):
    """  fucntion build_atomic_grid
    
    This function organizes the atoms in their respective position 
    of the grid (atomic grid) - Nescessary to calculate distances between 
    atoms in different elements of the grid
    
    self.grid_size = is the size of a grid element - size of a sector
    
    
              atomic grid
              
        |-------|-------|-------| |
        |       | grid  |       | |
        |       |element|       | | grid_size
        |-1,1,0 | 0,1,0 | 1,1,0 | |
        |-------|-------|-------| |
        |       |       |       |
        |       |       |       |
        |-1,0,0 | 0,0,0 | 1,0,0 |
        |-------|-------|-------|
        |       |       |       |
        |       |       |       |
        |-1,-1,0| 0,-1,0| 1,-1,0|
        |-------|-------|-------|
                         -------
                        grid_size
    
    
    grid element = list of atoms
    """
    #int grid_size
    cdef dict  atomic_grid = {}
    
    for atom in atoms:
        a = atom[9][0]
        b = atom[9][1]
        c = atom[9][2]
        
        if (a,b,c) in atomic_grid:
            atomic_grid[(a,b,c)].append(atom)
        else:
            atomic_grid[(a,b,c)] = []
            atomic_grid[(a,b,c)].append(atom)
    return atomic_grid

cpdef list determine_the_paired_atomic_grid_elements(atomic_grid):
    '''
    There is also an array vOff that specifies the offsets of each of the 14 neighbor
    cells. The array covers half the neighboring cells, together with the cell itself; its
    size and contents are specified as
    
    {{0,0,0}, {1,0,0}, {1,1,0}, {0,1,0}, {-1,1,0}, {0,0,1},
    {1,0,1}, {1,1,1}, {0,1,1}, {-1,1,1}, {-1,0,1},
    {-1,-1,1}, {0,-1,1}, {1,-1,1}}
    
    
                                |-------|-------|-------| 
                                |\\\\\\\|\\\\\\\|\\\\\\\| 
                                |\\\\\\\|\\\\\\\|\\\\\\\| 
                                |-1,1,1 | 0,1,1 | 1,1,1 | 
                                |-------|-------|-------| 
                                |\\\\\\\|\\\\\\\|\\\\\\\|
                                |\\\\\\\|\\\\\\\|\\\\\\\|
                                |-1,0,1 | 0,0,1 | 1,0,1 |
                                |-------|-------|-------|
                                |\\\\\\\|\\\\\\\|\\\\\\\|
                                |\\\\\\\|\\\\\\\|\\\\\\\|
                                |-1,-1,1| 0,-1,1| 1,-1,1|
                                |-------|-------|-------|
        
        |-------|-------|-------| 
        |\\\\\\\|\\\\\\\|\\\\\\\| 
        |\\\\\\\|\\\\\\\|\\\\\\\| 
        |-1,1,0 | 0,1,0 | 1,1,0 | 
        |-------|-------|-------| 
        |       |XXXXXXX|\\\\\\\|
        |       |XXXXXXX|\\\\\\\|
        |-1,0,0 | 0,0,0 | 1,0,0 |
        |-------|-------|-------|
        |       |       |       |
        |       |       |       |
        |-1,-1,0| 0,-1,0| 1,-1,0|
        |-------|-------|-------|
    
    always. the combination between {0,0,0} and some element of the list (\\\\\\) 
    
    returns a list contain lists of atoms [[atoms1],atoms2], ...]

    '''
    cdef list pair_of_sectors2
    cdef list grid_offset
    #cdef list element
    #cdef list offset_element
    
    #initial = time.time()
    
    pair_of_sectors2 = []
    grid_offset = [
                             #[ 1,-1, 0],
                             #[ 0,-1, 0],
                             #[-1,-1, 0],
                             #[-1, 0, 0],
                   [ 0, 0, 0], 
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
    done = []
    for element in atomic_grid.keys():
        for offset_element in  grid_offset:              
            
            element1  = (element[0], 
                         element[1], 
                         element[2])
                          
            element2  = (element[0]+offset_element[0], 
                         element[1]+offset_element[1], 
                         element[2]+offset_element[2]) 
                    
            if element2 in atomic_grid:                        
                #pair_of_sectors2.append([atomic_grid[element1][0],
                #                         atomic_grid[element2][0]])
                
                if [element1, element2] in done or [element2, element1] in done:
                    print ('already in the list:'[element1, element2])
                    pass
                
                
                else:
                    done.append([element1, element2])
                    pair_of_sectors2.append([atomic_grid[element1],
                                             atomic_grid[element2]])
                    
                    print([element1, element2])

    return pair_of_sectors2






cpdef tuple C_generate_bonds_int_lists (list list_of_atoms  , 
                                        list atoms          , 
                                        list bonds_pair_of_indexes   ,  #indexes of connected atoms
                                        list bonds_full_indexes    ,
                                        list non_bonded_list): #pairs_of_
    """
        Calculate the distances and bonds 
        between atoms within a single element 
        of the atomic grid
        
                  |-------|-------|-------|
                  |       |       |       |
                  |       |       |       |
                  |       |       |       |
                  |-------|-atoms-|-------|
                  |       |       |       |
                  |       | i<->j |       |
                  |       |       |       |
                  |-------|-------|-------|
                  |       |       |       |
                  |       |       |       |
                  |       |       |       |
                  |-------|-------|-------|
    
    
    
    atoms = [[index, at_name, cov_rad,  at_pos, at_res_i, at_res_n, at_ch], ...]
            each elemte is a list contain required data.
    
    
    bonds_pair_of_indexes [[a,b],[b,c], ...] where a and b are indexes. 
    returns a list of pair of indexes "bonds_pair_of_indexes"
    
    """

    cdef int i
    cdef int j
    cdef int size
    cdef int index_i

    cdef double atom_ix
    cdef double atom_iy
    cdef double atom_iz
    cdef double cov_rad_i, cov_rad_j
    
    cdef double r_ij
    cdef double dX
    cdef double dY
    cdef double dZ

    size =  len(atoms)
    
    cdef int list_index = 0 
    
    for i in list_of_atoms[:-1]:
        atom_ix   = atoms[i][3][0]
        atom_iy   = atoms[i][3][1]    
        atom_iz   = atoms[i][3][2]
        cov_rad_i = atoms[i][2]
        index_i   = atoms[i][0]
        
        list_index+= 1
        
        for j in list_of_atoms[list_index:]:    
            if i == j:
                pass
            
            else:
                dX              = (atom_ix - atoms[j][3][0])**2
                dY              = (atom_iy - atoms[j][3][1])**2
                dZ              = (atom_iz - atoms[j][3][2])**2
                
                cov_rad_j       = atoms[j][2]
                
                cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*1.4
                
                
                if (dX > cov_rad_ij_sqrt or 
                    dY > cov_rad_ij_sqrt or 
                    dZ > cov_rad_ij_sqrt):
                    pass

                else:
                    r_ij = (dX + dY + dZ)
                    if r_ij <= cov_rad_ij_sqrt:
                        pass
                        bonds_pair_of_indexes.append([index_i , atoms[j][0]])
                        
                        bonds_full_indexes.append  (index_i               )
                        bonds_full_indexes.append  (atoms[j][0]           )                 
                        
                        atoms[i][8].append  (atoms[j][0]           )
                        atoms[j][8].append  (atoms[i][0]           )
                        
                        #non_bonded_list[index_i    ] = False
                        #non_bonded_list[atoms[j][0]] = False

                    
                    else:
                        pass

    return atoms, bonds_full_indexes , bonds_pair_of_indexes, non_bonded_list

cpdef tuple C_generate_bonds_between_sectors_int_lists (list lits_of_atoms1       , 
                                                        list lits_of_atoms2       , 
                                                        list atoms                , 
                                                        list bonds_pair_of_indexes,  #indexes of connected atoms
                                                        list bonds_full_indexes   ,
                                                        list non_bonded_list      ):
    """
   
    Calculate the distances and connections 
    between atoms from different elements 
    of the atomic grid
    
                |-------|-------|-------|
                |       |       |       |
                |       |       |       |
                |       |       |       |
                |-------|-atoms1|-------|
                |       |   i   |       |
                |       |    \  |       |
                |       |     \ |       |
                |-------|------\|-atoms2|
                |       |       \       |
                |       |       |\      |
                |       |       | j     |
                |-------|-------|-------|
    
    
    atoms1 = [[index, at_name, cov_rad,  at_pos, at_res_i, at_res_n, at_ch], ...]
    
    atoms2 = [[index, at_name, cov_rad,  at_pos, at_res_i, at_res_n, at_ch], ...]

    bonds_pair_of_indexes [[a,b],[b,c], ...] where a and b are indexes. 
    returns a list of pair of indexes "bonds_pair_of_indexes"
    """

    cdef int i
    cdef int j
    cdef int size1, size2
    cdef int index_i
    cdef double atom_ix
    cdef double atom_iy
    cdef double atom_iz
    cdef double cov_rad_i, cov_rad_j
    cdef double r_ij
    cdef double dX
    cdef double dY
    cdef double dZ
    
    
    #size1 =  len(atoms1)
    #size2 =  len(atoms2)

    for i in lits_of_atoms1:   
        atom_ix   = atoms[i][3][0]
        atom_iy   = atoms[i][3][1]    
        atom_iz   = atoms[i][3][2]
        cov_rad_i = atoms[i][2]
        index_i   = atoms[i][0]

        for j in lits_of_atoms2:    
            index_j = atoms[j][0]
            #if 
            
            dX              = (atom_ix - atoms[j][3][0])**2
            dY              = (atom_iy - atoms[j][3][1])**2
            dZ              = (atom_iz - atoms[j][3][2])**2

            cov_rad_j       = atoms[j][2]
            cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*1.2
            
            if (dX > cov_rad_ij_sqrt or 
                dY > cov_rad_ij_sqrt or 
                dZ > cov_rad_ij_sqrt):
                pass

            else:
                
                r_ij = (dX + dY + dZ)
                
                if r_ij <= cov_rad_ij_sqrt:
                    bonds_pair_of_indexes.append( [index_i , atoms[j][0]] )
                    
                    bonds_full_indexes.append   (index_i                )
                    bonds_full_indexes.append   (atoms[j][0]            )                 
                    
                    atoms[i][8].append   (atoms[j][0]            )
                    atoms[j][8].append   (atoms[i][0]            )
                    
                    #non_bonded_list[index_i    ] = False
                    #non_bonded_list[atoms[j][0]] = False
                
                else:
                    pass

    return atoms, bonds_full_indexes, bonds_pair_of_indexes, non_bonded_list


cpdef dict build_atomic_grid_list(list atoms):
    """  fucntion build_atomic_grid
    
    This function organizes the atoms in their respective position 
    of the grid (atomic grid) - Nescessary to calculate distances between 
    atoms in different elements of the grid
    
    self.grid_size = is the size of a grid element - size of a sector
    
    
              atomic grid
              
        |-------|-------|-------| |
        |       | grid  |       | |
        |       |element|       | | grid_size
        |-1,1,0 | 0,1,0 | 1,1,0 | |
        |-------|-------|-------| |
        |       |       |       |
        |       |       |       |
        |-1,0,0 | 0,0,0 | 1,0,0 |
        |-------|-------|-------|
        |       |       |       |
        |       |       |       |
        |-1,-1,0| 0,-1,0| 1,-1,0|
        |-------|-------|-------|
                         -------
                        grid_size
    
    
    grid element = list of atoms
    """
    #int grid_size
    cdef dict  atomic_grid = {}
    
    for atom in atoms:
        a = atom[9][0]
        b = atom[9][1]
        c = atom[9][2]
        
        if (a,b,c) in atomic_grid:
            atomic_grid[(a,b,c)].append(atom[0])
        else:
            atomic_grid[(a,b,c)] = []
            atomic_grid[(a,b,c)].append(atom[0])
    return atomic_grid


cpdef dict build_atomic_grid_int_lists (list atoms):
    """  fucntion build_atomic_grid
    
    This function organizes the atoms in their respective position 
    of the grid (atomic grid) - Nescessary to calculate distances between 
    atoms in different elements of the grid
    
    self.grid_size = is the size of a grid element - size of a sector
    
    
              atomic grid
              
        |-------|-------|-------| |
        |       | grid  |       | |
        |       |element|       | | grid_size
        |-1,1,0 | 0,1,0 | 1,1,0 | |
        |-------|-------|-------| |
        |       |       |       |
        |       |       |       |
        |-1,0,0 | 0,0,0 | 1,0,0 |
        |-------|-------|-------|
        |       |       |       |
        |       |       |       |
        |-1,-1,0| 0,-1,0| 1,-1,0|
        |-------|-------|-------|
                         -------
                        grid_size
    
    
    grid element = list of atoms
    """
    #int grid_size
    cdef dict  atomic_grid = {}
    
    for atom in atoms:
        a = atom[9][0]
        b = atom[9][1]
        c = atom[9][2]
        
        if (a,b,c) in atomic_grid:
            atomic_grid[(a,b,c)].append(atom[0])
        else:
            atomic_grid[(a,b,c)] = []
            atomic_grid[(a,b,c)].append(atom[0])
    return atomic_grid
















