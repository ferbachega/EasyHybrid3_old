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
#  
#try:
import molecular_model as mm
#except:
#    import molecular_model as mm
    
import os
import numpy as np
from pprint import pprint
import time
import multiprocessing


def load_pdb_files (infile = None):
    """ Function doc """
    print ('\nstarting: parse_pdb')
    initial = time.time()
    
    with open(infile, 'r') as pdb_file:
        pdbtext = pdb_file.read()
        
        #if 'ENDMDL' in pdbtext:
        #    print ('multiple frames')
        frames =  pdbtext.split('ENDMDL')
        # retunr a single frame for PDB with no ENDMDL label - standard pdbfiles
        atoms  =  get_atom_list_from_pdb_frame(frames[0])
        frames =  get_trajectory_coordinates_from_pdb_frames (raw_frames = frames)
    
    final   = time.time() 
    print ('ending parse_pdb: ', final - initial, '\n')
    return atoms, frames

    	
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
    print ('Frame size: ', len(frame_coordinates)/3)
    
    if len(frame_coordinates) == 0:
        return None
    
    return frame_coordinates

	
def get_atom_list_from_pdb_frame (frame):
    """ Function doc """
    #print ('\nstarting: parse_pdb - building atom list')
    #initial          = time.time()
    pdb_file_lines  = frame.split('\n')
    atoms = []
    for line in pdb_file_lines:
	
        if line[:4] == 'ATOM' or line[:6] == 'HETATM':
            at_name  = line[12:16].strip()
            at_pos   = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
            at_res_i = int(line[22:26])
            at_res_n = line[17:20].strip()
            at_ch    = line[21]             
            
            atom      = mm.Atom(name    =  at_name, 
                      #index        =  index, 
                      pos          =  at_pos, 
                      resi         =  at_res_i, 
                      resn         =  at_res_n, 
                      chain        =  at_ch, 
                      #atom_id      =  counter, 
                      )
            #Vobject.atoms.append(atom)
            atoms.append(atom)
    print ('Numeber of atoms: ', len(atoms))
    #print ('ending parse_pdb: - building atom list', final - initial, '\n')
    return atoms


def parse_pdb (infile = None):
    """ Function doc """
    print ('\nstarting: parse_pdb')
    initial          = time.time()
    
    with open(infile, 'r') as pdb_file:

        label = os.path.basename(infile)
        pdb_file_lines = pdb_file.readlines()
        
        atoms = []
        frame = []     
       
        for line in pdb_file_lines:
            if line[:4] == 'ATOM' or line[:6] == 'HETATM':
                at_name = line[12:16].strip()
                #at_index = int(line[6:11])
                at_pos = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
                at_res_i = int(line[22:26])
                at_res_n = line[17:20].strip()
                at_ch    = line[21]             
                
                atom      = mm.Atom(name    =  at_name, 
                                  #index        =  index, 
                                  pos          =  at_pos, 
                                  resi         =  at_res_i, 
                                  resn         =  at_res_n, 
                                  chain        =  at_ch, 
                                  #atom_id      =  counter, 
                                  )
                #Vobject.atoms.append(atom)
                atoms.append(atom)
            if 'ENDMDL' in line:
                break

    #Vobject     = mm.Vobject(label = label, atoms = atoms)
    #atom_dic_id = Vobject.generate_chain_structure(counter = counter, atom_dic_id = atom_dic_id)
    final       = time.time() 
    print ('ending parse_pdb: ', final - initial, '\n')
    return atoms



    
