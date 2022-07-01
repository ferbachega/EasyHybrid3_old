#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#FILE = RelaxedScan.py

##############################################################
#-----------------...EasyHybrid 3.0...-----------------------#
#-----------Credits and other information here---------------#
##############################################################
#=============================================================
import pymp
import numpy as np 
#-----------------------------
#my library
from GeometrySearcher import * 
#-----------------------------
#pDynamo library
from pMolecule import *
from pMolecule.QCModel import *
from LogFile import LogFileWriter
#**************************************************************
class SCAN:
    '''
    Class to setup and execute relaxed surface scan procedure
    '''
    #---------------------------------------------------------------
    def __init__(self,_system,_baseFolder,_optimizer,ADAPTATIVE=False):
        '''
        Default constructor
        Parameters:
            _system    : reference molecular information ; System instance from pDynamo library
            _baseFolser: path for the folder where the results will be written; string or os.path
            _optmizer  : Geometry searcher optimizer algorithm to be used in the relaxation steps; string 
            ADAPTATIVE : flag indicating whether the run is allowed to modified the convergence parameters in regions of high energy; boolean 
        
        Future Development Notes: 
            Implement the possibility of a third coordinate.
            Implement the possibility to deal with other type of restraits               
                Thether
        '''
        self.parameters         = None 
        self.logfile            = None
        
        self.baseName           = _baseFolder
        self.molecule           = _system 
        self.nDim               = 0                                  # Number of active reaction coordinates to Scan
        self.reactionCoordinate1= []                                 # array with the first reaction coordinate in angstroms
        self.reactionCoordinate2= []                                 # array with the second reaction coordinate in angstroms
        self.atoms              = []                                 # array of the atomic indices for the reaction coordinates
        self.nprocs             = 1                                  # Maximum virtual threads to use in parallel runs using pymp
        self.energiesMatrix     = None                               # Multidimensional array to store calculated energy values
        self.DMINIMUM           = [ 0.0, 0.0 ]                       # List with the Minimum distances for the reaction coordinates
        self.DINCREMENT         = [ 0.0, 0.0 ]                       # List with the increment distances for the reaction coordinates
        self.forceC             = [ 2500.0, 2500.0 ]                 # Force constant for restraint model
        self.forceCRef          = [ self.forceC[0], self.forceC[1] ] # Inital value for the force constant
        self.EnergyRef          = 0.0                               # Float to hold energy reference value for adaptative scheme
        self.massConstraint     = True                              # Boolean indicating if the reaction coordinates have mass constraints 
        self.multipleDistance   = [False,False]                     # List of booleand indicating if the reaction coordinates are of multiple distance type
        self.nsteps             = [ 1, 1 ]                          # List of integer indicating the number of steps to be taken
        self.maxIt              = 800                               # Maximum number of iterations in goemtry search 
        self.rmsGT              = 0.1                               # Float with root mean square tolerance for geometry optimization 
        self.optmizer           = _optimizer                        # string with optimizer algorithm for geomtry optimization
        self.sigma_a1_a3        = [ 0.0,0.0 ]                       # Mass contraint weight list for the reaction coordinates
        self.sigma_a3_a1        = [ 0.0,0.0 ]                       # Mass contraint weight list for the reaction coordinates
        self.adaptative         = ADAPTATIVE                        # Boolean indicating if the scan can use the adptative scheme to change the convergence paramters
        self.text               = ""                                # Text container for energy log
        self.dihedral           = False                             # If the simulation are from dihedral reaction coordinates
        self.saveFormat         = None
        self.trajFolder         = "ScanTraj"
               
        #------------------------------------------------------------------------  
        #set the parameters dict for the geometry search classes
        self.GeoOptPars =   { "maxIterations":self.maxIt  ,
                              "rmsGradient"  : self.rmsGT   }
    #===========================================================================================
    def ChangeDefaultParameters(self,_parameters):
        '''
        Class method to alter deafult parameters
        '''
        self.parameters = _parameters
        self.parameters["system_name"]         = self.molecule.label
        self.parameters["initial_coordinates"] = self.molecule.coordinates3 
        #-----------------------------------------------------------
        if "traj_folder_name" in _parameters: self.trajFolder = _parameters["traj_folder_name"]
        if "rmsGradient"      in _parameters: self.GeoOptPars["rmsGradient"]   = _parameters["rmsGradient"]
        if "maxIterations"    in _parameters: self.GeoOptPars["maxIterations"] = _parameters["maxIterations"]
        if "log_frequency"    in _parameters: self.GeoOptPars["log_frequency"] = _parameters["log_frequency"]
        if "NmaxThreads"      in _parameters: self.nprocs                      = _parameters["NmaxThreads"]        
        if "force_constant_1" in _parameters: self.forceC[0]  = _parameters["force_constant_1"]
        if "force_constant_2" in _parameters: self.forceC[1]  = _parameters["force_constant_2"] 
        if "save_format"      in _parameters: self.saveFormat = _parameters["save_format"] 
        if "force_constant"   in _parameters: 
            self.forceC[0] = _parameters["force_constant"]
            self.forceC[1] = _parameters["force_constant"]     
        #-----------------------------------------------------------------

        if not "system_name"         in self.parameters: self.parameters["system_name"]     = self.molecule.label
        if not "initial_coordinates" in self.parameters: self.parameters["system_name"]     = "internal"
        if not "ATOMS_RC1_NAMES"     in self.parameters: self.parameters["ATOMS_RC1_NAMES"] = ""
        if not "ATOMS_RC2_NAMES"     in self.parameters: self.parameters["ATOMS_RC2_NAMES"] = ""
        if not "optimizer"           in self.parameters: self.parameters["optimizer"]       = self.optmizer
        if not "rmsGradient"         in self.parameters: self.parameters["rmsGradient"]     = self.rmsGT
        if not "maxIterations"       in self.parameters: self.parameters["maxIterations"]   = self.maxIt
        if not "nprocs"              in self.parameters: self.parameters["nprocs"]          = self.nprocs


        if self.parameters:
            self.logfile = LogFileWriter()
            self.logfile.add_simulation_parameters_text (self.parameters)

    #===========================================================================================
    def ChangeConvergenceParameters(self,_xframe,_yframe):
        '''
        '''
        if not self.energiesMatrix[_xframe,_yframe] == 0.0:
            delta = self.energiesMatrix[_xframe,_yframe]  
            if delta < 150.0:
                #self.forceC[0] = self.forceCRef[0]
                #self.forceC[1] = self.forceCRef[1]
                self.molecule.qcModel.converger.energyTolerance  = 0.0001
                self.molecule.qcModel.converger.densityTolerance = 3e-08
                self.molecule.qcModel.converger.diisDeviation    = 1e-06
            elif delta >= 150.0:
                #self.forceC[0] = self.forceCRef[0] - self.forceCRef[0]*0.40
                #self.forceC[1] = self.forceCRef[1] - self.forceCRef[1]*0.40
                self.molecule.qcModel.converger.energyTolerance  = 0.0003
                self.molecule.qcModel.converger.densityTolerance = 3e-08
                self.molecule.qcModel.converger.diisDeviation    = 1e-06
                if delta > 160.0 and delta < 170.0:
                    #self.forceC[0] = self.forceCRef[0] - self.forceCRef[0]*0.50
                    #self.forceC[1] = self.forceCRef[1] - self.forceCRef[1]*0.50
                    self.molecule.qcModel.converger.energyTolerance  = 0.0006
                    self.molecule.qcModel.converger.densityTolerance = 1e-07
                    self.molecule.qcModel.converger.diisDeviation    = 2e-06
                elif delta > 170.0 and delta <180.0 :
                    #self.forceC[0] = self.forceCRef[0] - self.forceCRef[0]*0.50
                    #self.forceC[1] = self.forceCRef[1] - self.forceCRef[1]*0.50
                    self.molecule.qcModel.converger.energyTolerance  = 0.001
                    self.molecule.qcModel.converger.densityTolerance = 3e-07
                    self.molecule.qcModel.converger.diisDeviation    = 5e-06
                elif delta > 180.0 and delta < 185.0:
                    #self.forceC[0] = self.forceCRef[0] - self.forceCRef[0]*0.70
                    #self.forceC[1] = self.forceCRef[1] - self.forceCRef[0]*0.70
                    self.molecule.qcModel.converger.energyTolerance  = 0.0015
                    self.molecule.qcModel.converger.densityTolerance = 1e-06
                    self.molecule.qcModel.converger.diisDeviation    = 1e-05
                elif delta > 185.0 and delta <200.0:
                    #self.forceC[0] = self.forceCRef[0] - self.forceCRef[0]*0.70
                    #self.forceC[1] = self.forceCRef[1] - self.forceCRef[1]*0.70
                    self.molecule.qcModel.converger.energyTolerance  = 0.003
                    self.molecule.qcModel.converger.densityTolerance = 1e-05
                    self.molecule.qcModel.converger.diisDeviation    = 5e-05
                elif delta > 200.0:
                    #self.forceC[0] = self.forceCRef[0] - self.forceCRef[0]*0.80
                    #self.forceC[1] = self.forceCRef[1] - self.forceCRef[1]*0.80
                    self.molecule.qcModel.converger.energyTolerance  = 0.003
                    self.molecule.qcModel.converger.densityTolerance = 1e-04
                    self.molecule.qcModel.converger.diisDeviation    = 5e-04
    
    #=============================================================================================
    def SetReactionCoord(self,_RC):
        '''
        Set reaction coordinate, determining initial parameters from the atoms information
        '''
        #------------------------------------------------------------
        ndim = self.nDim # temp var to hold the index of the curren dim
        self.nDim += 1
        self.atoms.append(_RC.atoms)

        self.DINCREMENT[ndim]       = _RC.increment
        self.sigma_a1_a3[ndim]      = _RC.weight13
        self.sigma_a3_a1[ndim]      = _RC.weight31
        self.DMINIMUM[ndim]         = _RC.minimumD
        self.massConstraint         = _RC.massConstraint
        if len(_RC.atoms) == 3:
            self.multipleDistance[ndim] = True
        elif len(_RC.atoms) == 4:
            self.dihedral = True
    #===============================================================================================
    def Run1DScan(self,_nsteps):
        '''
        Manage and execute one-dimensional relaxed scan 
        '''
        if not os.path.exists( os.path.join( self.baseName, self.trajFolder +".ptGeo" ) ):  os.makedirs(  os.path.join( self.baseName,self.trajFolder +".ptGeo"  ) )

        text_line = "{0:>3s} {1:>15s} {2:>15s}".format('x','RC1','Energy' )
        #self.text += "x RC1 Energy\n"
        self.text += text_line+"\n"
        
        self.logfile.add_text_Line("")
        self.logfile.add_text_Line("DATA  "+text_line)
        
        
        self.energiesMatrix      = pymp.shared.array( (_nsteps), dtype=float ) 
        self.reactionCoordinate1 = pymp.shared.array( (_nsteps), dtype=float )
        self.nsteps[0] = _nsteps
        if self.dihedral:  self.Run1DScanDihedral()
        else:
            if    self.multipleDistance[0]:  self.Run1DScanMultipleDistance()
            else: self.Run1DScanSimpleDistance()        
        for i in range(_nsteps):              
            text_line =  "{0:3d} {1:15.8f} {2:15.8f}".format( i,self.reactionCoordinate1[i], self.energiesMatrix[i])
            self.text += text_line+ '\n'
            self.logfile.add_text_Line("DATA  "+text_line)            
            
    #=================================================================================================
    def Run1DScanSimpleDistance(self):
        '''
        Execute the relaxed scan with one reaction coordinate
        '''
        #-------------------------------------------------------------------------
        #Setting some local vars to ease the notation in the pDynamo methods
        #----------------------------------
        atom1 = self.atoms[0][0]
        atom2 = self.atoms[0][1]                   
        #---------------------------------
        restraints = RestraintModel()
        self.molecule.DefineRestraintModel( restraints )                     
        #----------------------------------------------------------------------------------------
        for i in range(self.nsteps[0]):       
            distance = self.DMINIMUM[0] + ( self.DINCREMENT[0] * float(i) )
            #--------------------------------------------------------------------
            rmodel            = RestraintEnergyModel.Harmonic(distance, self.forceC[0])
            restraint         = RestraintDistance.WithOptions(energyModel = rmodel, point1= atom1, point2= atom2)
            restraints["RC1"] = restraint            
            #--------------------------------------------------------------------
            relaxRun = GeometrySearcher(self.molecule,self.baseName)
            relaxRun.ChangeDefaultParameters(self.GeoOptPars)
            relaxRun.Minimization(self.optmizer)
            #--------------------------------------------------------------------
            if i == 0:
                self.EnergyRef = en0 = self.molecule.Energy(log=None)
                self.energiesMatrix[i] = 0.0
            else: self.energiesMatrix[i] = self.molecule.Energy(log=None) - en0 
            #--------------------------------------------------------------------
            self.reactionCoordinate1[i] = self.molecule.coordinates3.Distance( atom1 , atom2  )   
            Pickle( os.path.join( self.baseName,self.trajFolder+".ptGeo", "frame{}.pkl".format(i) ), self.molecule.coordinates3 ) 
        #---------------------------------------
        self.molecule.DefineRestraintModel(None)
    #===================================================================================================
    def Run1DScanMultipleDistance(self):
        '''
        '''
        atom1 = self.atoms[0][0]
        atom2 = self.atoms[0][1]
        atom3 = self.atoms[0][2]
        weight1 = self.sigma_a1_a3[0]
        weight2 = self.sigma_a3_a1[0] 
        #---------------------------------
        restraints = RestraintModel()
        self.molecule.DefineRestraintModel( restraints )
        #---------------------------------
        for i in range(0,self.nsteps[0]):
            distance = self.DMINIMUM[0] + ( self.DINCREMENT[0] * float(i) )             
            #--------------------------------------------------------------------
            rmodel    = RestraintEnergyModel.Harmonic( distance, self.forceC[0] )
            restraint = RestraintMultipleDistance.WithOptions( energyModel = rmodel, distances= [ [ atom2, atom1, weight1 ], [ atom2, atom3, weight2 ] ] )
            restraints["RC1"] =  restraint            
            #--------------------------------------------------------------------
            relaxRun = GeometrySearcher(self.molecule, self.baseName)
            relaxRun.ChangeDefaultParameters(self.GeoOptPars)
            relaxRun.Minimization(self.optmizer)
            #--------------------------------------------------------------------
            if i == 0:
                self.EnergyRef = en0 = self.molecule.Energy(log=None)
                self.energiesMatrix[0] = 0.0
            else: self.energiesMatrix[i] = self.molecule.Energy(log=None) - en0 
            #--------------------------------------------------------------------
            self.reactionCoordinate1[i] = self.molecule.coordinates3.Distance( atom1 , atom2  ) - self.molecule.coordinates3.Distance( atom2, atom3  ) 
            Pickle( os.path.join( self.baseName,self.trajFolder+".ptGeo", "frame{}.pkl".format(i) ), self.molecule.coordinates3 )
        self.molecule.DefineRestraintModel(None)
    #===================================================================================================
    def Run1DScanDihedral(self):
        '''
        Run scan in dihedral angles.
        '''
        atom1 = self.atoms[0][0]
        atom2 = self.atoms[0][1]
        atom3 = self.atoms[0][2]
        atom4 = self.atoms[0][3]               
        #---------------------------------
        restraints = RestraintModel()
        self.molecule.DefineRestraintModel( restraints )
        #---------------------------------
        if self.DINCREMENT[0] == 0.0: self.DINCREMENT[0] = 360.0/float(self.nsteps[0])
        #----------------------------------------------------------------------------------------
        for i in range(0,self.nsteps[0]):
            angle = self.DMINIMUM[0] +  self.DINCREMENT[0] * float(i) 
            #--------------------------------------------------------------------
            rmodel    = RestraintEnergyModel.Harmonic( angle, self.forceC[0], period = 360.0 )
            restraint = RestraintDihedral.WithOptions( energyModel = rmodel,
                                                       point1      = atom1 ,
                                                       point2      = atom2 ,
                                                       point3      = atom3 ,
                                                       point4      = atom4 )
            restraints["PHI"] =  restraint            
            #--------------------------------------------------------------------
            relaxRun = GeometrySearcher(self.molecule, self.baseName  )
            relaxRun.ChangeDefaultParameters(self.GeoOptPars)
            relaxRun.Minimization(self.optmizer)
            #--------------------------------------------------------------------
            if i == 0:
                self.EnergyRef = en0 = self.molecule.Energy(log=None)
                self.energiesMatrix[0] = 0.0
            else: self.energiesMatrix[i]  = self.molecule.Energy(log=None) - en0 
            #--------------------------------------------------------------------
            self.reactionCoordinate1[i] = self.molecule.coordinates3.Dihedral( atom1 , atom2, atom3, atom4 ) 
            Pickle( os.path.join( self.baseName,self.trajFolder+".ptGeo", "frame{}.pkl".format(i) ), self.molecule.coordinates3 )
        #----------------------------------------
        self.molecule.DefineRestraintModel(None)
    #===================================================================================================
    def Run2DScan(self,_nsteps_x,_nsteps_y):
        '''
        Run two-dimensional relaxed surface scan.
        '''
        if not os.path.exists( os.path.join( self.baseName, self.trajFolder +".ptGeo" ) ):  os.makedirs(  os.path.join( self.baseName,self.trajFolder +".ptGeo"  ) )
        #------------------------------------------------------
        #self.text += "x y RC1 RC2 Energy\n" 
        
        text_line = "{0:>3s} {1:>3s} {2:>15s} {3:>15s} {4:>15s}".format('x', 'y', 'RC1', 'RC2', 'Energy' )
        #self.text += "{0:>3s} {1:>3s} {2:>15s} {3:>15s} {4:>15s}\n".format('x', 'y', 'RC1', 'RC2', 'Energy' )#i,j,self.reactionCoordinate1[i,j], self.reactionCoordinate2[i,j], self.energiesMatrix[i,j])
        
        self.text += text_line+"\n"
        #------------------------------------------------------               
        self.logfile.add_text_Line("")
        self.logfile.add_text_Line("DATA  "+text_line)
        
        
        self.nsteps[0] = X = _nsteps_x   
        self.nsteps[1] = Y = _nsteps_y 
        self.energiesMatrix = pymp.shared.array( (X,Y), dtype=float ) 
        self.reactionCoordinate1 = pymp.shared.array( (X,Y), dtype=float )   
        self.reactionCoordinate2 = pymp.shared.array( (X,Y), dtype=float )   
   
        if self.dihedral: self.Run2DScanDihedral(X,Y)
        else:
            if self.multipleDistance[0] and self.multipleDistance[1]           : self.Run2DScanMultipleDistance(X,Y)            
            elif self.multipleDistance[0] and self.multipleDistance[1] == False: self.Run2DMixedDistance(X,Y)
            else                                                               : self.Run2DSimpleDistance(X,Y)
        #------------------------------------
        for i in range(X):
            for j in range(Y):
                text_line =  "{0:3d} {1:3d} {2:15.8f} {3:15.8f} {4:15.8f}".format( i,j,self.reactionCoordinate1[i,j], self.reactionCoordinate2[i,j], self.energiesMatrix[i,j])
                self.text += text_line+ '\n'
                self.logfile.add_text_Line("DATA  "+text_line)    
    #=============================================================================
    def Run2DSimpleDistance(self, X, Y ):
        '''
        Run two-dimensional simple distance relaxed surface scan
        '''
        atom1 = self.atoms[0][0]
        atom2 = self.atoms[0][1]
        atom3 = self.atoms[1][0]
        atom4 = self.atoms[1][1]

        restraints = RestraintModel( )
        self.molecule.DefineRestraintModel( restraints )

        self.reactionCoordinate1[ 0,0 ] = self.molecule.coordinates3.Distance( atom1, atom2 ) 
        self.reactionCoordinate2[ 0,0 ] = self.molecule.coordinates3.Distance( atom3, atom4 ) 

        rmodel     =  RestraintEnergyModel.Harmonic( self.DMINIMUM[0], self.forceC[0] )
        restraint  =  RestraintDistance.WithOptions( energyModel = rmodel,  point1=atom1, point2=atom2  )
        restraints["RC1"] = restraint                
        #----------------------------------------------------------------------------------------------                
        rmodel      = RestraintEnergyModel.Harmonic( self.DMINIMUM[1], self.forceC[1] )
        restraint   = RestraintDistance.WithOptions( energyModel = rmodel, point1=atom3, point2=atom4 )                    
        restraints["RC2"] = restraint 
        #----------------------------------------------------------------------------------------------
        coordinateFile = os.path.join( self.baseName ,self.trajFolder+".ptGeo","frame{}_{}.pkl".format( 0, 0 ) )
        relaxRun = GeometrySearcher( self.molecule, self.baseName )
        relaxRun.ChangeDefaultParameters( self.GeoOptPars )
        relaxRun.Minimization(self.optmizer)
        #-----------------------------------------------------------------------------------------------
        self.EnergyRef = self.en0 = self.molecule.Energy(log=None)         
        Pickle( coordinateFile, self.molecule.coordinates3 )

        for i in range ( 1, X ):  
            #---------------------------------------------------------------------------------------------
            if self.adaptative: self.ChangeConvergenceParameters(i-1,0)
            #---------------------------------------------------------------------------------------------             
            distance_1 = self.DMINIMUM[0] + ( self.DINCREMENT[0] * float(i) ) 
            rmodel     =  RestraintEnergyModel.Harmonic( distance_1, self.forceC[0] )
            restraint  =  RestraintDistance.WithOptions( energyModel = rmodel,  point1=atom1, point2=atom2  )
            restraints["RC1"] = restraint                
            #----------------------------------------------------------------------------------------------                
            distance_2  = self.DMINIMUM[1]
            rmodel      = RestraintEnergyModel.Harmonic( distance_2, self.forceC[1] )
            restraint   = RestraintDistance.WithOptions( energyModel = rmodel, point1=atom3, point2=atom4 )                    
            restraints["RC2"] = restraint  
            #----------------------------------------------------------------------------------------------                   
            initCoordinateFile = os.path.join( self.baseName,self.trajFolder+".ptGeo", "frame{}_{}.pkl".format( 0 , 0) ) 
            self.molecule.coordinates3 = ImportCoordinates3( initCoordinateFile, log=None )               
            #----------------------------------------------------------------------------------------------
            coordinateFile = os.path.join( self.baseName,self.trajFolder+".ptGeo", "frame{}_{}.pkl".format( i, 0 ) )
            relaxRun = GeometrySearcher( self.molecule, self.baseName )
            relaxRun.ChangeDefaultParameters(self.GeoOptPars)
            relaxRun.Minimization(self.optmizer)
            #----------------------------------------------------------------------------------------------
            self.energiesMatrix[ i,0 ]      = self.molecule.Energy(log=None) - self.en0
            self.reactionCoordinate1[ i,0 ] = self.molecule.coordinates3.Distance( atom1, atom2 ) 
            self.reactionCoordinate2[ i,0 ] = self.molecule.coordinates3.Distance( atom3, atom4 )   
            #-----------------------------------------------------------------------------------
            Pickle( coordinateFile, self.molecule.coordinates3 )                
        #-------------------------------------------------------------------------------------------
        with pymp.Parallel(self.nprocs) as p:
            #Pergomr the calculations for the rest of the grid
            for i in p.range ( 0, X ):
                #----------------------------------------------------------------------------------------------
                distance_1 = self.DMINIMUM[0] + ( self.DINCREMENT[0] * float(i) )
                rmodel     = RestraintEnergyModel.Harmonic( distance_1, self.forceC[0] )
                restraint  = RestraintDistance.WithOptions(energyModel =rmodel, point1=atom1, point2=atom2  )
                restraints["RC1"] = restraint
                #----------------------------------------------------------------------------------------------
                for j in range( 1, Y ):
                    distance_2  = self.DMINIMUM[1] + ( self.DINCREMENT[1] * float(j) )
                    rmodel      = RestraintEnergyModel.Harmonic( distance_2, self.forceC[1] )
                    restraint   = RestraintDistance.WithOptions(energyModel = rmodel, point1=atom3, point2=atom4  )
                    restraints["RC2"] = restraint                    
                    #------------------------------------------------------------------------------------------
                    initCoordinateFile = os.path.join( self.baseName,self.trajFolder+".ptGeo" , "frame{}_{}.pkl".format( i, j-1 ) )                    
                    self.molecule.coordinates3 = ImportCoordinates3( initCoordinateFile, log=None )             
                    #----------------------------------------------------------------------------------------------
                    if self.adaptative: self.ChangeConvergenceParameters(i,j-1)
                    coordinateFile = os.path.join( self.baseName,self.trajFolder+".ptGeo", "frame{}_{}.pkl".format( i, j ) )
                    relaxRun = GeometrySearcher( self.molecule, self.baseName  )
                    relaxRun.ChangeDefaultParameters( self.GeoOptPars )
                    relaxRun.Minimization(self.optmizer) 
                    #----------------------------------------------------------------------------------------------
                    self.energiesMatrix[ i,j ] = self.molecule.Energy(log=None) - self.en0
                    self.reactionCoordinate1[ i,j ] = self.molecule.coordinates3.Distance( atom1, atom2 ) 
                    self.reactionCoordinate2[ i,j ] = self.molecule.coordinates3.Distance( atom3, atom4 )
                    #-----------------------------------------------------------------------------------
                    Pickle( coordinateFile, self.molecule.coordinates3 )
                    #-----------------------------------------------------------------------------------
        self.molecule.DefineRestraintModel(None)
    #=======================================================   
    def Run2DMixedDistance(self,X, Y ):
        '''
        Run two-dimensional simple distance relaxed surface scan
        '''
        atom1 = self.atoms[0][0]
        atom2 = self.atoms[0][1]
        atom3 = self.atoms[0][2]
        atom4 = self.atoms[1][0]
        atom5 = self.atoms[1][1]
        
        weight1 = self.sigma_a1_a3[0]
        weight2 = self.sigma_a3_a1[0]

        restraints = RestraintModel( )
        self.molecule.DefineRestraintModel( restraints )
        
        self.reactionCoordinate1[ 0,0 ] = self.molecule.coordinates3.Distance( atom1, atom2 ) - self.molecule.coordinates3.Distance( atom3, atom2 )
        self.reactionCoordinate2[ 0,0 ] = self.molecule.coordinates3.Distance( atom4, atom5 )
       
        distance_1 = self.DMINIMUM[0] 
        rmodel     = RestraintEnergyModel.Harmonic( distance_1, self.forceC[0] )
        restraint  = RestraintMultipleDistance.WithOptions(energyModel = rmodel, distances = [ [ atom2, atom1, weight1 ],[ atom2, atom3, weight2 ] ] )
        restraints["RC1"] = restraint                
        #--------------------------------------------------------------------------------
        distance_2  = self.DMINIMUM[1]
        rmodel      = RestraintEnergyModel.Harmonic( distance_2, self.forceC[1] )
        restraint   = RestraintDistance.WithOptions( energyModel = rmodel, point1=atom4, point2=atom5 )                
        restraints["RC2"] = restraint 
        #--------------------------------------------------------------------------------
        coordinateFile = os.path.join( self.baseName ,self.trajFolder+".ptGeo","frame{}_{}.pkl".format( 0, 0 ) )
        relaxRun = GeometrySearcher( self.molecule, self.baseName )
        relaxRun.ChangeDefaultParameters( self.GeoOptPars )
        relaxRun.Minimization(self.optmizer)
        #-----------------------------------------------------------------------------------------------
        self.EnergyRef = self.en0 = self.molecule.Energy(log=None)         
        Pickle( coordinateFile, self.molecule.coordinates3 )

        for i in range ( 1, X ):  
            if self.adaptative: self.ChangeConvergenceParameters(i-1,0) 
            distance_1 = self.DMINIMUM[0] + self.DINCREMENT[0] * float(i)
            rmodel     = RestraintEnergyModel.Harmonic( distance_1, self.forceC[0] )
            restraint  = RestraintMultipleDistance.WithOptions(energyModel = rmodel, distances = [ [ atom2, atom1, weight1 ],[ atom2, atom3, weight2 ] ] )
            restraints["RC1"] = restraint                
            #--------------------------------------------------------------------------------
            distance_2  = self.DMINIMUM[1]
            rmodel      = RestraintEnergyModel.Harmonic( distance_2, self.forceC[1] )
            restraint   = RestraintDistance.WithOptions( energyModel = rmodel, point1=atom4, point2=atom5 )                
            restraints["RC2"] = restraint  
            #---------------------------------------------------------------------------------                    
            initCoordinateFile = os.path.join( self.baseName,self.trajFolder+".ptGeo", "frame{}_{}.pkl".format(0,0) ) 
            self.molecule.coordinates3 = ImportCoordinates3( initCoordinateFile, log = None )                
            #--------------------------------------------------------------------------------
            coordinateFile = os.path.join( self.baseName,self.trajFolder+".ptGeo", "frame{}_{}.pkl".format( i, 0 ) )
            relaxRun = GeometrySearcher( self.molecule, self.baseName )
            relaxRun.ChangeDefaultParameters( self.GeoOptPars )
            relaxRun.Minimization(self.optmizer)
            #-------------------------------------------------------------------------------- 
            self.energiesMatrix[ i,0 ]      = self.molecule.Energy(log=None) - self.en0
            self.reactionCoordinate1[ i,0 ] = self.molecule.coordinates3.Distance( atom1, atom2 ) - self.molecule.coordinates3.Distance( atom3, atom2 )
            self.reactionCoordinate2[ i,0 ] = self.molecule.coordinates3.Distance( atom4, atom5 )              
            #-----------------------------------------------------------------------------------
            Pickle( coordinateFile, self.molecule.coordinates3 ) 
        #---------------------------------------------------------------------------------------------
        with pymp.Parallel(self.nprocs) as p:
            #Pergomr the calculations for the rest of the grid
            for i in p.range ( 0, X ):
                distance_1 = self.DMINIMUM[0] + self.DINCREMENT[0] * float(i) 
                rmodel     =  RestraintEnergyModel.Harmonic( distance_1, self.forceC[0] )
                restraint  =  RestraintMultipleDistance.WithOptions( energyModel = rmodel, distances= [ [ atom2, atom1, weight1 ],[ atom2, atom3, weight2 ] ] )
                restraints["RC1"] = restraint
                #-----------------------------------------------------------------------------------
                for j in range( 1, Y ):
                    distance_2  = self.DMINIMUM[1] + ( self.DINCREMENT[1] * float(j) )
                    rmodel      = RestraintEnergyModel.Harmonic( distance_2, self.forceC[1] )
                    restraint   = RestraintDistance.WithOptions( energyModel = rmodel, point1=atom4, point2=atom5 )
                    restraints["RC2"] = restraint  
                    #-----------------------------------------------------------------------------------
                    initCoordinateFile = os.path.join( self.baseName,self.trajFolder+".ptGeo" , "frame{}_{}.pkl".format( i, j-1 ) )                 
                    #-----------------------------------------------------------------------------------
                    self.molecule.coordinates3 = ImportCoordinates3( initCoordinateFile, log=None )             
                    #-----------------------------------------------------------------------------------
                    if self.adaptative: self.ChangeConvergenceParameters(i,j-1)
                    #-----------------------------------------------------------------------------------
                    coordinateFile = os.path.join( self.baseName,self.trajFolder+".ptGeo", "frame{}_{}.pkl".format( i, j ) )
                    relaxRun = GeometrySearcher( self.molecule, self.baseName  )
                    relaxRun.ChangeDefaultParameters( self.GeoOptPars )
                    relaxRun.Minimization(self.optmizer)
                    #-----------------------------------------------------------------------------------
                    self.energiesMatrix[ i,j ]      = self.molecule.Energy(log=None) - self.en0
                    self.reactionCoordinate1[ i,j ] = self.molecule.coordinates3.Distance( atom1, atom2 ) - self.molecule.coordinates3.Distance( atom3, atom2 )
                    self.reactionCoordinate2[ i,j ] = self.molecule.coordinates3.Distance( atom4, atom5 )
                    #-----------------------------------------------------------------------------------
                    Pickle( coordinateFile, self.molecule.coordinates3 )
                    #...................................................
        self.molecule.DefineRestraintModel(None)
    
    #===========================================================
    def Run2DScanMultipleDistance(self, X, Y ):
        '''
        Run two-dimensional simple distance relaxed surface scan
        '''
        atom1 = self.atoms[0][0]
        atom2 = self.atoms[0][1]
        atom3 = self.atoms[0][2]
        atom4 = self.atoms[1][0]
        atom5 = self.atoms[1][1]
        atom6 = self.atoms[1][2]
        weight1 = self.sigma_a1_a3[0]
        weight2 = self.sigma_a3_a1[0]
        weight3 = self.sigma_a1_a3[1]
        weight4 = self.sigma_a3_a1[1]
        restraints = RestraintModel( )
        self.molecule.DefineRestraintModel( restraints )
        self.reactionCoordinate1[ 0,0 ] = self.molecule.coordinates3.Distance( atom1, atom2 ) - self.molecule.coordinates3.Distance( atom3, atom2 )
        self.reactionCoordinate2[ 0,0 ] = self.molecule.coordinates3.Distance( atom4, atom5 ) - self.molecule.coordinates3.Distance( atom6, atom5 )
        #-------------------------------------------------------------------------------------
        distance_1 = self.DMINIMUM[0] 
        rmodel     = RestraintEnergyModel.Harmonic( distance_1, self.forceC[0] )
        restraint  = RestraintMultipleDistance.WithOptions( energyModel = rmodel, distances = [ [ atom2, atom1, weight1 ] , [ atom2, atom3, weight2 ] ] )
        restraints["RC1"] = restraint
        #---- ----------------------------------------------------------------------------        
        distance_2  = self.DMINIMUM[1]
        rmodel      = RestraintEnergyModel.Harmonic( distance_2, self.forceC[1] )
        restraint   = RestraintMultipleDistance.WithOptions( energyModel = rmodel, distances = [ [ atom5, atom4, weight3 ],[ atom5, atom6, weight4 ] ] )
        restraints["RC2"] = restraint  
        #---- ----------------------------------------------------------------------------   
        coordinateFile = os.path.join( self.baseName ,self.trajFolder+".ptGeo","frame{}_{}.pkl".format( 0, 0 ) )
        relaxRun = GeometrySearcher( self.molecule, self.baseName )
        relaxRun.ChangeDefaultParameters( self.GeoOptPars )
        relaxRun.Minimization(self.optmizer)
        #-----------------------------------------------------------------------------------------------
        self.EnergyRef = self.en0 = self.molecule.Energy(log=None)         
        Pickle( coordinateFile, self.molecule.coordinates3 )     

        for i in range ( 1, X ):  
            #.---- ----------------------------------------------------------------------------            
            distance_1 = self.DMINIMUM[0] + self.DINCREMENT[0] * float(i) 
            rmodel     = RestraintEnergyModel.Harmonic( distance_1, self.forceC[0] )
            restraint  = RestraintMultipleDistance.WithOptions( energyModel = rmodel, distances = [ [ atom2, atom1, weight1 ] , [ atom2, atom3, weight2 ] ] )
            restraints["RC1"] = restraint
            #---------------------------------------------------------------------------------        
            distance_2  = self.DMINIMUM[1]
            rmodel      = RestraintEnergyModel.Harmonic( distance_2, self.forceC[1] )
            restraint   = RestraintMultipleDistance.WithOptions( energyModel = rmodel, distances = [ [ atom5, atom4, weight3 ],[ atom5, atom6, weight4 ] ] )
            restraints["RC2"] = restraint  
            #---------------------------------------------------------------------------------
            initCoordinateFile = os.path.join( self.baseName,self.trajFolder+".ptGeo", "frame{}_{}.pkl".format(0,0) ) 
            self.molecule.coordinates3 = ImportCoordinates3( initCoordinateFile, log = None )             
            #-----------------------------------------------------------------------------------
            if self.adaptative: self.ChangeConvergenceParameters(i-1,0)
            #-----------------------------------------------------------------------------------
            relaxRun = GeometrySearcher( self.molecule, self.baseName )
            relaxRun.ChangeDefaultParameters(self.GeoOptPars)
            relaxRun.Minimization(self.optmizer)
            #-----------------------------------------------------------------------------------
            self.energiesMatrix[ i,0 ]      = self.molecule.Energy(log=None) - self.en0
            self.reactionCoordinate1[ i,0 ] = self.molecule.coordinates3.Distance( atom1, atom2 ) - self.molecule.coordinates3.Distance( atom3, atom2 )
            self.reactionCoordinate2[ i,0 ] = self.molecule.coordinates3.Distance( atom4, atom5 ) - self.molecule.coordinates3.Distance( atom6, atom5 )
            #-----------------------------------------------------------------------------------
            coordinateFile = os.path.join( self.baseName,self.trajFolder+".ptGeo", "frame{}_{}.pkl".format( i, 0 ) )                       
            Pickle( coordinateFile, self.molecule.coordinates3 )        
        #........................................................................................
        with pymp.Parallel(self.nprocs) as p:
            for i in p.range ( 0, X ):
                distance_1  = self.DMINIMUM[0] + self.DINCREMENT[0] * float(i) 
                rmodel      = RestraintEnergyModel.Harmonic( distance_1, self.forceC[0] )
                restraint   = RestraintMultipleDistance.WithOptions( energyModel = rmodel, distances= [ [ atom2, atom1, weight1 ],[ atom2, atom3, weight2 ] ] )
                restraints["RC1"] = restraint                       
                #---------------------------------------------------------------------------------
                for j in range( 1, Y ):
                    distance_2  =  self.DMINIMUM[1] + self.DINCREMENT[1] * float(j) 
                    rmodel      = RestraintEnergyModel.Harmonic( distance_2, self.forceC[1] )
                    restraint   = RestraintMultipleDistance.WithOptions( energyModel = rmodel, distances = [ [ atom5, atom4, weight3 ],[ atom5, atom6, weight4 ] ] )
                    restraints["RC2"] = restraint  
                    #---------------------------------------------------------------------------------
                    initCoordinateFile = os.path.join( self.baseName,self.trajFolder+".ptGeo" , "frame{}_{}.pkl".format( i, j-1 ) )  
                    #----------------------------------------------------------------------------              
                    self.molecule.coordinates3 = ImportCoordinates3( initCoordinateFile, log = None )             
                    if self.adaptative: self.ChangeConvergenceParameters(i,j-1)
                    #----------------------------------------------------------------------------
                    relaxRun = GeometrySearcher( self.molecule, self.baseName  )
                    relaxRun.ChangeDefaultParameters(self.GeoOptPars)
                    relaxRun.Minimization( self.optmizer )
                    #----------------------------------------------------------------------------
                    self.energiesMatrix[ i,j ]      = self.molecule.Energy(log=None) - self.en0
                    self.reactionCoordinate1[ i,j ] = self.molecule.coordinates3.Distance( atom1, atom2 ) - self.molecule.coordinates3.Distance( atom3, atom2 )
                    self.reactionCoordinate2[ i,j ] = self.molecule.coordinates3.Distance( atom4, atom5 ) - self.molecule.coordinates3.Distance( atom6, atom5 )
                    #-----------------------------------------------------------------------------------
                    coordinateFile = os.path.join( self.baseName, self.trajFolder+".ptGeo", "frame"+str(i)+"_"+str(j)+".pkl" )
                    Pickle( coordinateFile, self.molecule.coordinates3 )                    
        #--------------------------------------                
        self.molecule.DefineRestraintModel(None)
    #=======================================================================================
    def Run2DScanDihedral(self, X, Y):
        '''
        Run two-dimensional dihedral relaxed surface scan
        '''
        atom1 = self.atoms[0][0]
        atom2 = self.atoms[0][1]
        atom3 = self.atoms[0][2]
        atom4 = self.atoms[0][3]
        atom5 = self.atoms[1][0]
        atom6 = self.atoms[1][1]
        atom7 = self.atoms[1][2]
        atom8 = self.atoms[1][3]

        restraints = RestraintModel( )
        self.molecule.DefineRestraintModel( restraints )

        self.reactionCoordinate1[ 0,0 ] = self.molecule.coordinates3.Dihedral( atom1, atom2, atom3, atom4 ) 
        self.reactionCoordinate2[ 0,0 ] = self.molecule.coordinates3.Dihedral( atom5, atom6, atom7, atom8 )
        if self.DINCREMENT[0] == 0.0: self.DINCREMENT[0] = 360.0/float(X)
        if self.DINCREMENT[1] == 0.0: self.DINCREMENT[1] = 360.0/float(Y)
        #-------------------------------------------------------------------------------------
        for i in range ( 1, X ):  
        #.--------------------------------------------------------------------------------            
            angle_1    = self.DMINIMUM[0] + float(i)*self.DINCREMENT[0] 
            rmodel     = RestraintEnergyModel.Harmonic( angle_1, self.forceC[0], period = 360.0 )
            restraint  = RestraintDihedral.WithOptions( energyModel = rmodel,
                                                        point1 = atom1      ,
                                                        point2 = atom2      ,
                                                        point3 = atom3      ,
                                                        point4 = atom4      )
            restraints["PHI"] = restraint
            #--------------------------------------------------------------------------------        
            angle_2     = self.DMINIMUM[1]
            rmodel      = RestraintEnergyModel.Harmonic( angle_2, self.forceC[1], period = 360.0 )
            restraint   = RestraintDihedral.WithOptions( energyModel = rmodel, 
                                                         point1 = atom5      ,
                                                         point2 = atom6      ,
                                                         point3 = atom7      ,
                                                         point4 = atom8      )
            restraints["PSI"] = restraint  
            #---------------------------------------------------------------------------------
            initCoordinateFile = os.path.join( self.baseName,self.trajFolder+".ptGeo", "frame{}_{}.pkl".format(0,0) ) 
            self.molecule.coordinates3 = ImportCoordinates3( initCoordinateFile, log = None )                          
            #-----------------------------------------------------------------------------------
            relaxRun = GeometrySearcher( self.molecule, self.baseName )
            relaxRun.ChangeDefaultParameters(self.GeoOptPars)
            relaxRun.Minimization(self.optmizer)
            #-----------------------------------------------------------------------------------
            self.energiesMatrix[ i,0 ]      = self.molecule.Energy(log=None) - self.en0
            self.reactionCoordinate1[ i,0 ] = self.molecule.coordinates3.Dihedral( atom1, atom2, atom3, atom4 )
            self.reactionCoordinate2[ i,0 ] = self.molecule.coordinates3.Dihedral( atom5, atom6, atom7, atom8 )
            #-----------------------------------------------------------------------------------
            coordinateFile = os.path.join( self.baseName,self.trajFolder+".ptGeo", "frame{}_{}.pkl".format( i, 0 ) )                       
            Pickle( coordinateFile, self.molecule.coordinates3 )        
        #........................................................................................
        with pymp.Parallel(self.nprocs) as p:
            for i in p.range ( 0, X ):
                angle_1     = self.DMINIMUM[0] + float(i)*self.DINCREMENT[0]  
                rmodel      = RestraintEnergyModel.Harmonic( angle_1, self.forceC[0], period = 360.0  )
                restraint   = RestraintDihedral.WithOptions( energyModel = rmodel, 
                                                             point1 = atom1      ,
                                                             point2 = atom2      ,
                                                             point3 = atom3      ,
                                                             point4 = atom4      )
                restraints["PHI"] = restraint                       
                #---------------------------------------------------------------------------------
                for j in range( 1, Y ):
                    angle_2  =  self.DMINIMUM[1] + float(j)*self.DINCREMENT[1]
                    rmodel      = RestraintEnergyModel.Harmonic( angle_2, self.forceC[1], period = 360.0  )
                    restraint   = RestraintDihedral.WithOptions( energyModel = rmodel, 
                                                                 point1 = atom5      ,
                                                                 point2 = atom6      ,
                                                                 point3 = atom7      ,
                                                                 point4 = atom8      )
                    restraints["PSI"] = restraint  
                    #---------------------------------------------------------------------------------
                    initCoordinateFile = os.path.join( self.baseName,self.trajFolder+".ptGeo" , "frame{}_{}.pkl".format( i, j-1 ) )  
                    #----------------------------------------------------------------------------              
                    self.molecule.coordinates3 = ImportCoordinates3( initCoordinateFile, log = None )      
                    #----------------------------------------------------------------------------
                    relaxRun = GeometrySearcher( self.molecule, self.baseName  )
                    relaxRun.ChangeDefaultParameters(self.GeoOptPars)
                    relaxRun.Minimization( self.optmizer )
                    #----------------------------------------------------------------------------
                    self.energiesMatrix[ i,j ]      = self.molecule.Energy(log=None) - self.en0
                    self.reactionCoordinate1[ i,j ] = self.molecule.coordinates3.Dihedral( atom1, atom2, atom3, atom4 ) 
                    self.reactionCoordinate2[ i,j ] = self.molecule.coordinates3.Dihedral( atom5, atom6, atom7, atom8 )
                    #-----------------------------------------------------------------------------------
                    coordinateFile = os.path.join( self.baseName, self.trajFolder+".ptGeo", "frame"+str(i)+"_"+str(j)+".pkl" )
                    Pickle( coordinateFile, self.molecule.coordinates3 )                    
        #--------------------------------------                
        self.molecule.DefineRestraintModel(None)

    #=======================================================================================
    def Finalize(self):
        '''
        Writing logs, making plots and saving trajectories
        '''       
        if self.nDim == 1:
            #..................................................
            if not self.saveFormat == None: 
                print(self.saveFormat)
                trajName = os.path.join( self.baseName, self.trajFolder+self.saveFormat )
                trajpath = os.path.join( self.baseName, self.trajFolder+".ptGeo" )
                Duplicate( trajpath, trajName, self.molecule )
        #..................................................
        
        if self.logfile:
            trajName = os.path.join( self.baseName, self.trajFolder+self.saveFormat )
            trajpath = os.path.join( self.baseName, self.trajFolder+".ptGeo" )
            
            
            print(self.baseName, self.trajFolder)
            #self.logfile.save_logfile("datafile", "/home/fernando")
            self.logfile.save_logfile(self.trajFolder, trajpath)
            
        textLog = open( os.path.join(self.baseName,self.trajFolder+".log"), "w" ) 
        textLog.write(self.text)
        textLog.close() 
        #..................................................

    #========================================================================================
    def Print(self):
        '''
        Printing relaxed scan parameters
        '''
        pass


#==============================================================================#
#=====================END OF CLASS FILE========================================#
#==============================================================================#
