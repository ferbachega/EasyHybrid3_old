#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#FILE = CoreInterface.py

##############################################################
#-----------------...EasyHybrid 3.0...-----------------------#
#-----------Credits and other information here---------------#
##############################################################

import os, glob, sys
#--------------------------------------------------------------
#Loading own libraries
from commonFunctions import *
from SimulationsPreset import Simulation
import LogFile
#--------------------------------------------------------------
#loading pDynamo Libraries
from pBabel                    import *                                     
from pCore                     import *                                     
from pMolecule                 import *                              
from pMolecule.MMModel         import *
from pMolecule.NBModel         import *                                     
from pMolecule.QCModel         import *
from pScientific               import *                                
from pSimulation               import *
#==========================================================================

#**************************************************************************
class SimulationProject:
    '''
    Class to setup pDynamo simulations from a remote framework, i.e. without using VisMol GUI 
    '''  
    #.-------------------------------------------------------------------------
    def __init__(self,_projectName,DEBUG=False):
        '''
        Class constructor
        Parameters:
            _projectName: name of the project; string or path
            DEBUG       : if this paramters it set True, some extra steps in the system setting will be performe to check the things up
        '''        
        self.baseName       = _projectName
        self.cSystem        = None          #current system
        self.SystemStates   = []            #list of Systems as hystory 
        self.simulation     = "Single-Point"#Name of the Simulation type        
        self.systemCoutCurr = 0 
        self.DEBUG          = DEBUG
        #Some status variable for current Sytem instance ( For now without any great utility )
        self.NBmodel        = None 
        self.QCmodel        = None
        self.MMmodel        = None                
    #===================================================================================
    def LoadSystemFromForceField(self,_topologyFile,_coordinateFile):
        '''
        Load the current system from topology and coordinate files from molecular dynamics packages
        Parameters:
            _topologyFile  : topology file name; string or path
            _coordinateFile: coordinate file name; string or path
        '''
        #------------------------------------------------------------
        oldSystem = Clone(self.cSystem) 
        #------------------------------------------------------------
        self.cSystem              = ImportSystem(_topologyFile, log=None)
        self.cSystem.coordinates3 = ImportCoordinates3(_coordinateFile, log=None)
        self.cSystem.label        = self.baseName + "_#" + str(self.systemCoutCurr)
        self.systemCoutCurr      += 1
        #------------------------------------------------------------
        if not oldSystem == None:
            oldSystem = copySystem(self.cSystem)
            self.SystemStates.append(oldSystem) 
        #------------------------------------------------------------
        #testing the MMmodel
        self.NBmodel = NBModelCutOff.WithDefaults( )
        self.cSystem.DefineNBModel( self.NBmodel )
        #------------------------------------------------------------
        if self.DEBUG:
            energy = self.cSystem.Energy( doGradients = True )
            self.cSystem.Summary()
        #------------------------------------------------------------      
        self.NBmodel = self.cSystem.nbModel
        self.MMmodel = self.cSystem.mmModel
    #====================================================================================
    def LoadSystemFromSavedProject(self,_pklPath):
        '''
        Load the current system from a pDynamo pkl. 
        Parameters:
            _pklPath: PKL file path; string or path 
        '''
        if self.cSystem == None:
            self.cSystem = ImportSystem(_pklPath,log=None)
            self.cSystem.label = self.baseName + "_#" + str(self.systemCoutCurr)
            self.systemCoutCurr += 1
        else:
            oldSystem = copySystem(self.cSystem)
            self.SystemStates.append( oldSystem ) # put the current system 
            #------------------------------------------------------
            self.cSystem         = ImportSystem(_pklPath, log=None)
            self.cSystem.label   = self.baseName + "_#" + str(self.systemCoutCurr)
            self.systemCoutCurr += 1
        #----------------------------------------------------------
        self.NBmodel = self.cSystem.nbModel
        self.MMmodel = self.cSystem.mmModel
        self.QCmodel = self.cSystem.qcModel
        #----------------------------------------------------------
        if self.DEBUG:
            energy = self.cSystem.Energy( doGradients = True )            
            self.cSystem.Summary()
    #====================================================================================
    def SphericalPruning(self, _centerAtom, _radius):
        '''
        Perform a spherical pruning from a certain atom center coordinates.
        Parameters:
            _centerAtom:
            _radius    :
        '''
        #---------------------------------------------------
        oldSystem = copySystem(self.cSystem)
        self.SystemStates.append(oldSystem)
        self.systemCoutCurr += 1
        #---------------------------------------------------
        atomref      = AtomSelection.FromAtomPattern( self.cSystem, _centerAtom )
        core         = AtomSelection.Within(self.cSystem,atomref,_radius)
        core2        = AtomSelection.ByComponent(self.cSystem,core)
        self.cSystem = PruneByAtom( self.cSystem , Selection(core2) )
        #---------------------------------------------------
        self.cSystem.label = self.baseName + "#{} Pruned System ".format(self.systemCoutCurr) 
        self.cSystem.DefineNBModel( self.NBmodel )
        #---------------------------------------------------
        if self.DEBUG:
            self.cSystem.Energy()
    #======================================================================================
    def SettingFixedAtoms(self,_centerAtom,_radius):
        '''
        Set the list of atoms to keep with the positions fixed through the next simulations
        Parameters:
            _centerAtom:
            _radius    :
        '''
        #-----------------------------------------------------
        oldSystem = copySystem(self.cSystem)
        self.SystemStates.append(oldSystem)
        self.systemCoutCurr += 1
        #-----------------------------------------------------
        atomref = AtomSelection.FromAtomPattern( self.cSystem, _centerAtom )
        core    = AtomSelection.Within(self.cSystem,atomref,_radius)
        mobile  = AtomSelection.ByComponent(self.cSystem,core)        
        #-----------------------------------------------------
        if self.DEBUG:
            MobileSys = PruneByAtom( self.cSystem, Selection(mobile) )
            ExportSystem("MobileSystemCheck.pdb",MobileSys)
        #-----------------------------------------------------        
        self.cSystem.freeAtoms = mobile       
        self.cSystem.label = self.baseName + "#{} With Fixed Atoms ".format(self.systemCoutCurr) 
        self.cSystem.DefineNBModel( self.NBmodel )
        self.cSystem.Energy()    
    #=====================================================================================
    def SetSMOHybridModel(self,_method,_region,_QCcharge,_QCmultiplicity):
        '''
        Set a semiempirical quantum chemistry Energy Model for the current system.
        Parameters:
            _method        :
            _region        :
            _QCcharge      :
            _QCmultiplicity: 
        '''
        #---------------------------------------------------------------------
        if not VerifyMNDOKey(_method):
            return(-1)            
        #---------------------------------------------
        # Define the QC atoms list
        atomlist = []
        for sel in _region:
            if type(sel) == int:
                atomlist.append(sel)
            elif type(_region) == list:
                for i in range( len(sel) ):
                    atomlist.append( sel[i] )            
        #---------------------------------------------
        #define QC atoms selection
        converger = DIISSCFConverger.WithOptions( energyTolerance   = 3.0e-4,
                                                  densityTolerance  = 1.0e-8,
                                                  maximumIterations = 2500  )
        _QCRegion = Selection.FromIterable(atomlist)    
        #---------------------------------------------
        #Appending sytem
        self.NBmodel = self.cSystem.nbModel
        self.cSystem.nbModel = None
        oldSystem = Clone(self.cSystem)       
        self.SystemStates.append( oldSystem )        
        self.cSystem.label = self.baseName + "#{} {} Hamiltonian and QC region Set".format(self.systemCoutCurr,_method)
        self.systemCoutCurr += 1
        #Setting QC model 
        self.cSystem.electronicState = ElectronicState.WithOptions ( charge =_QCcharge , multiplicity =_QCmultiplicity )
        _QCmodel = QCModelMNDO.WithOptions( hamiltonian = _method, converger=converger )        
        #------------------------------------------------------------------------
        self.cSystem.DefineQCModel( _QCmodel, qcSelection=_QCRegion )
        self.cSystem.DefineNBModel( self.NBmodel )       
        #------------------------------------------------------------------------
        if self.DEBUG:
            qcSystem = PruneByAtom(self.cSystem, _QCRegion)
            ExportSystem(self.baseName+"_qcSystem.pdb",qcSystem)
            ExportSystem(self.baseName+"_qcSystemEntire.pdb",self.cSystem)
            energy = self.cSystem.Energy() 
    #=====================================================================================
    def SetOrcaSystem(self,_model,_basis,_region,_QCcharge,_QCmultiplicity):
        '''
        Set or modify the QC model to run with ORCA.
        Parameters:
            _model         :
            _basis         :
            _region        :
            _QCcharge      :
            _QCmultiplicity:
        '''
        #seting scratch path
        _scratch = os.path.join( orcaScratchBase,self.baseName )
        if not os.path.exists(_scratch):
            os.makedirs(_scratch)
        #---------------------------------------------
        options =  "\n% output\n"
        options +=  "print [ p_mos ] 1\n"
        options +=  "print [ p_overlap ] 5\n"
        options +=  "end # output"
        #---------------------------------------------
        atomlist = []
        for sel in _region:
            if type(sel) == int:
                atomlist.append(sel)
            elif type(sel) == list:
                for i in range( len(sel) ):
                    atomlist.append( sel[i] )            
        #define QC atoms selection
        _QCRegion = Selection.FromIterable(atomlist)         
        #---------------------------------------------
        #Appending qc system
        self.cSystem.nbModel = None
        oldSystem            = Clone( self.cSystem )
        self.SystemStates.append( oldSystem )
        self.cSystem.label  = self.baseName + "#{} ORCA and QC region Set".format(self.systemCoutCurr)
        self.systemCoutCurr += 1
        #--------------------------------------------------------------------------------
        #Setting QC model
        self.cSystem.electronicState = ElectronicState.WithOptions(charge       = _QCcharge       , 
                                                                   multiplicity = _QCmultiplicity )
        #................................................................................
        _QCmodel = QCModelORCA.WithOptions( keywords        = [ _model, _basis, options ], 
                                            deleteJobFiles  = False                      ,
                                            scratch         =_scratch                    )
        #Export the set QC region for visual inspection
        #---------------------------------------------------------------------------------
        if self.DEBUG:
            qcSystem = PruneByAtom(self.cSystem, _QCRegion)
            ExportSystem(self.baseName+"_qcSystem.pdb",qcSystem)        
        #---------------------------------------------
        self.NBmodel = NBModelORCA.WithDefaults()
        self.cSystem.DefineQCModel( _QCmodel , qcSelection=_QCRegion )
        self.cSystem.DefineNBModel(self.NBmodel)
    #==========================================================================
    def SetDFTBsystem(self,_region,_QCcharge,_QCmultiplicity):
        '''
        Set or modify the QC model to run with DFTB model.
        Parameters:
            _region:
            _QCcharge:
            _QCmultiplicity:
        '''
        #----------------------------------------------
        atomlist = []
        for sel in _region:
            if type(sel) == int:
                atomlist.append(sel)
            elif type(sel) == list:
                for i in range( len(sel) ):
                    atomlist.append( sel[i] )
        #---------------------------------------------
        #define QC atoms selection
        _QCRegion = Selection.FromIterable(atomlist)
        #---------------------------------------------
        #Sending the system
        self.cSystem.nbModel = None
        oldSystem = Clone( self.cSystem )      
        self.SystemStates.append( oldSystem )
        self.cSystem.label   = self.baseName + "#{} DFTB and QC region Set".format(self.systemCoutCurr)
        self.systemCoutCurr += 1
        self.cSystem.electronicState = ElectronicState.WithOptions( charge = _QCcharge, multiplicity = _QCmultiplicity )
        #---------------------------------------------
        #Export the set QC region for visual inspection
        if self.DEBUG:
            qcSystem = PruneByAtom(self.cSystem, _QCRegion)
            ExportSystem(self.baseName+"_qcSystem.pdb",qcSystem)
        #---------------------------------------------
        _scratch = os.path.join(os.getcwd(),self.baseName,"dftbjob")
        if not os.path.exists(_scratch): os.makedirs(_scratch)
        #--------------------------------------------------------------------
        #task adjust the parameters for customizable options
        _QCmodel = QCModelDFTB.WithOptions ( deleteJobFiles = False   ,
                                             randomScratch  = True    ,
                                             scratch        = _scratch,
                                             skfPath        = skfPath ,
                                             useSCC         = True    )
        #-----------------------------------------------------------------------
        self.NBmodel = NBModelDFTB.WithDefaults()
        self.cSystem.DefineQCModel( _QCmodel, qcSelection=_QCRegion )
        self.cSystem.DefineNBModel( self.NBmodel ) # reseting the non-bonded model
        #--------------------------------------------------------------------
        self.cSystem.qcModel.maximumSCCIterations=1200
        energy = self.cSystem.Energy()      
    #=========================================================================
    def RunSinglePoint(self):
        '''
        Calculate the energy for the system.
        '''
        #----------------------------------------------------------------
        energy = self.cSystem.Energy()
        #----------------------------------------------------------------
        print("Single Point Energy Calculations Done!\n")
        print(energy)
        #----------------------------------------------------------------
        return(energy)
    #=========================================================================
    def RunSimulation(self,_parameters):
        '''
        Execute a preset simulation for the current system. 
        Parameters:
           _parameters:
        '''
        #----------------------------------------------------------------------
        oldSystem = copySystem( self.cSystem )
        self.SystemStates.append( oldSystem )
        self.cSystem.label   = self.baseName + "#{} Input for Simulation: {}".format(self.systemCoutCurr,_parameters["simulation_type"])
        self.systemCoutCurr += 1
        #---------------------------------------------------------------------
        _parameters["active_system"] = self.cSystem
        bsname  = os.path.join( os.getcwd(), self.baseName )
        if not "folder" in _parameters:
            _parameters["folder"] = bsname        
        process = Simulation(_parameters)
        process.Execute()        
    #========================================================================================
    def PrintSystems(self):
        '''
        Method to print the summary of the loaded systems 
        '''
        print("There are {} loaded systems".format( self.systemCoutCurr) )
        ctn = input("Type any key to print the Summary of the Systems, or 'N' to cancel this")
        if not ctn == "N":
            if len(self.SystemStates) > 0:
                for system in self.SystemStates:
                    system.Summary()
                    print("***************************************************")
                print("Now, printing the current system Summary:")
                self.cSystem.Summary()

            elif self.systemCoutCurr == 1: print("There is only the current System loaded!\n Printing its information below!")
            else:                          print( "There are no loaded systems!")
    #==========================================================================================
    def SaveProject(self):
        '''
        The complete version of this function intends to save in pkl and another coordinate format
        the systems and trajectories worked in this simulations
        Though, in the current state only will save the current system to a pkl file
        '''
        Pickle(self.baseName+".pkl",self.cSystem)
        ExportSystem(self.baseName+".pdb",self.cSystem)        
    #.-------------------------------------------------------------------------
    def FinishRun(self):
        '''
        Finalize the run.
        '''
        
#==============================================================================

