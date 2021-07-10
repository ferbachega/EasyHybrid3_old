import os
import time
import numpy as np
import VISMOL.vModel.cDistances as cdist
from   VISMOL.vModel import VismolObject


def load_amber_topology_files (infile = None, VMSession =  None, gridsize = 3):
    """ Function doc """
    at  =  VMSession.vConfig.atom_types
    filename = infile
    infile = open(infile, 'r')
    text = infile.read()
    #print(text)
    text2 = text.split("%FLAG")
    
    atom_names      = None
    atomic_numbers  = None
    bonds_H         = None
    bonds_noH       = None
    residues_names  = None  
    pointers        = None
    
    at_names    = []
    at_numbers  = []
    bonds       = []
    bonds2      = []
    res_names   = []
    res_indexes = []
    
    total_bonds = []
    for block in text2:
        
        block2 = block.split('\n')
        string = ''
        for block3  in block2[2:]:
            string += block3
        
        #print(string)
        if 'ATOM_NAME' in block:
            atom_names = string
            #print(atom_names)
            for i in range(0, len(atom_names),4):
                at_name = atom_names[i:i+4]
                at_names.append(at_name.strip())
        
        if 'ATOMIC_NUMBER' in block:
            atomic_numbers = string
            #atomic_numbers = atomic_numbers.split()
            
            for i in range(0, len(atomic_numbers),8):
                atomic_number = atomic_numbers[i:i+8]
                at_numbers.append(int(atomic_number.strip()))
        
        if 'BONDS_INC_HYDROGEN' in block:
            bonds_H = string
            
            for i in range(0, len(bonds_H),8):
                bond = bonds_H[i:i+8]
                #bond = int((int(bond.strip())/3) + 1) 
                bond = int((int(bond.strip())/3)) 
                bonds.append(bond)
            for i in range(0, len(bonds),3):
                #print(bonds[i:i+2])
                total_bonds.append(bonds[i:i+2])
                
        if 'BONDS_WITHOUT_HYDROGEN' in block:
            bonds_noH = string
            for i in range(0, len(bonds_noH),8):
                bond = bonds_noH[i:i+8]
                #bond = int((int(bond.strip())/3) + 1) 
                bond = int((int(bond.strip())/3)) 
                bonds2.append(bond)
            
            for i in range(0, len(bonds2),3):
                #print(bonds2[i:i+2])
                total_bonds.append(bonds2[i:i+2])




        if 'RESIDUE_LABEL' in block:
            labels = string
            res_names_short = []
            #print (labels)
            for i in range(0, len(labels),4):
                label = labels[i:i+4]
                res_names_short.append(label.strip())
                #bonds2.append(bond)
            
            
        if 'RESIDUE_POINTER' in block:
            
            pointers = string.split()
            #print (pointers)
            pointers2 = []
            
            for i in pointers:
                pointers2.append(int(i))
            
            pointers2.append(len(at_names)+1)
            
            #print (pointers2)
            
            
            
            idx = 0
            residue_counter = 1
            
            for atom in at_names:
                if idx < pointers2[residue_counter]-1:
                    #print (idx, atom, residue_counter, pointers2, res_names_short[residue_counter-1])
                    
                    res_indexes.append(residue_counter)
                    res_names.append(res_names_short[residue_counter-1])
                else:
                    residue_counter += 1 
                    #print (idx, atom, residue_counter, pointers2, res_names_short[residue_counter-1])
                    res_indexes.append(residue_counter)
                    res_names.append(res_names_short[residue_counter-1])
                idx+=1
            
            
            
            '''
            residue_counter = 1
            for i in range(0, len(at_names)):
                
                if i <= pointers2[residue_counter]-1:
                    print (pointers2[residue_counter]-1, residue_counter, pointers2, at_names[i],i )
                    pass

                    #print (i+1, pointers, residue_counter, at_names[i], res_names_short[residue_counter-1])
                    res_indexes.append(residue_counter)
                    res_names.append(res_names_short[residue_counter-1])
                else:
                    residue_counter += 1 
                #print (len(res_indexes), len(res_names))
            '''
            #for i in range(0, len(pointers),8):
            #    pointers = pointers[i:i+8]
            #    print (pointers ) 
            #    res_indexes.append(pointers)
            #    #bonds2.append(bond)
 



    #print (len(at_names), len(at_numbers), len(res_names),len(res_indexes))
    print (at_numbers)
    #print (at_names, at_numbers)

    #print (bonds)
    #print (bonds2)
    #print (res_names_short)
    

    #print (res_names)
    #print (res_indexes)
    
    resi_counter  = 1 
    atoms = []
    
    for index in range(len(at_names)):
        
        at_name  = at_names[index]
        at_pos   = np.array([0.0,0.0,0.0])
        
        
        
        at_resn  = res_names[index]
        at_resi  = res_indexes[index]
        at_chain = 'X'
        
        at_occup   = 0.0     #occupancy
        at_bfactor = 0.0
        at_charge  = 0.0
                
        #print (index, at_name, at_resn, at_resi,  at_chain, at_pos, at_numbers[index] )
        #print(at.ATOM_TYPES_BY_ATOMICNUMBER, at_numbers[index])
        #if at_numbers != []:
        #    at_symbol = at.ATOM_TYPES_BY_ATOMICNUMBER[at_numbers[index]]
        #else:
        at_symbol = at.get_symbol(at_name)
        cov_rad   = at.get_cov_rad (at_symbol)
        gridpos   = [0,0,0]
        

        atoms.append([index, at_name, cov_rad,  at_pos, at_resi, at_resn, at_chain, at_symbol, [], gridpos, at_occup, at_bfactor, at_charge ])
        #print([index, at_name, cov_rad,  at_pos, at_resi, at_resn, at_chain, at_symbol, [], gridpos, at_occup, at_bfactor, at_charge ])

    #print (total_bonds)

    
    
    #for bond in total_bonds:
    #    print(bond, atoms[bond[0]], atoms[bond[1]])


    name = os.path.basename(filename)
    vismol_object  = VismolObject.VismolObject(name                           = name       , 
                                               atoms                          = atoms      , 
                                               VMSession                      = VMSession  , 
                                               bonds_pair_of_indexes          = total_bonds,
                                               trajectory                     = []         ,
                                               auto_find_bonded_and_nonbonded = False      )
        
    return   vismol_object  
    
        
        
def load_amber_crd_file (infile, vismol_object):
    """ Function doc """
    #at  =  VMSession.vConfig.atom_types
    #filename = infile
    
    text = open(infile, 'r')
    text = text.read()
    print(text)
    
    #print(text)
    #text2 = text.split("%FLAG")
        
        
        
        
        



def get_atom_list_from_mol2_frame (raw_atoms, frame = True, gridsize = 3, at =  None):
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



            at_symbol= line[5].split('.')
            at_symbol= at_symbol[0]
            cov_rad  = at.get_cov_rad (at_symbol)



            gridpos  = [int(at_pos[0]/gridsize), int(at_pos[1]/gridsize), int(at_pos[2]/gridsize)]
            #atoms.append([index, at_name, cov_rad,  at_pos, at_resi, at_resn, at_ch, at_symbol, [], gridpos, at_occup, at_bfactor, at_charge ])
            atoms.append([index, at_name, cov_rad,  at_pos, at_resi, at_resn, at_ch, at_symbol, [], gridpos, at_occup, at_bfactor, at_charge ])



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
#load_amber_topology_files (infile = '/home/fernando/Documents/Paola/cas.top', VMSession =  None, gridsize = 3)
#load_amber_topology_files (infile = '/home/fernando/Documents/Paola/pep.top', VMSession =  None, gridsize = 3)
