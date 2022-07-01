#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#FILE = MolecularDynamics.py

##############################################################
#-----------------...EasyHybrid 3.0...-----------------------#
#-----------Credits and other information here---------------#
##############################################################

#==============================================================================

#---------------------------------------
#importing libraries
import os
#import sys
#----------------------------------------
# pDynamo
from pBabel                    import *                                     
from pCore                     import *                                     
from pMolecule                 import *                              
from pMolecule.MMModel         import *
from pMolecule.NBModel         import *                                     
from pMolecule.QCModel         import *
from pScientific               import *                                     
from pScientific.Arrays        import *                                     
from pScientific.Geometry3     import *                                     
from pScientific.RandomNumbers import *                                     
from pScientific.Statistics    import *
from pScientific.Symmetry      import *                                     
from pSimulation               import *

#---------------------------------------

#**************************************************************************
class MD:
    '''
    Class to set up Molecular Dynamics Sumulations.
    '''
    #.---------------------------------------
    def __init__(self,_system,_baseFolder,_integrator,_trajName="production"):
        '''
        Default constructor. 
        Receives a list of paramters to set the simulations.
        '''        
        #Important parameters that are recurrently wanted to be change by the user
        self.molecule               = _system
        self.baseName               = _baseFolder 
        self.trajName               = _trajName
        self.trajectoryNameSoft     = _baseFolder+self.trajName+".ptRes" # this naming scheme makes sense for the umbrella sampling runs
        self.trajectoryNameCurr     = os.path.join(_baseFolder,self.trajName+".ptGeo")
        self.trajectory             = None
        self.trajectorySoft         = None
        self.algorithm              = _integrator
        self.saveFormat             = None # binary file format to save the trajectory
        self.Nsteps                 = 20000 
        self.timeStep               = 0.001
        self.temperature            = 300.15
        self.pressureControl        = False
        self.samplingFactor         = 0
        self.logFreq                = 200
        self.seed                   = 3029202042
        self.softConstraint         = False # boolean flags signlizing whether the system has soft constraints or not              
        #Default constants less acessible by the users
        self.collFreq               = 25.0 
        self.pressureCoupling       = 2000.0       
        self.temperatureScaleFreq   = 10
        self.pressure               = 1.0   
        self.temperatureScaleOption = "linear"
        self.startTemperature       = 10  
        self.DEBUG                  = False             
        #Setting parameters based on information that we collected on the instance construction
        self.RNG                    = NormalDeviateGenerator.WithRandomNumberGenerator ( RandomNumberGenerator.WithSeed ( self.seed ) )
        if not os.path.exists(_baseFolder): os.makedirs(_baseFolder)
    #===============================================================================    
    def ChangeDefaultParameters(self,_parameters):
        '''
        Class method to set more specifc parameters.           
        '''     
        if "temperature"                in _parameters: self.temperature            = _parameters["temperature"]   
        if "start_temperature"          in _parameters: self.startTemperature       = _parameters["start_temperature"]
        if "coll_freq"                  in _parameters: self.collFreq               = _parameters["coll_freq"]
        if "pressure"                   in _parameters: self.pressure               = _parameters["pressure"]
        if "pressure_coupling"          in _parameters: self.pressureCoupling       = _parameters["pressure_coupling"] 
        if "temperature_scale"          in _parameters: self.temperatureScaleFreq   = _parameters["temperature_scale"]
        if "timeStep"                   in _parameters: self.timeStep               = _parameters["timeStep"]
        if "sampling_factor"            in _parameters: self.samplingFactor         = _parameters["sampling_factor"]
        if "log_frequency"              in _parameters: self.logFrequency           = _parameters["log_frequency"]
        if "temperature_scale_option"   in _parameters: self.temperatureScaleOption = _parameters["temperature_scale_option"]
        if "Debug"                      in _parameters: self.DEBUG                  = _parameters["Debug"]
        if "seed"                       in _parameters:
            self.seed = _parameters["seed"]
            self.RNG  = NormalDeviateGenerator.WithRandomNumberGenerator ( RandomNumberGenerator.WithSeed ( self.seed ) )
    #=============================================================================================    
    def HeatingSystem(self,_nsteps,_samplingFactor):
        '''
        Run a Velocity Verlet molecular dynamics simulation to gradually 
        make the system reach certain temperature. 
        '''
        self.nsteps             = _nsteps
        self.trajectoryNameCurr = os.path.join(self.baseName,self.trajName+"heating.ptGeo")  
        self.trajectory         = ExportTrajectory( self.trajectoryNameCurr, self.molecule,log=None )
        self.samplingFactor     = _samplingFactor
        #---------------------------------------------------------------------------------------------
        if not os.path.exists( self.trajectoryNameCurr ): os.makedirs( self.trajectoryNameCurr )
        #---------------------------------------------------------------------------------------------
        VelocityVerletDynamics_SystemGeometry(self.molecule                                                      ,
                                              logFrequency              = self.logFreq                           ,
                                              normalDeviateGenerator    = self.RNG                               ,
                                              steps                     = self.nsteps                            ,
                                              timeStep                  = self.timeStep                          ,
                                              trajectories              = [(self.trajectory,self.samplingFactor)],
                                              temperatureScaleFrequency = self.temperatureScaleFreq              ,
                                              temperatureScaleOption    = self.temperatureScaleOption            ,
                                              temperatureStart          = self.startTemperature                  ,
                                              temperatureStop           = self.temperature                       )            
    #===============================================================================================    
    def RunProduction(self,_prodSteps,_samplingFactor,_Restricted=False):
        '''
        Run a molecular dynamics simulation for data collection.
        '''
        self.softConstraint     = _Restricted
        self.nsteps             = _prodSteps
        self.samplingFactor     = _samplingFactor

        self.trajectory = ExportTrajectory( self.trajectoryNameCurr, self.molecule, log=None )
        if not os.path.exists( self.trajectoryNameCurr ): os.makedirs( self.trajectoryNameCurr )
        if _Restricted: 
            self.trajectorySoft = ExportTrajectory( self.trajectoryNameSoft, self.molecule, log=None )
            if not os.path.exists( self.trajectoryNameSoft ): os.makedirs( self.trajectoryNameSoft )
        if   self.DEBUG: self.Print()        
        if   self.algorithm == "Verlet":      self.runVerlet()
        elif self.algorithm == "LeapFrog":    self.runLeapFrog()
        elif self.algorithm == "Langevin":    self.runLangevin()       
    #===================================================================================================
    def runVerlet(self):
        '''
        Execute velocity verlet molecular dynamics from pDynamo methods. 
        '''
        trajectory_list = [( self.trajectory, self.samplingFactor)]
        if   self.softConstraint and self.samplingFactor >  0:  trajectory_list = [ ( self.trajectory, self.samplingFactor ), (self.trajectorySoft, 1) ]
        elif self.softConstraint and self.samplingFactor == 0:  trajectory_list = [ (self.trajectorySoft, 1) ]  
        VelocityVerletDynamics_SystemGeometry(  self.molecule                                           ,
                                                logFrequency                = self.logFreq              ,
                                                normalDeviateGenerator      = self.RNG                  ,
                                                steps                       = self.nsteps               ,
                                                timeStep                    = self.timeStep             ,
                                                temperatureScaleFrequency   = self.temperatureScaleFreq ,
                                                temperatureScaleOption      = "constant"                ,
                                                trajectories                = trajectory_list           ,
                                                temperatureStart            = self.temperature          )

    #====================================================================================================
    def runLeapFrog(self):
        '''
        Execute Leap Frog molecular dynamics from pDynamo methods.
        '''
        #--------------------------------------------------------------------------------
        trajectory_list = [( self.trajectory, self.samplingFactor)]
        if   self.softConstraint and self.samplingFactor >  0:  trajectory_list = [ ( self.trajectory, self.samplingFactor ), (self.trajectorySoft, 1) ]
        elif self.softConstraint and self.samplingFactor == 0:  trajectory_list = [ (self.trajectorySoft, 1) ]
        LeapFrogDynamics_SystemGeometry(self.molecule                                   ,
                                        trajectories            = trajectory_list       ,
                                        logFrequency            = self.logFreq          ,
                                        normalDeviateGenerator  = self.RNG              ,
                                        pressure                = self.pressure         ,
                                        pressureCoupling        = self.pressureCoupling ,
                                        steps                   = self.nsteps           ,
                                        timeStep                = self.timeStep         ,
                                        temperatureControl      = True                  ,
                                        temperature             = self.temperature      , 
                                        temperatureCoupling     = 0.1                   ) 
    
    #======================================================================================
    def runLangevin(self):
        '''
        Execute Langevin molecular dynamics from pDynamo methods.
        '''
        #-----------------------------------------------------------------------------
        trajectory_list = [( self.trajectory, self.samplingFactor)]
        if   self.softConstraint and self.samplingFactor >  0:  trajectory_list = [ ( self.trajectory, self.samplingFactor ), (self.trajectorySoft, 1) ]
        elif self.softConstraint and self.samplingFactor == 0:  trajectory_list = [ (self.trajectorySoft, 1) ]
        LangevinDynamics_SystemGeometry ( self.molecule                             ,
                                          collisionFrequency     = self.collFreq    ,
                                          logFrequency           = self.logFreq     ,
                                          normalDeviateGenerator = self.RNG         ,
                                          steps                  = self.nsteps      ,
                                          temperature            = self.temperature ,
                                          timeStep               = self.timeStep    ,
                                          trajectories           = trajectory_list  )

    #=====================================================================================
    def Print(self):
        '''
        Print basic information and paremeters for the molecular dynamics.
        '''
        ps_time = self.nsteps * self.timeStep
        print( "Molecular Dynamics working folder:{}".format(self.baseName) )
        print( "Molecular Dynamics production trajectory folder:{}".format(self.trajectoryNameCurr) )
        print( "Simulation time (ps): {}".format(ps_time) )
        print( "Simulation steps (n): {}".format(self.nsteps) )
        print( "Frame save frequency: {}".format(self.samplingFactor) )
        print( "Selected Integrator:  {}".format(self.algorithm) )
        print( "temperature (K): {}".format(self.temperature) )
        if self.pressureControl:
            print( "Pressure control applied!")
            print( "Pressure (bar): {}".format(self.pressure) )
        if self.softConstraint:
            print( "Restrictions applied!")
            print( "Molecular Dynamics restraints trajectory folder:{}".format(self.trajectorySoft) )

#===============================================================================#
#. End of class MD =============================================================#
#===============================================================================#
       
    
    
