import os
import time
import multiprocessing
import numpy as np
#import vModel.atom_types as at 
import vModel.cDistances as cdist
from   vModel import VismolObject
#from   vModel import MolecularProperties


'''
@<TRIPOS>MOLECULE
DCM Pose 1
   32    33     0     0     0
SMALL
USER_CHARGES

@<TRIPOS>ATOM
      1 N          63.2680   27.8610   32.2290 N.3     4  VAL4        0.0000

      1 C1         18.8934    5.5819   24.1747 C.2       1 <0>       -0.1356 
      2 C2         18.1301    4.7642   24.8969 C.2       1 <0>       -0.0410 
      3 C3         18.2645    6.8544   23.7342 C.2       1 <0>        0.4856 
      4 C4         16.2520    6.2866   24.7933 C.2       1 <0>        0.8410 
      5 C5         15.3820    3.0682   25.1622 C.3       1 <0>        0.0000 
      6 C6         15.4162    1.8505   26.0566 C.3       1 <0>        0.2800 
      7 C7         16.7283    2.0138   26.8111 C.3       1 <0>        0.2800 
      8 C8         16.0764    4.1199   26.0119 C.3       1 <0>        0.5801 
      9 C9         17.9106    1.3823   26.0876 C.3       1 <0>        0.2800 
     10 N1         17.0289    7.1510   24.0411 N.2       1 <0>       -0.6610 
     11 N2         16.8196    5.0644   25.2302 N.am      1 <0>       -0.4691 
     12 N3         19.0194    7.7275   22.9859 N.pl3     1 <0>       -0.8500 
     13 O1         18.7676   -2.3524   26.1510 O.3       1 <0>       -1.0333 
     14 O2         20.3972   -0.3812   26.2318 O.3       1 <0>       -1.0333 
     15 O3         15.0888    6.5824   25.0727 O.2       1 <0>       -0.5700 
     16 O4         18.9314   -0.7527   24.1606 O.2       1 <0>       -1.0333 
     17 O5         16.9690    3.4315   26.8994 O.3       1 <0>       -0.5600 
     18 O6         14.3223    1.8946   26.9702 O.3       1 <0>       -0.6800 
     19 O7         17.9091   -0.0135   26.3390 O.3       1 <0>       -0.5512 
     20 P1         19.0969   -0.9440   25.6653 P.3       1 <0>        1.3712 
     21 H1         19.9176    5.3550   23.9105 H         1 <0>        0.1500 
     22 H2         18.5100    3.8155   25.2595 H         1 <0>        0.1500 
     23 H3         15.8520    2.8983   24.1870 H         1 <0>        0.0000 
     24 H4         14.3405    3.3601   24.9711 H         1 <0>        0.0000 
     25 H5         15.3663    0.9351   25.4839 H         1 <0>        0.0000 
     26 H6         16.6681    1.6130   27.8171 H         1 <0>        0.0000 
     27 H7         15.3483    4.6961   26.6094 H         1 <0>        0.0000 
     28 H8         18.8490    1.8078   26.4511 H         1 <0>        0.0000 
     29 H9         17.8303    1.5497   25.0110 H         1 <0>        0.0000 
     30 H10        19.9527    7.4708   22.7715 H         1 <0>        0.4000 
     31 H11        18.5977    8.5756   22.6932 H         1 <0>        0.4000 
     32 H12        14.2530    1.0535   27.4278 H         1 <0>        0.4000 
@<TRIPOS>BOND
    1     1     2 2
    2     1     3 1
    3     2    11 1
    4     3    10 2
    5     3    12 1
    6     4    10 1
    7     4    11 am
    8     4    15 2
    9     5     6 1
   10     5     8 1
   11     6     7 1
   12     6    18 1
   13     7     9 1
   14     7    17 1
   15     8    11 1
   16     8    17 1
   17     9    19 1
   18    13    20 1
   19    14    20 1
   20    16    20 2
   21    19    20 1
   22     1    21 1
   23     2    22 1
   24     5    23 1
   25     5    24 1
   26     6    25 1
   27     7    26 1
   28     8    27 1
   29     9    28 1
   30     9    29 1
   31    12    30 1
   32    12    31 1
   33    18    32 1
@<TRIPOS>SUBSTRUCTURE
'''

def load_mol2_files (infile = None, vm_session =  None, gridsize = 3):
    """ Function doc """
    print ('\nstarting: parse_mol2')

    #at  = MolecularProperties.AtomTypes()
    with open(infile, 'r') as mol2_file:
        filetext = mol2_file.read()

        molecules     =  filetext.split('@<TRIPOS>MOLECULE')
        firstmolecule =  molecules[1].split('@<TRIPOS>ATOM')
        header        =  firstmolecule[0]
        firstmolecule =  firstmolecule[1].split('@<TRIPOS>BOND')
        raw_atoms     =  firstmolecule[0]
        bonds         =  firstmolecule[1]

    header    = header.split('\n')
    raw_atoms = raw_atoms.split('\n')
    bonds     = bonds.split('\n')

    print (raw_atoms)
    atoms, frames = get_atom_list_from_mol2_frame(raw_atoms = raw_atoms, frame = True)#,  gridsize = gridsize,  at = at)

    #-------------------------------------------------------------------------------------------
    #                         Building   V I S M O L    O B J
    #-------------------------------------------------------------------------------------------
    name = os.path.basename(infile)
    vobject  = VismolObject.VismolObject(name        = name, 
                                               atoms       = atoms, 
                                               vm_session   = vm_session, 
                                               trajectory  = frames)
    #-------------------------------------------------------------------------------------------
    return vobject











def get_atom_list_from_mol2_frame (raw_atoms, frame = True):#, gridsize = 3, at =  None):
    """ Function doc """
    #nCPUs =  multiprocessing.cpu_count()
    #pool  = multiprocessing.Pool(nCPUs)
    #pdb_file_lines  = frame.split('\n')   
    #atoms = (pool.map(parse_pdb_line, pdb_file_lines))
    
    atoms  = []
    frames = []
    frame_coordinates = []
    #print (raw_atoms)
    for line in raw_atoms:
        line = line.split()
        if len(line) > 1:
            #print (line) 
            index    = int(line[0])-1
            
            at_name  = line[1]
            
            at_pos   = np.array([float(line[2]), float(line[3]), float(line[4])])
            
            at_resi = int(line[6])
            
            at_resn = line[7]


            at_ch   = 'X'          

            at_occup   = 0.0     #occupancy
            at_bfactor = 0.0
            at_charge  = float(line[8])


            at_symbol  = None# at.get_symbol(at_name)
            
            #at_symbol= line[5].split('.')
            #at_symbol= at_symbol[0]
            #cov_rad  = at.get_cov_rad (at_symbol)



            #gridpos  = [int(at_pos[0]/gridsize), int(at_pos[1]/gridsize), int(at_pos[2]/gridsize)]
            #atoms.append([index, at_name, cov_rad,  at_pos, at_resi, at_resn, at_ch, at_symbol, [], gridpos, at_occup, at_bfactor, at_charge ])
            #atoms.append([index, at_name, cov_rad,  at_pos, at_resi, at_resn, at_ch, at_symbol, [], gridpos, at_occup, at_bfactor, at_charge ])
            
            atoms.append({
                          'index'      : index      , 
                          'name'       : at_name    , 
                          'resi'       : at_resi    , 
                          'resn'       : at_resn    , 
                          'chain'      : at_ch      , 
                          'symbol'     : at_symbol  , 
                          'occupancy'  : at_occup   , 
                          'bfactor'    : at_bfactor , 
                          'charge'     : at_charge   
                          })


            #atoms.append([index, at_name, cov_rad,  at_pos, at_res_i, at_res_n, at_ch])
            
            #atom     = Atom(name      =  at_name, 
            #                index     =  index, 
            #                pos       =  at_pos, 
            #                resi      =  at_res_i, 
            #                resn      =  at_res_n, 
            #                chain     =  at_ch, 
            #                )
            #atoms.append(atom)
            frame_coordinates.append(float(line[2]))
            frame_coordinates.append(float(line[3]))
            frame_coordinates.append(float(line[4]))
    frame_coordinates = np.array(frame_coordinates, dtype=np.float32)
    frames.append(frame_coordinates)
    #print (frames)
    #print (atoms)
    return atoms, frames#, coords

def get_bonds (raw_bonds):
    """ Function doc """
    index_bonds              = []
    index_bonds_pairs        = []
    index_bonds_pairs_orders = []
    
    #print (raw_bonds)
    #print ('Obtain bonds from original MOL2 file')
    for line in raw_atoms:
        line = line.split()
        if len(line) == 4:
            index    = int(line[0])            
            atom1    = int(line[1]-1)
            atom2    = int(line[2]-1)
            order    = line[3]

            index_bonds      .append(atom1)
            index_bonds      .append(atom2)
            index_bonds_pairs.append([atom1,atom2])
            
            index_bonds_pairs_orders.append(order)

    return [index_bonds, index_bonds_pairs]


'''  	
def get_trajectory_coordinates_from_pdb_frames (raw_frames = None):
    """ Function doc """
    n_processor = multiprocessing.cpu_count()
    pool        = multiprocessing.Pool(n_processor)
    frames      = pool.map(get_pdb_frame_coordinates, raw_frames)
    
    if None in frames:
        index = frames.index(None)
        frames.pop(index)
    return frames


def get_pdb_frame_coordinates (frame):
    """ Function doc """
    #print ('\nstarting: parse_pdb - building atom list')
    #initial          = time.time()
    pdb_file_lines    = frame.split('\n')
    frame_coordinates = []
    for line in pdb_file_lines:
        if line[:4] == 'ATOM' or line[:6] == 'HETATM':
            #at_name  = line[12:16].strip()
            frame_coordinates.append(float(line[30:38]))
            frame_coordinates.append(float(line[38:46]))
            frame_coordinates.append(float(line[46:54]))
            #at_pos   = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])

    frame_coordinates = np.array(frame_coordinates, dtype=np.float32)
    #print ('Frame size: ', len(frame_coordinates)/3)
    
    if len(frame_coordinates) == 0:
        return None
    
    return frame_coordinates
'''
	
