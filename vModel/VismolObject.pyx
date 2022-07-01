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

import glCore.vismol_font as vmf

from vModel.Atom              import Atom
from vModel.Chain             import Chain
from vModel.Residue           import Residue
from vModel.Bond              import Bond
from vModel.Representations   import LinesRepresentation
from vModel.Representations   import NonBondedRepresentation
from vModel.Representations   import SticksRepresentation
from vModel.Representations   import DotsRepresentation
from vModel.Representations   import SpheresRepresentation
from vModel.Representations   import GlumpyRepresentation
from vModel.Representations   import WiresRepresentation
from vModel.Representations   import RibbonsRepresentation
#from vModel.Representations   import SphereInstanceRepresentation

from vModel.MolecularProperties import COLOR_PALETTE

import vModel.cDistances as cdist


#class VismolGeometricObject:
#    """ Class doc """
#    
#    def __init__ (self, vm_session =  None):
#        """ Class initialiser """
#        self.vm_session = vm_session
#        
#        self.atoms              = []    # this a list  atom objects!
#        #-----------------------#
#        #         Bonds         #
#        #-----------------------#
#        self.index_bonds        = []
#        self.bonds              = [] 
#        self.frames             = []
#
#		#-----------------------------------------#
#		#      R E P R E S E N T A T I O N S      #
#        #-----------------------------------------#
#        self.representations = {
#                                'lines'     : None,
#                                }
#        
#        #-----------------------------------------------------------------    
#        self.model_mat = np.identity(4, dtype=np.float32)
#        self.trans_mat = np.identity(4, dtype=np.float32)
#        #-----------------------------------------------------------------
#    
#    def add_new_atom_list_to_vismol_geometric_object (self, atoms):
#        """ Function doc """
#        frame_number = self.vm_session.frame -1
#        #self.set_model_matrix(self.self.vm_session.glwidget.vm_widget.model_mat)
#        self.frames      = [] 
#        self.index_bonds = []
#        self.atoms       = atoms
#        frame            = []
#        
#        self.color_indexes  = []
#        self.colors         = []
#
#
#        atom1 = self.atoms[0]
#        atom2 = self.atoms[1]
#        atom3 = self.atoms[2]
#        atom4 = self.atoms[3]
#
#        #print(atom1)
#        #print(atom2)
#        #print(atom3)
#        #print(atom4)
#
#
#
#        if atom1 != None and atom2 != None:
#            frame.append(atom1.coords(frame_number))
#            frame.append(atom2.coords(frame_number))
#            self.index_bonds.append(0)
#            self.index_bonds.append(1)
#            
#            
#        if atom2 != None and atom3 != None:
#            frame.append(atom2.coords(frame_number))
#            frame.append(atom3.coords(frame_number))
#            self.index_bonds.append(1)
#            self.index_bonds.append(2)
#        
#        if atom3 != None and atom4 != None:
#            frame.append(atom2.coords(frame_number))
#            frame.append(atom3.coords(frame_number))
#            self.index_bonds.append(2)
#            self.index_bonds.append(3)
#
#        frame =  np.array(frame, dtype=np.float32)
#        self.frames = [frame]
#
#        self._generate_color_vectors()
#
#
#        
#        print (self.index_bonds)
#        if len(self.index_bonds)>= 2:
#            
#            rep  = LinesRepresentation (name = 'lines', active = True, _type = 'geo', vobject = self, glCore = self.vm_session.glwidget.vm_widget)
#            self.representations['lines'] = rep
#        else:
#            if self.representations['lines']:
#                self.representations['lines'].active =  False
#        #print(self.representations['lines'].active)
#
#    def set_model_matrix(self, mat):
#        """ Function doc
#        """
#        self.model_mat = np.copy(mat)
#        return True
#
#    def _generate_color_vectors (self):
#        """ Function doc 
#        
#        (1) This method assigns to each atom of the system a 
#        unique identifier based on the RGB color standard. 
#        This identifier will be used in the selection function. 
#        There are no two atoms with the same color ID in  
#        
#        
#        
#        (2) This method builds the "colors" np array that will 
#        be sent to the GPU and which contains the RGB values 
#        for each atom of the system.
#       
#        """
#        
#        size       = len(self.atoms)
#        half       = int(size/2)
#        quarter    = int(size/4)
#        color_step = 1.0/(size/4)
#        red   = 0.0
#        green = 0.0
#        blue  = 1.0 
#        #print (size,half, quarter, color_step )
#        
#        
#        
#        
#        self.color_indexes  = []
#        self.colors         = []        
#        self.color_rainbow  = []
#
#        self.vdw_dot_sizes  = []
#        self.cov_dot_sizes  = []
#        
#        counter = 0
#        temp_counter = 0
#        
#        for atom in self.atoms:
#            if atom:
#                #-------------------------------------------------------
#                # (1)                  ID Colors
#                #-------------------------------------------------------
#                '''
#                i = atom.atom_id
#                r = (i & 0x000000FF) >>  0
#                g = (i & 0x0000FF00) >>  8
#                b = (i & 0x00FF0000) >> 16
#                '''
#                
#                '''
#                self.color_indexes.append(r/255.0)
#                self.color_indexes.append(g/255.0)
#                self.color_indexes.append(b/255.0)
#                '''
#                
#                self.color_indexes.append(atom.color[0])
#                self.color_indexes.append(atom.color[1])
#                self.color_indexes.append(atom.color[2])
#                
#                '''
#                pickedID = r + g * 256 + b * 256*256
#                atom.color_id = [r/255.0, g/255.0, b/255.0]
#                #print (pickedID)
#                self.vm_session.atom_dic_id[pickedID] = atom
#                '''
#                #-------------------------------------------------------
#                # (2)                   Colors
#                #-------------------------------------------------------
#                
#                self.colors.append(atom.color[0])        
#                self.colors.append(atom.color[1])        
#                self.colors.append(atom.color[2])   
#
#                #-------------------------------------------------------
#                # (3)                  VdW list
#                #-------------------------------------------------------
#                self.vdw_dot_sizes.append(atom.vdw_rad*3)
#                self.cov_dot_sizes.append(atom.cov_rad)
#            
#                #-------------------------------------------------------
#                # (4)                Rainbow colors
#                #-------------------------------------------------------
#                if counter <= 1*quarter:
#                    self.color_rainbow.append(red   )
#                    self.color_rainbow.append(green )
#                    self.color_rainbow.append(blue  )
#                    
#                    green += color_step
#
#                if counter >= 1*quarter  and counter <= 2*quarter:
#                    self.color_rainbow.append(red   )
#                    self.color_rainbow.append(green )
#                    self.color_rainbow.append(blue  )
#
#                    blue -= color_step
#
#                if counter >= 2*quarter  and counter <= 3*quarter:
#                    
#                    self.color_rainbow.append(red   )
#                    self.color_rainbow.append(green )
#                    self.color_rainbow.append(blue  )
#
#                    red += color_step
#
#                if counter >= 3*quarter  and counter <= 4*quarter:
#                    
#                    self.color_rainbow.append(red   )
#                    self.color_rainbow.append(green )
#                    self.color_rainbow.append(blue  )
#                    green -= color_step
#                
#                ##print(red, green, blue,counter )
#                counter += 1
#                #-------------------------------------------------------
#
#        self.color_indexes  = np.array(self.color_indexes, dtype=np.float32)
#        self.colors         = np.array(self.colors       , dtype=np.float32)    
#        self.vdw_dot_sizes  = np.array(self.vdw_dot_sizes, dtype=np.float32)
#        self.cov_dot_sizes  = np.array(self.cov_dot_sizes, dtype=np.float32)
#        self.colors_rainbow = np.array(self.color_rainbow, dtype=np.float32) 
#
class VismolObject:
    """ Class doc 
    
    
    Visual Object contains the information necessary for openGL to draw 
    a model on the screen. Everything that is represented in the graphical 
    form is stored in the form of a VismolObject.
    
    Arguments
    
    name       = string  - Label that describes the object  
    atoms      = list of atoms  - [index, at_name, cov_rad,  at_pos, at_res_i, at_res_n, at_ch]
    vm_session  = Vismol Session - Necessary to build the "atomtree_structure"
                 vm_session contains the atom_id_counter (self.vm_session.atom_id_counter)
    
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
    self.atoms              = [Atom1, atom2, ...] <--- Atom objects (from vModel.Atom       import Atom)
    
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
                  active                         = False,
                  name                           = 'UNK', 
                  atoms                          = []   ,
                  vm_session                     = None , 
                  trajectory                     = None ,
                  trajectory_type                = 1    ,
                  bonds_pair_of_indexes          = None , 
                  color_palette                  = None , 
                  auto_find_bonded_and_nonbonded = True  
                  ):
        
        """ Class initialiser """
        #-----------------------------------------------------------------
        #                V I S M O L   a t t r i b u t e s
        #----------------------------------------------------------------- 
        self.vm_session    = vm_session     #
        self.index            = 0             # import to find vobject in self.vm_session.vobjects_dic
        self.active           = active        # for "show and hide"   enable/disable
        self.editing          = False         # for translate and rotate  xyz coords 
        self.Type             = 'molecule'    # Not used yet
        self.name             = name          # 
        self.vm_font          = vmf.VisMolFont()
        #self.color_pick_index = 0             #this is an integer num to access the color pick for carbon atoms (0 = green, 1 = purple, ...) 
        
        if color_palette:
            self.color_palette    = color_palette #this is an integer num to access the color pick for carbon atoms (0 = green, 1 = purple, ...) 
        else:
            self.color_palette = COLOR_PALETTE[0]
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
        self.chains             = {}    # A dictionary that connects the character (chain id) to the chain object 
        self.atoms_by_chains    = {}    # A dictionary, access key is the chain id that connects with list of atom objects     
        self.frames             = trajectory
        
        if trajectory_type == 2:
            self.trajectory_type = trajectory_type
            
            self.trajectory2D_xy_indexes = {}
            self.trajectory2D_f_indexes  = {}
            self.trajectory2D_x_size     = 0
            self.trajectory2D_y_size     = 0
        
        else:
            self.trajectory_type = 1
            
            
        self.cov_radiues_list   = []    # a list of covalent radius values for all  --> will be used to calculate de bonds
        self.atom_unique_id_dic = {}

        self.vobj_selected_atoms= []

        #-----------------------#
        #         Bonds         #
        #-----------------------#
        self.dynamic_bonds       = [] # Pair of atoms, something like: [0,1,1,2,3,4] 
        self.index_bonds        = [] # Pair of atoms, something like: [1, 3, 1, 17, 3, 4, 4, 20]
        self.index_metal_bonds  = []
        self.bonds              = [] # A list of bond-like objects                     

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
        self.non_bonded_atoms    = [] # A list of indexes
        self.metal_bonded_atoms  = [] # A list of indexes
        
        self.residues_in_protein = []
        self.residues_in_solvent = []
        self.residues_ligands    = []
        
        self.atoms_in_protein = [] # a list of atoms belonging to a protein
        self.atoms_in_solvent = []
        
        

		#-----------------------------------------#
		#      R E P R E S E N T A T I O N S      #
        #-----------------------------------------#
        self.representations = {'nonbonded'     : None,
                                'lines'         : None,
                                'dotted_lines'  : None,
                                'dots'          : None,
                                'spheres'       : None,
                                'sticks'        : None,
                                'dynamic_bonds' : None,
                                'ribbons'       : None,
                                'surface'       : None,
                                'wires'         : None,
                                'glumpy'        : None,
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
        
        
        
        
        if len(atoms) != 0:
            #self._generate_atomtree_structure_old()
            self._generate_atomtree_structure()
            self._generate_color_vectors()
        #else:
            #print("vobject's list of atoms is empty")
        
        
        
        '''
        This step is performed when no information about connections 
        between atoms is provided.
        '''
        if auto_find_bonded_and_nonbonded:
            # this used just when the vobject is initialized
            self._init_find_bonded_and_nonbonded_atoms(selection = self.atoms,
                                                       frame     = 0         , 
                                                       gridsize  = self.vm_session.vConfig.gl_parameters['gridsize'], 
                                                       maxbond   = self.vm_session.vConfig.gl_parameters['maxbond' ],
                                                       tolerance = self.vm_session.vConfig.gl_parameters['bond_tolerance'])

            '''the nonbonded attribute of the atom object concerns representation. 
            When true, I mean that the atom must be drawn with a small cross'''
            # you must assign the nonbonded attribute = True to atoms that are not bonded.
            for index in self.non_bonded_atoms:
                #print (index, self.atoms[index].name,  self.atoms[index].nonbonded)
                self.atoms[index].nonbonded = True
            self._get_center_of_mass()
              

        if bonds_pair_of_indexes:
            self.bonds_from_pair_of_indexes_list(bonds_pair_of_indexes)            
            if self.non_bonded_atoms == []:
                self.import_non_bonded_atoms_from_bond()
                    
        

    
    def _add_new_atom_to_vobj (self, atom):
        """ Function doc """       
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
                             vobject = self)
                                
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
                             vobject = self)
                                
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
        self.cov_radiues_list.append(atom.cov_rad)   
        #sum_x += atom.pos[0]
        #sum_y += atom.pos[1]
        #sum_z += atom.pos[2]
        
        self.vm_session.atom_dic_id[self.vm_session.atom_id_counter] = atom
        self.vm_session.atom_id_counter +=1
    
    
    def create_new_representation (self, rtype = 'lines', indexes = None):
        """ Function doc """
        #print('\n\n\n',indexes)
        if rtype == 'lines':
            
            self.representations['lines']      = LinesRepresentation (name = 'lines', 
                                                                    active = True, 
                                                                     _type = 'geo', 
                                                                   indexes = indexes, 
                                                                    vobject = self, 
                                                                    glCore = self.vm_session.glwidget.vm_widget)
        if rtype == 'nonbonded':

            self.representations['nonbonded']  = NonBondedRepresentation (name = 'nonbonded', 
                                                                active =  True, 
                                                                 _type = 'geo', 
                                                               indexes = indexes, 
                                                                vobject =  self, 
                                                                glCore = self.vm_session.glwidget.vm_widget)

        if rtype == 'dots':

            self.representations['dots']  = DotsRepresentation (name   = 'dots', 
                                                                active =  True, 
                                                                 _type = 'geo', 
                                                               indexes = indexes, 
                                                                vobject =  self, 
                                                                glCore = self.vm_session.glwidget.vm_widget)
        

        if rtype == 'sticks':

            self.representations['sticks']  = SticksRepresentation (name   = 'sticks', 
                                                                active =  True, 
                                                                 _type = 'geo', 
                                                               indexes = indexes, 
                                                                vobject =  self, 
                                                                glCore = self.vm_session.glwidget.vm_widget )               
        if rtype == 'ribbons':

            self.representations['ribbons']  = RibbonsRepresentation (name   = 'ribbons', 
                                                                active =  True, 
                                                                 _type = 'geo', 
                                                                vobject =  self, 
                                                                glCore = self.vm_session.glwidget.vm_widget )               
                                                                
        if rtype == 'spheres':

            self.representations['spheres'] =  SpheresRepresentation (name    = rtype, 
                                                                      active  = True, 
                                                                      _type   = 'mol', 
                                                                      vobject  = self,
                                                                      glCore  = self.vm_session.glwidget.vm_widget,
                                                                      indexes  = indexes
                                                                     )
                            
            #self.representations['spheres']._create_sphere_data()                                
        
        
        
        #if rtype == 'spheresInstace':
        #
        #    self.representations['spheres_instance'] =  SphereInstanceRepresentation (name    = rtype, 
        #                                                              active  = True, 
        #                                                              _type   = 'mol', 
        #                                                              vobject  = self,
        #                                                              glCore  = self.vm_session.glwidget.vm_widget,
        #                                                              indexes  = indexes
        #                                                             )
        #                    
            #self.representations['spheres_instance']._create_sphere_data()                                








        
        
        
        
        
        if rtype == 'dotted_lines':
            ##print('dotted_lines')
            self.representations['dotted_lines']  = LinesRepresentation (name = 'dotted_lines', 
                                                                       active =  True, 
                                                                        _type = 'geo', 
                                                                       vobject =  self, 
                                                                       glCore = self.vm_session.glwidget.vm_widget)
        
        
        
        
        
        #self.representations['lines'] = rep
  

    def _get_center_of_mass (self, frame = 0):
        """ Function doc """
        
        frame_size = len(self.frames)-1
        
        if frame <= frame_size:
            pass
        else:
            frame = frame_size
        
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

        #print('type2', initial -  final)



        total = len(atoms)        
        self.mass_center = np.array([sum_x / total,
                                     sum_y / total, 
                                     sum_z / total])

    
    def load_data_from_easyhybrid_serialization_file (self, d_atoms, frames, dynamic_bonds):
        """ Function doc """
        print ('\ngenerate_chain_structure (easyhybrid_serialization_file) starting')
        initial           = time.time()
                          
        self.frames       = frames
        self.atoms        = [] 
        self.dynamic_bonds = dynamic_bonds
        
        
        bonds_by_indexes = []
        for d_atom in d_atoms:
                        
            for bond in d_atom['bonds']:
                i = bond['atom_index_i']
                j = bond['atom_index_j']
                bonds_by_indexes.append([i,j])
            
            
            atom        = Atom(name          = d_atom['name']                      ,
                               index         = d_atom['index']                     ,
                               symbol        = d_atom['symbol']                    , 
                               resi          = d_atom['resi']                      ,
                               resn          = d_atom['resn']                      ,
                               chain         = d_atom['chain']                     ,
                               
                               atom_id       = self.vm_session.atom_id_counter  , 
                               
                               color         = d_atom['color']                     , 
                               
                               radius        = d_atom['radius'     ]               ,
                               vdw_rad       = d_atom['vdw_rad'    ]               ,
                               cov_rad       = d_atom['cov_rad'    ]               ,
                               ball_radius   = d_atom['ball_radius']               ,
                               
                               bonds_indexes = d_atom['bonds_indexes']             ,
                               occupancy     = d_atom['occupancy']                 ,
                               bfactor       = d_atom['bfactor']                   ,
                               charge        = d_atom['charge']                    ,
                               vobject       = self                                ,
                               )
            
            atom.selected       = d_atom['selected'] 
            atom.lines          = d_atom['lines'] 
            atom.dots           = d_atom['dots'] 
            atom.nonbonded      = d_atom['nonbonded'] 
            atom.ribbons        = d_atom['ribbons'] 
            atom.ball_and_stick = d_atom['ball_and_stick'] 
            atom.sticks         = d_atom['sticks'] 
            atom.spheres        = d_atom['spheres'] 
            atom.surface        = d_atom['surface'] 
            atom.bonds_indexes  = d_atom['bonds_indexes'] 
            atom.bonds          = d_atom['bonds'] 
            atom.isfree         = d_atom['isfree'] 

            self.vm_session.atom_dic_id[self.vm_session.atom_id_counter] = atom
            self._add_new_atom_to_vobj(atom)  
            
        
        self._generate_color_vectors()
        self.bonds_from_pair_of_indexes_list(bonds_by_indexes)            
        if self.non_bonded_atoms == []:
            self.import_non_bonded_atoms_from_bond()
        
        self.get_backbone_indexes()

        
        #self._get_center_of_mass()

        final = time.time() 
        print ('_generate_atomtree_structure (easyhybrid_serialization_file) end -  total time: ', final - initial, '\n')
        
        #if get_backbone_indexes:
        #    self.get_backbone_indexes()
        #else:
        #    pass
        



    def _generate_atomtree_structure (self, get_backbone_indexes = False):
        """ Function doc """
        
        print ('\ngenerate_chain_structure starting')
        initial          = time.time()
        frame            = []
        #self.atoms   = [None for x in self.atoms2] 
        self.atoms   = [] 

        for atom2 in self.atoms2:
            if 'color' in atom2.keys():
                pass
            else:
                atom2['color'] = []
            atom        = Atom(name          = atom2['name']                      ,
                               index         = atom2['index']+1                   ,
                               symbol        = atom2['symbol']                    , 
                               resi          = atom2['resi']                      ,
                               resn          = atom2['resn']                      ,
                               chain         = atom2['chain']                     ,
                               atom_id       = self.vm_session.atom_id_counter , 
                               occupancy     = atom2['occupancy']                 ,
                               bfactor       = atom2['bfactor']                   ,
                               charge        = atom2['charge']                    ,
                               color         = atom2['color']                     ,
                               vobject       = self                               ,
                               )
            self.vm_session.atom_dic_id[self.vm_session.atom_id_counter] = atom
            self._add_new_atom_to_vobj(atom)  
            
        
        self._get_center_of_mass()

        final = time.time() 
        print ('_generate_atomtree_structure end -  total time: ', final - initial, '\n')
        
        if get_backbone_indexes:
            self.get_backbone_indexes()
        else:
            pass
        
        
        for chain in self.chains.keys():
            self.residues += self.chains[chain].residues
        #print('total number of residues at self.residues', len(self.residues))
        return True






    def _generate_color_vectors (self, do_colors         = True,
                                       do_colors_idx     = True,
                                       do_colors_raindow = True,
                                       do_vdw_dot_sizes  = True,
                                       do_cov_dot_sizes  = True,
                                    ):
        """ Function doc 
        
        (1) This method assigns to each atom of the system a 
        unique identifier based on the RGB color standard. 
        This identifier will be used in the selection function. 
        There are no two atoms with the same color ID in  
        
        
        
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
        #print (size,half, quarter, color_step )
        
        
        
        if do_colors:
            self.colors         = []
        
        if do_colors_idx:
            self.color_indexes  = []
        
        if do_colors_raindow:
            self.color_rainbow  = []
        
        if do_vdw_dot_sizes:
            self.vdw_dot_sizes  = []
        
        if do_cov_dot_sizes:
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
            if do_colors_idx:
                self.color_indexes.append(atom.color_id[0])
                self.color_indexes.append(atom.color_id[1])
                self.color_indexes.append(atom.color_id[2])
            
            '''
            pickedID = r + g * 256 + b * 256*256
            atom.color_id = [r/255.0, g/255.0, b/255.0]
            #print (pickedID)
            self.vm_session.atom_dic_id[pickedID] = atom
            '''
            #-------------------------------------------------------
            # (2)                   Colors
            #-------------------------------------------------------
            if do_colors:
                self.colors.append(atom.color[0])        
                self.colors.append(atom.color[1])        
                self.colors.append(atom.color[2])   

            #-------------------------------------------------------
            # (3)                  VdW list / cov_dot_sizes:
            #-------------------------------------------------------
            if do_vdw_dot_sizes: 
                self.vdw_dot_sizes.append(atom.vdw_rad*3)

            if do_cov_dot_sizes: 
                self.cov_dot_sizes.append(atom.cov_rad)
        
            #-------------------------------------------------------
            # (4)                Rainbow colors
            #-------------------------------------------------------
            if do_colors_raindow:
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
                
            ##print(red, green, blue,counter )
            counter += 1
            #-------------------------------------------------------


        if do_colors:
            self.colors         = np.array(self.colors       , dtype=np.float32)
        
        if do_colors_idx:
            self.color_indexes  = np.array(self.color_indexes, dtype=np.float32)
        
        if do_colors_raindow:
            self.colors_rainbow = np.array(self.color_rainbow, dtype=np.float32)
        
        if do_vdw_dot_sizes:
            self.vdw_dot_sizes  = np.array(self.vdw_dot_sizes, dtype=np.float32)
        
        if do_cov_dot_sizes:
            self.cov_dot_sizes  = np.array(self.cov_dot_sizes, dtype=np.float32)
        
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
        #p#print(self.residues)
        
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

    def bonds_from_pair_of_indexes_list (self, bonds_list = [] ):
        """ Function doc 
        bonds_list = [[0,1] , [0,4] , [1,3], ...]
        
        """
        
        #print (bonds_list)
        for i in range(0,len(bonds_list)-1,2):
            
            
            index_i = bonds_list[i]
            index_j = bonds_list[i+1]
            
            bond  =  Bond(atom_i       = self.atoms[index_i], 
                          atom_index_i = self.atoms[index_i].index-1,
                          atom_j       = self.atoms[index_j],
                          atom_index_j = self.atoms[index_j].index-1,
                          )

            
            
            if self.atoms[index_i].is_metal or self.atoms[index_j].is_metal:
                self.index_metal_bonds.append(index_i)
                self.index_metal_bonds.append(index_j)
                
                if self.atoms[index_i].is_metal:
                    #self.atoms[index_i].dotted_lines = True
                    self.atoms[index_i].lines        = False
                    self.non_bonded_atoms.append(index_i)
                    self.metal_bonded_atoms.append(index_i)
                
                if self.atoms[index_j].is_metal:
                    #self.atoms[index_j].dotted_lines = True
                    self.atoms[index_j].lines        = False
                    self.non_bonded_atoms.append(index_j)
                    self.metal_bonded_atoms.append(index_j)
                
                bond.has_metal = True
                #self.index_bonds.append(index_i)
                #self.index_bonds.append(index_j)
            
            else:
                self.index_bonds.append(index_i)
                self.index_bonds.append(index_j)
                bond.has_metal = False
                
            self.bonds.append(bond)
            self.atoms[index_i].bonds.append(bond)
            self.atoms[index_j].bonds.append(bond)
            
            
        
        self.index_bonds = np.array(self.index_bonds, dtype=np.uint32)
        
        '''
        #print (bonds_list)
        for raw_bond in bonds_list:
            index_i = raw_bond[0]
            index_j = raw_bond[1]
            
            bond  =  Bond(atom_i       = self.atoms[index_i], 
                          atom_index_i = self.atoms[index_i].index-1,
                          atom_j       = self.atoms[index_j],
                          atom_index_j = self.atoms[index_j].index-1,
                          )

            self.bonds.append(bond)
            
            self.index_bonds.append(index_i)
            self.index_bonds.append(index_j)
            
            self.atoms[index_i].bonds.append(bond)
            self.atoms[index_j].bonds.append(bond)
            
            
        
        self.index_bonds = np.array(self.index_bonds, dtype=np.uint32)
        '''
        
    def import_non_bonded_atoms_from_bond(self, selection = None):
        """ Function doc """
        if selection == None:
            selection = self.atoms
        
        self.non_bonded_atoms = []
        
        for atom in selection:
            
            if len(atom.bonds) == 0:
                atom.nonbonded = True
                self.non_bonded_atoms.append(atom.index-1)
            
            else:
                atom.nonbonded = False
                pass
            
    def find_dynamic_bonds (self, atom_list = None, index_list = None, update = True ):
        """ Function doc """
        initial       = time.time()
        if atom_list == None:
            atom_list = []
            for index in index_list:
                atom_list.append(self.atoms[index])
        
        
        if update:
            nframes   =  len(self.frames)      # current number of frames
            ndynBonds = len(self.dynamic_bonds) # current number of dynamic bonds
        
        else:
            nframes   =  len(self.frames)      # current number of frames
            ndynBonds =  0 
            
        
        self.dynamic_bonds = []
        
        for i in range (0, len(self.frames)):
            indexes = []
            bonds_by_pairs = self.find_bonded_and_nonbonded_by_selection(selection = atom_list, 
                                                                                frame = i,  
                                                                             gridsize = self.vm_session.vConfig.gl_parameters['gridsize'],
                                                                            tolerance = self.vm_session.vConfig.gl_parameters['bond_tolerance'])
            indexes = np.array(bonds_by_pairs,dtype=np.uint32)
            self.dynamic_bonds.append(indexes)        
        final = time.time()   
        print ('Bonds calcultation time : ', final - initial, '\n')  
        
        

    def find_bonded_and_nonbonded_by_selection (self, selection = None, frame = 0, gridsize = 1.4 , tolerance = 1.4, maxbond = 2.6):
        """ Function doc """
        if selection == None:
            selection = self.atoms
        else:
            pass
        
        
        '''
        initial       = time.time()
        atomic_grid = self._build_the_atomic_grid(selection, gridsize, frame)
        final1 = time.time()
        bonds_pair_of_indexes = self.get_atomic_bonds_from_atomic_grids( atomic_grid, gridsize, maxbond, tolerance, frame)
        final2 = time.time()
        '''
        atoms_list   = []
        indexes      = []
        cov_rad      = np.array(self.cov_radiues_list, dtype=np.float32)
        coords       = self.frames[frame]
        gridpos_list = []
        
        for atom in selection:
            indexes.append(atom.index -1)
            gridpos_list.append(atom.get_grid_position (gridsize = gridsize, frame = frame))
    
        bonds_pair_of_indexes = cdist.ctype_get_atomic_bonds_from_atomic_grids(indexes, coords , cov_rad, gridpos_list, gridsize, maxbond)
        #bonds_pair_of_indexes = cdist.ctype_get_atomic_bonds_from_atomic_grids_parallel(indexes, coords , cov_rad, gridpos_list, gridsize)
        return  bonds_pair_of_indexes 



    def _init_find_bonded_and_nonbonded_atoms(self, selection = None, frame = 0, gridsize = 1.33, maxbond =  2.66, tolerance = 1.4, log = True):
        """ Function doc """
        initial       = time.time()
        final1 = time.time()
        bonds_pair_of_indexes = self.find_bonded_and_nonbonded_by_selection( selection = None, frame = 0, gridsize = gridsize, tolerance = 1.0, maxbond = maxbond)
        #print(bonds_pair_of_indexes)
        final2 = time.time()        
        
        if log:
            
            print ('building grid elements  : ', final1 - initial, '\n')#
            #--------------------------------------------------------------#
            #print (non_bonded_list)
            print ('Total number of Atoms   :', len(selection)             )
            #print ('Number of grid elements :', len(atomic_grid)           )
            
            print('gridsize'  ,gridsize)
            #print('maxbond'   ,maxbond)
            #print('borderGrid',  maxbond/gridsize)


            print ('Bonds                   :', len(bonds_pair_of_indexes))
            print ('Bonds calcultation time : ', final2 - initial, '\n')   #
            #--------------------------------------------------------------#
        
        '''
        bonds_pair_of_indexes = self.find_bonded_and_nonbonded_by_selection (selection = None, 
                                                                             frame     = frame, 
                                                                             gridsize  = gridsize, 
                                                                             maxbond   = maxbond, 
                                                                             log       = True)
        #print(bonds_pair_of_indexes)
        
        '''
        self.bonds_from_pair_of_indexes_list(bonds_pair_of_indexes)
        self.import_non_bonded_atoms_from_bond()
        
        
        #'''
        ## return  bonds_full_indexes, NB_indexes_list









