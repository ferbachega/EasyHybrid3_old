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

from VISMOL.vModel.Atom              import Atom
from VISMOL.vModel.Chain             import Chain
from VISMOL.vModel.Residue           import Residue
from VISMOL.vModel.Bond              import Bond
from VISMOL.vModel.Representations   import LinesRepresentation
from VISMOL.vModel.Representations   import NonBondedRepresentation
from VISMOL.vModel.Representations   import SticksRepresentation
from VISMOL.vModel.Representations   import DotsRepresentation
from VISMOL.vModel.Representations   import SpheresRepresentation
from VISMOL.vModel.Representations   import GlumpyRepresentation
from VISMOL.vModel.Representations   import WiresRepresentation

import VISMOL.vModel.cDistances as cdist




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
    
    self.active            = False
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
                  name                           = 'UNK', 
                  atoms                          = []   ,
                  VMSession                      = None , 
                  trajectory                     = None ,
                  bonds_pair_of_indexes          = None , 
                  auto_find_bonded_and_nonbonded = True):
        
        """ Class initialiser """
        #-----------------------------------------------------------------
        #                V I S M O L   a t t r i b u t e s
        #----------------------------------------------------------------- 
        self.vismol_session = VMSession     #
        self.active         = False         # for "show and hide"   enable/disable
        self.editing        = False         # for translate and rotate  xyz coords 
        self.Type           = 'molecule'    # Not used yet
        self.name           = name          # 
        self.vm_font        = vmf.VisMolFont()

        #-----------------------------------------------------------------
        self.mass_center = None
        #-----------------------------------------------------------------

		
		#-------------------------#
		#    R A W    L I S T     #
		#-------------------------#
		
        #-----------------------------------------------------------------
        self.atoms2             = atoms # this is a raw list : [0, 'C5', 0.77, array([ 0.295,  2.928, -0.407]), 1, 'GLC', ' ', 'C ', [1, 12, 8, 10], [0, 0, 0]]
        #-----------------------------------------------------------------

        self.atoms              = []    # this a list  atom objects!
        self.residues           = []
        self.chains             = {}
        self.atoms_by_chains    = {}
        self.frames             = trajectory
        self.atom_unique_id_dic = {}

        self.vobj_selected_atoms= []

        #-----------------------#
        #         Bonds         #
        #-----------------------#
        self.dynamic_bons       = [] #  [0,1,1,2,3,4] 
        self.index_bonds        = []
        self.bonds              = []                        

        #-----------------------#
        #      No H atoms       #
        #-----------------------#
        self.noH_atoms = []           
        
        #-----------------------#
        #    Calpha  Ribbons    #
        #-----------------------#
        self.c_alpha_bonds = []           
        self.c_alpha_atoms = []
        #-----------------------#
        #       Nonbonded       #
        #-----------------------#
        self.non_bonded_atoms   = []
        
        self.residues_in_protein = []
        self.residues_in_solvent = []
        self.residues_ligands    = []
        
        self.atoms_in_protein = [] # a list of atoms belonging to a protein
        self.atoms_in_solvent = []
        
        

		#-----------------------------------------#
		#      R E P R E S E N T A T I O N S      #
        #-----------------------------------------#
        self.representations = {'nonbonded' : None,
                                'lines'     : None,
                                'dots'      : None,
                                'spheres'   : None,
                                'sticks'    : None,
                                'ribbons'   : None,
                                'surface'   : None,
                                'wires'     : None,
                                'glumpy'    : None,
                                }
        
        #-----------------------------------------------------------------
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
        
        
        
        
        if auto_find_bonded_and_nonbonded:
            self.find_bonded_and_nonbonded_atoms(atoms)
            self._get_center_of_mass()
        
        else:
            self._generate_atomtree_structure()
            self._generate_color_vectors()
            #self._get_center_of_mass()
        
        if bonds_pair_of_indexes:
            
            for pair in bonds_pair_of_indexes:
                self.index_bonds.append(pair[0])
                self.index_bonds.append(pair[1])
    
            self.index_bonds = np.array(self.index_bonds, dtype=np.uint32)
            
            self.import_bonds(bonds_pair_of_indexes)
            
            if self.non_bonded_atoms == []:
                self.import_non_bonded_atoms_from_bond()
                    
    
    
    
    
    
    def _add_new_atom_to_vobj (self, name          ,
                                     index         ,
                                     symbol        ,
                                     pos           ,
                                     resi          ,
                                     resn          ,
                                     chain         ,
                                     atom_id       ,
                                     occupancy     ,
                                     bfactor       ,
                                     charge        ,
                                     bonds_indexes ,
                                     Vobject       ,
                                                 ):
        """ Function doc """
    
        atom        = Atom(name          =  name          ,
                           index         =  index         ,
                           symbol        =  symbol        , 
                           pos           =  pos           ,
                           resi          =  resi          ,
                           resn          =  resn          ,
                           chain         =  chain         ,
                           atom_id       =  atom_id       , 
                           occupancy     = occupancy     ,
                           bfactor       = bfactor       ,
                           charge        = charge        ,
                           bonds_indexes = bonds_indexes ,
                           Vobject       = Vobject       ,
                           )
        
        if atom.symbol == 'H':
            pass
        else:
            self.noH_atoms.append(atom)
        
        
        if atom.chain in self.atoms_by_chains.keys():
            self.atoms_by_chains[atom.chain].append(atom)
        
        else:
            self.atoms_by_chains[atom.chain] = []
            self.atoms_by_chains[atom.chain].append(atom)

        
        
        
        
        if atom.chain in self.chains.keys():
            ch = self.chains[atom.chain]
        
        else:
            ch = Chain(name = atom.chain, label = 'UNK')
            self.chains[atom.chain] = ch
        
        
        '''This step checks if a residue has already been created and adds it to the respective chain.'''
        if len(ch.residues) == 0:
            residue = Residue(name=atom.resn, 
                             index=atom.resi, 
                             chain=atom.chain,
                             Vobject = self)
                                
            atom.residue     = residue
            residue.atoms.append(atom)
            
            #if residue in self.residues:
            #    pass
            #else:
            #    self.residues.append(residue)
            
            ch.residues.append(residue)
            ch.residues_by_index[atom.resi] = residue
        elif atom.resi == ch.residues[-1].resi:# and at_res_n == parser_resn:
            
            atom.residue = ch.residues[-1]
            ch.residues[-1].atoms.append(atom)

        else:
            residue = Residue(name=atom.resn, 
                             index=atom.resi, 
                             chain=atom.chain,
                             Vobject = self)
                                
            atom.residue     = residue
            residue.atoms.append(atom)
            
            #self.residues.append(residue)
            
            ch.residues.append(residue)
            ch.residues_by_index[atom.resi] = residue
            
            #'Checks whether RESN belongs to the solvent or protein'
            #---------------------------------------------------------
            if residue.isProtein:
                self.residues_in_protein.append(residue)
            
            elif residue.isSolvent:
                self.residues_in_solvent.append(residue)
            
            else:
                self.residues_ligands.append(residue)
                pass
            #---------------------------------------------------------

            #parser_resi  = atom.resi
            #parser_resn  = atom.resn


        if atom.name == 'CA':
            ch.backbone.append(atom)
        
        self.atoms.append(atom)
        
        #sum_x += atom.pos[0]
        #sum_y += atom.pos[1]
        #sum_z += atom.pos[2]
        
        self.vismol_session.atom_dic_id[self.vismol_session.atom_id_counter] = atom
        self.vismol_session.atom_id_counter +=1
    
    
    
  

    def _get_center_of_mass (self, frame = 0):
        """ Function doc """
        
        frame_size = len(self.frames)-1
        
        if frame <= frame_size:
            pass
        else:
            frame = frame_size
        

        #print (self.frames)

        
        
        #initial          = time.time()
        ##type 1
        #atoms = self.atoms
        #sum_x = 0.0 
        #sum_y = 0.0 
        #sum_z = 0.0 
        #if len(self.frames) == 0:
        #    #print ('if len(self.frames) == 0')
        #    pass
        #    #for atom in atoms:
        #    #    sum_x += atom.pos[0]
        #    #    sum_y += atom.pos[1]
        #    #    sum_z += atom.pos[2]
        #    
        #else:
        #    #print('for coord in self.frames[frame]')
        #    n = 0
        #    
        #    for coord in self.frames[frame]:
        #        if n == 0:
        #            sum_x += coord
        #        if n == 1:
        #            sum_y += coord
        #        if n == 2:
        #            sum_z += coord
        #        
        #        n += 1
        #
        #        if n == 3:
        #            n = 0
        #final          = time.time()
        #print('type1', initial -  final)
        #
        #total = len(atoms)        
        #self.mass_center = np.array([sum_x / total,
        #                             sum_y / total, 
        #                             sum_z / total])
        
        
        if len(self.noH_atoms) == 0:
            atoms = self.atoms
        else:
            atoms = self.noH_atoms
        
        sum_x = 0.0 
        sum_y = 0.0 
        sum_z = 0.0
        
        initial          = time.time()
        #type 2
        #atoms = self.noH_atoms
        if len(self.frames) == 0:
            pass
            
        else:
            for atom in atoms:
                coord = atom.coords (frame)
                sum_x += coord[0]
                sum_y += coord[1]
                sum_z += coord[2]
        final          = time.time()

        print('type2', initial -  final)



        total = len(atoms)        
        self.mass_center = np.array([sum_x / total,
                                     sum_y / total, 
                                     sum_z / total])

    
    
    def _generate_atomtree_structure (self, get_backbone_indexes = False):
        """ Function doc """
        
        print ('\ngenerate_chain_structure starting')
        initial          = time.time()
        #chains_m     = {}
        frame        = []
        
        self.atoms   = [] 

        
        for atom2 in self.atoms2:
            index       = atom2[0]
            at_name     = atom2[1]
            cov_rad     = atom2[2]
            at_pos      = atom2[3]
            at_res_i    = atom2[4]
            at_res_n    = atom2[5]
            at_ch       = atom2[6]
            at_symbol   = atom2[7]
            #bonds_idxes = atom2[8]
            #self._add_new_atom_to_vobj
            
            
            
            
            #'''
            self._add_new_atom_to_vobj(name          =  at_name,  
                                       index         =  index+1, 
                                       symbol        =  at_symbol, 
                                       pos           =  at_pos, 
                                       resi          =  at_res_i, 
                                       resn          =  at_res_n, 
                                       chain         =  at_ch, 
                                       atom_id       =  self.vismol_session.atom_id_counter  ,
                                       occupancy     = atom2[10],
                                       bfactor       = atom2[11],
                                       charge        = atom2[12],
                                       bonds_indexes = atom2[8],
                                       Vobject       =  self
                                        )
            #'''
        
        
        #self._get_center_of_mass()

        final = time.time() 
        print ('_generate_atomtree_structure end -  total time: ', final - initial, '\n')
        
        if get_backbone_indexes:
            self.get_backbone_indexes()
        else:
            pass
        
        
        for chain in self.chains.keys():
            self.residues += self.chains[chain].residues
        print('total number of residues at self.residues', len(self.residues))
        
        return True


    def _generate_color_vectors (self):
        """ Function doc 
        
        (1) This method assigns to each atom of the system a 
        unique identifier based on the RGB color standard. 
        This identifier will be used in the selection function. 
        There are no two atoms with the same color ID in  
        vismol.
        
        
        (2) This method builds the "colors" np array that will 
        be sent to the GPU and which contains the RGB values 
        for each atom of the system.
       
        """
        
        size       = len(self.atoms)
        half       = int(size/2)
        quarter    = int(size/4)
        color_step = 1.0/(size/4)
        red   = 0.0
        green = 0.0
        blue  = 1.0 
        print (size,half, quarter, color_step )
        
        
        
        
        self.color_indexes  = []
        self.colors         = []        
        self.color_rainbow  = []

        self.vdw_dot_sizes  = []
        self.cov_dot_sizes  = []
        
        counter = 0
        temp_counter = 0
        
        for atom in self.atoms:
            #-------------------------------------------------------
            # (1)                  ID Colors
            #-------------------------------------------------------
            '''
            i = atom.atom_id
            r = (i & 0x000000FF) >>  0
            g = (i & 0x0000FF00) >>  8
            b = (i & 0x00FF0000) >> 16
            '''
            
            '''
            self.color_indexes.append(r/255.0)
            self.color_indexes.append(g/255.0)
            self.color_indexes.append(b/255.0)
            '''
            
            self.color_indexes.append(atom.color_id[0])
            self.color_indexes.append(atom.color_id[1])
            self.color_indexes.append(atom.color_id[2])
            
            '''
            pickedID = r + g * 256 + b * 256*256
            atom.color_id = [r/255.0, g/255.0, b/255.0]
            #print (pickedID)
            self.vismol_session.atom_dic_id[pickedID] = atom
            '''
            #-------------------------------------------------------
            # (2)                   Colors
            #-------------------------------------------------------
            
            self.colors.append(atom.color[0])        
            self.colors.append(atom.color[1])        
            self.colors.append(atom.color[2])   

            #-------------------------------------------------------
            # (3)                  VdW list
            #-------------------------------------------------------
            self.vdw_dot_sizes.append(atom.vdw_rad*3)
            self.cov_dot_sizes.append(atom.cov_rad)
        
            #-------------------------------------------------------
            # (4)                Rainbow colors
            #-------------------------------------------------------
            if counter <= 1*quarter:
                self.color_rainbow.append(red   )
                self.color_rainbow.append(green )
                self.color_rainbow.append(blue  )
                
                green += color_step

            if counter >= 1*quarter  and counter <= 2*quarter:
                self.color_rainbow.append(red   )
                self.color_rainbow.append(green )
                self.color_rainbow.append(blue  )

                blue -= color_step

            if counter >= 2*quarter  and counter <= 3*quarter:
                
                self.color_rainbow.append(red   )
                self.color_rainbow.append(green )
                self.color_rainbow.append(blue  )

                red += color_step

            if counter >= 3*quarter  and counter <= 4*quarter:
                
                self.color_rainbow.append(red   )
                self.color_rainbow.append(green )
                self.color_rainbow.append(blue  )
                green -= color_step
            
            #print(red, green, blue,counter )
            counter += 1
            #-------------------------------------------------------

        self.color_indexes  = np.array(self.color_indexes, dtype=np.float32)
        self.colors         = np.array(self.colors       , dtype=np.float32)    
        self.vdw_dot_sizes  = np.array(self.vdw_dot_sizes, dtype=np.float32)
        self.cov_dot_sizes  = np.array(self.cov_dot_sizes, dtype=np.float32)
        self.colors_rainbow = np.array(self.color_rainbow, dtype=np.float32) 

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
        
        self.c_alpha_bonds = []
        
        self.c_alpha_atoms = []
        for chain in self.chains:
            for residue in self.chains[chain].residues:
                
                #print ('chain', chain ,'name', residue.resn, 'index',residue.resi)
                if residue.isProtein:
                    for atom in residue.atoms:
                        if atom.name == 'CA':
                            #print ('index',atom.index,'name', atom.name,'chain', atom.chain)
                            self.c_alpha_atoms.append(atom)
                        else:
                            pass
                else:
                    pass
        #pprint(self.residues)
        
        for n  in range(1, len(self.c_alpha_atoms)):

            atom_before  = self.c_alpha_atoms[n-1]
            resi_before  = atom_before.resi
            index_before = self.atoms.index(atom_before)
            
            atom   = self.c_alpha_atoms[n]
            resi   = atom.resi
            index  = self.atoms.index(atom)
            #print (index_before, 
            #       resi_before , 
            #       'chain', atom_before.chain ,
            #       'and',
            #       index , 
            #       resi, 
            #       'chain', atom.chain )
            
            if resi == resi_before + 1:
                #print ('bond: ',index_before, resi_before ,'and',index , resi )
                
                bond =  Bond( atom_i       = atom_before, 
                              atom_index_i = index_before,
                              atom_j       = atom        ,
                              atom_index_j = index       ,
                              )
                
                distance = bond.distance()
                if distance  >= 4.0:
                    pass
                else:
                    self.c_alpha_bonds.append(bond)

    def import_bonds (self, bonds_list = [] ):
        """ Function doc """
        #print (bonds_list)
        for raw_bond in bonds_list:
            index_i = raw_bond[0]
            index_j = raw_bond[1]
            
            #try:
            #    print(raw_bond,  self.atoms[index_i], self.atoms[index_j], len(self.atoms), bonds_list[-1])
            #except:
            #    print(raw_bond,  index_i, index_j, len(self.atoms), bonds_list[-1])

            #print(raw_bond, 
            #      self.atoms[index_i], 
            #      self.atoms[index_i].index-1,
            #      self.atoms[index_j],
            #      self.atoms[index_j].index-1,
            #)
            
            
            bond  =  Bond(atom_i       = self.atoms[index_i], 
                          atom_index_i = self.atoms[index_i].index-1,
                          atom_j       = self.atoms[index_j],
                          atom_index_j = self.atoms[index_j].index-1,
                          )
            
            '''
            print ('creating bond:', self.atoms[index_i].name,
                                     self.atoms[index_i].index, bond.atom_index_i,
                                     self.atoms[index_j].name,
                                     self.atoms[index_j].index, bond.atom_index_j)
            
            '''
            
            self.bonds.append(bond)
            
            self.atoms[index_i].bonds.append(bond)
            self.atoms[index_j].bonds.append(bond)
        
    def import_non_bonded_atoms_from_bond(self):
        """ Function doc """
            
        for atom in self.atoms:
            if atom.bonds == []:
                self.non_bonded_atoms.append(atom.index)
            else:
                pass
                

    def find_bonded_and_nonbonded_atoms(self, atoms):
        """ Function doc """
        #print(atoms)
        bonds_full_indexes, bonds_pair_of_indexes, NB_indexes_list = cdist.generete_full_NB_and_Bonded_lists(atoms)
        #print (bonds_full_indexes, bonds_pair_of_indexes)
        self.non_bonded_atoms  = NB_indexes_list
        
        self._generate_atomtree_structure()
        
        self._generate_color_vectors()
        
        self.index_bonds       = bonds_full_indexes
        
        self.import_bonds(bonds_pair_of_indexes)





