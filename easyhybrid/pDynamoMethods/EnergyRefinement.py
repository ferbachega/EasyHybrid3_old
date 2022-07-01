#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#FILE = EnergyRefinement.py

##############################################################
#-----------------...EasyHybrid 3.0...-----------------------#
#-----------Credits and other information here---------------#
##############################################################

#================================
import pymp
from commonFunctions import *
from pMolecule import *
from pMolecule.QCModel import *
from MopacQCMMinput import *
import os, glob, sys, shutil
import numpy as np 

from pMolecule import * 

from pSimulation import *
#================================
#**********************************************************
class EnergyRefinement:
	'''
	Energy calculations for a set of structures using several QC methods and or External softwares
	'''
	def __init__(self,_refSystem,_trajFolder,_outFolder,_dims,_chg,_mult):
		'''
		Default constructor.
		Parameters:
			_refSystem : reference molecular information; System pDynamo class instance
			_trajFolder: folder path of the structures; string or path
			_outFolder : folder path where the results will be written; string or path
			_dims      : reaction coordinates size; list of integers
			_chg       : reference QC region charge; integer
			_multi     : reference QC region multiplicity; integer
		'''
		self.molecule 	 = _refSystem
		self.trajFolder  = _trajFolder  
		self.pureQCAtoms = []
		self.RC1 	 	 = []
		self.RC2 		 = []
		self.rc1CoordName= []
		self.rc2CoordName= []
		self.restart     = False
		self.xlen        = _dims[0]
		self.ylen        = _dims[1]
		self.charge 	 = _chg
		self.multiplicity= _mult
		self.text 		 = ""
		self.methods 	 = []
		self.fileLists   = []
		
		if hasattr(self.molecule,"qcState"): 
			self.pureQCAtoms = list(self.molecule.qcState.pureQCAtoms)
		i = 0
		self.baseName = _outFolder	
		if not os.path.exists(self.baseName): os.makedirs(self.baseName)
		if self.xlen > 1:
			_path = os.path.join( _trajFolder,"")
			self.fileLists  = glob.glob(_path + "frame*.pkl")			
		elif self.xlen == 1:
			self.fileLists.append(_trajFolder+".pkl")		
		#----------------------------------------------------------------------
		if self.ylen  == 0:
			self.energiesArray = pymp.shared.array( (self.xlen) , dtype='float')
			self.indexArrayX   = pymp.shared.array( (self.xlen) , dtype='uint8')
			self.indexArrayY   = pymp.shared.array( (self.xlen) , dtype='uint8')
		else:
			self.energiesArray = pymp.shared.array( (self.ylen,self.xlen) , dtype='float')
			self.indexArrayX   = pymp.shared.array( (self.ylen,self.xlen) , dtype='uint8')
			self.indexArrayY   = pymp.shared.array( (self.ylen,self.xlen) , dtype='uint8')
		self.SMOenergies   = None
	
	#=====================================================================================
	def GetQCCharge(self,_system):
		'''
		'''
		qc_charge=0.0
		mmCharges = _system.mmState.charges
		for i in range(len(mmCharges)): qc_charge += mmCharges[i]			
		return( round(qc_charge) )
	#=====================================================================================
	def ChangeQCRegion(self,_centerAtom,_radius,_crd3=None):
		'''
		Redefine QC selection from a given atomic coordinates with a certain radius
		Parameters:
			_centerAtom:
			_radius    :
		'''
		if type(_centerAtom) == list:  
			atom_list = [] 		
			for i in self.molecule.atoms.items:
				x    = self.molecule.coordinates3[i.index, 0] 
				y    = self.molecule.coordinates3[i.index, 1]
				z    = self.molecule.coordinates3[i.index, 2]
				xd   = (x-_centerAtom[0])**2
				yd   = (y-_centerAtom[1])**2
				zd   = (z-_centerAtom[2])**2
				dist = np.sqrt( xd+yd+zd ) 
				if dist < _radius:
					atom_list.append(i.index)

			sel              = Selection.FromIterable(atom_list)
			newSelection 	 = AtomSelection.ByComponent(self.molecule,sel)
			newSystem    	 = PruneByAtom(self.molecule, Selection(newSelection) )		
			self.charge  	 = self.GetQCCharge(newSystem)
			self.pureQCAtoms = list(newSelection)	
			qcModel          = None
			if self.molecule.qcModel == None:
				qcModel = QCModelMNDO.WithOptions( hamiltonian = "am1" )
			else: qcModel = self.molecule.qcModel
			#-------------------------------------------------------------------------------
			self.molecule.electronicState = ElectronicState.WithOptions( charge = self.charge, multiplicity = self.multiplicity )
			self.molecule.DefineQCModel(qcModel, qcSelection=Selection(self.pureQCAtoms) )
			self.molecule.Summary()			

		#-------------------------------------------------------------------
		else:
			sel              = Selection.FromIterable([_centerAtom])
			newSelection  	 = AtomSelection.Within(self.molecule,sel,_radius)
			newSelection 	 = AtomSelection.ByComponent(self.molecule,newSelection)
			newSystem    	 = PruneByAtom(self.molecule, Selection(newSelection) )		
			self.charge  	 = self.GetQCCharge(newSystem)
			self.pureQCAtoms = list(newSelection)	
			qcModel          = None
			if self.molecule.qcModel == None:
				qcModel = QCModelMNDO.WithOptions( hamiltonian = "am1" )
			else: qcModel = self.molecule.qcModel
			#-------------------------------------------------------------------------------
			self.molecule.electronicState = ElectronicState.WithOptions( charge = self.charge, multiplicity = self.multiplicity )
			self.molecule.DefineQCModel(qcModel, qcSelection=Selection(self.pureQCAtoms) )
			self.molecule.Summary()		
        	#---------------------------------------------------
        
	#=====================================================================================
	def RunInternalSMO(self,_methods,_NmaxThreads):
		'''
		Run energy refinement with the semiempirical hamiltonians available wihthin pDynamo
		Parameters:
			_methods:     List of Hamiltoninas
			_NmaxThreads: Number of maximum threds to be used in the parallel section
		'''
		self.SMOenergies = {}
		self.methods 	 = _methods
		NBmodel 	 	 = self.molecule.nbModel
		converger = DIISSCFConverger.WithOptions( energyTolerance   = 1.0e-4,
                                                  densityTolerance  = 1.0e-6,
                                                  maximumIterations = 500   )
		#--------------------------------------------------------------------
		for smo in _methods:
			if VerifyMNDOKey(smo):
				with pymp.Parallel(_NmaxThreads) as p:
					for i in p.range( len(self.fileLists) ):
						qcModel = QCModelMNDO.WithOptions( hamiltonian = smo,converger=converger )
						self.molecule.electronicState = ElectronicState.WithOptions( charge = self.charge, multiplicity = self.multiplicity )
						self.molecule.DefineQCModel( qcModel, qcSelection=Selection(self.pureQCAtoms) )
						self.molecule.DefineNBModel( NBmodel )
						self.molecule.coordinates3 = ImportCoordinates3( self.fileLists[i],log=None )
						lsFrames= GetFrameIndex(self.fileLists[i][:-4])						
						if self.ylen > 0:
							self.energiesArray[ lsFrames[1], lsFrames[0] ] = self.molecule.Energy(log=None)
							self.indexArrayX[ lsFrames[1], lsFrames[0] ] = lsFrames[0]
							self.indexArrayY[ lsFrames[1], lsFrames[0] ] = lsFrames[1]
						else:
							self.energiesArray[ lsFrames[0] ] = self.molecule.Energy(log=None)
							self.indexArrayX[ lsFrames[0] ] = lsFrames[0]	
				#-----------------------------------------
				if self.ylen > 0:
					self.SMOenergies[smo] = self.energiesArray
					self.energiesArray = pymp.shared.array( (self.ylen,self.xlen) , dtype='float')	
				else:
					self.SMOenergies[smo] = self.energiesArray
					self.energiesArray = pymp.shared.array( (self.xlen) , dtype='float')		
			else:
				continue		
	#====================================================
	def RunInternalDFT(self,_functional,_basis,_NmaxThreads):
		'''
		Run energy refinement with the semiempirical hamiltonians available wihthin pDynamo
		Parameters:
			_methods:     List of Hamiltoninas
			_NmaxThreads: Number of maximum threds to be used in the parallel section
		'''
		self.SMOenergies = {}		
		self.methods.append(_functional)

		converger      = DIISSCFConverger.WithOptions( densityTolerance = 1.0e-10, maximumIterations = 550 )
		gridIntegrator = DFTGridIntegrator.WithOptions( accuracy = DFTGridAccuracy.Medium, inCore = True )
		qcModel        = None
		NBmodel        = self.molecule.nbModel

		if _functional == "hf": 
			qcModel = QCModelDFT.WithOptions(converger=converger,functional="hf", orbitalBasis=_basis, fitBasis = "demon" )
		else                  :
			qcModel = QCModelDFT.WithOptions(converger=converger,functional=_functional,gridIntegrator=gridIntegrator, orbitalBasis=_basis)

		self.molecule.electronicState = ElectronicState.WithOptions(charge = self.charge)
		self.molecule.DefineQCModel( qcModel, qcSelection=Selection(self.pureQCAtoms) )		
		self.molecule.DefineNBModel( NBmodel )		
		
		with pymp.Parallel(_NmaxThreads) as p:
			for i in p.range( len(self.fileLists) ):				
				self.molecule.coordinates3 = ImportCoordinates3( self.fileLists[i],log=None )
				lsFrames= GetFrameIndex(self.fileLists[i][:-4])						
				if self.ylen > 0:
					self.energiesArray[ lsFrames[1], lsFrames[0] ] = self.molecule.Energy()
					self.indexArrayX[ lsFrames[1], lsFrames[0] ] = lsFrames[0]
					self.indexArrayY[ lsFrames[1], lsFrames[0] ] = lsFrames[1]
				else:
					self.energiesArray[ lsFrames[0] ] = self.molecule.Energy()
					self.indexArrayX[ lsFrames[0] ] = lsFrames[0]	
			#-----------------------------------------
			if self.ylen > 0:
				self.SMOenergies[ self.methods[0] ] = self.energiesArray
				self.energiesArray = pymp.shared.array( (self.ylen,self.xlen), dtype='float')	
			else:
				self.SMOenergies[ self.methods[0] ] = self.energiesArray
				self.energiesArray = pymp.shared.array( (self.xlen), dtype='float')

	#====================================================
	def RunMopacSMO(self,_methods,_keyWords):
		'''
		Create input for Mopac with its available Hamiltonians enabling the QC(QM)/MM potential
		Parameters:
			_methods: List of hamiltonians available in MOPAC 
			_NmaxThreads: Number of maximum threds to be used in the parallel section
		'''
		self.SMOenergies = {}
		self.methods     = _methods
		NBmodel          = self.molecule.nbModel	
		_mopacKeys       = _keyWords
		
		for smo in _methods:
			for i in range( len(self.fileLists) ):
				mop = MopacQCMMinput(self.molecule,self.baseName,self.fileLists[i],_mopacKeys,smo)
				mop.CalculateGradVectors()
				mop.write_input(self.charge,self.multiplicity)
				mop.Execute()				
				lsFrames = []
				if self.fileLists[i] == "single.pkl": lsFrames.append(0)
				else: lsFrames = GetFrameIndex(self.fileLists[i][:-4])						
				if self.ylen > 0:
					self.energiesArray[ lsFrames[1], lsFrames[0] ] = mop.GetEnergy()
					self.indexArrayX[ lsFrames[1], lsFrames[0] ] = lsFrames[0]
					self.indexArrayY[ lsFrames[1], lsFrames[0] ] = lsFrames[1]
				else:
					self.energiesArray[ lsFrames[0] ] = mop.GetEnergy()
					self.indexArrayX[ lsFrames[0] ] = lsFrames[0]					
			#----------------			
			if self.ylen > 0:
				self.SMOenergies[smo] = self.energiesArray
				self.energiesArray    = pymp.shared.array( (self.ylen,self.xlen) , dtype='float')	
			else:
				self.SMOenergies[smo] = self.energiesArray
				self.energiesArray    = pymp.shared.array( (self.xlen) , dtype='float')	
			
	#====================================================
	def RunDFTB(self,_NmaxThreads):
		'''
		Perform energy refinement using the interface available on the pDynamo with the DFTB+ software, enabling QC(QM)/MM potential.
		Parameters:
			_NmaxThreads: Number of maximum threds to be used in the parallel section
		'''
		self.methods.append("DFTB")
		for i in p.range(0, len(self.fileLists) ):				
			fle2 = os.path.basename(self.fileLists[i][:-4])
			_scratch = os.path.join(self.baseName, fle2)				
			if not os.path.exists(_scratch):
				os.makedirs(_scratch)
							
			self.molecule.electronicState = ElectronicState.WithOptions(charge       = self.charge 		, 
			                                                          	multiplicity = self.multiplicity )
			#-------------------------------------------------------------
			_QCmodel = QCModelDFTB.WithOptions( deleteJobFiles = False   ,
			                                	randomScratch  = True    ,
			                                 	scratch        = _scratch,
			                                 	skfPath        = skfPath ,
			                                 	useSCC         = True    )
			#-------------------------------------------------------------
			NBmodel = NBModelDFTB.WithDefaults()
			self.molecule.DefineQCModel( _QCmodel, qcSelection=Selection(self.pureQCAtoms) )
			self.cSystem.DefineNBModel( self.NBmodel ) # reseting the non-bonded model
			#--------------------------------------------------------------------
			self.molecule.qcModel.maximumSCCIterations=1200
			energy = self.cSystem.Energy()			
			self.molecule.coordinates3 = ImportCoordinates3( self.fileLists[i] )
				
			if self.ylen > 0:
				self.energiesArray[ lsFrames[1], lsFrames[0] ] = self.molecule.Energy()					
				self.indexArrayX[ lsFrames[1], lsFrames[0] ]   = lsFrames[1]
				self.indexArrayY[ lsFrames[1], lsFrames[0] ]   = lsFrames[0]
				tmpText = "{}".format(self.energiesArray[ lsFrames[1], lsFrames[0] ])
				tmpLog.write(tmpText)
				tmpLog.close()
			else:					
				self.energiesArray[ lsFrames[0] ] = self.molecule.Energy()
				self.indexArrayX[ lsFrames[0] ]   = lsFrames[0]
				tmpText = "{}".format(self.energiesArray[ lsFrames[1], lsFrames[0] ])
				tmpLog.write(tmpText)
				tmpLog.close()
		 
	#====================================================
	def SetRestart4Orca(self):
		'''
		Set the files to be run in the energy refinement for ORCA with the restart option.
		The function will read a files named frame*_**.eTmp written in the folder with the energy of the frame.
		If the Orca Refinement run terminate succesfully, these files will be removed and the entire log file will be written.
		'''
		_path = os.path.join(self.baseName,"") 
		tmpList = glob.glob(_path+"*.eTmp")
		for fle in tmpList:
			lf = GetFrameIndex(fle[:-5])
			File = open(fle,'r')
			energy = File.read()
			if self.ylen > 1:
				self.indexArrayX[lf[1],lf[0]] 	= lf[0]
				self.indexArrayY[lf[1],lf[0]] 	= lf[1]
				self.energiesArray[lf[1],lf[0]]	= float(energy)
			else:
				self.indexArrayX[lf[0]] 	= lf[0]
				self.energiesArray[lf[0]]	= float(energy)
		#-------------------------
		#remove files from list that already were calculated
		for fle in reversed(self.fileLists):			
			fle2 = os.path.basename(fle[:-4])
			_scratch = os.path.join(self.baseName, fle2, ".eTmp")
			if os.path.exists(_scratch):
				self.fileLists.remove(fle)			
		
	#====================================================
	def RunORCA(self,_method,_base,_NmaxThreads,_restart=False):
		'''
		Perform energy refinement using the interface available on the pDynamo with the ORCA software, enabling QC(QM)/MM potential.
		Parameters:
			_NmaxThreads: Number of maximum threds to be used in the parallel section
		'''
		self.methods.append(_method+"/"+_base)
		self.restart = _restart		
		if self.restart: self.SetRestart4Orca()	
		self.SMOenergies = {}			
		#---------------------------------------------------------
		#Initiate parallel run
		with pymp.Parallel(_NmaxThreads) as p:
			#----------------------------------------
			#Initiate Loop			
			for i in p.range(0, len(self.fileLists) ):				
				fle2 = os.path.basename(self.fileLists[i][:-4])
				_scratch = os.path.join(self.baseName, fle2 )				
				_scratch2 = os.path.join(self.baseName, fle2,".eTmp" )				
				if not os.path.exists(_scratch):
					os.makedirs(_scratch)
				#----------------------------------------------
				lsFrames= GetFrameIndex(self.fileLists[i][:-4])
				#----------------------------------------------
				tmpLog = ""
				if self.ylen > 1: tmpPath = os.path.join( self.baseName,"frame{}_{}.eTmp".format(lsFrames[0],lsFrames[1]) )
				else: 			  tmpPath = os.path.join( self.baseName,"frame{}.eTmp".format(lsFrames[0]) )
				tmpLog  = open(tmpPath,'w')
				tmpText = ""
				#---------------------------------------------
				options =  "\n% output\n"
				options +=  "print [ p_mos ] 1\n"
				options +=  "print [ p_overlap ] 5\n"
				options +=  "end # output\n"
				options +=  "! SlowConv\n"
				if self.restart:
					options += "%scf \nMaxIter 500\n "
					options += "SOSCFStart 0.00033 \n end\n"
					#options += '!MORead \n %moinp "orcaJob.gbw"'			

				#...............................................................................................
				self.molecule.electronicState = ElectronicState.WithOptions(charge       = self.charge 		, 
				                                                          	multiplicity = self.multiplicity )
				#...............................................................................................
				QCmodel = QCModelORCA.WithOptions( keywords        = [_method, _base, options], 
				                                   deleteJobFiles  = False                    ,
				                                   scratch         =_scratch                  )
				#...............................................................................................
				NBmodel = NBModelORCA.WithDefaults()
				self.molecule.DefineQCModel( QCmodel , qcSelection=Selection(self.pureQCAtoms) )
				self.molecule.DefineNBModel( NBmodel)
				self.molecule.coordinates3 = ImportCoordinates3( self.fileLists[i] )
				#---------------------------------------------------------------------------
				if self.ylen > 1:
					self.energiesArray[ lsFrames[1], lsFrames[0] ] = self.molecule.Energy()					
					self.indexArrayX[ lsFrames[1], lsFrames[0] ]   = lsFrames[1]
					self.indexArrayY[ lsFrames[1], lsFrames[0] ]   = lsFrames[0]
					tmpText = "{}".format(self.energiesArray[ lsFrames[1], lsFrames[0] ])
					tmpLog.write(tmpText)
					tmpLog.close()
				else:					
					self.energiesArray[ lsFrames[0] ] = self.molecule.Energy()
					self.indexArrayX[ lsFrames[0] ]   = lsFrames[0]
					tmpText = "{}".format(self.energiesArray[ lsFrames[0] ])
					tmpLog.write(tmpText)
					tmpLog.close()
		#--------------------
		self.SMOenergies[self.methods[0]] = self.energiesArray
		#--------------------
		self.TreatOrcaFiles()		
	#====================================================
	def TreatOrcaFiles(self):
		'''
		Rename orca files on the scratch folder, bringing them to the base folder with the name related with the respective frames
		'''
		outFiles = glob.glob( self.baseName+"/frame*/"+"orcaJob.log" )
		for out in outFiles:
			outS = out.split("/")
			finalPath = os.path.join( self.baseName, outS[-2] + ".out" )
			shutil.move(out,finalPath)

	#====================================================
	def WriteLog(self):
		'''
		Write calculate energies to file.
		'''
		if self.ylen > 0:
			for smo in self.methods:
				for i in range(self.xlen):
					for j in range(self.ylen):
						self.text +="{} {} {} {}\n".format(self.indexArrayX[ j, i ],self.indexArrayY[ j,i ], self.SMOenergies[smo][j,i] - self.SMOenergies[smo][0,0], smo)
		else:
			for smo in self.methods:
				for i in range(self.xlen):
					self.text +="{} {} {}\n".format(self.indexArrayX[i], self.SMOenergies[smo][i] - self.SMOenergies[smo][0], smo)
		#--------------------------------------------------------------
		_filename = os.path.join(self.baseName,"energy.log")
		#----------------------------
		logFile = open(_filename,'w')
		logFile.write(self.text)
		logFile.close()
		#----------------------------
		#filesTmp = glob.glob( self.baseName+"/*.eTmp" )
		#for ftpm in filesTmp: os.remove(ftpm)		

#==========================================================


