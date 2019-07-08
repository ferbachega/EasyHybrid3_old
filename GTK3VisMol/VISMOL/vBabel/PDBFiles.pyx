import os
import time
import multiprocessing
import numpy as np
import VISMOL.vModel.atom_types as at 
import VISMOL.vModel.cDistances as cdist
from   VISMOL.vModel import VismolObject


cpdef load_pdb_file (infile = None, gridsize = 3, VMSession =  None):
    """ Function doc 

    gridsize =

    The longest covalent bond I can find is the bismuth-iodine single bond.
    The order of bond lengths is single > double > triple.
    The largest atoms should form the longest covalent bonds. 
    So we look at atoms in the lower right corner of the Periodic Table.
    The most likely candidates are Pb, Bi, and I.
    The experimental bond lengths are:
    Bi-I = 281 pm; Pb-I = 279 pm; I-I = 266.5 pm.
    So the polar covalent Bi-I bond is the longest covalent measured so far.

    """
    #-------------------------------------------------------------------------------------------
    #                                P D B     P A R S E R 
    #-------------------------------------------------------------------------------------------
    with open(infile, 'r') as pdb_file:
        pdbtext = pdb_file.read()

        rawframes = pdbtext.split('ENDMDL')
        atoms     = get_list_of_atoms_from_rawframe(rawframes[0], gridsize)
        frames    = get_list_of_frames_from_pdb_rawframes (rawframes = rawframes)
    #-------------------------------------------------------------------------------------------
    
    
    
    #-------------------------------------------------------------------------------------------
    #                                Bonded and NB lists 
    #-------------------------------------------------------------------------------------------
    atoms, bonds_full_indexes, bonds_pair_of_indexes, NB_indexes_list = cdist.generete_full_NB_and_Bonded_lists(atoms)
    #-------------------------------------------------------------------------------------------
    
    
    #-------------------------------------------------------------------------------------------
    #                         Building   V I S M O L    O B J
    #-------------------------------------------------------------------------------------------
    name = os.path.basename(infile)
    vismol_object  = VismolObject.VismolObject(name        = name, 
                                               atoms       = atoms, 
                                               VMSession   = VMSession, 
                                               trajectory  = frames)
    
    
    vismol_object._generate_atomtree_structure()
    vismol_object._generate_atom_unique_color_id()
    vismol_object.index_bonds       = bonds_full_indexes
    vismol_object.index_bonds_pairs = bonds_pair_of_indexes
    vismol_object.non_bonded_atoms  = NB_indexes_list
    vismol_object.generate_dot_indexes()
    #vismol_object.get_backbone_indexes()
    #-------------------------------------------------------------------------------------------
    return vismol_object
    
    
    
    
    
    
cpdef get_list_of_atoms_from_rawframe(rawframe, gridsize = 3):
    """ Function doc 

ATOM      1  N   THR A   1      -1.820  24.919  -5.344  1.00  0.00           N  
ATOM      2  CA  THR A   1      -1.256  24.379  -4.074  1.00  0.00           C  
ATOM     61  CB  ILE A   4      -7.386  -0.466   0.343  1.00  0.00           C  
ATOM  16     HO2 GLC  1       2.188   -0.704  0.939   1.00  300.00          H 0.0000   
ATOM     27  NH1 ARG A   5      68.029  23.029  29.719  1.00 38.75           N1+

iCode = ""
( serial       ,
  name         ,
  altLoc       ,
  resName      ,
  chainID      ,
  resSeq       ,
  u00          ,
  u11          ,
  u22          ,
  u01          ,
  u02          ,
  u12          ,
  segID        ,
  atomicNumber ,
  formalCharge ) = self._ParseFixedFormatLine ( line                    ,
                                                (  6, 11, int  , None ) ,
                                                ( 12, 16, None , ""   ) ,
                                                ( 16, 17, None , ""   ) ,
                                                ( 17, 20, None , ""   ) ,
                                                ( 21, 22, None , ""   ) ,
                                                ( 22, 27, int  , None ) ,
                                                ( 28, 35, float, None ) ,
                                                ( 35, 42, float, None ) ,
                                                ( 42, 49, float, None ) ,
                                                ( 49, 56, float, None ) ,
                                                ( 56, 63, float, None ) ,
                                                ( 63, 70, float, None ) ,
                                                ( 72, 76, None , ""   ) ,
                                                ( 76, 78, PeriodicTable.AtomicNumberFromSymbol, -1 ) ,
                                                ( 78, 80, None , ""   ) )

    """
    #nCPUs = multiprocessing.cpu_count()
    #pool  = multiprocessing.Pool(nCPUs)
    #gridsize = 3
    pdb_file_lines  = rawframe.split('\n')   
    atoms           = []
    cdef int index           = 0
    for line in pdb_file_lines:
        if line[:4] == 'ATOM' or line[:6] == 'HETATM':
            
            at_name  = line[12:16].strip()
            at_pos   = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
            at_resi  = int(line[22:27])
            at_resn  = line[17:20].strip()
            at_ch    = line[21]             
            at_symbol= line[76:78]
            cov_rad  = at.get_cov_rad (at_name)
            gridpos  = [int(at_pos[0]/gridsize), int(at_pos[1]/gridsize), int(at_pos[2]/gridsize)]
                            #0      1      2           3       4        5        6       7       8
            atoms.append([index, at_name, cov_rad,  at_pos, at_resi, at_resn, at_ch, at_symbol, [], gridpos ])
            #atoms.append([index, at_name, cov_rad, at_resi, at_resn, at_ch, at_symbol])
            index += 1
            #atom     = Atom(name      =  at_name, 
            #                #index    =  index, 
            #                pos       =  at_pos, 
            #                resi      =  at_res_i, 
            #                resn      =  at_res_n, 
            #                chain     =  at_ch, 
            #                #atom_id  =  counter, 
            #                )
            #atoms.append(atom)
    return atoms#, coords





cpdef get_list_of_frames_from_pdb_rawframes (rawframes = None):
    """ Function doc """
    n_processor = multiprocessing.cpu_count()
    pool        = multiprocessing.Pool(n_processor)
    frames      = pool.map(get_pdb_frame_coordinates, rawframes)
    return frames





cpdef get_pdb_frame_coordinates (str frame):
    """ Function doc """
    #print ('\nstarting: parse_pdb - building atom list')
    #initial          = time.time()
    pdb_file_lines    = frame.split('\n')
    
    #cdef float *frame_coordinates
    frame_coordinates = []
    
    
    for line in pdb_file_lines:
        if line[:4] == 'ATOM' or line[:6] == 'HETATM':
            #at_name  = line[12:16].strip()
            frame_coordinates.append(float(line[30:38]))
            frame_coordinates.append(float(line[38:46]))
            frame_coordinates.append(float(line[46:54]))
            #at_pos   = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])

    frame_coordinates = np.array(frame_coordinates, dtype=np.float32)

    if len(frame_coordinates) == 0:
        return None
    
    return frame_coordinates
