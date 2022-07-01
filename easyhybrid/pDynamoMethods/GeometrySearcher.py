#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#FILE = GeometrySearcher.py

##############################################################
#-----------------...EasyHybrid 3.0...-----------------------#
#-----------Credits and other information here---------------#
##############################################################

#==============================================================================
import os, sys
#importing our library functions
import commonFunctions
from LogFile import LogFileWriter
# pDynamo
from pBabel                    import *                                     
from pCore                     import *                                     
from pMolecule                 import *                  
from pScientific               import *                                     
from pScientific.Arrays        import *                                     
from pScientific.Geometry3     import *                 
from pSimulation               import *
#*********************************************************************************
class GeometrySearcher:
    '''
    Class to handle with pDynamo methods that search geometries for the system, such as global/local minimuns
    as saddle points and reaction path trajectories. 
    '''
    #.-------------------------------------------------------------------------   
    def __init__(self,_system,_baseFolder,_trajName=None):
        '''
        Class constructor.
        '''
        self.molecule       = _system
        self.baseName       = _baseFolder
        self.optAlg         = "ConjugatedGradient"
        self.InitCrd3D      = Clone(_system.coordinates3)
        self.finalCrd3D     = None
        self.massWeighting  = False
        self.logFreq        = 50 # deafult value for otimizations, must to be changed through the specific class method
        self.trajectoryName = None
        self.savePdb        = False
        self.saveFormat     = None    
        self.rmsGrad        = 0.1
        self.maxIt          = 500
        self.saveFrequency  = 0
        self.DEBUG          = False
        if not _trajName == None: self.trajectoryName = os.path.join(_baseFolder,_trajName)
    #=========================================================================
    def ChangeDefaultParameters(self,_parameters):
        '''
        Class method to modify default parameters for the minimization runs
        '''       
        if "save_pdb"       in _parameters: self.savePdb        = _parameters["save_pdb"]
        if "maxIterations"  in _parameters: self.maxIt          = _parameters['maxIterations']            
        if "log_frequency"  in _parameters: self.logFreq        = _parameters["log_frequency"] 
        if "save_format"    in _parameters: self.saveFormat     = _parameters["save_format"]
        if "save_frequency" in _parameters: self.saveFrequency  = _parameters["save_frequency"]        
        if "rmsGradient"    in _parameters: self.rmsGrad        = _parameters["rmsGradient"]
        if "Debug"          in _parameters: self.DEBUG          = _parameters["Debug"]
    #======================================================================================
    # Main minimization class method
    def Minimization(self,_optimizer):
        '''
        Execute the minimization routine for search of geometry corresponding to local minima
        '''
        #------------------------------------------------------------------
        self.optAlg = _optimizer                 
        # run the minimization for the chosen algorithm
        if   self.optAlg == "ConjugatedGradient": self.RunConjugatedGrad()
        elif self.optAlg == "SteepestDescent"   : self.RunSteepestDescent()
        elif self.optAlg == "LFBGS"             : self.RunLFBGS()
        elif self.optAlg == "QuasiNewton"       : self.RunQuasiNewton()
        elif self.optAlg == "FIRE"              : self.RunFIREmin()
        self.finalCrd3D = Clone(self.molecule.coordinates3)
        if self.DEBUG:
            self.Print()
            pdbFileA = os.path.join(self.baseName, "initialCoord_{}.pdb".format(self.optAlg) )
            pdbFileB = os.path.join(self.baseName, "finalCoord_{}.pdb".format(self.optAlg) )
            self.molecule.coordinates3 = Clone(self.InitCrd3D)
            ExportSystem(pdbFileA,self.molecule)
            self.molecule.coordinates3 = Clone(self.finalCrd3D)
            ExportSystem(pdbFileB,self.molecule)
    #=============================================================================
    #Minimizers methods
    def RunConjugatedGrad(self):
        '''
        Class method to apply the conjugated gradient minimizer
        '''
        if self.trajectoryName == None:
            ConjugateGradientMinimize_SystemGeometry(self.molecule                      ,                
                                                     logFrequency           = self.logFreq  ,
                                                     maximumIterations      = self.maxIt    ,
                                                     rmsGradientTolerance   = self.rmsGrad  )
        else:            
            trajectory = ExportTrajectory( self.trajectoryName, self.molecule, log=None )
            ConjugateGradientMinimize_SystemGeometry(self.molecule                        ,                
                                                 logFrequency           = self.logFreq    ,
                                                 trajectories           = [(trajectory, self.saveFrequency)],
                                                 maximumIterations      = self.maxIt      ,
                                                 rmsGradientTolerance   = self.rmsGrad    )

    #=====================================================================================
    def RunSteepestDescent(self):
        '''
        Class method to apply the steepest descent minimizer
        '''        
        if self.trajectoryName == None:
            SteepestDescentMinimize_SystemGeometry(self.molecule                       ,               
                                                logFrequency            = self.logFreq ,
                                                maximumIterations       = self.maxIt   ,
                                                rmsGradientTolerance    = self.rmsGrad )
        else:
            trajectory = ExportTrajectory( self.trajectoryName, self.molecule, log=None  )
            SteepestDescentMinimize_SystemGeometry(self.molecule                       ,               
                                                logFrequency            = self.logFreq ,
                                                trajectories            = [(trajectory, self.saveFrequency)],
                                                maximumIterations       = self.maxIt   ,
                                                rmsGradientTolerance    = self.rmsGrad )
    #============================================================================
    def RunLFBGS(self):
        '''
        Class method to apply the LFBGS minimizer
        '''        
        if self.trajectoryName == None:
            LBFGSMinimize_SystemGeometry(self.molecule                          ,                
                                    logFrequency         = self.logFreq         ,
                                    maximumIterations    = self.maxIt           ,
                                    rmsGradientTolerance = self.rmsGrad         )
        else:
            trajectory = ExportTrajectory( self.trajectoryName, self.molecule, log=None )
            LBFGSMinimize_SystemGeometry(self.molecule                          ,                
                                    logFrequency         = self.logFreq         ,
                                    trajectories         = [(trajectory, self.saveFrequency)],
                                    maximumIterations    = self.maxIt           ,
                                    rmsGradientTolerance = self.rmsGrad         )    
    #=============================================================================
    def RunQuasiNewton(self):
        '''
        Class method to apply the Quaisi-Newton minimizer
        '''        
        if self.trajectoryName == None: 
            QuasiNewtonMinimize_SystemGeometry( self.molecule                       ,                
                                                logFrequency         = self.logFreq ,
                                                maximumIterations    = self.maxIt   ,
                                                rmsGradientTolerance = self.rmsGrad )
        else:
            trajectory = ExportTrajectory( self.trajectoryName, self.molecule, log=None )
            QuasiNewtonMinimize_SystemGeometry( self.molecule                       ,                
                                                logFrequency         = self.logFreq ,
                                                trajectories         = [(trajectory, self.saveFrequency)],
                                                maximumIterations    = self.maxIt   ,
                                                rmsGradientTolerance = self.rmsGrad )
    #==============================================================================
    def RunFIREmin(self):
        '''
        '''
        if self.trajectoryName == None:
            FIREMinimize_SystemGeometry( self.molecule                  ,                
                                         logFrequency         = self.logFreq ,
                                         maximumIterations    = self.maxIt   ,
                                         rmsGradientTolerance = self.rmsGrad )
        else:
            trajectory = ExportTrajectory( self.trajectoryName, self.molecule, log=None )
            FIREMinimize_SystemGeometry( self.molecule                                            ,                
                                         logFrequency         = self.logFreq                      ,
                                         trajectories         = [(trajectory, self.saveFrequency)],
                                         maximumIterations    = self.maxIt                        ,
                                         rmsGradientTolerance = self.rmsGrad                      )        
    #=============================================================================
    # Reaction path searchers
    def NudgedElasticBand(self,_parameters):
        '''
        Nudget Elastic Band procedure to estimate a reaction path
        '''
        #-------------------------------------------------------------------------
        rmdGIS          = 1
        springCF        = 500.0
        fixedTerminal   = False
        useSpline       = False
        spline_tol      = 1.5
        if "spring_constant_force"      in _parameters: springCF      = _parameters["spring_constant_force"]
        if "fixed_terminal_images"      in _parameters: fixedTerminal = _parameters["fixed_terminal_images"]
        if "RMS_growing_intial_string"  in _parameters: rmsGIS        = _parameters["RMS_growing_intial_string"]
        if "spline_redistribution"      in _parameters: useSpline     = _parameters["spline_redistribution"]

        self.trajectoryName = os.path.join(self.baseName,self.trajectoryName+".ptGeo")
        #Note: is interesting to think in a window were the user select the initial and final coords
        # here we excpect to ibe in pkl probably from a scan or optimization already done using the software
        if "init_coord"  in _parameters: self.InitCrd3D  = ImportCoordinates3( _parameters["init_coord"], log=None  )
        if "final_coord" in _parameters: self.finalCrd3D = ImportCoordinates3( _parameters["final_coord"], log=None )
        trajectory = None
        #-----------------------------------------------------------------------------------------
        if not "traj_source" in _parameters:
            GrowingStringInitialPath(self.molecule              ,
                                    _parameters["traj_bins"]    ,
                                    self.InitCrd3D              ,
                                    self.finalCrd3D             ,  
                                    self.trajectoryName         ,
                                    rmsGradientTolerance=rmsGIS )
            trajectory = ExportTrajectory( self.trajectoryName, self.molecule, append=True )
        else:
            self.trajectoryName = _parameters["traj_source"]
            trajectory = ExportTrajectory( _parameters["traj_source"], self.molecule, append=True ) 
        #------------------------------------------------------------------------------------------
        ChainOfStatesOptimizePath_SystemGeometry (  self.molecule                                       ,   
                                                    trajectory                                          ,
                                                    logFrequency         = 1                            ,
                                                    maximumIterations    = self.maxIt                   ,
                                                    fixedTerminalImages  = fixedTerminal                ,
                                                    springForceConstant  = springCF                     ,
                                                    splineRedistributionTolerance=spline_tol            ,
                                                    forceSplineRedistributionCheckPerIteration=useSpline,
                                                    rmsGradientTolerance = self.rmsGrad   )
    #========================================================================================
    def SelfAvoidWalking(self,_parameters):
        '''
        Self-Avoid-Walking procedure to estimate a reaction path
        '''       
        self.trajectoryName = self.baseName + "SAW.ptGeo"
        self.traj = ExportTrajectory( self.trajectoryName, self.molecule, append=True ) 
        ExpandByLinearInterpolation( _parameters["traj_source"], self.trajectoryName, self.molecule, _parameters["traj_bins"])
        Gamma = 100.0
        Rho   = 2.0
        Kappa = 5000.0
        if "gamma" in _parameters: Gamma = _parameters["gamma"]
        if "rho"   in _parameters: Rho   = _parameters["rho"]
        if "kappa" in _parameters: Kappa = _parameters["kappa"]
        SAWOptimize_SystemGeometry ( self.molecule, self.traj, gamma=Gamma, kappa=Kappa )
    #========================================================================================
    def SteepestDescentPathSearch(self,_parameters):
        '''
        '''
        massW    = True
        funcStep = 2.0
        pathStep = 0.025 

        if "mass_weighting" in _parameters: massw    = _parameters["mass_weighting"]
        if "function_step"  in _parameters: funcStep = _parameters["function_step"]
        if "path_step"      in _parameters: pathStep = _parameters["path_step"]

        self.molecule.coordinates3 = _parameters["saddle_conformation"]
        self.trajectoryName = self.baseName + ".steepPath.ptGeo"
        self.traj = ExportTrajectory( self.trajectoryName, self.molecule )
        SteepestDescentPath_SystemGeometry( self.molecule                           ,
                                            functionStep      = funcStep            ,
                                            logFrequency      = self.logFrequency   ,
                                            maximumIterations = self.maxIt          ,
                                            pathStep          = pathStep            ,
                                            saveFrequency     = self.save_frequency ,
                                            trajectory        = self.traj           ,
                                            useMassWeighting  = massW               )

    #========================================================================================
    def BakerSaddleOptimizer(self,_parameters):
        '''
        Class method to search saddle-points transition structure
        '''

        self.InitCrd3D = ImportCoordinates3(_parameters["saddle_coord"] )
        self.molecule.coordinates3 = Clone(self.InitCrd3D)
        BakerSaddleOptimize_SystemGeometry( self.molecule                       ,
                                            logFrequency         =      1       ,
                                            maximumIterations    = self.maxIt   ,
                                            rmsGradientTolerance = self.rmsGrad )

        self.finalCrd3D = Clone(self.molecule.coordinates3)
        Pickle(self.baseName+"_BakerOpt.pkl",self.finalCrd3D)
        if savePdb: 
            ExportSystem(self.baseName+"_BakerOpt.pdb",self.finalCrd3D)
            savePdb = False

    #=========================================================================================
    def CalculateRMS(self):
        '''
        Calculate the root mean square of deviation of the final coordinate found with the first set given.
        '''
        masses = Array.FromIterable ( [ atom.mass for atom in self.molecule.atoms ] )
        self.InitCrd3D.Superimpose ( self.finalCrd3D, weights = masses )
        rms = self.InitCrd3D.RootMeanSquareDeviation ( self.finalCrd3D, weights = masses )
        print("Root Mean Sqaute of Deviation of the optimized structure from the initial: {}".format(rms))
    #===========================================================================================
    def Finalize(self):
        '''
        Finaluze the Geometry searcher procedures, save structures and/or trajectories
        '''
        self.CalculateRMS()
        #----------------------------------------------------------------------
        #Save structures and/or trajectories
        if self.savePdb:
            pdbFile = self.baseName + "opt_{}.pdb".format(self.optAlg)
            i = 0;
            while os.path.exists(pdbFile):
                pdbFile = self.baseName + "_#{}_opt_{}.pdb".format(i,self.optAlg)
                i += 1
            ExportSystem(pdbFile,self.molecule)
        #----------------------------------------------------------------------
        if self.saveFormat == ".dcd" or self.saveFormat == ".mdcrd":
            if self.saveFormat != self.trajectoryName:
                traj_save = os.path.splitext(self.trajectoryName)[0] + self.saveFormat
                Duplicate(self.trajectoryName,traj_save,self.molecule)
    #===========================================================================================
    def Print(self):
        '''
        Print to screen basic info for the simulation. 
        '''        
        print( "Geometry Searcher working trajectory folder:{}".format(self.trajectoryName) )
        print( "RMS gradient tolerance: {}".format(self.rmsGrad) )
        print( "Optimization Algorithm: {}".format(self.optAlg) )
        print( "Maximum number of maxIterations: {}".format(self.maxIt) )
        
#================================================================================================#
#======================================END OF THE FILE===========================================#
#================================================================================================#
