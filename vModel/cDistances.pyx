import numpy as np
import time
import multiprocessing

cpdef list calculate_grid_offset(gridsize, maxbond = 2.6):
    '''
    grid_offset_full = [
               [ 1,-1, 0],
                         #[ 0,-1, 0],
                         #[-1,-1, 0],
                         #[-1, 0, 0],
               #[ 0, 0, 0], 
               [ 1, 0, 0], 
               [ 1, 1, 0], 
               [ 0, 1, 0], 
               [-1, 1, 0], 
               
                    #[-1, 2, 0],
                    #[ 0, 2, 0],
                    #[ 1, 2, 0],
                    #[ 2, 2, 0],
                    #[ 2, 1, 0],
                    #[ 2, 0, 0],
                    #[ 2,-1, 0],                   
               
               [ 0, 0, 1],
               [ 1, 0, 1], 
               [ 1, 1, 1], 
               [ 0, 1, 1], 
               [-1, 1, 1], 
               [-1, 0, 1],
               [-1,-1, 1], 
               [ 0,-1, 1], 
               [ 1,-1, 1],
               
                    #[-1, 2, 1],
                    #[ 0, 2, 1],
                    #[ 1, 2, 1],
                    #[ 2, 2, 1],
                    #[ 2, 1, 1],
                    #[ 2, 0, 1],
                    #[ 2,-1, 1],
                    #
                    #
                    #[ 0, 0, 2],
                    #[ 1, 0, 2], 
                    #[ 1, 1, 2], 
                    #[ 0, 1, 2], 
                    #[-1, 1, 2], 
                    #[-1, 0, 2],
                    #[-1,-1, 2], 
                    #[ 0,-1, 2], 
                    #[ 1,-1, 2],
                    #
                    #[-1, 2, 2],
                    #[ 0, 2, 2],
                    #[ 1, 2, 2],
                    #[ 2, 2, 2],
                    #[ 2, 1, 2],
                    #[ 2, 0, 2],
                    #[ 2,-1, 2],
               ]

   
   
    #'''


    #'''
    grid_offset_full = []
    borderGrid  = maxbond/gridsize
    borderGrid  = int(borderGrid) 

    #'''#------------------------- first floor -----------------------------

    #               |-------|-------|-------|-------|-------| 
    #               |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
    #               |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
    #               |-2,2,0 |-1,2,0 | 0,2,0 | 1,2,0 | 2,2,0 | 
    #               |-------|-------|-------|-------|-------| 
    #               |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
    #               |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
    #               |-1,1,0 |-1,1,0 | 0,1,0 | 1,1,0 | 2,1,0 | 
    #               |-------|-------|-------|-------|-------| 
    #               |       |       |XXXXXXX|\\\\\\\|\\\\\\\|
    #               |       |       |XXXXXXX|\\\\\\\|\\\\\\\|
    #               |-1,0,0 |-1,0,0 | 0,0,0 | 1,0,0 | 2,0,0 |
    #               |-------|-------|-------|-------|-------|
    #               |       |       |       |       |       |
    #               |       |       |       |       |       |
    #               |-1,-1,0|-1,-1,0| 0,-1,0| 1,-1,0| 2,-1,0|
    #               |-------|-------|-------|-------|-------|

    ''''''
    N = 0
    for i in range (-borderGrid, borderGrid + 1):

        n = 0
        for j in range(0, borderGrid + 1):
            #counter = i + n #+ 2
            
            # we don't need all the elements to the first floor
            if i < -1 and j == 0:
                pass
            
            else:

                # we don't need the [0,0,0] element to the first floor
                if [i,j, 0] == [0,0,0]:
                    pass
                else:
                    grid_offset_full.append([i,j,0])
                    N+=1
            
            n+=1
    #-------------------------------------------------------------------
    #'''
    #'''
    #--------------------- floors above---------------------------------
    #                                    
    #                                     |-------|-------|-------|-------| 
    #                                     |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
    #                                     |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
    #                                     |-1,2,2 | 0,2,2 | 1,2,2 | 2,2,2 | 
    #                                     |-------|-------|-------|-------| 
    # |-------|-------|-------|-------|   |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
    # |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|   |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
    # |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|   |-1,1,2 | 0,1,2 | 1,1,2 | 2,1,2 | 
    # |-1,2,1 | 0,2,1 | 1,2,1 | 2,2,1 |   |-------|-------|-------|-------| 
    # |-------|-------|-------|-------|   |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
    # |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|   |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
    # |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|   |-1,0,2 | 0,0,2 | 1,0,2 | 2,0,2 |
    # |-1,1,1 | 0,1,1 | 1,1,1 | 2,1,1 |   |-------|-------|-------|-------|
    # |-------|-------|-------|-------|   |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
    # |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|   |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
    # |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|   |-1,-1,2| 0,-1,2| 1,-1,2| 2,-1,2|
    # |-1,0,1 | 0,0,1 | 1,0,1 | 2,0,1 |   |-------|-------|-------|-------|  
    # |-------|-------|-------|-------|
    # |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
    # |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
    # |-1,-1,1| 0,-1,1| 1,-1,1| 2,-1,1|
    # |-------|-------|-------|-------|
        

    
    excluded_list = [] 
    n = 0
    for i in range (-borderGrid, borderGrid + 1):
        for j in range(-borderGrid, borderGrid + 1):
            
            for k in range(1, borderGrid + 1):
            #for k in range(0, borderGrid + 1):
                if [i, j,  k] in excluded_list:
                    pass
                else:
                    grid_offset_full.append([i,j,k])
                    #print([i,j,k], n+1)
                n+=1
    #-------------------------------------------------------------------
    #'''
    return grid_offset_full
    
    

cpdef double calculate_sqrt_distance (int i, int j,  coords):
    """ Function doc """
   
    dX              = (coords[i*3  ] - coords[j*3  ])**2
    dY              = (coords[i*3+1] - coords[j*3+1])**2
    dZ              = (coords[i*3+2] - coords[j*3+2])**2
    r_ij = dX + dY + dZ
    return r_ij


cpdef list ctype_get_connections_within_grid_element (list list_of_atoms, coords, cov_rad, double tolerance, gridsize):         
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
    
    
    bonds_pair_of_indexes [[a,b],[b,c], ...] where a and b are indices. 
    returns a list of pair of indices "bonds_pair_of_indexes"
    
    """

    bonds_pair_of_indexes = []
    
    cpdef double r_ij
    cpdef int i
    cpdef int atom_idx_i
    cpdef int atom_idx_j
    cpdef double cov_rad_ij_sqrt

    
    for i, atom_idx_i in enumerate(list_of_atoms[:-1]):
        for atom_idx_j in list_of_atoms[i:]:    
            if atom_idx_i == atom_idx_j :
                pass            
            else:
                
                r_ij            = calculate_sqrt_distance(atom_idx_i, atom_idx_j, coords)
                cov_rad_ij_sqrt = ( (cov_rad[atom_idx_i] + cov_rad[atom_idx_j] )**2)*1.4
                
                #print (atom_idx_i, atom_idx_j,cov_rad[atom_idx_j],cov_rad[atom_idx_j] , r_ij, cov_rad_ij_sqrt)
                if r_ij <= cov_rad_ij_sqrt:
                    pass
                    #bonds_pair_of_indexes.append([atom_idx_i , atom_idx_j])
                    bonds_pair_of_indexes.append(atom_idx_i)
                    bonds_pair_of_indexes.append(atom_idx_j)
                else:
                    pass

    return bonds_pair_of_indexes


cpdef list ctype_get_connections_between_grid_elements(list atomic_grid1, 
                                                       list atomic_grid2, 
                                                       coords, 
                                                       cov_rad, 
                                                       double  tolerance, 
                                                       gridsize):
    
    cpdef double r_ij
    cpdef double cov_rad_ij_sqrt
    cpdef int atom_idx_i
    cpdef int atom_idx_j

    cpdef list bonds_pair_of_indexes
    bonds_pair_of_indexes = []
    
    
    if atomic_grid1 == atomic_grid2:
        pass
    else:
        for atom_idx_i in atomic_grid1:   
            #xyz       = atom_i[2]
            #atom_ix   = xyz[0]
            #atom_iy   = xyz[1]    
            #atom_iz   = xyz[2]
            #cov_rad_i = atom_i[3]
            #index_i   = atom_i[0]

            for atom_idx_j in atomic_grid2:    

                if atom_idx_i == atom_idx_j :
                    pass            
                else:
                    r_ij            = calculate_sqrt_distance(atom_idx_i, atom_idx_j, coords)
                    #cov_rad_ij_sqrt =  cov_rad[atom_idx_i] + cov_rad[atom_idx_j] 
                    cov_rad_ij_sqrt = ( (cov_rad[atom_idx_i] + cov_rad[atom_idx_j] )**2)*1.4
                    #print (atom_idx_i, atom_idx_j,cov_rad[atom_idx_j],cov_rad[atom_idx_j] , r_ij, cov_rad_ij_sqrt)
                    if r_ij <= cov_rad_ij_sqrt:
                        #bonds_pair_of_indexes.append([atom_idx_i , atom_idx_j])
                        bonds_pair_of_indexes.append(atom_idx_i )
                        bonds_pair_of_indexes.append(atom_idx_j )
                    else:
                        pass

    return bonds_pair_of_indexes


cpdef dict ctype_build_the_atomic_grid ( list indexes     ,
                                         list gridpos_list):
    cpdef int atom

    atomic_grid = {}
    
    for atom, grid_pos in enumerate(gridpos_list):
        if grid_pos in atomic_grid:
            atomic_grid[grid_pos].append(indexes[atom])
        else:
            
            atomic_grid[grid_pos] = []
            atomic_grid[grid_pos].append(indexes[atom])
    
    return atomic_grid


cpdef list ctype_get_atomic_bonds_from_atomic_grids( list indexes, 
                                                      coords, 
                                                      cov_rad, 
                                                      list gridpos_list, 
                                                      double gridsize,
                                                      double maxbond
                                                      ):
    
    
    cpdef double tolerance
    #cpdef double maxbond
    #maxbond   = 3.0
    tolerance = 1.4
    
    atomic_grid = ctype_build_the_atomic_grid ( indexes     ,
                                                gridpos_list)

    grid_offset_full = calculate_grid_offset(gridsize, maxbond)
   
    #print ('gridsize',  gridsize )
    #print ('maxbond',   maxbond )
    #print ('borderGrid',  int(maxbond/gridsize)   )
    #print ('grid_offset_full', len(grid_offset_full))
    
    n = 0
    bonds_pair_of_indexes = [] 
   
    for element in atomic_grid.keys():
        
        atomic_grid1   = atomic_grid[element]

        #----------------------------------------------------------------------------------------#
        if len(atomic_grid1) == 1:
            pass
        else:
            pass
            element1_bonds = ctype_get_connections_within_grid_element( atomic_grid1, coords, cov_rad, tolerance, gridsize)        
            bonds_pair_of_indexes += element1_bonds
        #----------------------------------------------------------------------------------------#
        n+=1
        #----------------------------------------------------------------------------------------#
        for offset_element in  grid_offset_full:              
            
            element2  = (element[0]+offset_element[0], 
                         element[1]+offset_element[1], 
                         element[2]+offset_element[2]) 

            if element2 in atomic_grid:                        
                n+=1
                pass
                element1_2_bonds = ctype_get_connections_between_grid_elements(atomic_grid1, atomic_grid[element2], coords, cov_rad, tolerance, gridsize)
                bonds_pair_of_indexes += element1_2_bonds
        #----------------------------------------------------------------------------------------#
    #print('n interaction', n)
    return bonds_pair_of_indexes
        
    
    
    
    
    
        
#cpdef list ctype_get_atomic_bonds_from_atomic_grids_parallel( list indexes, 
#                                                              coords, 
#                                                              cov_rad, 
#                                                             list gridpos_list, 
#                                                             double gridsize):
#    
#    
#    cpdef double tolerance
#    
#    tolerance = 1.4
#    atomic_grid = ctype_build_the_atomic_grid ( indexes     ,
#                                                gridpos_list)
#
#    #'''
#    grid_offset_full = [
#               [ 1,-1, 0],
#                         #[ 0,-1, 0],
#                         #[-1,-1, 0],
#                         #[-1, 0, 0],
#               #[ 0, 0, 0], 
#               [ 1, 0, 0], 
#               [ 1, 1, 0], 
#               [ 0, 1, 0], 
#               [-1, 1, 0], 
#               
#                    #[-1, 2, 0],
#                    #[ 0, 2, 0],
#                    #[ 1, 2, 0],
#                    #[ 2, 2, 0],
#                    #[ 2, 1, 0],
#                    #[ 2, 0, 0],
#                    #[ 2,-1, 0],                   
#               
#               [ 0, 0, 1],
#               [ 1, 0, 1], 
#               [ 1, 1, 1], 
#               [ 0, 1, 1], 
#               [-1, 1, 1], 
#               [-1, 0, 1],
#               [-1,-1, 1], 
#               [ 0,-1, 1], 
#               [ 1,-1, 1],
#               
#                    #[-1, 2, 1],
#                    #[ 0, 2, 1],
#                    #[ 1, 2, 1],
#                    #[ 2, 2, 1],
#                    #[ 2, 1, 1],
#                    #[ 2, 0, 1],
#                    #[ 2,-1, 1],
#                    #
#                    #
#                    #[ 0, 0, 2],
#                    #[ 1, 0, 2], 
#                    #[ 1, 1, 2], 
#                    #[ 0, 1, 2], 
#                    #[-1, 1, 2], 
#                    #[-1, 0, 2],
#                    #[-1,-1, 2], 
#                    #[ 0,-1, 2], 
#                    #[ 1,-1, 2],
#                    #
#                    #[-1, 2, 2],
#                    #[ 0, 2, 2],
#                    #[ 1, 2, 2],
#                    #[ 2, 2, 2],
#                    #[ 2, 1, 2],
#                    #[ 2, 0, 2],
#                    #[ 2,-1, 2],
#               ]
#
#
#
#
#
#        
#    bonds_pair_of_indexes = []
#    
#    #'''
#    multiprocessing_list  = []
#    for element in atomic_grid.keys():
#        multiprocessing_list.append([element, atomic_grid, grid_offset_full, coords, cov_rad, tolerance])
#    
#    n_processor = multiprocessing.cpu_count()
#    pool        = multiprocessing.Pool(n_processor)
#    outlist     = pool.map(parallel_get_connections_between_grid_elements_new, multiprocessing_list)
#    for bond_list in outlist:
#        for bond in bond_list:
#            bonds_pair_of_indexes.append(bond)
#    return bonds_pair_of_indexes
#  
#
#cpdef  list parallel_get_connections_between_grid_elements_new (list parameters):
#        
#    element          = parameters[0]
#    atomic_grid      = parameters[1]
#    grid_offset_full = parameters[2]
#    coords           = parameters[3]
#    cov_rad          = parameters[4]
#    tolerance        = parameters[5]
#    gridsize= 1
#    atomic_grid1   = atomic_grid[element]
#    bonds_pair_of_indexes = []
#    #----------------------------------------------------------------------------------------#
#    element1_bonds = ctype_get_connections_within_grid_element( atomic_grid1, coords, cov_rad, tolerance, gridsize)        
#    bonds_pair_of_indexes += element1_bonds
#    #----------------------------------------------------------------------------------------#
#    
#    #----------------------------------------------------------------------------------------#
#    for offset_element in  grid_offset_full:              
#        
#        element2  = (element[0]+offset_element[0], 
#                     element[1]+offset_element[1], 
#                     element[2]+offset_element[2]) 
#                
#        if element2 in atomic_grid:                        
#            element1_2_bonds = ctype_get_connections_between_grid_elements(atomic_grid1, atomic_grid[element2], coords, cov_rad, tolerance, gridsize)
#            bonds_pair_of_indexes += element1_2_bonds
#    #----------------------------------------------------------------------------------------#
#    return bonds_pair_of_indexes
#    
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#def _build_the_atomic_grid ( atoms, gridsize = 3, frame = None ):
#    """  fucntion build_atomic_grid
#    
#    This function organizes the atoms in their respective position 
#    of the grid (atomic grid) - Nescessary to calculate distances between 
#    atoms in different elements of the grid
#    
#    self.grid_size = is the size of a grid element - size of a sector
#    
#    
#              atomic grid
#              
#        |-------|-------|-------| |
#        |       | grid  |       | |
#        |       |element|       | | grid_size
#        |-1,1,0 | 0,1,0 | 1,1,0 | |
#        |-------|-------|-------| |
#        |       |       |       |
#        |       |       |       |
#        |-1,0,0 | 0,0,0 | 1,0,0 |
#        |-------|-------|-------|
#        |       |       |       |
#        |       |       |       |
#        |-1,-1,0| 0,-1,0| 1,-1,0|
#        |-------|-------|-------|
#                         -------
#                        grid_size
#    
#    
#    grid element = list of atoms
#    """
#    atomic_grid = {}
#    
#   
#    for atom in atoms:
#        #grid_pos = (a,b,c) a tuple of grid indexes
#        grid_pos = atom.get_grid_position(gridsize = gridsize, 
#                                            frame = frame)
#        xyz   = atom.coords (frame = frame)
#        atom2 = [atom.index-1    ,    # 0
#                 atom.name       ,    # 1
#                 xyz             ,    # 2
#                 atom.cov_rad    ,    # 3
#                 grid_pos        ]
#        
#        
#        if grid_pos in atomic_grid:
#            atomic_grid[grid_pos].append(atom2)
#            
#        else:
#            atomic_grid[grid_pos] = []
#            atomic_grid[grid_pos].append(atom2)
#    return atomic_grid
#
#
#def get_atomic_bonds_from_atomic_grids(atomic_grid, gridsize, maxbond  = 2.66, tolerance= 1.4, frame= None):
#    '''
#    There is also an array vOff that specifies the offsets of each of the 14 neighbor
#    cells. The array covers half the neighboring cells, together with the cell itself; its
#    size and contents are specified as
#    
#    {{0,0,0}, {1,0,0}, {1,1,0}, {0,1,0}, {-1,1,0}, {0,0,1},
#    {1,0,1}, {1,1,1}, {0,1,1}, {-1,1,1}, {-1,0,1},
#    {-1,-1,1}, {0,-1,1}, {1,-1,1}}
#
#    '''
#
#    grid_offset_full = [
#                [ 1,-1, 0],
#                         #[ 0,-1, 0],
#                         #[-1,-1, 0],
#                         #[-1, 0, 0],
#               #[ 0, 0, 0], 
#               [ 1, 0, 0], 
#               [ 1, 1, 0], 
#               [ 0, 1, 0], 
#               [-1, 1, 0], 
#               
#                    #[-1, 2, 0],
#                    #[ 0, 2, 0],
#                    #[ 1, 2, 0],
#                    #[ 2, 2, 0],
#                    #[ 2, 1, 0],
#                    #[ 2, 0, 0],
#                    #[ 2,-1, 0],                   
#               
#               [ 0, 0, 1],
#               [ 1, 0, 1], 
#               [ 1, 1, 1], 
#               [ 0, 1, 1], 
#               [-1, 1, 1], 
#               [-1, 0, 1],
#               [-1,-1, 1], 
#               [ 0,-1, 1], 
#               [ 1,-1, 1],
#               
#                    #[-1, 2, 1],
#                    #[ 0, 2, 1],
#                    #[ 1, 2, 1],
#                    #[ 2, 2, 1],
#                    #[ 2, 1, 1],
#                    #[ 2, 0, 1],
#                    #[ 2,-1, 1],
#                    #
#                    #
#                    #[ 0, 0, 2],
#                    #[ 1, 0, 2], 
#                    #[ 1, 1, 2], 
#                    #[ 0, 1, 2], 
#                    #[-1, 1, 2], 
#                    #[-1, 0, 2],
#                    #[-1,-1, 2], 
#                    #[ 0,-1, 2], 
#                    #[ 1,-1, 2],
#                    #
#                    #[-1, 2, 2],
#                    #[ 0, 2, 2],
#                    #[ 1, 2, 2],
#                    #[ 2, 2, 2],
#                    #[ 2, 1, 2],
#                    #[ 2, 0, 2],
#                    #[ 2,-1, 2],
#
#               ]
#
#
#    '''
#    
#    bulding grid offset
#    '''
#    
#    
#    """
#    grid_offset_full = []
#    
#    
#    
#    borderGrid  = maxbond/gridsize
#    borderGrid  = int(borderGrid)+1
#    #'''
#    #------------------------- first floor -----------------------------
#    N = 0
#    for i in range (-borderGrid, borderGrid + 1):
#        
#        n = 0
#        for j in range(0, borderGrid + 1):
#            counter = i + n #+ 2
#            
#            # we don't need all the elements to the first floor
#            if counter < 0:
#                pass
#            
#            else:
#
#                # we don't need the [0,0,0] element to the first floor
#                if [i,j, 0] == [0,0,0]:
#                    pass
#                    #grid_offset_full.append([0,0,0])
#            
#                else:
#                        
#                    #if -i == j:
#                    #    print([i,j,0], N+1, 'diagonal')
#                    #else:
#                    #    print([i,j,0], N+1, '')
#                    
#                    grid_offset_full.append([i,j,0])
#                    N+=1
#            
#            n+=1
#    #-------------------------------------------------------------------
#    #'''
#    #--------------------- floors above---------------------------------
#    n = 0
#    for i in range (-borderGrid, borderGrid + 1):
#        for j in range(-borderGrid, borderGrid + 1):
#            for k in range(1, borderGrid + 1):
#            #for k in range(-borderGrid, borderGrid + 1):
#                grid_offset_full.append([i,j,k])
#                #print([i,j,k], n+1)
#                n+=1
#    #-------------------------------------------------------------------
#    '''
#    """
#
#    
#    bonds_pair_of_indexes = []
#    '''
#    for element in atomic_grid.keys():
#        parameters = [element, atomic_grid, grid_offset_full, frame, tolerance]
#        outlist = parallel_get_connections_between_grid_elements (parameters)
#        
#        for bond in outlist:
#            bonds_pair_of_indexes.append(bond)
#    '''
#    
#    
#    multiprocessing_list  = []
#    for element in atomic_grid.keys():
#        multiprocessing_list.append([element, atomic_grid, grid_offset_full, frame, tolerance])
#    
#    n_processor = multiprocessing.cpu_count()
#    pool        = multiprocessing.Pool(n_processor)
#    outlist     = pool.map(parallel_get_connections_between_grid_elements, multiprocessing_list)
#    for bond_list in outlist:
#        for bond in bond_list:
#            bonds_pair_of_indexes.append(bond)
#    #print (outlist)
#    
#    
#    
#    '''
#    for element in atomic_grid.keys():
#        
#        
#        multiprocessing_list = [] 
#        
#        element1 = (element[0], 
#                    element[1], 
#                    element[2])
#        
#        atomic_grid1   = atomic_grid[element1]
#        element1_bonds = self.new_generate_connections_into_a_grid_element( atomic_grid1 , tolerance, frame)        
#        bonds_pair_of_indexes += element1_bonds
#
#        
#
#        for offset_element in  grid_offset_full:              
#            
#            element1 = (element[0], 
#                        element[1], 
#                        element[2])
#            
#            element2  = (element[0]+offset_element[0], 
#                         element[1]+offset_element[1], 
#                         element[2]+offset_element[2]) 
#                    
#            if element2 in atomic_grid:                        
#                element1_2_bonds = self.new_generate_connections_between_grid_elements(atomic_grid[element1], atomic_grid[element2], tolerance, frame)
#                bonds_pair_of_indexes += element1_2_bonds
#
#    #'''
#    return bonds_pair_of_indexes 
#
#
#
#
#def parallel_get_connections_between_grid_elements (parameters):
#    """ Function doc """
#    #[element1, atomic_grid, grid_offset_full]
#    element          = parameters[0]
#    atomic_grid      = parameters[1]
#    grid_offset_full = parameters[2]
#    frame            = parameters[3]
#    tolerance        = parameters[4]
#    
#    bonds_pair_of_indexes = []
#    
#    atomic_grid1   = atomic_grid[element]
#    element1_bonds = get_connections_within_grid_element( atomic_grid1 , tolerance, frame)        
#    bonds_pair_of_indexes += element1_bonds
#
#    
#
#    for offset_element in  grid_offset_full:              
#        
#        element1 = (element[0], 
#                    element[1], 
#                    element[2])
#        
#        element2  = (element[0]+offset_element[0], 
#                     element[1]+offset_element[1], 
#                     element[2]+offset_element[2]) 
#                
#        if element2 in atomic_grid:                        
#            element1_2_bonds = get_connections_between_grid_elements(atomic_grid[element1], atomic_grid[element2], tolerance, frame)
#            bonds_pair_of_indexes += element1_2_bonds
#
#    return bonds_pair_of_indexes
#    #print(bonds_pair_of_indexes)
#
#def  get_connections_within_grid_element (  
#                                          list_of_atoms , 
#                                          tolerance,  
#                                          frame ):         
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
#    bonds_pair_of_indexes [[a,b],[b,c], ...] where a and b are indices. 
#    returns a list of pair of indices "bonds_pair_of_indexes"
#    
#    """
#
#    bonds_pair_of_indexes = []
#    for i, atom_i in enumerate(list_of_atoms[:-1]):
#        xyz       = atom_i[2]
#        atom_ix   = xyz[0]
#        atom_iy   = xyz[1]    
#        atom_iz   = xyz[2]
#        cov_rad_i = atom_i[3]
#        index_i   = atom_i[0]
#                
#        
#        for atom_j in list_of_atoms[i:]:    
#            #xyz2      = atom_j[2]
#            #atom_jx   = xyz2[0]
#            #atom_jy   = xyz2[1]    
#            #atom_jz   = xyz2[2]
#            #cov_rad_j = atom_j[3]
#            #index_j   = atom_j[0]
#            
#            
#            if atom_i == atom_j :
#                pass
#           
#            
#            else:
#                xyz2       = atom_j[2]
#                dX              = (atom_ix - xyz2[0])**2
#                dY              = (atom_iy - xyz2[1])**2
#                dZ              = (atom_iz - xyz2[2])**2
#                
#                cov_rad_j       = atom_j[3]
#                
#                cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*tolerance
#                if (dX > cov_rad_ij_sqrt or 
#                    dY > cov_rad_ij_sqrt or 
#                    dZ > cov_rad_ij_sqrt):
#                    pass
#                else:
#                    r_ij = (dX + dY + dZ)
#                    if r_ij <= cov_rad_ij_sqrt:
#                        pass
#                        bonds_pair_of_indexes.append([index_i , atom_j[0]])
#                    else:
#                        pass
#
#    return bonds_pair_of_indexes
#
#
#def get_connections_between_grid_elements ( list_of_atoms1      , 
#                                            list_of_atoms2      ,
#                                            tolerance           ,
#                                            frame):
#    bonds_pair_of_indexes = []
#    if list_of_atoms1 == list_of_atoms2:
#        pass
#    else:
#
#        for atom_i in list_of_atoms1:   
#            xyz       = atom_i[2]
#            atom_ix   = xyz[0]
#            atom_iy   = xyz[1]    
#            atom_iz   = xyz[2]
#            cov_rad_i = atom_i[3]
#            index_i   = atom_i[0]
#
#            for atom_j in list_of_atoms2:    
#                index_j    = atom_j[0]
#                xyz2       = atom_j[2]
#                dX              = (atom_ix - xyz2[0])**2
#                dY              = (atom_iy - xyz2[1])**2
#                dZ              = (atom_iz - xyz2[2])**2
#            
#                cov_rad_j       = atom_j[3]
#                
#                cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*tolerance
#                #print(tolerance)
#                if (dX > cov_rad_ij_sqrt or 
#                    dY > cov_rad_ij_sqrt or 
#                    dZ > cov_rad_ij_sqrt):
#                    pass
#
#                else:
#                    r_ij = (dX + dY + dZ)
#                    if r_ij <= cov_rad_ij_sqrt:
#                        bonds_pair_of_indexes.append( [index_i ,index_j] )
#                    
#    return bonds_pair_of_indexes
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#





















#
#
#
#
#
#
#
#
#cpdef list new_generate_connections_into_a_grid_element (list list_of_atoms         , 
#                                                         double tolerance 
#                                                          #list atoms                 , 
#                                                          #list bonds_pair_of_indexes ,  #indices of connected atoms
#                                                          #list bonds_full_indices    ,
#                                                          #list non_bonded_list
#                                                          ):         #pairs_of_
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
#    bonds_pair_of_indexes [[a,b],[b,c], ...] where a and b are indices. 
#    returns a list of pair of indices "bonds_pair_of_indexes"
#    
#    """
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
#    cdef list bonds_pair_of_indexes
#
#    bonds_pair_of_indexes = []
#    
#    for i, atom_i in enumerate(list_of_atoms[:-1]):
#        atom_ix   = atom_i[3][0]
#        atom_iy   = atom_i[3][1]    
#        atom_iz   = atom_i[3][2]
#        cov_rad_i = atom_i[2]
#        index_i   = atom_i[0]
#                
#        for atom_j in list_of_atoms[i:]:    
#            
#            if atom_i[0] == atom_j[0]:
#                pass
#           
#            else:
#                dX              = (atom_ix - atom_j[3][0])**2
#                dY              = (atom_iy - atom_j[3][1])**2
#                dZ              = (atom_iz - atom_j[3][2])**2
#                
#                cov_rad_j       = atom_j[2]
#                
#                cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*1.4#*tolerance
#                
#                
#                if (dX > cov_rad_ij_sqrt or 
#                    dY > cov_rad_ij_sqrt or 
#                    dZ > cov_rad_ij_sqrt):
#                    pass
#
#                else:
#                    r_ij = (dX + dY + dZ)
#                    if r_ij <= cov_rad_ij_sqrt:
#                        pass
#                        bonds_pair_of_indexes.append([index_i , atom_j[0]])
#                        
#                        #bonds_full_indices.append  (index_i  )
#                        #bonds_full_indices.append  (atom_j[0])                 
#                        
#                        #atom_i[8].append  (atom_j[0] )
#                        #atom_j[8].append  (atom_i[0] )
#                        
#                        #non_bonded_list[index_i  ] = False
#                        #non_bonded_list[atom_j[0]] = False
#
#                    
#                    else:
#                        pass
#
#    #return atoms, bonds_full_indices , bonds_pair_of_indexes, non_bonded_list
#    return bonds_pair_of_indexes
#    
#cpdef list new_generate_connections_between_grid_elements ( list lits_of_atoms1       , 
#                                                            list lits_of_atoms2      ,
#                                                            double tolerance):
#
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
#    bonds_pair_of_indexes [[a,b],[b,c], ...] where a and b are indices. 
#    returns a list of pair of indices "bonds_pair_of_indexes"
#    """
#    
#
#        
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
#    cdef list bonds_pair_of_indexes
#    #size1 =  len(atoms1)
#    #size2 =  len(atoms2)
#    
#    bonds_pair_of_indexes = []
#    if lits_of_atoms1 == lits_of_atoms2:
#        pass
#    else:
#        
#        for atom_i in lits_of_atoms1:   
#            atom_ix   = atom_i[3][0]
#            atom_iy   = atom_i[3][1]    
#            atom_iz   = atom_i[3][2]
#            cov_rad_i = atom_i[2]
#            index_i   = atom_i[0]
#
#            for atom_j in lits_of_atoms2:    
#                index_j = atom_j[0]
#                #if 
#                
#                dX              = (atom_ix - atom_j[3][0])**2
#                dY              = (atom_iy - atom_j[3][1])**2
#                dZ              = (atom_iz - atom_j[3][2])**2
#
#                cov_rad_j       = atom_j[2]
#                cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*1.4 #tolerance
#                
#                if (dX > cov_rad_ij_sqrt or 
#                    dY > cov_rad_ij_sqrt or 
#                    dZ > cov_rad_ij_sqrt):
#                    pass
#
#                else:
#                    
#                    r_ij = (dX + dY + dZ)
#                    
#                    if r_ij <= cov_rad_ij_sqrt:
#                        bonds_pair_of_indexes.append( [index_i , atom_j[0]] )
#                        
#                        #bonds_full_indices.append   (index_i   )
#                        #bonds_full_indices.append   (atom_j[0] )                 
#                        
#                        #atom_i[8].append   (atom_j[0]          )
#                        #atom_j[8].append   (atom_i[0]          )
#
#                        #non_bonded_list[index_i  ] = False
#                        #non_bonded_list[atom_j[0]] = False
#
#
#    #return atoms, bonds_full_indices, bonds_pair_of_indexes, non_bonded_list
#    return bonds_pair_of_indexes
#    
#cpdef list new_determine_the_paired_atomic_grid_elements(atomic_grid, gridsize, maxbond  = 2.66, tolerance= 1.4):
#    '''
#    There is also an array vOff that specifies the offsets of each of the 14 neighbor
#    cells. The array covers half the neighboring cells, together with the cell itself; its
#    size and contents are specified as
#    
#    {{0,0,0}, {1,0,0}, {1,1,0}, {0,1,0}, {-1,1,0}, {0,0,1},
#    {1,0,1}, {1,1,1}, {0,1,1}, {-1,1,1}, {-1,0,1},
#    {-1,-1,1}, {0,-1,1}, {1,-1,1}}
#    
#   
#   
#                                                                |-------|-------|-------|-------| 
#                                                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#                                                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#                                                                |-1,2,2 | 0,2,2 | 1,2,2 | 2,2,2 | 
#                                                                |-------|-------|-------|-------| 
#                                                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#                                                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#                                                                |-1,1,2 | 0,1,2 | 1,1,2 | 2,1,2 | 
#                                                                |-------|-------|-------|-------| 
#                                                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                                                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                                                                |-1,0,2 | 0,0,2 | 1,0,2 | 2,0,2 |
#                                                                |-------|-------|-------|-------|
#                                                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                                                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                                                                |-1,-1,2| 0,-1,2| 1,-1,2| 2,-1,2|
#                                                                |-------|-------|-------|-------|   
#                                   
#   
#    
#                                |-------|-------|-------|-------| 
#                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#                                |-1,2,1 | 0,2,1 | 1,2,1 | 2,2,1 | 
#                                |-------|-------|-------|-------| 
#                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#                                |-1,1,1 | 0,1,1 | 1,1,1 | 2,1,1 | 
#                                |-------|-------|-------|-------| 
#                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                                |-1,0,1 | 0,0,1 | 1,0,1 | 2,0,1 |
#                                |-------|-------|-------|-------|
#                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                                |-1,-1,1| 0,-1,1| 1,-1,1| 2,-1,1|
#                                |-------|-------|-------|-------|
#                                
#                                
#                                
#                                
#|-------|-------|-------|-------|-------| 
#|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#|-2,2,0 |-1,2,0 | 0,2,0 | 1,2,0 | 2,2,0 | 
#|-------|-------|-------|-------|-------| 
#        |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#        |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#        |-1,1,0 | 0,1,0 | 1,1,0 | 2,1,0 | 
#        |-------|-------|-------|-------| 
#        |       |XXXXXXX|\\\\\\\|\\\\\\\|
#        |       |XXXXXXX|\\\\\\\|\\\\\\\|
#        |-1,0,0 | 0,0,0 | 1,0,0 | 2,0,0 |
#        |-------|-------|-------|-------|
#        |       |       |       |       |
#        |       |       |       |       |
#        |-1,-1,0| 0,-1,0| 1,-1,0| 2,-1,0|
#        |-------|-------|-------|-------|
#    
#    always. the combination between {0,0,0} and some element of the list (\\\\\\) 
#    
#    returns a list contain lists of atoms [[atoms1],atoms2], ...]
#
#    '''
#    cdef list pair_of_sectors2
#    cdef list grid_offset
#    #cdef list element
#    #cdef list element1
#    #cdef list element2
#    #cdef list offset_element
#    
#    #initial = time.time()
#    
#    pair_of_sectors2 = []
#    grid_offset = [
#                   #[ 1,-1, 0],
#                   #[ 0,-1, 0],
#                   #[-1,-1, 0],
#                   #[-1, 0, 0],
#                   
#                   #[ 0, 0, 0], 
#                   # first floor
#                   [ 1, 0, 0], 
#                   [ 1, 1, 0], 
#                   [ 0, 1, 0], 
#                   [-1, 1, 0], 
#                   
#                   [-2, 2, 0],
#                   [-1, 2, 0],
#                   [ 0, 2, 0],
#                   [ 1, 2, 0],
#                   [ 2, 2, 0],
#                   [ 2, 1, 0],
#                   [ 2, 0, 0],
#                   
#                   # 2sd floord       #|-------|-------|-------|-------|
#                   #[ 2,-1, 0],       #|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|           
#                                      #|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|              
#                   [ 0, 0, 1],        #|-1,2,1 | 0,2,1 | 1,2,1 | 2,2,1 |
#                   [ 1, 0, 1],        #|-------|-------|-------|-------|
#                   [ 1, 1, 1],        #|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                   [ 0, 1, 1],        #|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                   [-1, 1, 1],        #|-1,1,1 | 0,1,1 | 1,1,1 | 2,1,1 |
#                   [-1, 0, 1],        #|-------|-------|-------|-------|
#                   [-1,-1, 1],        #|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                   [ 0,-1, 1],        #|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                   [ 1,-1, 1],        #|-1,0,1 | 0,0,1 | 1,0,1 | 2,0,1 |
#                                      #|-------|-------|-------|-------|
#                   [-1, 2, 1],        #|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                   [ 0, 2, 1],        #|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                   [ 1, 2, 1],        #|-1,-1,1| 0,-1,1| 1,-1,1| 2,-1,1|
#                   [ 2, 2, 1],        #|-------|-------|-------|-------|
#                   [ 2, 1, 1],
#                   [ 2, 0, 1],
#                   [ 2,-1, 1],
#                   #
#                   #
#                   #[1,-2, -1],
#                
#
#                   [ 0, 0, 2],         #|-------|-------|-------|-------|
#                                       #|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                   [ 1, 0, 2],         #|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                   [ 1, 1, 2],         #|-1,2,2 | 0,2,2 | 1,2,2 | 2,2,2 |
#                   [ 0, 1, 2],         #|-------|-------|-------|-------|
#                   [-1, 1, 2],         #|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                   [-1, 0, 2],         #|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                   [-1,-1, 2],         #|-1,1,2 | 0,1,2 | 1,1,2 | 2,1,2 |
#                   [ 0,-1, 2],         #|-------|-------|-------|-------|
#                   [ 1,-1, 2],         #|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                   #                   #|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                   #                   #|-1,0,2 | 0,0,2 | 1,0,2 | 2,0,2 |
#                   [-1, 2, 2],         #|-------|-------|-------|-------|
#                   [ 0, 2, 2],         #|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                   [ 1, 2, 2],         #|\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                   [ 2, 2, 2],         #|-1,-1,2| 0,-1,2| 1,-1,2| 2,-1,2|
#                   [ 2, 1, 2],         #|-------|-------|-------|-------|
#                   [ 2, 0, 2],         #
#                   [ 2,-1, 2],
#
#                
#                   ]
#    done = []
#    
#
#    '''
#    
#    bulding grid offset
#    '''
#
#    grid_offset_full = []
#    borderGrid  = maxbond/gridsize
#    borderGrid  = int(borderGrid) 
#    
#    #------------------------- first floor -----------------------------
#    N = 0
#    for i in range (-borderGrid, borderGrid + 1):
#        
#        n = 0
#        for j in range(0, borderGrid + 1):
#            counter = i + n #+ 2
#            
#            # we don't need all the elements to the first floor
#            if counter < 0:
#                pass
#            
#            else:
#
#                # we don't need the [0,0,0] element to the first floor
#                if [i,j, 0] == [0,0,0]:
#                    pass
#                    #grid_offset_full.append([0,0,0])
#            
#                else:
#                        
#                    #if -i == j:
#                    #    print([i,j,0], N+1, 'diagonal')
#                    #else:
#                    #    print([i,j,0], N+1, '')
#                    
#                    grid_offset_full.append([i,j,0])
#                    N+=1
#            
#            n+=1
#    #-------------------------------------------------------------------
#
#    #--------------------- floors above---------------------------------
#    n = 0
#    for i in range (-borderGrid, borderGrid + 1):
#        for j in range(-borderGrid, borderGrid + 1):
#            for k in range(1, borderGrid + 1):
#                grid_offset_full.append([i,j,k])
#                #print([i,j,k], n+1)
#                n+=1
#    #-------------------------------------------------------------------
#    
#    
#
#    #print('gridsize'  ,gridsize)
#    #print('maxbond'   ,maxbond)
#    #print('borderGrid',  borderGrid )
#    #print('grid_offset_full', len(grid_offset_full))
#    
#    bonds_pair_of_indexes = []
#
#    for element in atomic_grid.keys():
#        #print (element)
#
#        element1 = (element[0], 
#                    element[1], 
#                    element[2])
#        
#        atomic_grid1   = atomic_grid[element1]
#        
# 
#        element1_bonds = new_generate_connections_into_a_grid_element( atomic_grid1 , tolerance)        
#        bonds_pair_of_indexes += element1_bonds
#
#        for offset_element in  grid_offset_full:              
# 
#            element2  = (element[0]+offset_element[0], 
#                         element[1]+offset_element[1], 
#                         element[2]+offset_element[2]) 
#                    
#            if element2 in atomic_grid:                        
#                if element1 == element2:
#                    pass
#                    #print(element1, element2, 'repetidos')
#                else:
#                    #print(element1, element2)
#                    pass
#                    element1_2_bonds = new_generate_connections_between_grid_elements(atomic_grid[element1], atomic_grid[element2], tolerance)
#                    bonds_pair_of_indexes += element1_2_bonds
#
#    #'''
#    return bonds_pair_of_indexes 
#
#cpdef new_generete_full_NB_and_Bonded_lists(atoms , gridsize, maxbond, tolerance = 1.4, log = False):
#    '''
#    atoms = [] it's a list
#    
#    list element = [atom.index-1    ,    # 0
#                    atom.name       ,    # 1
#                    atom.cov_rad    ,    # 2
#                    np.array(coods) ,    # 3
#                    atom.resi       ,    # 4
#                    atom.resn       ,    # 5
#                    atom.chain      ,    # 6
#                    atom.symbol     ,    # 7
#                    []              ,    # 8
#                    gridpos         ]
#    
#    '''
#    #----------------------------------------------------------------------------------------------
#    #                                Pairwise grid elements
#    #----------------------------------------------------------------------------------------------
#
#    #--------------------------------------------------------------#
#    initial       = time.time()                                    #
#    #--------------------------------------------------------------#
#    atomic_grid               = _build_the_atomic_grid(atoms)
#    final1 = time.time()                                            #
#
#    
#    bonds_pair_of_indexes     = new_determine_the_paired_atomic_grid_elements(atomic_grid, gridsize, maxbond, tolerance)
#    #--------------------------------------------------------------#
#    final2 = time.time()                                            #
#    
#    
#    if log:
#        print ('building grid elements  : ', final1 - initial, '\n')#
#        #--------------------------------------------------------------#
#        #print (non_bonded_list)
#        print ('Total number of Atoms   :', len(atoms)                 )
#        print ('Number of grid elements :', len(atomic_grid)           )
#    #'''
#    if log:
#        print('gridsize'  ,gridsize)
#        print('maxbond'   ,maxbond)
#        print('borderGrid',  maxbond/gridsize)
#
#
#        print ('Bonds                   :', len(bonds_pair_of_indexes))
#        print ('Bonds calcultation time : ', final2 - initial, '\n')    #
#        #--------------------------------------------------------------#
#    return bonds_pair_of_indexes
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#cpdef list _determine_the_paired_atomic_grid_elements(atomic_grid):
#    '''
#    There is also an array vOff that specifies the offsets of each of the 14 neighbor
#    cells. The array covers half the neighboring cells, together with the cell itself; its
#    size and contents are specified as
#    
#    {{0,0,0}, {1,0,0}, {1,1,0}, {0,1,0}, {-1,1,0}, {0,0,1},
#    {1,0,1}, {1,1,1}, {0,1,1}, {-1,1,1}, {-1,0,1},
#    {-1,-1,1}, {0,-1,1}, {1,-1,1}}
#    
#   
#   
#                                                                |-------|-------|-------|-------| 
#                                                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#                                                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#                                                                |-1,2,2 | 0,2,2 | 1,2,2 | 2,2,2 | 
#                                                                |-------|-------|-------|-------| 
#                                                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#                                                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#                                                                |-1,1,2 | 0,1,2 | 1,1,2 | 2,1,2 | 
#                                                                |-------|-------|-------|-------| 
#                                                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                                                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                                                                |-1,0,2 | 0,0,2 | 1,0,2 | 2,0,2 |
#                                                                |-------|-------|-------|-------|
#                                                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                                                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                                                                |-1,-1,2| 0,-1,2| 1,-1,2| 2,-1,2|
#                                                                |-------|-------|-------|-------|   
#                                   
#   
#    
#                                |-------|-------|-------|-------| 
#                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#                                |-1,2,1 | 0,2,1 | 1,2,1 | 2,2,1 | 
#                                |-------|-------|-------|-------| 
#                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#                                |-1,1,1 | 0,1,1 | 1,1,1 | 2,1,1 | 
#                                |-------|-------|-------|-------| 
#                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                                |-1,0,1 | 0,0,1 | 1,0,1 | 2,0,1 |
#                                |-------|-------|-------|-------|
#                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                                |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\|
#                                |-1,-1,1| 0,-1,1| 1,-1,1| 2,-1,1|
#                                |-------|-------|-------|-------|
#                                
#                                
#                                
#                                
#        |-------|-------|-------|-------| 
#        |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#        |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#        |-1,2,0 | 0,2,0 | 1,2,0 | 2,2,0 | 
#        |-------|-------|-------|-------| 
#        |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#        |\\\\\\\|\\\\\\\|\\\\\\\|\\\\\\\| 
#        |-1,1,0 | 0,1,0 | 1,1,0 | 2,1,0 | 
#        |-------|-------|-------|-------| 
#        |       |XXXXXXX|\\\\\\\|\\\\\\\|
#        |       |XXXXXXX|\\\\\\\|\\\\\\\|
#        |-1,0,0 | 0,0,0 | 1,0,0 | 2,0,0 |
#        |-------|-------|-------|-------|
#        |       |       |       |       |
#        |       |       |       |       |
#        |-1,-1,0| 0,-1,0| 1,-1,0| 2,-1,0|
#        |-------|-------|-------|-------|
#    
#    always. the combination between {0,0,0} and some element of the list (\\\\\\) 
#    
#    returns a list contain lists of atoms [[atoms1],atoms2], ...]
#
#    '''
#    cdef list pair_of_sectors2
#    cdef list grid_offset
#    #cdef list element
#    #cdef list offset_element
#    
#    #initial = time.time()
#    
#    pair_of_sectors2 = []
#    grid_offset = [
#                   #[ 1,-1, 0],
#                   #[ 0,-1, 0],
#                   #[-1,-1, 0],
#                   #[-1, 0, 0],
#                   
#                   #[ 0, 0, 0], 
#                   
#                   [ 1, 0, 0], 
#                   [ 1, 1, 0], 
#                   [ 0, 1, 0], 
#                   [-1, 1, 0], 
#                   
#                   [-1, 2, 0],
#                   [ 0, 2, 0],
#                   [ 1, 2, 0],
#                   [ 2, 2, 0],
#                   [ 2, 1, 0],
#                   [ 2, 0, 0],
#                   [ 2,-1, 0],                   
#                   
#                   [ 0, 0, 1],
#                   [ 1, 0, 1], 
#                   [ 1, 1, 1], 
#                   [ 0, 1, 1], 
#                   [-1, 1, 1], 
#                   [-1, 0, 1],
#                   [-1,-1, 1], 
#                   [ 0,-1, 1], 
#                   [ 1,-1, 1],
#                   
#                   [-1, 2, 1],
#                   [ 0, 2, 1],
#                   [ 1, 2, 1],
#                   [ 2, 2, 1],
#                   [ 2, 1, 1],
#                   [ 2, 0, 1],
#                   [ 2,-1, 1],
#
#
#                   [1,-2, -1],
#                
#
#                   [ 0, 0, 2],
#                   [ 1, 0, 2], 
#                   [ 1, 1, 2], 
#                   [ 0, 1, 2], 
#                   [-1, 1, 2], 
#                   [-1, 0, 2],
#                   [-1,-1, 2], 
#                   [ 0,-1, 2], 
#                   [ 1,-1, 2],
#                   
#                   
#                   [-1, 2, 2],
#                   [ 0, 2, 2],
#                   [ 1, 2, 2],
#                   [ 2, 2, 2],
#                   [ 2, 1, 2],
#                   [ 2, 0, 2],
#                   [ 2,-1, 2],
#
#                   ]
#    done = []
#    for element in atomic_grid.keys():
#        for offset_element in  grid_offset:              
#            
#            element1  = (element[0], 
#                         element[1], 
#                         element[2])
#                          
#            element2  = (element[0]+offset_element[0], 
#                         element[1]+offset_element[1], 
#                         element[2]+offset_element[2]) 
#                    
#            if element2 in atomic_grid:                        
#                if element1 == element2:
#                    pass
#                    #print(element1, element2, 'repetidos')
#                else:
#                    #print(element1, element2)
#                    pair_of_sectors2.append([atomic_grid[element1],
#                                             atomic_grid[element2]])
#                
#                #if [element1, element2] in done or [element2, element1] in done:
#                #    #print ('already in the list:'[element1, element2])
#                #    pass
#                #
#                #
#                #else:
#                #    done.append([element1, element2])
#                #    pair_of_sectors2.append([atomic_grid[element1],
#                #                             atomic_grid[element2]])
#                #    
#                #    #print([element1, element2])
#    #print(pair_of_sectors2)
#    return pair_of_sectors2
#
#cpdef tuple _generate_connections_into_a_grid_element (list list_of_atoms  , 
#                                                       list atoms          , 
#                                                       list bonds_pair_of_indices   ,  #indices of connected atoms
#                                                       list bonds_full_indices    ,
#                                                       list non_bonded_list): #pairs_of_
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
#    bonds_pair_of_indices [[a,b],[b,c], ...] where a and b are indices. 
#    returns a list of pair of indices "bonds_pair_of_indices"
#    
#    """
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
#    cdef int list_index = 0 
#    #print(len(atoms), list_of_atoms, atoms)
#    
#    
#    for i, atom_i in enumerate(list_of_atoms[:-1]):
#        atom_ix   = atom_i[3][0]
#        atom_iy   = atom_i[3][1]    
#        atom_iz   = atom_i[3][2]
#        cov_rad_i = atom_i[2]
#        index_i   = atom_i[0]
#        
#        list_index+= 1
#        
#        for j, atom_j in enumerate(list_of_atoms[i:]):    
#            if i == j:
#                pass
#                #print('i=j')
#            
#            else:
#                dX              = (atom_ix - atom_j[3][0])**2
#                dY              = (atom_iy - atom_j[3][1])**2
#                dZ              = (atom_iz - atom_j[3][2])**2
#                
#                cov_rad_j       = atom_j[2]
#                
#                cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*1.4
#                
#                
#                if (dX > cov_rad_ij_sqrt or 
#                    dY > cov_rad_ij_sqrt or 
#                    dZ > cov_rad_ij_sqrt):
#                    pass
#
#                else:
#                    r_ij = (dX + dY + dZ)
#                    if r_ij <= cov_rad_ij_sqrt:
#                        pass
#                        bonds_pair_of_indices.append([index_i , atom_j[0]])
#                        
#                        bonds_full_indices.append  (index_i  )
#                        bonds_full_indices.append  (atom_j[0])                 
#                        
#                        atom_i[8].append  (atom_j[0] )
#                        atom_j[8].append  (atom_i[0] )
#                        
#                        #non_bonded_list[index_i  ] = False
#                        #non_bonded_list[atom_j[0]] = False
#
#                    
#                    else:
#                        pass
#
#    return atoms, bonds_full_indices , bonds_pair_of_indices, non_bonded_list
#
#cpdef tuple _generate_connections_between_grid_elements (list lits_of_atoms1       , 
#                                                        list lits_of_atoms2       , 
#                                                        list atoms                , 
#                                                        list bonds_pair_of_indices,  #indices of connected atoms
#                                                        list bonds_full_indices   ,
#                                                        list non_bonded_list      ):
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
#    bonds_pair_of_indices [[a,b],[b,c], ...] where a and b are indices. 
#    returns a list of pair of indices "bonds_pair_of_indices"
#    """
#    
#
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
#    #size1 =  len(atoms1)
#    #size2 =  len(atoms2)
#    
#    
#    if lits_of_atoms1 == lits_of_atoms2:
#        pass
#    else:
#        for atom_i in lits_of_atoms1:   
#            atom_ix   = atom_i[3][0]
#            atom_iy   = atom_i[3][1]    
#            atom_iz   = atom_i[3][2]
#            cov_rad_i = atom_i[2]
#            index_i   = atom_i[0]
#
#            for atom_j in lits_of_atoms2:    
#                index_j = atom_j[0]
#                #if 
#                
#                dX              = (atom_ix - atom_j[3][0])**2
#                dY              = (atom_iy - atom_j[3][1])**2
#                dZ              = (atom_iz - atom_j[3][2])**2
#
#                cov_rad_j       = atom_j[2]
#                cov_rad_ij_sqrt = ((cov_rad_i + cov_rad_j)**2)*1.4
#                
#                if (dX > cov_rad_ij_sqrt or 
#                    dY > cov_rad_ij_sqrt or 
#                    dZ > cov_rad_ij_sqrt):
#                    pass
#
#                else:
#                    
#                    r_ij = (dX + dY + dZ)
#                    
#                    if r_ij <= cov_rad_ij_sqrt:
#                        bonds_pair_of_indices.append( [index_i , atom_j[0]] )
#                        
#                        bonds_full_indices.append   (index_i   )
#                        bonds_full_indices.append   (atom_j[0] )                 
#                        
#                        atom_i[8].append   (atom_j[0]          )
#                        atom_j[8].append   (atom_i[0]          )
#
#                        #non_bonded_list[index_i  ] = False
#                        #non_bonded_list[atom_j[0]] = False
#
#
#    return atoms, bonds_full_indices, bonds_pair_of_indices, non_bonded_list
#
#cpdef dict _build_the_atomic_grid (list atoms):
#    """  fucntion build_atomic_grid
#    
#    This function organizes the atoms in their respective position 
#    of the grid (atomic grid) - Nescessary to calculate distances between 
#    atoms in different elements of the grid
#    
#    self.grid_size = is the size of a grid element - size of a sector
#    
#    
#              atomic grid
#              
#        |-------|-------|-------| |
#        |       | grid  |       | |
#        |       |element|       | | grid_size
#        |-1,1,0 | 0,1,0 | 1,1,0 | |
#        |-------|-------|-------| |
#        |       |       |       |
#        |       |       |       |
#        |-1,0,0 | 0,0,0 | 1,0,0 |
#        |-------|-------|-------|
#        |       |       |       |
#        |       |       |       |
#        |-1,-1,0| 0,-1,0| 1,-1,0|
#        |-------|-------|-------|
#                         -------
#                        grid_size
#    
#    
#    grid element = list of atoms
#    """
#    #int grid_size
#    cdef dict  atomic_grid = {}
#    
#    for atom in atoms:
#        a = atom[9][0]
#        b = atom[9][1]
#        c = atom[9][2]
#        #print((a,b,c), atom[0], atom[1])
#        if (a,b,c) in atomic_grid:
#            atomic_grid[(a,b,c)].append(atom)
#        else:
#            atomic_grid[(a,b,c)] = []
#            atomic_grid[(a,b,c)].append(atom)
#    return atomic_grid
#
#cpdef _generete_NB_list_from_TrueFalse_list(list NB_TrueFalse_list):
#
#    #debug =  {'pName': '_generete_NB_list_from_TrueFalse_list'}
#    NB_indices_list  = []
#    #---------------------------------------------------------------#
#    #initial       = time.time()
#    #---------------------------------------------------------------#
#    index = 0
#    
#    for TrueFalse in NB_TrueFalse_list:
#        if TrueFalse:
#            NB_indices_list.append(index)
#        index += 1
#    NB_indices_list = np.array(NB_indices_list, dtype=np.uint32)
#    #--------------------------------------------------------------#
#    #final = time.time()                                            #
#    #print ('method2 time : ', final - initial, '\n')#
#    #--------------------------------------------------------------#
#    
#    return NB_indices_list#, debug
#
#
#cpdef generete_full_NB_and_Bonded_lists(atoms , log = False):
#    '''
#    atoms = [] it's a list
#    
#    list element = [atom.index-1    ,    # 0
#                    atom.name       ,    # 1
#                    atom.cov_rad    ,    # 2
#                    np.array(coods) ,    # 3
#                    atom.resi       ,    # 4
#                    atom.resn       ,    # 5
#                    atom.chain      ,    # 6
#                    atom.symbol     ,    # 7
#                    []              ,    # 8
#                    gridpos         ]
#    
#    '''
#    #----------------------------------------------------------------------------------------------
#    #                                Pairwise grid elements
#    #----------------------------------------------------------------------------------------------
#
#    #--------------------------------------------------------------#
#    initial       = time.time()                                    #
#    #--------------------------------------------------------------#
#    bonds_full_indices, bonds_pair_of_indices = [], []
#    
#    atomic_grid               = _build_the_atomic_grid(atoms)
#    pairs_of_grid_elements    = _determine_the_paired_atomic_grid_elements(atomic_grid)
#    NB_TrueFalse_list         = [True]*len(atoms)
#    #--------------------------------------------------------------#
#    final = time.time()                                            #
#    
#    
#    if log:
#        print ('building grid elements  : ', final - initial, '\n')#
#        #--------------------------------------------------------------#
#        #print (non_bonded_list)
#        print ('Total number of Atoms   :', len(atoms)                 )
#        print ('Number of grid elements :', len(atomic_grid)           )
#        print ('Pairs                   :', len(pairs_of_grid_elements))
#
#    #----------------------------------------------------------------------------------------------
#    
#    
#    '''
#    #-----------------------------------------------------------------------------------------------------------------------------------------------
#    #                                                B O N D S
#    #-----------------------------------------------------------------------------------------------------------------------------------------------
#    '''
#    #---------------------------------------------------------------#
#    initial       = time.time()
#    #---------------------------------------------------------------#
#
#    #'''
#    for list_of_atoms in atomic_grid.values():
#        #print (len(atoms))
#        atoms, bonds_full_indices, bonds_pair_of_indices, NB_TrueFalse_list = _generate_connections_into_a_grid_element( list_of_atoms, 
#                                                                                                              atoms                   , 
#                                                                                                              bonds_pair_of_indices   , 
#                                                                                                              bonds_full_indices      ,
#                                                                                                              NB_TrueFalse_list       )    
#    #'''
#    #'''
#    for pair_of_grid_elements in pairs_of_grid_elements:
#        atoms, bonds_full_indices, bonds_pair_of_indices, NB_TrueFalse_list = _generate_connections_between_grid_elements(pair_of_grid_elements[0],
#                                                                                                                          pair_of_grid_elements[1],
#                                                                                                                          atoms                   ,
#                                                                                                                          bonds_pair_of_indices   , 
#                                                                                                                          bonds_full_indices      ,
#                                                                                                                          NB_TrueFalse_list           )
#    #'''
#    if log:
#        print ('Bonds                   :', len(bonds_pair_of_indices))
#        #--------------------------------------------------------------#
#        final = time.time()                                            #
#        print ('Bonds calcultation time : ', final - initial, '\n')    #
#        #--------------------------------------------------------------#
#    #print(bonds_pair_of_indices)
#    return bonds_pair_of_indices
#    #return bonds_full_indices, bonds_pair_of_indices
#
#
#
#
#
#
#
#
#
#
#
