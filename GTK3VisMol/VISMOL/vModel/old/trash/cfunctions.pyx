#from cython.parallel import parallel, prange
#cimport openmp
#from libc.stdlib cimport malloc, free
#import cython 
#from cython.parallel import prange, parallel




import numpy as np
import time
import multiprocessing


#'''
cpdef list C_generate_bonds2(list atoms):
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
    
    
    index_bonds2 [[a,b],[b,c], ...] where a and b are indexes. 
    returns a list of pair of indexes "index_bonds2"
    
    """

    index_bonds2 = []

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
    
    for i in range (0, size-1):
        atom_ix   = atoms[i][3][0]
        atom_iy   = atoms[i][3][1]    
        atom_iz   = atoms[i][3][2]
        cov_rad_i = atoms[i][2]
        index_i   = atoms[i][0]
        
        for j in range (i+1, size):    
            
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
                    index_bonds2.append([index_i , atoms[j][0]])
                    #index_bonds .append( index_i           )
                    #index_bonds .append( atoms[j].index -1 )
                    #atoms[i].connected.append(atoms[j])
                    #atoms[j].connected.append(atoms[i])
                else:
                    pass

    return index_bonds2#, index_bonds

#'''
cpdef list C_generate_bonds_between_sectors2(list atoms1, list atoms2):
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

    index_bonds2 [[a,b],[b,c], ...] where a and b are indexes. 
    returns a list of pair of indexes "index_bonds2"
    """
    cdef list index_bonds2 = []

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
    
    
    size1 =  len(atoms1)
    size2 =  len(atoms2)

    for i in range (0, size1):   
        atom_ix   = atoms1[i][3][0]
        atom_iy   = atoms1[i][3][1]    
        atom_iz   = atoms1[i][3][2]
        cov_rad_i = atoms1[i][2]
        index_i   = atoms1[i][0]

        for j in range (0, size2):    

            dX              = (atom_ix - atoms2[j][3][0])**2
            dY              = (atom_iy - atoms2[j][3][1])**2
            dZ              = (atom_iz - atoms2[j][3][2])**2

            cov_rad_j       = atoms2[j][2]
            cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*1.4
            
            if (dX > cov_rad_ij_sqrt or 
                dY > cov_rad_ij_sqrt or 
                dZ > cov_rad_ij_sqrt):
                pass

            else:
                
                r_ij = (dX + dY + dZ)
                
                if r_ij <= cov_rad_ij_sqrt:
                    index_bonds2.append([index_i , atoms2[j][0]])
                    
                    #index_bonds .append( index_i           )
                    #index_bonds .append( atoms[j].index -1 )
                    #atoms1[i].connected.append(atoms2[j])
                    #atoms2[j].connected.append(atoms1[i])
                else:
                    pass

    return index_bonds2#, index_bonds


cpdef dict build_atomic_grid (list atoms, int grid_size = 3):
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
        a = int((atom[3][0]) / grid_size)
        b = int((atom[3][1]) / grid_size)
        c = int((atom[3][2]) / grid_size)
        
        if (a,b,c) in atomic_grid:
            atomic_grid[(a,b,c)].append(atom)
        else:
            atomic_grid[(a,b,c)] = []
            atomic_grid[(a,b,c)].append(atom)
    return atomic_grid

    
cpdef list determine_the_paired_atomic_grid_elements(dict atomic_grid):
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
            
            element1  = (element[0], 
                         element[1], 
                         element[2])
                          
            element2  = (element[0]+offset_element[0], 
                         element[1]+offset_element[1], 
                         element[2]+offset_element[2]) 
                    
            if element2 in atomic_grid:                        
                pair_of_sectors2.append([atomic_grid[element1],
                                         atomic_grid[element2]])

    final = time.time()    
    print ('Pairwise grid elements time : ', final - initial, '\n')  
    return pair_of_sectors2
    

cpdef list calculate_distances_between_grid_elements_parallel2(list pair_of_grid_elements):
    cdef list index_bonds
    index_bonds = C_generate_bonds_between_sectors2(pair_of_grid_elements[0], 
                                                    pair_of_grid_elements[1])
    
    return index_bonds


cpdef list calculate_distances_per_grid_element_parallel2 (list grid_element):
    cdef list index_bonds
    index_bonds = C_generate_bonds2(grid_element)
    return index_bonds

    
cpdef full_generate_bonds (list atoms):
    """ 
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
    cdef dict atomic_grid
    #cdef list full_index_bonds_pairs, full_index_bonds
    cdef int nCPUs
    cdef float initial, final
    
    
    atomic_grid = build_atomic_grid (atoms)
    
    full_index_bonds_pairs = []
    full_index_bonds       = []
    
    nCPUs  =  multiprocessing.cpu_count()
    print ('Delta compression using up to', nCPUs ,'threads.')
    #--------------------------------------------------------------------------------------------------
    
    
    
    #'''
    #--------------------------------------------------------------------------------------------------
    #  (1)      P A R A L L E L        Calculate distances between atoms in a sector
    #--------------------------------------------------------------------------------------------------
    initial       = time.time()
    #--------------------------------------------------------------------------------------------------
    pool          = multiprocessing.Pool(nCPUs)        
    grid_elements = atomic_grid.values()
    #with nogil:
    pool_of_index_bonds = (pool.map(C_generate_bonds2, grid_elements))
    #pool_of_index_bonds   = np.array(pool_of_index_bonds, dtype=np.int32)
    
    for index_bonds in pool_of_index_bonds:
        for pair_of_indexes in index_bonds:
            full_index_bonds.append(pair_of_indexes[0])
            full_index_bonds.append(pair_of_indexes[1]) 
            full_index_bonds_pairs.append(pair_of_indexes)      
    
    #--------------------------------------------------------------------------------------------------
    final = time.time()    
    print ('Cython PARALLEL C_generate connections between atoms within a single element of the atomic grid total time: ', final - initial, '\n')
    #--------------------------------------------------------------------------------------------------
    

    #'''
    #--------------------------------------------------------------------------------------------------
    #  (2)      P A R A L L E L        Calculate distances between atoms in neighboring sectors  
    #--------------------------------------------------------------------------------------------------
    initial = time.time()
    #--------------------------------------------------------------------------------------------------

    pair_of_grid_elements = determine_the_paired_atomic_grid_elements(atomic_grid)
    pool_of_index_bonds   = (pool.map(calculate_distances_between_grid_elements_parallel2, pair_of_grid_elements))
    
    #pool_of_index_bonds   = np.array(pool_of_index_bonds, dtype=np.int32)
    for index_bonds in pool_of_index_bonds:
        for pair_of_indexes in index_bonds:
            full_index_bonds.append(pair_of_indexes[0])
            full_index_bonds.append(pair_of_indexes[1]) 
            full_index_bonds_pairs.append(pair_of_indexes)
    #--------------------------------------------------------------------------------------------------
    final = time.time()    
    print ('Cython PARALLEL C_generate connections between atoms between different elements of the atomic grid total time: ', final - initial, '\n')  
    #--------------------------------------------------------------------------------------------------
    
    full_index_bonds       = np.array(full_index_bonds      , dtype=np.int32)
    full_index_bonds_pairs = np.array(full_index_bonds_pairs, dtype=np.int32)
    
    list_of_atoms          = range(0, len(atoms))
    list_of_atoms          = np.array(list_of_atoms         , dtype=np.int32)
    non_bonded_atoms       = generate_non_bonded_list (list_of_atoms, full_index_bonds)
    return  full_index_bonds , full_index_bonds_pairs, non_bonded_atoms
    

cpdef generate_non_bonded_list (list_of_atoms, full_index_bonds):
    
    
    

    non_bonded_atoms   =  []
    #initial = time.time()
    #
    #for atom_index in list_of_atoms:
    #    if atom_index in full_index_bonds:
    #        pass
    #    else:
    #        non_bonded_atoms.append(atom_index)
    non_bonded_atoms = np.array(non_bonded_atoms, dtype=np.uint32)
    #final = time.time()    
    #print ('Cython PARALLEL _generate_non_bonded_list total time: ', final - initial, '\n') 
    
    return non_bonded_atoms






'''







#'''




#'''
#cpdef full_generate_bonds (list atoms):
#cpdef full_generate_bonds (int [:] index  , 
#                         float [:] cov_rad, 
#                         float [:] X      ,  
#                         float [:] Y      , 
#                         float [:] Z      ):
#
#    """ 
#        (1)Calculate the distances and bonds 
#        between atoms within a single element 
#        of the atomic grid
#        |-------|-------|-------|
#        |       |       |       |
#        |       |       |       |
#        |       |       |       |
#        |-------|-------|-------|
#        |       |       |       |
#        |       | i<->j |       |
#        |       |       |       |
#        |-------|-------|-------|
#        |       |       |       |
#        |       |       |       |
#        |       |       |       |
#        |-------|-------|-------|
#        
#        
#        (2)Calculate the distances and connections 
#        between atoms between different elements 
#        of the atomic grid
#        |-------|-------|-------|
#        |       |       |       |
#        |       |       |       |
#        |       |       |       |
#        |-------|-------|-------|
#        |       |   i   |       |
#        |       |    \  |       |
#        |       |     \ |       |
#        |-------|------\|-------|
#        |       |       \       |
#        |       |       |\      |
#        |       |       | j     |
#        |-------|-------|-------|
#    
#    """
#    cdef dict atomic_grid
#    cdef list full_index_bonds_pairs, full_index_bonds, grid_elements
#    cdef int nCPUs
#    cdef float initial, final
#    
#    atomic_grid = build_atomic_grid (index, 
#                                     X    ,      
#                                     Y    ,      
#                                     Z    )     
#
#    full_index_bonds_pairs = []
#    full_index_bonds       = []
#    
#    nCPUs  =  multiprocessing.cpu_count()
#    
#    print ('Delta compression using up to', nCPUs ,'threads.')
#    #--------------------------------------------------------------------------------------------------
#    
#    
#    
#    #'''
#    #--------------------------------------------------------------------------------------------------
#    #  (1)      P A R A L L E L        Calculate distances between atoms in a sector
#    #--------------------------------------------------------------------------------------------------
#    initial       = time.time()
#    #--------------------------------------------------------------------------------------------------
#    pool          = multiprocessing.Pool(nCPUs)        
#    grid_elements = atomic_grid.values()
#    
#    pool_of_index_bonds = (pool.map(C_generate_bonds2, grid_elements))
#    #pool_of_index_bonds   = np.array(pool_of_index_bonds, dtype=np.int32)
#    for index_bonds in pool_of_index_bonds:
#        for pair_of_indexes in index_bonds:
#            full_index_bonds.append(pair_of_indexes[0])
#            full_index_bonds.append(pair_of_indexes[1]) 
#            full_index_bonds_pairs.append(pair_of_indexes)      
#    
#    #--------------------------------------------------------------------------------------------------
#    final = time.time()    
#    print ('Cython PARALLEL C_generate connections between atoms within a single element of the atomic grid total time: ', final - initial, '\n')
#    #--------------------------------------------------------------------------------------------------
#    
#
#    #'''
#    #--------------------------------------------------------------------------------------------------
#    #  (2)      P A R A L L E L        Calculate distances between atoms in neighboring sectors  
#    #--------------------------------------------------------------------------------------------------
#    initial = time.time()
#    #--------------------------------------------------------------------------------------------------
#
#    pair_of_grid_elements = determine_the_paired_atomic_grid_elements(atomic_grid)
#    pool_of_index_bonds   = (pool.map(calculate_distances_between_grid_elements_parallel2, pair_of_grid_elements))
#    
#    #pool_of_index_bonds   = np.array(pool_of_index_bonds, dtype=np.int32)
#    for index_bonds in pool_of_index_bonds:
#        for pair_of_indexes in index_bonds:
#            full_index_bonds.append(pair_of_indexes[0])
#            full_index_bonds.append(pair_of_indexes[1]) 
#            full_index_bonds_pairs.append(pair_of_indexes)
#    #--------------------------------------------------------------------------------------------------
#    final = time.time()    
#    print ('Cython PARALLEL C_generate connections between atoms between different elements of the atomic grid total time: ', final - initial, '\n')  
#    #--------------------------------------------------------------------------------------------------
#    
#    full_index_bonds       = np.array(full_index_bonds      , dtype=np.int32)
#    full_index_bonds_pairs = np.array(full_index_bonds_pairs, dtype=np.int32)
#    
#    list_of_atoms          = range(0, len(atoms))
#    list_of_atoms          = np.array(list_of_atoms         , dtype=np.int32)
#    non_bonded_atoms       = generate_non_bonded_list (list_of_atoms, full_index_bonds)
#    return  full_index_bonds , full_index_bonds_pairs, non_bonded_atoms
#












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


'''
def calculate_distance(atom_i, atoms):
    
    """ Function doc 
    if dist2 <= ((atoms[i].cov_rad + atoms[j].cov_rad)**2) *1.1:
    """
    cdef double dX
    cdef double dY
    cdef double dZ
    
    cdef double atom_ix   = atom_i.pos[0]
    cdef double atom_iy   = atom_i.pos[1]
    cdef double atom_iz   = atom_i.pos[2]
    cdef double cov_rad_i = atom_i.cov_rad
    cdef double cov_rad_j , cov_rad_ij_sqrt
    cdef double r_ij  
    indexes = []
    
    for atom_j in atoms:
        dX              = (atom_ix - atom_j.pos[0])**2
        dY              = (atom_iy - atom_j.pos[1])**2
        dZ              = (atom_iz - atom_j.pos[2])**2
        cov_rad_j       = atom_j.cov_rad
        cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*1.5

        if (dX**2 > cov_rad_ij_sqrt or 
            dY**2 > cov_rad_ij_sqrt or 
            dZ**2 > cov_rad_ij_sqrt):
            pass
        else:
            r_ij = (dX**2 + dY**2 + dZ**2)
            if r_ij <= cov_rad_ij_sqrt:  
                
                j_index = atom_j.index-1
                i_index = atom_i.index-1
                
                atom_i.connected.append(j_index)
                atom_j.connected.append(i_index)
                indexes.append([i_index, j_index])
    
    return indexes
'''   
'''
cpdef C_generate_bonds_between_sectors(sector_atoms_1 = None, sector_atoms_2 = None):
    
    bonds        = []
    index_bonds  = []
    index_bonds2 = []

    arr1  = np.array([0,0,1])
    cdef int i
    cdef int j
    
    for atom1 in sector_atoms_1:
        for atom2 in sector_atoms_2:
            #print ('aqui!!!!', atom1.index ,atom2.index )
            if (atom1.pos[0] - atom2.pos[0] >= 2.0 or 
                atom1.pos[1] - atom2.pos[1] >= 2.0 or 
                atom1.pos[2] - atom2.pos[2] >= 2.0):
                pass
            
            else:
                v_dist =  [atom1.pos[0] - atom2.pos[0],
                           atom1.pos[1] - atom2.pos[1],
                           atom1.pos[2] - atom2.pos[2]]
                
                dist2 = v_dist[0]**2 + v_dist[1]**2 + v_dist[2]**2

                if dist2 <= ((atom1.cov_rad + atom2.cov_rad)**2) *1.1:
                    angle = 0
                    vec_o = 0
                    
                    index_bonds2.append([atom1.index -1, atom2.index -1])
                    index_bonds. append( atom1.index -1    )
                    index_bonds. append( atom2.index -1    )


                    atom1.connected.append(atom2)
                    atom2.connected.append(atom1)
              
                else:
                    pass
    return index_bonds, index_bonds2
#'''

'''
cpdef C_generate_bonds(atoms, _limit = 50):
    bonds        = []
    index_bonds  = []
    index_bonds2 = []

    #arr1  = np.array([0,0,1])
    cdef int i
    cdef int j
    #cdef int num_threads

    size =  len(atoms)
    
    if size >= _limit:
        limit = _limit
    else: 
        limit = size

    for i in range (0, size):
        
        if i + limit <= size:
            pass
        else:
            limit = limit-1
        
        for j in range (i+1, i+ limit):    
            if (atoms[i].pos[0] - atoms[j].pos[0] >= 2.0 or 
                atoms[i].pos[1] - atoms[j].pos[1] >= 2.0 or 
                atoms[i].pos[2] - atoms[j].pos[2] >= 2.0):
                pass
            
            else:
                v_dist =  [atoms[i].pos[0] - atoms[j].pos[0],
                           atoms[i].pos[1] - atoms[j].pos[1],
                           atoms[i].pos[2] - atoms[j].pos[2]]
                
                dist2 = v_dist[0]**2 + v_dist[1]**2 + v_dist[2]**2

                
                
                if dist2 <= ((atoms[i].cov_rad + atoms[j].cov_rad)**2) *1.1:

                    distance = dist2**0.5
                    midpoint = [(atoms[i].pos[0] + atoms[j].pos[0])/2.0,
                                (atoms[i].pos[1] + atoms[j].pos[1])/2.0,
                                (atoms[i].pos[2] + atoms[j].pos[2])/2.0]
                    
                    angle = 0
                    vec_o = 0
                    
                    index_bonds2.append([atoms[i].index -1 , atoms[j].index - 1])
                    index_bonds .append( atoms[i].index -1 )
                    index_bonds .append( atoms[j].index -1 )
                    
                    atoms[i].connected.append(atoms[j])
                    atoms[j].connected.append(atoms[i])
              
                else:
                    pass

    return index_bonds, index_bonds2

#'''

'''
cpdef C_generate_bonds(atoms):
    #bonds        = []
    #index_bonds  = []
    index_bonds2 = []

    cdef int i
    cdef int j
    cdef int size
    
    cdef double atom_ix
    cdef double atom_iy
    cdef double atom_iz
    cdef double cov_rad_i, cov_rad_j
    
    
    size =  len(atoms)
    
    for i in range (0, size-1):
        
        atom_ix   = atoms[i].pos[0]
        atom_iy   = atoms[i].pos[1]    
        atom_iz   = atoms[i].pos[2]
        cov_rad_i = atoms[i].cov_rad
        index_i   = atoms[i].index-1
        
        for j in range (i+1, size):    
            
            dX              = (atom_ix - atoms[j].pos[0])**2
            dY              = (atom_iy - atoms[j].pos[1])**2
            dZ              = (atom_iz - atoms[j].pos[2])**2
            
            cov_rad_j       = atoms[j].cov_rad
            cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*1.2
            
            
            if (dX > cov_rad_ij_sqrt or 
                dY > cov_rad_ij_sqrt or 
                dZ > cov_rad_ij_sqrt):
                pass

            else:
                r_ij = (dX + dY + dZ)
                if r_ij <= cov_rad_ij_sqrt:
                    index_bonds2.append([index_i , atoms[j].index - 1])
                    #index_bonds .append( index_i           )
                    #index_bonds .append( atoms[j].index -1 )
                    atoms[i].connected.append(atoms[j])
                    atoms[j].connected.append(atoms[i])
                else:
                    pass

    return index_bonds2#, index_bonds

#'''

'''
cpdef C_generate_bonds_between_sectors(atoms1, atoms2):
    #bonds        = []
    #index_bonds  = []
    index_bonds2 = []

    cdef int i
    cdef int j
    cdef int size1, size2
    
    cdef double atom_ix
    cdef double atom_iy
    cdef double atom_iz
    cdef double cov_rad_i, cov_rad_j
    
    
    size1 =  len(atoms1)
    size2 =  len(atoms2)

    for i in range (0, size1):
        
        atom_ix   = atoms1[i].pos[0]
        atom_iy   = atoms1[i].pos[1]    
        atom_iz   = atoms1[i].pos[2]
        cov_rad_i = atoms1[i].cov_rad
        index_i   = atoms1[i].index-1
        
        for j in range (0, size2):    
            
            dX              = (atom_ix - atoms2[j].pos[0])**2
            dY              = (atom_iy - atoms2[j].pos[1])**2
            dZ              = (atom_iz - atoms2[j].pos[2])**2
            
            cov_rad_j       = atoms2[j].cov_rad
            cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*1.2
            
            
            if (dX > cov_rad_ij_sqrt or 
                dY > cov_rad_ij_sqrt or 
                dZ > cov_rad_ij_sqrt):
                pass

            else:
                r_ij = (dX + dY + dZ)
                if r_ij <= cov_rad_ij_sqrt:
                    index_bonds2.append([index_i , atoms2[j].index - 1])
                    #index_bonds .append( index_i           )
                    #index_bonds .append( atoms[j].index -1 )
                    atoms1[i].connected.append(atoms2[j])
                    atoms2[j].connected.append(atoms1[i])
                else:
                    pass

    return index_bonds2#, index_bonds

#'''

