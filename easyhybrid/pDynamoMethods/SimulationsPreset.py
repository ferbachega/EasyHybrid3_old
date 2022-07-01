 #!/usr/bin/env python3
# -*- coding: utf-8 -*-

#FILE = SimulationsPreset.py

##############################################################
#-----------------...EasyHybrid 3.0...-----------------------#
#-----------Credits and other information here---------------#
##############################################################

#--------------------------------------------------------------
import os, glob, sys
import numpy as np
#--------------------------------------------------------------
VISMOL_HOME = os.environ.get('VISMOL_HOME')
HOME        = os.environ.get('HOME')
if not VISMOL_HOME == None: sys.path.append(os.path.join(VISMOL_HOME,"easyhybrid/pDynamoMethods") ) 
else:                       sys.path.append(os.path.join("/home/igorchem/easyhybrid/pDynamoMethods") ) 
#-----------------------------------------------------------------------------------------------------
#Loading own libraries
#-------------------------------------------------------------
from EnergyAnalysis     	import EnergyAnalysis
from TrajectoryAnalysis 	import TrajectoryAnalysis
#-------------------------------------------------------------
from GeometrySearcher 	    import GeometrySearcher
from RelaxedScan 			import SCAN
from MolecularDynamics  	import MD
from UmbrellaSampling  	    import US
from PotentialOfMeanForce   import PMF
from ReactionCoordinate 	import ReactionCoordinate
from EnergyRefinement	 	import EnergyRefinement
#--------------------------------------------------------------
#loading pDynamo Libraries
from pBabel                    import *                                     
from pCore                     import *
#---------------------------------------                                     
from pMolecule                 import *                              
from pMolecule.MMModel         import *
from pMolecule.NBModel         import *                                     
from pMolecule.QCModel         import *
#---------------------------------------
from pScientific               import *                                     
from pScientific.Arrays        import *                                     
from pScientific.Geometry3     import *                                     
from pScientific.RandomNumbers import *                                     
from pScientific.Statistics    import *
from pScientific.Symmetry      import *
#--------------------------------------                                    
from pSimulation               import *
#=============================================================
class Simulation:
	'''
	Class to set up preset simulations to be perfomed
	'''
	def __init__(self,_parameters):
		'''
		Deafault constructor
		'''
		self.molecule   = _parameters["active_system"]
		self.parameters = _parameters
		self.baseFolder = None
		if "folder" in self.parameters:			
			self.baseFolder = self.parameters["folder"]
			if not os.path.exists(self.parameters["folder"]):
				os.makedirs(self.parameters["folder"])		
	#=======================================================================
	def Execute(self):
		'''
		Function to call the class method to execute the preset simulation
		Mandatory keys:
			"simulation_type": Name of the simulation to execute
		'''		
		#-------------------------------------------------------------------------------------------------------------------------
		if 	 self.parameters["simulation_type"] == "Energy_Refinement": 			self.EnergyRefine()		
		elif self.parameters["simulation_type"] == "Geometry_Optimization":			self.GeometryOptimization()
		elif self.parameters["simulation_type"] == "Relaxed_Surface_Scan":	 		self.RelaxedSurfaceScan()
		elif self.parameters["simulation_type"] == "Molecular_Dynamics":			self.MolecularDynamics()	
		elif self.parameters["simulation_type"] == "Restricted_Molecular_Dynamics": self.RestrictedMolecularDynamics()
		elif self.parameters["simulation_type"] == "Umbrella_Sampling":				self.UmbrellaSampling()
		elif self.parameters["simulation_type"] == "PMF_Analysis":					self.PMFAnalysis()			
		elif self.parameters["simulation_type"] == "Normal_Modes":					self.NormalModes()		
		elif self.parameters["simulation_type"] == "Delta_Free_Energy":				self.DeltaFreeEnergy()		
		elif self.parameters["simulation_type"] == "NEB":							self.ReactionSearchers()		
		elif self.parameters["simulation_type"] == "SAW":							self.ReactionSearchers()		
		elif self.parameters["simulation_type"] == "Baker_Saddle":					self.ReactionSearchers()
		elif self.parameters["simulation_type"] == "Steep_Path_Searcher":			self.ReactionSearchers()				
		elif self.parameters["simulation_type"] == "Simulating_Annealing":			self.SimulatingAnnealing()		
		elif self.parameters["simulation_type"] == "Steered_Molecular_Dynamics":	self.SMD()		
		elif self.parameters["simulation_type"] == "Monte_Carlo":					self.MonteCarlo()				
		elif self.parameters["simulation_type"] == "Trajectory_Analysis":			self.TrajectoryPlots() 		
		elif self.parameters["simulation_type"] == "Energy_Plots":					self.EnergyPlots()
	#=================================================================================================================
	def EnergyRefine(self):
		'''
		Set up and execute energy refinement using a series of methods
		Mandatory keys in self.parameters:
			"xbins"			: Number of frames for first/only coordinate 
			"source_folder" : path of folder containing frames to refine 
			"folder"        : path to output logs and other results
			"charge"        : charge for QM region
			"multiplicity"  : multiplicity for QM region
			"Software"  	: engine used to calculate the energy refinement
		Optinal keys in self.parameters:
			"ybins" 		  : Number of frames for second coordinate
			"change_qc_region": Flag indicating the intention of modifying the QC regions
			"center"		  : The center of the new QC region
			"radius"		  : The radius from the center of the new QC region
			"orca_method"     : Energy method provided in ORCA (eg.: HF, b3lyp, mp2...)
			"basis"           : String containing the orca key for basis functions
			"NmaxThreads"     : Maximum number of virtual threads to be used by pymp
		'''
		_Restart      = False
		dimensions    = [0,0] 
		dimensions[0] =  self.parameters["xnbins"]
		nmaxthreads   = 1 
		_trajfolder   = "single"
		if "ynbins"        in self.parameters: dimensions[1] = self.parameters["ynbins"]
		if "restart"       in self.parameters: _Restart = self.parameters["restart"]
		if "NmaxThreads"   in self.parameters: nmaxthreads = self.parameters["NmaxThreads"]
		if "source_folder" in self.parameters: _trajfolder = self.parameters["source_folder"] 
		#------------------------------------------------------------------
		ER = EnergyRefinement(self.molecule  				,
							  _trajfolder  					,
							  self.parameters["folder"]     ,
							  dimensions                    ,
							  self.parameters["charge"]     ,
							  self.parameters["multiplicity"])
		#------------------------------------------------------------------
		if "change_qc_region" in self.parameters        : ER.ChangeQCRegion(self.parameters["center"],self.parameters["radius"])
		if 	 self.parameters["Software"] == "pDynamo"   : ER.RunInternalSMO(self.parameters["methods_lists"],nmaxthreads)
		elif self.parameters["Software"] == "pDynamoDFT": ER.RunInternalDFT(self.parameters["functional"],self.parameters["basis"],nmaxthreads)
		elif self.parameters["Software"] == "DFTBplus"  : ER.RunDFTB()
		elif self.parameters["Software"] == "ORCA"		: ER.RunORCA(self.parameters["orca_method"],self.parameters["basis"],nmaxthreads,_restart=_Restart)
		elif self.parameters["Software"] == "mopac" or self.parameters["Software"]=="MOPAC":
			_mopacKeyWords = ["AUX","LARGE"] 
			if "mopac_keywords" in self.parameters:
				for key in self.parameters["mopac_keywords"]: _mopacKeyWords.append(key)
			ER.RunMopacSMO(self.parameters["methods_lists"],_mopacKeyWords)
		#------------------------------------------------------------
		#===============================================================
		#Set plor parameters
		cnt_lines  	= 12
		crd1_label 	= "Reaction Coordinate #1"
		crd2_label 	= "Reaction Coordinate #2"
		xlim 		= [ 0, dimensions[0] ]
		ylim 		= [ 0, dimensions[1] ]
		show  		= False
		#check parameters for plot
		if "contour_lines" in self.parameters: cnt_lines  = self.parameters["contour_lines"]
		if "crd1_label"    in self.parameters: crd1_label = self.parameters["crd1_label"]
		if "crd2_label"    in self.parameters: crd2_label = self.parameters["crd2_label"]
		if "xlim_list"     in self.parameters: xlim       = self.parameters["xlim_list"]
		if "ylim_list"     in self.parameters: ylim 	  = self.parameters["ylim_list"]
		if "show" 		   in self.parameters: show       = self.parameters["show"]
		#------------------------------------------------------------
		ER.WriteLog()
		if dimensions[1] > 0: TYPE = "2DRef"
		else: TYPE = "1DRef"		
		EA = EnergyAnalysis(dimensions[0],dimensions[1],_type=TYPE)
		EA.ReadLog( os.path.join(ER.baseName,"energy.log") )
		#-------------------------------------------------------------
		if dimensions[1] > 0: EA.MultPlot2D(cnt_lines,crd1_label,crd2_label,xlim,ylim,show)
		else:
			if "methods_lists" in self.parameters:
				if len(self.parameters["methods_lists"]) > 1: 
					EA.MultPlot1D(crd1_label)
				else: 
					EA.Plot1D(crd1_label,xlim,show)
			else: 
				EA.Plot1D(crd1_label,xlim,show)

	#==================================================================
	def GeometryOptimization(self):
		'''
		Set up and execture the search of local minima for the system passed
		Mandatory keys in self.parameters:
			optimizer: name of the optimization algorithm					 
		Optinal keys:
			trajectory_name: name to save the trajectory
			maxIterations: maximum number of itetarions (integer) 
			log_frequency: log frequency  (integer)
			save_pdb     : whether to save the final coordinates in pdb format (boolean)
			save_format  : name of the extra binary file ( could be of the format: .dcd, .mdcrd ...) 
            save_frequency : save frame frequency  (integer)
			rmsGradient  : root mean square gradient tolerance ( float )						
		'''
		_Optimizer = "ConjugatedGradient"
		_traj_name = None
		if "optmizer" 		 in self.parameters: _Optimizer = self.parameters["optmizer"]
		if "trajectory_name" in self.parameters: _traj_name = self.parameters["trajectory_name"]
		Gopt = GeometrySearcher(self.molecule,self.baseFolder,_trajName=_traj_name)		
		Gopt.ChangeDefaultParameters(self.parameters)
		Gopt.Minimization(_Optimizer)
		Gopt.Finalize()
	#==================================================================
	def RelaxedSurfaceScan(self, plot = True):
		'''
		Set up and execute one/two-dimensional relaxed surface scans 
		By the defualt the PKLs were saved on a child folder from the base path passed in the parameters, named "ScanTraj.ptGeo"
		The trajectory can be saved as files of the formats allowed by pDynamo 3.0
		Mandatory keys in self.parameters:
			"ndim"      : number of reaction coordinates to be treated
			"ATOMS_RC1" : list of atoms indices of the first reaction coordinate
			"nSteps_RC1": integer indicating the number of steps to scan for the first reaction coordinate
		Condirional:
			"ATOMS_RC2" :list of atoms indices of the second reaction coordinate. Needed if "ndim = 2"
			"nSteps_RC2": integer indicating the number of steps to scan for the second reaction coordinate. Needed if "ndim = 2"
		Optinal   :
			"dminimum_RC1"    :parameter given from window
			"dminimum_RC2"    :parameter given from window
			"sigma_pk1pk3_rc1":parameter given from window
			"sigma_pk3pk1_rc1":parameter given from window
			"sigma_pk1pk3_rc2":parameter given from window
			"sigma_pk3pk1_rc2":parameter given from window
			"force_constant"  : Float indicating the constant value of energy penalty for the harmonic potential restriction function
			"force_constant_1": Specifies the force constant for the first reaction coordinate
			"force_constant_2": Specified the force constant for the second reaction coordinate
			"maxIterations"   : Number of maximum iteration for the geometry optimizations
			"rmsGradient"     : rms torlerance for the stop parameter
			"optimizer"       : string containing the optimizer algorithm to be used in geometry optimization
			"dincre_RC1"      : float with the step increment for the first reaction coordinate ( Warning! If not passed, 0.0 will be assumed )
			"dincre_RC2"      : float with the step increment for the second reaction coordinate
			"MC_RC1"          : bool indicating whether to set mass constrained restrictions for the first reaction coordinate 
			"MC_RC2"          : bool indicating whether to set mass constrained restrictions for the second reaction coordinate 
			"rc_type_1"       : string containing the type for the first reaction coordinate ( Distance or Dihedral ) 
			"rc_type_2"       : string containing the type for the second reaction coordinate ( Distance or Dihedral )
			"adaptative"      : bool indicating wheter to activate or not the adaptative scheme for two-dimensional scans
			"save_format"     : format in which the trajectory will be saved, works only for 1D scans 
			"log_frequency"   : parameter for geometry optimization runs
		All plot parameters are optionals. This dict can be passed as none, if so the plots will be perfomed with default parameters. 
			"contour_lines"   : integer indicating the number of contour lines to be used in two-dimensional plots
			"show":boolean indicating whether to display the plot before exiting. 
		'''
		#------------------------------------------------------------------
		#default varibales
		_Adaptative = False
		_Optmizer   = "ConjugatedGradient"
		MCR1 		= False
		MCR2 		= False
		rcType1     = "Distance"
		rcType2     = "Distance"
		nDims       = self.parameters['ndim']
		dincre1     = 0.0
		dincre2     = 0.0
		nRC2        = 0
		dminimum_RC1 = None
		dminimum_RC2 = None
		sigma_pk1pk3_rc1 = None
		sigma_pk3pk1_rc1 = None
		sigma_pk1pk3_rc2 = None
		sigma_pk3pk1_rc2 = None
		#checking parameters
		if "dincre_RC1"       in self.parameters: dincre1 	       = self.parameters["dincre_RC1"]
		if "dincre_RC2"       in self.parameters: dincre2 	       = self.parameters["dincre_RC2"]	
		if "nsteps_RC2"       in self.parameters: nRC2  	       = self.parameters["nsteps_RC2"]
		if "optmizer"         in self.parameters: _Optmizer        = self.parameters["optmizer"]
		if "adaptative"       in self.parameters: _Adaptative      = self.parameters["adaptative"] 
		if "MC_RC1"           in self.parameters: MCR1             = self.parameters["MC_RC1"]
		if "MC_RC2"           in self.parameters: MCR2             = self.parameters["MC_RC2"]		
		if "rc_type_1"        in self.parameters: rcType1 	       = self.parameters["rc_type_1"]
		if "rc_type_2"     	  in self.parameters: rcType2 	       = self.parameters["rc_type_2"]
		if "dminimum_RC1" 	  in self.parameters: dminimum_RC1     = self.parameters["dminimum_RC1"] 	
		if "dminimum_RC2" 	  in self.parameters: dminimum_RC2     = self.parameters["dminimum_RC2"] 
		if "sigma_pk1pk3_rc1" in self.parameters: sigma_pk1pk3_rc1 = self.parameters["sigma_pk1pk3_rc1"]
		if "sigma_pk3pk1_rc1" in self.parameters: sigma_pk3pk1_rc1 = self.parameters["sigma_pk3pk1_rc1"]	
		if "sigma_pk1pk3_rc2" in self.parameters: sigma_pk1pk3_rc2 = self.parameters["sigma_pk1pk3_rc2"]
		if "sigma_pk3pk1_rc2" in self.parameters: sigma_pk3pk1_rc2 = self.parameters["sigma_pk3pk1_rc2"]
		#--------------------------------------------------------------------
		scan = SCAN(self.molecule,self.baseFolder,_Optmizer,ADAPTATIVE=_Adaptative)
		scan.ChangeDefaultParameters(self.parameters)	
		#--------------------------------------------------------------------
		rc1 = ReactionCoordinate( self.parameters["ATOMS_RC1"], MCR1, _type=rcType1 )
		rc1.GetRCLabel(self.molecule)
		rc1.SetInformation(self.molecule,dincre1,_dminimum=dminimum_RC1,_sigma_pk1_pk3=sigma_pk1pk3_rc1,_sigma_pk3_pk1=sigma_pk3pk1_rc1)
		scan.SetReactionCoord(rc1)
		rc2 = None
		if nDims == 2:
			rc2 = ReactionCoordinate( self.parameters["ATOMS_RC2"], MCR2, _type=rcType2 )
			rc2.GetRCLabel(self.molecule)
			rc2.SetInformation(self.molecule,dincre2,_dminimum=dminimum_RC2,_sigma_pk1_pk3=sigma_pk1pk3_rc2,_sigma_pk3_pk1=sigma_pk3pk1_rc2)
			scan.SetReactionCoord(rc2)
			scan.Run2DScan(self.parameters["nsteps_RC1"], self.parameters["nsteps_RC2"] )
		else: scan.Run1DScan(self.parameters["nsteps_RC1"])		
		scan.Finalize()		
		
		#============================ P L O T ============================
		if plot:
			#Set plot parameters
			cnt_lines 	= 12
			crd1_label	= rc1.label
			crd2_label	= ""
			show 		= False
			if nDims == 2: crd2_label = rc2.label
			#check parameters for plot
			if "contour_lines" 	in self.parameters: cnt_lines = self.parameters["contour_lines"]			
			if "show" 			in self.parameters: show 	  = self.parameters["show"] 
			#------------------------------------------------------------
			if 	 nDims 	== 2: TYPE = "2D"
			elif nDims 	== 1: TYPE = "1D"	
			#------------------------------------------------------------		
			EA = EnergyAnalysis(self.parameters['nsteps_RC1'],nRC2,_type=TYPE)
			EA.ReadLog( os.path.join(scan.baseName,scan.trajFolder+".log") ) 
			#-------------------------------------------------------------
			if 	 nDims == 2: EA.Plot2D(cnt_lines,crd1_label,crd2_label,show)
			elif nDims == 1: EA.Plot1D(crd1_label,show)		
		#=================================================================
	
	def MolecularDynamics(self):
		'''
		Set up and execute molecular dynamics simulations.:
		Mandatory keys in self.parameters:
			"MD_method"	 	 : string containing the integrator algorithm name
			"protocol" 		 : string indicating if is a normal run or for heating
			"nsteps"   		 : Number of steps to be taken in the simulation
			"trajectory_name":
		Optinal  :
			"temperature" 			  : float with the simulation temperature. If not passed we assume 300.15K as default.
			"coll_freq"  			  : integer with the colision frequency. Generally set for Langevin integrator. 
			"pressure"   			  : float with the simulation pressure. If not passed we assume 1.0bar as default.
			"pressure_coupling"		  : boolean indicating if is to control the simulation pressure.
			"temperature_scale_option": string with the type of temperature scaling. Default is 'linear' ( relevant for "heating" protocol)
			"temperature_scale"		  : float with the  temperature scaling step. Default is 10K  ( relevant for "heating" protocol)
			"start_temperatue"		  : float with the start temperature for heating protocol
			"timeStep"   			  : float indicating the size of integration time step. 0.001 ps is taken as default.					
			"sampling_factor"		  : integer indicating in which frequency to save/collect structure/data. default 0.
			"seed"					  : integer indicating the seed for rumdomness of the simulations.
			"log_frequency"     	  : integer indicating the frequency of the screen log output.
		plot parameters keys in self.parameters
			Optinal   :
			"show"					: whether to show the analysis plots in the simulation end.
			"calculate_distances"	: indicate if to calculate distances distributions of passed reaction coordinates
			"ATOMS_RC1"             : list of atoms for the first reaction coordinate to be analyzed 
			"ATOMS_RC2"             : list of atoms for the second reaction coordinate to be analyzed 
		'''		
		
		traj_name = "trajectory"
		if "trajectory_name" in self.parameters: traj_name = self.parameters["trajectory_name"]
		MDrun = MD(self.molecule,self.baseFolder,self.parameters['MD_method'],traj_name)		
		MDrun.ChangeDefaultParameters(self.parameters)
		sampling = 0 
		show = False
		if "sampling_factor" in self.parameters: sampling = self.parameters["sampling_factor"]
		#---------------------------------------------------------------
		if "protocol" in self.parameters:
			if   self.parameters["protocol"] == "heating":  MDrun.HeatingSystem(self.parameters['nsteps'],sampling)
			elif self.parameters["protocol"] == "sampling": MDrun.RunProduction(self.parameters['nsteps'],sampling)			
		#----------------------------------------------------------------
		if not self.parameters == None and sampling > 0:			
			RCs  = None
			if "show" in self.parameters: show = self.parameters["show"]
			t_time = self.parameters["nsteps"]*0.001
			DA = TrajectoryAnalysis(MDrun.trajectoryNameCurr,self.molecule,t_time)
			DA.CalculateRG_RMSD()
			DA.PlotRG_RMS(show)						
			if "calculate_distances" in self.parameters:
				if self.parameters["calculate_distances"] == True:
					rc1 = ReactionCoordinate(self.parameters["ATOMS_RC1"],False,0)
					rc1.GetRCLabel(self.molecule)
					RCs = [rc1]
					rc2 = None
					if "ATOMS_RC2" in self.parameters:
						rc2 = ReactionCoordinate(self.parameters["ATOMS_RC2"],False,0)						
						rc2.GetRCLabel(self.molecule)
						RCs.append(rc2)
					DA.DistancePlots(RCs,show)
	#==================================================================
	def RestrictedMolecularDynamics(self):
		'''
		Set up and execute molecular dynamics simulations.
		Mandatory  keys in self.parameters: 
			"ndim"                : integer indicating the number of restricted dimensions.
			"force_constant_1"    : float with the force constant applied for the harmonic potential in the first reaction coordinate
			"rc_type_1"           : string specifying the type of coordinate to be used for the first restricted dimension
			"rc_type_2"           : string specifying the type of coordinate to be used for the second restricted dimension
			"ATOMS_RC1"           : list with the atoms indices to set the first coordinate. 
			nsteps"               : number of moleculer dynamics steps to production run. 					
		Optinal keys in self.parameters :
			"dminimum_RC1"        :
			"dminimum_RC2"        :
			"sigma_pk1pk3_rc1"    :
			"sigma_pk3pk1_rc1"    :
			"sigma_pk1pk3_rc2"    :
			"sigma_pk3pk1_rc2"    :
			"ATOMS_RC2"           : list with the atoms indices to set the second coordinate. 
			"force_constant_2"    : float with the force constant applied for the harmonic potential in the second reaction coordinate
			"rc_type_2"           : string specifying the type of coordinate to be used for the second restricted dimension
			"temperature" 		  : float with the simulation temperature. If not passed we assume 300.15K as default.
			"coll_freq"  	      : integer with the colision frequency. Generally set for Langevin integrator. 
			"pressure"   		  : float with the simulation pressure. If not passed we assume 1.0bar as default.
			"pressure_coupling"	  : boolean indicating if is to control the simulation pressure.
			"timeStep"   		  : float indicating the size of integration time step. 0.001 ps is taken as default.
			"sampling_factor"     : integer with the save/sampling frequency of frames.
			"seed"				  : integer indicating the seed for rumdomness of the simulations.
			"log_frequency"       : integer indicating the frequency of the screen log output.
		plot parameters keys in self.parameters :
			"show"				  : whether to show the analysis plots in the simulation end.
			"calculate_distances" : whether to calculate and plot distribution analysis from the passed reaction coordinates										
		'''
		#----------------------------------------------------------------
		restraints = RestraintModel()
		self.molecule.DefineRestraintModel( restraints )
		sampling = 0 		
		MCR1 = False
		MCR2 = False
		dminimum_RC1 = None
		dminimum_RC2 = None
		sigma_pk1pk3_rc1 = None
		sigma_pk3pk1_rc1 = None
		sigma_pk1pk3_rc2 = None
		sigma_pk3pk1_rc2 = None

		if "MC_RC1" in self.parameters:	MCR1 = self.parameters["MC_RC1"]
		if "MC_RC2" in self.parameters:	MCR2 = self.parameters["MC_RC2"]

		if "sampling_factor" in self.parameters: sampling = self.parameters["sampling_factor"]
		#--------------------
		rcType1 = "Distance"
		rcType2 = "Distance"
		if "dminimum_RC1" 	  in self.parameters: dminimum_RC1     = self.parameters["dminimum_RC1"] 	
		if "dminimum_RC2" 	  in self.parameters: dminimum_RC2     = self.parameters["dminimum_RC2"] 
		if "sigma_pk1pk3_rc1" in self.parameters: sigma_pk1pk3_rc1 = self.parameters["sigma_pk1pk3_rc1"]
		if "sigma_pk3pk1_rc1" in self.parameters: sigma_pk3pk1_rc1 = self.parameters["sigma_pk3pk1_rc1"]	
		if "sigma_pk1pk3_rc2" in self.parameters: sigma_pk1pk3_rc2 = self.parameters["sigma_pk1pk3_rc2"]
		if "sigma_pk3pk1_rc2" in self.parameters: sigma_pk3pk1_rc2 = self.parameters["sigma_pk3pk1_rc2"]
		if "rc_type_1"        in self.parameters: rcType1          = self.parameters["rc_type_1"]
		if "rc_type_2"        in self.parameters: rcType2          = self.parameters["rc_type_2"]
		#-------------------------------------------------------------------
		restrainDimensions = self.parameters['ndim']
		forcK_1 = self.parameters["force_constant_1"]
		#-------------------------------------------------------------------
		rc1 = ReactionCoordinate(self.parameters["ATOMS_RC1"],MCR1,_type=rcType1)
		rc1.GetRCLabel(self.molecule)
		rc1.SetInformation(self.molecule,0.0,_dminimum=dminimum_RC1,_sigma_pk1_pk3=sigma_pk1pk3_rc1,_sigma_pk3_pk1=sigma_pk3pk1_rc1)
		nDims = self.parameters['ndim']
		rc2 = None
		if nDims == 2:
			rc2 = ReactionCoordinate(self.parameters["ATOMS_RC2"],MCR2,_type=rcType2)
			rc2.GetRCLabel(self.molecule)
			rc2.SetInformation(self.molecule,0.0,_dminimum=dminimum_RC2,_sigma_pk1_pk3=sigma_pk1pk3_rc2,_sigma_pk3_pk1=sigma_pk3pk1_rc2)
			forcK_2 = self.parameters["force_constant_2"]
		#-------------------------------------------------------------------
		distance = rc1.minimumD
		rmodel = RestraintEnergyModel.Harmonic( distance, forcK_1 )
		if rc1.nAtoms == 3:				
			restraint = RestraintMultipleDistance.WithOptions( energyModel=rmodel, distances=[ [ rc1.atoms[1], rc1.atoms[0], rc1.weight13 ], [ rc1.atoms[1], rc1.atoms[2], rc1.weight31 ] ] ) 
		elif rc1.nAtoms == 2:				
			restraint = RestraintDistance.WithOptions( energyModel=rmodel, point1=rc1.atoms[0], point2=rc1.atoms[1] )
		elif rc1.nAtoms == 4:
			rmodel = RestraintEnergyModel.Harmonic( distance, forcK_1, period = 360.0 )
			restraint = RestraintDihedral.WithOptions( energyModel=rmodel, point1=rc1.atoms[0],point2=rc1.atoms[1],point3=rc1.atoms[2],point4=rc1.atoms[3] )
		restraints['M1'] =  restraint
		#-------------------------------------------------------------------
		if nDims == 2:
			distance = rc2.minimumD
			rmodel = RestraintEnergyModel.Harmonic( distance, forcK_2 )
			if rc2.nAtoms == 3:				
				restraint = RestraintMultipleDistance.WithOptions( energyModel = rmodel, distances= [ [ rc2.atoms[1], rc2.atoms[0], rc2.weight13 ], [ rc2.atoms[1], rc2.atoms[2], rc2.weight31 ] ] ) 
			elif rc2.nAtoms == 2:				
				restraint = RestraintDistance.WithOptions( energyModel=rmodel, point1=rc2.atoms[0], point2=rc2.atoms[1] )
			elif rc2.nAtoms == 4:
				rmodel = RestraintEnergyModel.Harmonic( distance, forcK_2, period = 360.0 )
				restraint = RestraintDihedral.WithOptions( energyModel=rmodel, point1=rc2.atoms[0],point2=rc2.atoms[1],point3=rc2.atoms[2],point4=rc2.atoms[3] )	
			restraints['M2'] =  restraint		
		#----------------------------------------------------------------
		traj_name = "trajectory"
		if "trajectory_name" in self.parameters: traj_name = self.parameters["trajectory_name"]
		MDrun = MD(self.molecule,self.baseFolder,self.parameters['MD_method'],traj_name)
		MDrun.ChangeDefaultParameters(self.parameters)
		MDrun.RunProduction(self.parameters['nsteps'],sampling,_Restricted=True)
		#-----------------------------------------------------------------		
		if not self.parameters == None and sampling > 0 :
			t_time = self.parameters["nsteps"]*MDrun.timeStep
			show = False
			if "show" in self.parameters: show = self.parameters["show"]
			DA = TrajectoryAnalysis(MDrun.trajectoryNameCurr,self.molecule,t_time)
			DA.CalculateRG_RMSD()
			DA.PlotRG_RMS(show)				
			RCs = [rc1]
			if nDims > 1: RCs.append(rc2)							
			DA.DistancePlots(RCs,show)
			DA.ExtractFrames()
	#=======================================================================
	def UmbrellaSampling(self):
		'''
		Set up and execute umbrella sampling simulations and Free energy calculations for reaction path trajectory.
		Mandatory: 
			"ATOMS_RC1"           : List containing the indices of the atoms for the first restricted reaction coordinate
			"ndim"                : integer indicating the number of treated reaction coordinates
			"equilibration_nsteps": integer given the number of molecular dynamics simulation steps to be conducted before data collection
			"production_nsteps"   : integer given the number of molecular dynamics simulation steps to perform the data collection
			"MD_method"           : string with the integrator algorithm name
			"source_folder"       : string with the path which to find de coordinate files to initialize the simulation in each window
		Optinal :
			"dminimum_RC1"        :
			"dminimum_RC2"        :
			"sigma_pk1pk3_rc1"    :
			"sigma_pk3pk1_rc1"    :
			"sigma_pk1pk3_rc2"    :
			"sigma_pk3pk1_rc2"    :
			"ATOMS_RC2"       	  : List containing the indices of the atoms for the second restricted reaction coordinate
			"force_constant_1"	  : float with the force constant applied for the harmonic potential in the first reaction coordinate. Default is 600.0 KJ
			"force_constant_2"	  : float with the force constant applied for the harmonic potential in the second reaction coordinate. Default is 600.0 KJ
			"optimize"        	  : Boolean indicating if the geometry must be optimized before molecular dynamics 
			"restart"         	  : Boolean indicating if the calculations must continue from those .ptRes that were not generated yet.
			"adaptative"      	  : BOolean inficating the usage of an adaptative shceme for convergence parameters. (UNSTABLE and UNTESTED)
			"coordinate_format"   : string containing the format of input coordinate files e.g.: ".xyz", ".pdb" or ".pkl". if not passed ".pkl" will be assumed.
			"save_format"         : Save production molecular dynamics for one-dimensional runs. Must set a valid sampling factor. 
		#MD PARAMETERS
			"temperature" 		  : float with the simulation temperature. If not passed we assume 300.15K as default.
			"pressure"   		  : float with the simulation pressure. If not passed we assume 1.0bar as default.
			"pressure_coupling"	  : boolean indicating if is to control the simulation pressure.
			"timeStep"   		  : float indicating the size of integration time step. 0.001 ps is taken as default.
			"sampling_factor"     : integer with the save/sampling frequency of frames for the data collection step.
			"seed"				  : integer indicating the seed for rumdomness of the simulations.
			"log_frequency_md"    : integer indicating the frequency of the screen log output for the molecular dynamics runs.
		#OPTIMIZATION PARAMETERS
			"trajectory_name"     : name to save the trajectory
			"maxIterations"       : maximum number of itetarions (integer) 
			"log_frequency_OPT"   : log frequency  (integer)
			"save_pdb"            : whether to save the final coordinates in pdb format (boolean)
			"save_format_opt"     : name of the extra binary file ( could be of the format: .dcd, .mdcrd ...) 
			"rmsGradient"         : root mean square gradient tolerance ( float )
		'''
		#---------------------------------------
		MCR1 = False
		MCR2 = False		
		rcType1 = "Distance"
		rcType2 = "Distance"
		#---------------------------------------
		if "MC_RC1" in self.parameters: MCR1 = True
		if "MC_RC2" in self.parameters:	MCR2 = True
		#---------------------------------------
		_Restart 	     = False
		_Adaptative      = False
		_Optimize        = False
		_crdFormat       = ".pkl"
		sampling         = 0
		dminimum_RC1     = None
		dminimum_RC2     = None
		sigma_pk1pk3_rc1 = None
		sigma_pk3pk1_rc1 = None
		sigma_pk1pk3_rc2 = None
		sigma_pk3pk1_rc2 = None
		#-------------------------------------------------------------------------------------------
		if "dminimum_RC1" 	   in self.parameters: dminimum_RC1     = self.parameters["dminimum_RC1"] 	
		if "dminimum_RC2" 	   in self.parameters: dminimum_RC2     = self.parameters["dminimum_RC2"] 
		if "sigma_pk1pk3_rc1"  in self.parameters: sigma_pk1pk3_rc1 = self.parameters["sigma_pk1pk3_rc1"]
		if "sigma_pk3pk1_rc1"  in self.parameters: sigma_pk3pk1_rc1 = self.parameters["sigma_pk3pk1_rc1"]	
		if "sigma_pk1pk3_rc2"  in self.parameters: sigma_pk1pk3_rc2 = self.parameters["sigma_pk1pk3_rc2"]
		if "sigma_pk3pk1_rc2"  in self.parameters: sigma_pk3pk1_rc2 = self.parameters["sigma_pk3pk1_rc2"]
		if "restart" 	 	   in self.parameters: _Restart         = self.parameters["restart"]
		if "adaptative"  	   in self.parameters: _Adaptative      = self.parameters["adaptative"]
		if "optimize"          in self.parameters: _Optimize        = self.parameters["optimize"]
		if "coordinate_format" in self.parameters: _crdFormat       = self.parameters["coordinate_format"]
		if "sampling_factor"   in self.parameters: sampling         = self.parameters["sampling_factor"]
		#------------------------------------------------------------------
		rc1 = ReactionCoordinate(self.parameters["ATOMS_RC1"],MCR1,_type=rcType1)
		rc1.GetRCLabel(self.molecule)
		rc1.SetInformation(self.molecule,0.0,_dminimum=dminimum_RC1,_sigma_pk1_pk3=sigma_pk1pk3_rc1,_sigma_pk3_pk1=sigma_pk3pk1_rc1)
		
		nDims = self.parameters['ndim']
		rc2 = None
		if nDims == 2:
			rc2 = ReactionCoordinate(self.parameters["ATOMS_RC2"],MCR2,_type=rcType2)
			rc2.GetRCLabel(self.molecule)
			rc2.SetInformation(self.molecule,0.0,_dminimum=dminimum_RC2,_sigma_pk1_pk3=sigma_pk1pk3_rc2,_sigma_pk3_pk1=sigma_pk3pk1_rc2)
		#---------------------------------------
		USrun = US(self.molecule  						  ,
			       self.baseFolder 						  ,
			       self.parameters["equilibration_nsteps"],
			       self.parameters["production_nsteps"]   ,
			       self.parameters["MD_method"]           ,
			       RESTART=_Restart                       ,
			       ADAPTATIVE=_Adaptative                 ,
			       OPTIMIZE=_Optimize                     )
		#---------------------------------------
		USrun.ChangeDefaultParameters(self.parameters)
		USrun.SetMode(rc1)
		if self.parameters["ndim"]   == 1: 
			USrun.Run1DSampling(self.parameters["source_folder"],_crdFormat,sampling)
		elif self.parameters["ndim"] == 2:
			USrun.SetMode(rc2)
			USrun.Run2DSampling(self.parameters["source_folder"],_crdFormat,sampling)
		#---------------
		USrun.Finalize()		
	#=========================================================================
	def PMFAnalysis(self):
		'''
		Calculate potential of mean force and Free energy from restricted molecular dynamics
		Mandatory keys: 
			"source_folder"	:
			"xbins"			:
			"ybins"			:
			"temperature"	:
		Optinal keys        :
		plot keys           :				
		'''
		ynbins = 0 
		if "ynbins" in self.parameters: ynbins = self.parameters["ynbins"]
		potmean = PMF( self.molecule, self.parameters["source_folder"], self.baseFolder )
		potmean.CalculateWHAM(self.parameters["xnbins"],ynbins,self.parameters["temperature"])
		#================================================================
		#Set default plot parameters
		cnt_lines  = 12
		crd1_label = ""
		crd2_label = ""
		nRC2       = ynbins
		show       = False
		xwin       = 0
		ywin       = 0 
		#-----------------------------------------------------------------
		nDims = 1
		if ynbins > 0: nDims = 2
		xlims = [ 0,  self.parameters['xnbins'] ]
		ylims = [ 0,  ynbins ]
		OneDimPlot = False
		#-------------------------------------------------------------
		#check parameters for plot
		if "contour_lines" 	in self.parameters: cnt_lines  = self.parameters["contour_lines"]		
		if "xlim_list" 		in self.parameters: xlims 	   = self.parameters["xlim_list"]
		if "ylim_list" 		in self.parameters:	ylims 	   = self.parameters["ylim_list"]
		if "show" 			in self.parameters:	show 	   = self.parameters["show"]
		if "crd1_label" 	in self.parameters:	crd1_label = self.parameters["crd1_label"]
		if "crd2_label" 	in self.parameters:	crd2_label = self.parameters["crd2_label"]
		if "xwindows" 		in self.parameters: xwin 	   = self.parameters["xwindows"]
		if "ywindows" 		in self.parameters:	ywin 	   = self.parameters["ywindows"]
		if "oneDimPlot"     in self.parameters: OneDimPlot = self.parameters["oneDimPlot"]
		#------------------------------------------------------------
		if   nDims == 2: TYPE = "WHAM2D"
		elif nDims == 1: TYPE = "WHAM1D"	
		#------------------------------------------------------------
		# Plot PMF graphs
		EA = EnergyAnalysis(self.parameters['xnbins'],nRC2,_type=TYPE)
		EA.ReadLog( os.path.join(potmean.baseName,"PotentialOfMeanForce.dat") ) 
		#-------------------------------------------------------------
		if   nDims == 2: EA.Plot2D(cnt_lines,crd1_label,crd2_label,xlims,ylims,show)
		elif nDims == 1: EA.Plot1D(crd1_label,SHOW=show)
		#-------------------------------------------
		#Plot Free energy of the calculated windows
		if 	 OneDimPlot == True: TYPE = "FE1D"
		elif nDims 		== 2: 	 TYPE = "FE2D"
		elif nDims 		== 1: 	 TYPE = "FE1D"

		xlims = [ np.min(EA.RC1), np.max(EA.RC1) ]

		if nDims  == 2:  ylims = [ np.min(EA.RC2), np.max(EA.RC2) ]	
		#------------------------------------------
		EAfe = EnergyAnalysis(xwin,ywin,_type=TYPE)
		EAfe.ReadLog( os.path.join(potmean.baseName,"FreeEnergy.log") ) 
		#-------------------------------------------------------------
		if nDims == 2: 
			if OneDimPlot: EAfe.Plot1D_FreeEnergy(crd1_label,crd2_label,show)
			else 		 : EAfe.Plot2D(cnt_lines,crd1_label,crd2_label,xlims,ylims,show)
		elif nDims == 1: EAfe.Plot1D(crd1_label,XLIM=xlims,SHOW=show)
	#=========================================================================
	def NormalModes(self):
		'''
		Simulation preset to calculate the normal modes and to write thr trajectory for a specific mode.
		Mandatory keys in self.parameters:

		Optinal keys in self.parameters  : 
			
		'''	
		mode 		= 0
		temperature = 300.15
		Cycles 		= 10 
		Frames  	= 10 
		#-------------------------------
		if "temperature" in self.parameters: temperature = self.parameters["temperature"]
		if "cycles" 	 in self.parameters: Cycles 	 = self.parameters["cycles"]
		if "frames" 	 in self.parameters: Frames 	 = self.parameters["frames"]
		if "mode" 	 	 in self.parameters: mode   	 = self.parameters["mode"]
		#-------------------------------
		NormalModes_SystemGeometry ( self.molecule, modify = ModifyOption.Project )
		if _mode > 0:
			trajectory = ExportTrajectory ( os.path.join (self.baseFolder, "NormalModes","ptGeo"), self.molecule )
			NormalModesTrajectory_SystemGeometry(	self.molecule		      ,
                                       			 	trajectory                ,
                                       				mode        = _mode	      ,
                                       				cycles      = Cycles      ,
                                       				frames      = Frames 	  ,
                                       				temperature = temperature )
	#==========================================================================
	def DeltaFreeEnergy(self):
		'''
		Calculate the free energy difference between two configurations of the system using the 
		statistical thermodynamics partition functions from through the normal modes calculations
		Mandatory keys:
		Optional keys :
		'''		
		#initial Structure
		pressure       = 1.0
		temperature    = 300.15 
		symmetryNumber = 1

		if "pressure" in self.parameters: pressure = self.parameters["pressure"]

		self.molecule.coordinates3 = ImportCoordinates3(self.parameters["initial_coordinates"])
		e0 = self.molecule.Energy()
		NormalModes_SystemGeometry( self.molecule, modify = ModifyOption.Project )
		Gibbs = [] 
		tdics = ThermodynamicsRRHO_SystemGeometry ( self.molecule 							,
                                                    pressure       = pressure       	,
                                                    symmetryNumber = self.symmetryNumber 	,
                                                    temperature    = self.temperature    	)
		Gibbs.append( tdics["Gibbs Free Energy"] )
    	# Final struct
		self.molecule.coordinates3 = ImportCoordinates3(self.parameters["final_coordinates"])
		e1 = self.molecule.Energy()
		NormalModes_SystemGeometry ( self.molecule, modify = ModifyOption.Project )
    	 
		tdics = ThermodynamicsRRHO_SystemGeometry ( self.molecule 							,
                                                    pressure       = self.pressure       	,
                                                    symmetryNumber = self.symmetryNumber 	,
                                                    temperature    = self.temperature    	)
		Gibbs.append( tdics["Gibbs Free Energy"] )
	#=========================================================================	
	def ReactionSearchers(self):
		'''
		Class method to set up and execute Nudget Elastic Band simulations to generate a reaction path trajectory
		Mandatory keys in self.parameters:
			"NEB_bins"  : Number of points in the NEB trajectory
			"init_coord":
			"final_coord":

		Optional keys in self.parameters:
			"spring_force_constant"    :
			"fixed_terminal_images"    :
			"RMS_growing_intial_string":
			"refine_methods"           : 
			"crd1_label"               :
			"show"                     :
			"xlim_list"                :
		'''


		_traj_name = "ReactionPath"
		if "trajectory_name" in self.parameters: _traj_name = self.parameters["trajectory_name"]
		RSrun = GeometrySearcher(self.molecule,self.baseFolder,_trajName=_traj_name)		
		RSrun.ChangeDefaultParameters(self.parameters)		

		if   self.parameters["simulation_type"] == "NEB"                : RSrun.NudgedElasticBand(self.parameters)
		elif self.parameters["simulation_type"] == "SAW"                : RSrun.SelfAvoidWalking(self.parameters)
		elif self.parameters["simulation_type"] == "SteepDescent_path"  : RSrun.SteepestDescentPathSearch(self.parameters)
		elif self.parameters["simulation_type"] == "Baker_Saddle"       : RSrun.BakerSaddleOptimizer(self.parameters) 

		
		nmaxthreads = 1
		if "NmaxThreads" in self.parameters: nmaxthreads = self.parameters["NmaxThreads"]

		refMethod = []
		if "refine_methods" in self.parameters: refMethod = self.parameters["refine_methods"]
		if len(refMethod) > 0: 
			ER = EnergyRefinement(self.molecule  					        ,
								  RSrun.trajectoryName                      ,
								  self.baseFolder                           ,
								  [self.parameters["traj_bins"],0]          ,
								  self.molecule.electronicState.charge      ,
								  self.molecule.electronicState.multiplicity)
			ER.RunInternalSMO(refMethod,nmaxthreads)
			ER.WriteLog()
			crd1_label 	= "Reaction Coordinate #1"
			xlim 		= [ 0, self.parameters["traj_bins"] ]
			show  		= False
			#check parameters for plot
			if "crd1_label" in self.parameters: crd1_label = self.parameters["crd1_label"]
			if "xlim_list"  in self.parameters: xlim       = self.parameters["xlim_list"]
			if "show" 		in self.parameters: show       = self.parameters["show"]
			#------------------------------------------------------------				
			EA = EnergyAnalysis(self.parameters["traj_bins"],1,_type="1DRef")
			EA.ReadLog( os.path.join(ER.baseName,"energy.log") )
			EA.MultPlot1D(crd1_label,show)	
			RSrun.Finalize()
	#=========================================================================	
	def TrajectoryPlots(self) :
		'''
		Mandatory keys in self.parameters:
		Optional keys in self.parameters:
		'''
		
		pass
	#=========================================================================
	def EnergyPlots(self):
		'''
		Produce Energy plots from previus simulations log files
		Mandatory keys in self.parameters:
		Optional keys in self.parameters:
		'''		
		multiPlot = False
		ndim      = 1 
		crd1_label= "Reaction Coordinate #1"
		crd2_label= "Reaction Coordinate #2"
		cnt_lines = 0 
		ysize     = 0
		if "ysize" in self.parameters: ysize = self.parameters["ysize"]
		xlim      = [ 0, self.parameters["xsize"] ]
		ylim 	  = [ 0, ysize ]
		show 	  = False
		#--------------------------------------------------------
		if "contour_lines" 	in self.parameters: cnt_lines  = self.parameters["contour_lines"]
		if "crd1_label" 	in self.parameters: crd1_label = self.parameters["crd1_label"]
		if "crd2_label" 	in self.parameters:	crd2_label = self.parameters["crd2_label"]
		if "xlim_list" 		in self.parameters: xlim  	   = self.parameters["xlim_list"]
		if "ylim_list" 		in self.parameters: ylim       = self.parameters["ylim_list"]
		if "show" 			in self.parameters: show       = self.parameters["show"]
		if "multiple_plot" 	in self.parameters: multiPlot  = self.parameters["multiple_plot"]		
		if ysize > 0: ndim = 2
		if "log_names" in self.parameters: multiPlot = True 
		#--------------------------------------------------------
		EA = EnergyAnalysis(self.parameters["xsize"],ysize,_type=self.parameters["type"] )
		if multiPlot:
			for log in self.parameters["log_names"]:
				EA.ReadLog( log )
				EA.MultPlot1D()
		else:	EA.ReadLog( self.parameters["log_name"] )
		#--------------------------------------------------------
		if 	 ndim == 1: EA.Plot1D(crd1_label,XLIM=xlim,SHOW=show)
		elif ndim == 2:	EA.Plot2D(cnt_lines,crd1_label,crd2_label,xlim,ylim,show)
	#=========================================================================
	def MonteCarlo(self):
		pass
	
	#=========================================================================
	def SimulatingAnnealing(self):
		'''
		Set up and execute Simulate annealing simulations	
		Mandatory keys in self.parameters:
		Optional keys in self.parameters:	
		'''
		pass
	#=========================================================================
	def SMD(self):
		'''
		Set up and execute Steered Molecular Dynamics simulations
		Mandatory keys in self.parameters:
		Optional keys in self.parameters:
		'''
		pass
	#=========================================================================	
	def Print(self):
		'''
		Printing information of the simulations that will be run.
		'''
		print("Simulation Type: {}".format(self.parameters["simulation_type"]) )
		print("Working folder: {}".format(self.parameters["folder"]) )

#=============================================================================
#========================END OF THE FILE======================================
#=============================================================================
