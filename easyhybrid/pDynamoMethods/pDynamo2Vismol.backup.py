#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Lembrar de colocar uma header nesse arquivo

##############################################################
#-----------------...EasyHybrid 3.0...-----------------------#
#-----------Credits and other information here---------------#
##############################################################

import glob, math, os, os.path, sys
import numpy as np
VISMOL_HOME = os.environ.get('VISMOL_HOME')
#path fo the core python files on your machine
sys.path.append(os.path.join(VISMOL_HOME,"easyhybrid/pDynamoMethods"))
#---------------------------------------
from pBabel                    import*                                     
from pCore                     import*  
#---------------------------------------
from pMolecule                 import*                              
from pMolecule.MMModel         import*
from pMolecule.NBModel         import*                                     
from pMolecule.QCModel         import*
#---------------------------------------
from pScientific               import*                                     
from pScientific.Arrays        import*                                     
from pScientific.Geometry3     import*                                     
from pScientific.RandomNumbers import*                                     
from pScientific.Statistics    import*
from pScientific.Symmetry      import*
#---------------------------------------                              
from pSimulation               import*
#---------------------------------------
#import our core lib
from SimulationsPreset import Simulation 


'''from easyhybrid.pDynamoMethods.SimulationsPreset import Simulation '''


#---------------------------------------
from vModel import VismolObject
from vModel.MolecularProperties import ATOM_TYPES_BY_ATOMICNUMBER
from vModel.MolecularProperties import COLOR_PALETTE

HOME = os.environ.get('HOME')

#==========================================================================
def get_atom_coords_from_pdynamo_system (system, atom, frame = None):
    '''
    Function to obtain the coordinates from a given atom of a System instance.
    '''

    if frame:
        xyz = system.coordinates3[atom.index]
        ##print(atom.index, atom.label, atom.atomicNumber, atom.connections, xyz[0], xyz[1], xyz[2] )
        frame.append(float(xyz[0]))
        frame.append(float(xyz[1]))
        frame.append(float(xyz[2]))
    return frame

#==========================================================================
def get_atom_info_from_pdynamo_atom_obj (atom, sequence):
    """
    It extracts the information from the atom object, 
    belonging to pdynamo, and organizes it in the form 
    of a list that will be delivered later to build the 
    vismolObj
    
    """
    
    entityLabel = atom.parent.parent.label
    useSegmentEntityLabels = False
    if useSegmentEntityLabels:
        chainID = ""
        segID   = entityLabel[0:4]
    else:
        chainID = entityLabel[0:1]
        segID   = ""

    

    resName, resSeq, iCode = sequence.ParseLabel ( atom.parent.label, fields = 3 )
    #print(atom.index, atom.label,resName, resSeq, iCode,chainID, segID,  atom.atomicNumber, atom.connections)#, xyz[0], xyz[1], xyz[2] )
    index        = atom.index
    at_name      = atom.label
    #at_pos       = np.array([float( xyz[0]), float(xyz[1]), float(xyz[2])])
    at_pos       = np.array([float(0), float(0), float(0)])
    at_resi      = int(resSeq)
    at_resn      = resName
    at_ch        = chainID
    at_symbol    = ATOM_TYPES_BY_ATOMICNUMBER[atom.atomicNumber] # at.get_symbol(at_name)
    cov_rad      = at.get_cov_rad (at_symbol)

    gridpos      = [int(at_pos[0]/gridsize), int(at_pos[1]/gridsize), int(at_pos[2]/gridsize)]
    at_occup     = 0.0
    at_bfactor   = 0.0
    at_charge    = 0.0
    
    return [index, at_name, cov_rad,  at_pos, at_resi, at_resn, at_ch, at_symbol, [], gridpos, at_occup, at_bfactor, at_charge ]

#==========================================================================
def load_pDynamo_system_from_file (filein,  gridsize = 3, vm_session =  None, frames_only = False):
    """ Function doc """
    at  =  vm_session.vConfig.atom_types
    
    system = ImportSystem (  filein  )
    system.BondsFromCoordinates3()
    #self.system.Summary ( )
    bonds = system.connectivity.bondIndices


    # . Get the sequence.
    sequence = getattr ( system, "sequence", None )
    if sequence is None: sequence = Sequence.FromAtoms ( system.atoms, componentLabel = "UNK.1" )
    #print (sequence)
    
    atoms           = []
    frames          = []
    
    frame = []
    for atom in system.atoms.items:
        
        frame = get_atom_coords_from_pdynamo_system (system, atom, frame)
        atoms.append(get_atom_info_from_pdynamo_atom_obj(atom, sequence))
        '''
        xyz = system.coordinates3[atom.index]
        ##print(atom.index, atom.label, atom.atomicNumber, atom.connections, xyz[0], xyz[1], xyz[2] )
        frame.append(float(xyz[0]))
        frame.append(float(xyz[1]))
        frame.append(float(xyz[2]))        
        
        entityLabel = atom.parent.parent.label
        useSegmentEntityLabels = False
        if useSegmentEntityLabels:
            chainID = ""
            segID   = entityLabel[0:4]
        else:
            chainID = entityLabel[0:1]
            segID   = ""        

        resName, resSeq, iCode = sequence.ParseLabel ( atom.parent.label, fields = 3 )
        #print(atom.index, atom.label,resName, resSeq, iCode,chainID, segID,  atom.atomicNumber, atom.connections, xyz[0], xyz[1], xyz[2] )
        index        = atom.index
        at_name      = atom.label
        at_pos       = np.array([float( xyz[0]), float(xyz[1]), float(xyz[2])])
        at_resi      = int(resSeq)
        at_resn      = resName
        at_ch        = chainID
        at_symbol    = vm_session.vConfig.ATOM_TYPES_BY_ATOMICNUMBER[atom.atomicNumber] # at.get_symbol(at_name)
        cov_rad      = at.get_cov_rad (at_symbol)

        gridpos      = [int(at_pos[0]/gridsize), int(at_pos[1]/gridsize), int(at_pos[2]/gridsize)]
        at_occup     = 0.0
        at_bfactor   = 0.0
        at_charge    = 0.0

        
        atoms.append([index, at_name, cov_rad,  at_pos, at_resi, at_resn, at_ch, at_symbol, [], gridpos, at_occup, at_bfactor, at_charge ])
        '''
        
    frame = np.array(frame, dtype=np.float32)
    name  = os.path.basename(filein)
    
    vobject  = VismolObject.VismolObject(name                           = name          ,    
                                               atoms                          = atoms         ,    
                                               vm_session                  = vm_session ,    
                                               bonds_pair_of_indexes          = bonds         ,    
                                               trajectory                     = [frame]       ,    
                                               auto_find_bonded_and_nonbonded = False         )

    return vobject


#+====================================================================================
class pDynamoSession:
    """ Class doc """
    
    def __init__ (self, vm_session = None):
        """ Class initialiser """
        self.vm_session  = vm_session
        self.name           = 'pDynamo_session'
        
        self.nbModel_default         = NBModelCutOff.WithDefaults ( )
        self.fixed_color             = [0.5, 0.5, 0.5]
        self.pdynamo_distance_safety = 0.5
        
        '''self.active_id is the attribute that tells which 
        system is active for calculations in pdynamo 
        (always an integer value)'''
        self.active_id       = 0
        
        
        '''Now we can open more than one pdynamo system. 
        Each new system loaded into memory is stored in 
        the form of a dictionary, which has an int as 
        an access key.'''
        self.systems =  {
                         0:None
                         }
        
        #self.systems_list = []
        self.counter      = 0
        self.color_palette_counter = 0

        
        
    def load_a_new_pDynamo_system_from_dict (self, filesin = {}, systype = 0, name = None):
        """ Function doc """
        
        
        '''Every new system is added in the form of a 
        dict, which contains the items:'''
        psystem = {
                  'id'            : 0    ,  # access number (same as the access key in the self.systems dictionary)
                  'name'          : None ,
                  'system'        : None ,  # pdynamo system
                  
                  'vobject' : None ,  # Vismol object associated with the system -> is the object that will 
                                            # undergo changes when something new is requested by the interface, for example: show the QC region
                  'active'        : False, 
                  'bonds'         : None ,
                  'sequence'      : None ,
                  'qc_table'      : None ,
                  'color_palette' : None , # will be replaced by a dict
                  'fixed_table'   : []   ,
                  'working_folder': HOME , 
                   }
        
        
        if systype == 0:
            system              = ImportSystem       ( filesin['amber_prmtop'] )
            system.coordinates3 = ImportCoordinates3 ( filesin['coordinates'] )
            self.define_NBModel(_type = 1, system = system)

            
        if systype == 1:
            parameters          = CHARMMParameterFileReader.PathsToParameters (filesin['charmm_par'])
            system              = ImportSystem       ( filesin['charmm_psf'] , isXPLOR = True, parameters = parameters )
            system.coordinates3 = ImportCoordinates3 ( filesin['coordinates'] )
            self.define_NBModel(_type = 1, system = system)

        
        
        if systype == 2:
            mmModel        = MMModelOPLS.WithParameterSet ( filesin['opls_folder'] )            
            system         = ImportSystem       ( filesin['coordinates'])
            system.DefineMMModel ( mmModel )
            self.define_NBModel(_type = 1, system = system)


                
        if systype == 3:
            system = ImportSystem (filesin['coordinates'])
            system.Summary()
            print ('mmModel',system.mmModel)
            print ('qcModel',system.qcModel)
            print ('nbModel',system.nbModel)

        
        
        if name:
            pass
        else:
            name = system.label
        #'''
        psystem['system']        =  system
        psystem['name']          =  name
        print('color_palette', self.color_palette_counter)
        psystem['color_palette'] =  COLOR_PALETTE[self.color_palette_counter]
        #'''

        #self.name  =  name
        self.append_system_to_pdynamo_session(psystem)
        


    def append_system_to_pdynamo_session (self, psystem):
        """ Function doc """
        psystem['id']               = self.counter
        self.systems[psystem['id']] = psystem 
        
        #self.systems_list.append(psystem)
        self.active_id   = self.counter  
        self.counter    += 1

        if self.color_palette_counter >= len(COLOR_PALETTE)-1:
            self.color_palette_counter = 0
        else:
            self.color_palette_counter += 1
            
        self.build_vobject_from_pDynamo_system (name = 'initial coordinates' )#psystem['system'].label)
        
    def get_bonds_from_pDynamo_system(self, safety = 0.5, id_system = False):
        self.systems[self.active_id]['system'].BondsFromCoordinates3(safety = safety)
        
        raw_bonds =self.systems[self.active_id]['system'].connectivity.bondIndices
        bonds = []
        for bond in raw_bonds:
            bonds.append(bond[0])
            bonds.append(bond[1])
        
        self.systems[self.active_id]['bonds'] = bonds #self.systems[self.active_id]['system'].connectivity.bondIndices
        return True
        
    def define_NBModel (self, _type = 1 , parameters =  None, system = None):
        """ Function doc """
        
        if _type == 0:
            self.nbModel = NBModelFull.WithDefaults ( )
        
        elif _type == 1:
            self.nbModel = NBModelCutOff.WithDefaults ( )
        
        elif _type == 2:
            self.nbModel = NBModelORCA.WithDefaults ( )
        
        elif _type == 3:
            self.nbModel = NBModelDFTB.WithDefaults ( )
        
        if system:
            system.DefineNBModel ( self.nbModel )
            system.Summary ( )
        else:
            self.systems[self.active_id]['system'].DefineNBModel ( self.nbModel )
            self.systems[self.active_id]['system'].Summary ( )
        
        return True

    def define_free_or_fixed_atoms_from_iterable (self, fixedlist = None):
        """ Function doc """
        if fixedlist == []:
            self.systems[self.active_id]['fixed_table'] = []
            self.systems[self.active_id]['system'].freeAtoms = None
            #self.refresh_qc_and_fixed_representations()

        else:
            selection_fixed                             = Selection.FromIterable (fixedlist)
            self.systems[self.active_id]['fixed_table'] = list(selection_fixed)
            selection_free                              = selection_fixed.Complement( upperBound = len (self.systems[self.active_id]['system'].atoms ) )
        
            self.systems[self.active_id]['system'].freeAtoms = selection_free
            #self.refresh_qc_and_fixed_representations()

        self.refresh_qc_and_fixed_representations()
        return True

    def define_a_new_QCModel (self, parameters = None):
        """ Function doc """
        
        #print(parameters)
        
        electronicState = ElectronicState.WithOptions ( charge = parameters['charge'], multiplicity = parameters['multiplicity'])
        self.systems[self.active_id]['system'].electronicState = electronicState

        qcModel         = QCModelMNDO.WithOptions ( hamiltonian = parameters['method'])
        

        
        if self.systems[self.active_id]['qc_table'] :
            self.systems[self.active_id]['system'].DefineQCModel (qcModel, qcSelection = Selection.FromIterable ( self.systems[self.active_id]['qc_table']) )
            self.refresh_qc_and_fixed_representations()
            
            #print('define NBModel = ', self.nbModel)
            self.systems[self.active_id]['system'].DefineNBModel ( NBModelCutOff.WithDefaults ( ) )
        
        else:
            self.systems[self.active_id]['system'].DefineQCModel (qcModel)
            self.refresh_qc_and_fixed_representations()

    def refresh_qc_and_fixed_representations (self):
        """ Function doc >>> 
        list(molecule.qcState.boundaryAtoms) 
        list(molecule.qcState.pureQCAtoms)  self.systems[self.active_id]['system'].eh_qc_table ) )
        list(molecule.qcState.qcAtoms)
        """
        #if self.selection_fixed_table:
        print('\n\n\nselection_fixed_table', self.systems[self.active_id]['fixed_table'])
        



        '''
        This loop is assigning the color of the fixed atoms to all objects 
        belonging to the pdynamo project that is active. 
        '''
        for key, vobject in self.vm_session.vobjects_dic.items():
            print(vobject.name, vobject.easyhybrid_system_id, vobject.active)
            
            if vobject.easyhybrid_system_id == self.active_id:
               
                self.vm_session.set_color_by_index(vobject = vobject , 
                                                      indexes       = self.systems[self.active_id]['fixed_table'], 
                                                      color         = self.fixed_color)






        #self.vm_session.set_color_by_index(vobject = self.systems[self.active_id]['vobject'] , 
        #                                      indexes       = self.systems[self.active_id]['fixed_table']   , 
        #                                      color         = self.fixed_color)
        
        if self.systems[self.active_id]['system'].qcModel:

            self.systems[self.active_id]['qc_table'] = list(self.systems[self.active_id]['system'].qcState.pureQCAtoms)
            #boundaryAtoms     = list(self.system.qcState.boundaryAtoms)
            
            vobject = self.systems[self.active_id]['vobject']
            
            # Here we have to hide all the sticks and spheres so that there is no confusion in the representation of the QC region
            self.vm_session.selections[self.vm_session.current_selection].selecting_by_indexes (vobject = vobject, indexes = range(0, len(vobject.atoms)))
            self.vm_session.show_or_hide_by_object (_type = 'spheres',  vobject = vobject, selection_table = range(0, len(vobject.atoms)),  show = False )
            self.vm_session.show_or_hide_by_object (_type = 'sticks',   vobject = vobject, selection_table = range(0, len(vobject.atoms)),  show = False )
            
            self.vm_session.selections[self.vm_session.current_selection].unselecting_by_indexes (vobject = vobject, indexes = range(0, len(vobject.atoms)))
            
            self.vm_session.selections[self.vm_session.current_selection].selecting_by_indexes (vobject = vobject, indexes = self.systems[self.active_id]['qc_table'])
            ##print('\n\n',self.vm_session.selections[self.vm_session.current_selection].selected_atoms)
            
            self.vm_session.show_or_hide_by_object (_type = 'spheres', vobject = vobject, selection_table = self.systems[self.active_id]['qc_table'] , show = True )
            self.vm_session.show_or_hide_by_object (_type = 'sticks' , vobject = vobject, selection_table = self.systems[self.active_id]['qc_table'] , show = True )
            self.vm_session.selections[self.vm_session.current_selection].unselecting_by_indexes (vobject = vobject, indexes = range(0, len(vobject.atoms)))
            ##print('\n\n',self.vm_session.selections[self.vm_session.current_selection].selected_atoms)

        else:
            pass

    def merge_systems (self, system1 = None, system2 =  None, label = 'Merged System', summary = True):
        """ Function doc """
        system  = MergeByAtom ( system1, system2 )
        system.label = label
        self.define_NBModel(_type = 1, system = system)
        #system.define_NBModel( self.nbModel )
        
        if summary:
            system.Summary ( )
        
        
        psystem = {
                  'id'            : 0      ,  # access number (same as the access key in the self.systems dictionary)
                  'name'          : label  ,
                  'system'        : system ,  # pdynamo system
                  
                  'vobject' : None ,  # Vismol object associated with the system -> is the object that will 
                                            # undergo changes when something new is requested by the interface, for example: show the QC region
                  'active'        : False, 
                  'bonds'         : None ,
                  'sequence'      : None ,
                  'qc_table'      : None ,
                  'color_palette' : None , # will be replaced by a dict
                  'fixed_table'   : []   ,
                   }
        
        
        self.append_system_to_pdynamo_session (psystem)
        
    def prune_system (self, selection = None, label = 'Pruned System', summary = True):
        """ Function doc """
        p_selection   = Selection.FromIterable ( selection )
        system        = PruneByAtom ( self.systems[self.active_id]['system'], p_selection )
        self.define_NBModel(_type = 1, system = system)
        system.label  = label        
        if summary:
            system.Summary ( )
            
            
        psystem = {
                  'id'            : 0      ,  # access number (same as the access key in the self.systems dictionary)
                  'name'          : label  ,
                  'system'        : system ,  # pdynamo system
                  
                  'vobject' : None ,  # Vismol object associated with the system -> is the object that will 
                                            # undergo changes when something new is requested by the interface, for example: show the QC region
                  'active'        : False, 
                  'bonds'         : None ,
                  'sequence'      : None ,
                  'qc_table'      : None ,
                  'color_palette' : None , # will be replaced by a dict
                  'fixed_table'   : []   ,
                   }
            
            
            
        self.append_system_to_pdynamo_session (psystem)

    
    def get_sequence_from_pDynamo_system (self):
        """ Function doc """
        
        self.systems[self.active_id]['sequence'] = getattr ( self.systems[self.active_id]['system'], "sequence", None )
        if  self.systems[self.active_id]['sequence'] is None: 
            self.systems[self.active_id]['sequence'] = Sequence.FromAtoms ( self.systems[self.active_id]['system'].atoms, 
                                                                                              componentLabel = "UNK.1" )
        return True

    def get_atom_coords_from_pdynamo_system (self, system = None,  atom = None):

        xyz = self.systems[self.active_id]['system'].coordinates3[atom.index]
        return [float(xyz[0]),float(xyz[1]), float(xyz[2])]

    def get_atom_info_from_pdynamo_atom_obj (self, system = None, atom = None):
        """
        It extracts the information from the atom object, 
        belonging to pdynamo, and organizes it in the form 
        of a list that will be delivered later to build the 
        vismolObj
        
        """

        entityLabel = atom.parent.parent.label
        useSegmentEntityLabels = False
        if useSegmentEntityLabels:
            chainID = ""
            segID   = entityLabel[0:4]
        else:
            chainID = entityLabel[0:1]
            segID   = ""

        

        resName, resSeq, iCode = self.systems[self.active_id]['sequence'].ParseLabel ( atom.parent.label, fields = 3 )
        ##print(atom.index, atom.label,resName, resSeq, iCode,chainID, segID,  atom.atomicNumber, atom.connections)#, xyz[0], xyz[1], xyz[2] )
        
        index        = atom.index
        at_name      = atom.label
        at_resi      = int(resSeq)
        at_resn      = resName
        at_ch        = chainID
        at_symbol    = ATOM_TYPES_BY_ATOMICNUMBER[atom.atomicNumber] # at.get_symbol(at_name)
        at_occup     = 0.0
        at_bfactor   = 0.0
        at_charge    = 0.0
        atom         = {
              'index'      : index      , 
              'name'       : at_name    , 
              'resi'       : at_resi    , 
              'resn'       : at_resn    , 
              'chain'      : at_ch      , 
              'symbol'     : at_symbol  , 
              'occupancy'  : at_occup   , 
              'bfactor'    : at_bfactor , 
              'charge'     : at_charge   
              }
        
        return atom
 
    def build_vobject_from_pDynamo_system (self                       , 
                                                 name = 'a_new_vismol_obj'  ,
                                                 system               = None,
                                                 vobject_active = True,
                                                 autocenter = True          ,):
        """ Function doc """
        self.get_bonds_from_pDynamo_system(safety = self.pdynamo_distance_safety)
        self.get_sequence_from_pDynamo_system()
        frames = []

        atoms = []     
        frame = []
        
        for atom in self.systems[self.active_id]['system'].atoms.items:
            xyz = self.get_atom_coords_from_pdynamo_system (atom   = atom)
            frame.append(xyz[0])
            frame.append(xyz[1])
            frame.append(xyz[2])
            
            atoms.append(self.get_atom_info_from_pdynamo_atom_obj(atom   = atom))
        

        
        frame = np.array(frame, dtype=np.float32)
        name  = os.path.basename(name)
        
        vobject  = VismolObject.VismolObject(name                           = name                                          ,    
                                                   atoms                          = atoms                                         ,    
                                                   vm_session                  = self.vm_session                            ,    
                                                   bonds_pair_of_indexes          = self.systems[self.active_id]['bonds']         ,    
                                                   trajectory                     = [frame]                                       ,  
                                                   color_palette                  = self.systems[self.active_id]['color_palette'] ,
                                                   auto_find_bonded_and_nonbonded = False               )
        
        vobject.easyhybrid_system_id = self.systems[self.active_id]['id']
        vobject.set_model_matrix(self.vm_session.glwidget.vm_widget.model_mat)
        vobject.active = vobject_active
        vobject._get_center_of_mass(frame = 0)
        
        if self.systems[self.active_id]['system'].qcModel:
            sum_x = 0.0 
            sum_y = 0.0 
            sum_z = 0.0
            
            self.systems[self.active_id]['qc_table'] = list(self.systems[self.active_id]['system'].qcState.pureQCAtoms)
            total = 0
            
            for atom_index in self.systems[self.active_id]['qc_table']:
                atom = vobject.atoms[atom_index]
                
                coord = atom.coords (frame = 0)
                sum_x += coord[0]
                sum_y += coord[1]
                sum_z += coord[2]
                total+=1
                
                    
            center = np.array([sum_x / total,
                               sum_y / total, 
                               sum_z / total])
            
        else:
            center = vobject.mass_center

        self.systems[self.active_id]['vobject'] = vobject
        self.vm_session.add_vobject_to_vismol_session (pdynamo_session  = self,
                                                                #rep              = True, 
                                                                vobject    = vobject, 
                                                                autocenter       = autocenter)
        
        self.vm_session.glwidget.vm_widget.center_on_coordinates(vobject, center)
        self.refresh_qc_and_fixed_representations()        
        self.vm_session.main_session.update_gui_widgets()
        return vobject

    def selections (self, _centerAtom, _radius, _method):
        """ Function doc """
        
        
        print (_centerAtom)
        print (_radius)
        print (_method)
        vobject = self.systems[self.active_id]['vobject']
        
        atomref = AtomSelection.FromAtomPattern( self.systems[self.active_id]['system'], _centerAtom )
        core    = AtomSelection.Within(self.systems[self.active_id]['system'],
                                                                      atomref,
                                                                      _radius)
                                                                      
        #core    = AtomSelection.Complement(self.systems[self.active_id]['system'],core)                                                
                                                        
                                                                      
        
        #print( core )
        
        if _method ==0:
            core    = AtomSelection.ByComponent(self.systems[self.active_id]['system'],core)
            core    = list(core)
            self.vm_session.selections[self.vm_session.current_selection].selecting_by_indexes (vobject   = vobject, 
                                                                                                              indexes = core , 
                                                                                                              clear   = True )
        
        if _method == 1:
            core    = AtomSelection.ByComponent(self.systems[self.active_id]['system'],core)
            core    = list(core)
            #'''******************** invert ? **********************
            inverted = []
            for i in range(0, len(vobject.atoms)):
                if i in core:
                    pass
                else:
                    inverted.append(i)
            
            core =  inverted
            self.vm_session.selections[self.vm_session.current_selection].selecting_by_indexes (vobject = vobject, 
                                                                                                      indexes = core, 
                                                                                                      clear   = True )

        if _method == 2:
            self.vm_session.selections[self.vm_session.current_selection].selecting_by_indexes (vobject   = vobject, 
                                                                                                              indexes = core , 
                                                                                                              clear   = True )
    def get_energy (self):
        """ Function doc """
        self.systems[self.active_id]['system'].Summary( )
        energy = self.systems[self.active_id]['system'].Energy( )
        return energy

    def import_trajectory (self, traj = None, first = 0 , last = -1, stride = 1):
        """ Function doc """
        
        traj   = '/home/fernando/programs/pDynamo3/scratch/examples-3.1.2/book/generatedFiles/cyclohexane_sdpath.ptGeo'
        frames = []
        frame  = []
        
        for atom in self.systems[self.active_id]['system'].atoms.items:
            xyz = self.get_atom_coords_from_pdynamo_system (atom   = atom)
            frame.append(xyz[0])
            frame.append(xyz[1])
            frame.append(xyz[2])
        frame = np.array(frame, dtype=np.float32)
        
        
        # . Define the trajectory.
        trajectory = ImportTrajectory ( traj, self.systems[self.active_id]['system'] )
        trajectory.ReadHeader ( )
        
        # . Loop over the frames in the trajectory.
        phi = []
        psi = []
        while trajectory.RestoreOwnerData ( ):
            frame = []
            for atom in self.systems[self.active_id]['system'].atoms.items:
                xyz = self.get_atom_coords_from_pdynamo_system (atom   = atom)
                frame.append(xyz[0])
                frame.append(xyz[1])
                frame.append(xyz[2])
            frame = np.array(frame, dtype=np.float32)
            #frames.append(frame)
            self.systems[self.active_id]['vobject'].frames.append(frame)

        # . Finish up.
        trajectory.ReadFooter ( )
        trajectory.Close ( )
        #return frames
        
    def run_ConjugateGradientMinimize_SystemGeometry (self                   , 
                                                      logFrequency           , 
                                                      maximumIterations      , 
                                                      rmsGradientTolerance   , 
                                                      save_trajectory = False,
                                                      trajectory_path = None):
        """ Function doc """
        if save_trajectory:
            
            #if trajectory_path == None:
                 
            trajectory_path = '/home/fernando/Documents'
            trajectory = ExportTrajectory ('/home/fernando/programs/pDynamo3/scratch/examples-3.1.2/book/generatedFiles/cyclohexane_sdpath.ptGeo', self.systems[self.active_id]['system'] )

            ConjugateGradientMinimize_SystemGeometry ( self.systems[self.active_id]['system']                        ,
                                                       logFrequency                       = logFrequency             ,
                                                       maximumIterations                  = maximumIterations        ,
                                                       rmsGradientTolerance               = rmsGradientTolerance     ,
                                                       trajectory                         = trajectory
                                                       )        
        
        else:
        
            ConjugateGradientMinimize_SystemGeometry ( self.systems[self.active_id]['system']                        ,
                                                       logFrequency                       = logFrequency             ,
                                                       maximumIterations                  = maximumIterations        ,
                                                       rmsGradientTolerance               = rmsGradientTolerance     )
        
        self.build_vobject_from_pDynamo_system (name = 'geometry optimization', autocenter = False)

    #--------------------------------------------------------- -----------------------
    def run_simulation(self, _parametersList = None, _parameters4Plot = None, _simulationType = None, folder = None):
        '''
        bsname = base name of the folder where will be created the next
        '''
        print (_parametersList)
        run = Simulation(self.systems[self.active_id]['system'],_simulationType, folder )
        run.Execute(_parametersList,_parameters4Plot)
        
        self.build_vobject_from_pDynamo_system (name = 'new_geometry', autocenter = False)
        
#======================================================================================================
 





