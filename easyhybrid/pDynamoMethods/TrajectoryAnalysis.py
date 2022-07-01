#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#FILE = Analysis.py

##############################################################
#-----------------...EasyHybrid 3.0...-----------------------#
#-----------Credits and other information here---------------#
##############################################################

#=============================================================
import os, sys, glob
import numpy as np
#--------------------------------------------------------------
import matplotlib.pyplot as plt
#--------------------------------------------------------------
from commonFunctions 			import *
from pBabel                     import *                                     
from pCore                      import *                                     
from pMolecule                  import *                   
from pScientific                import *                                                             
from pScientific.Statistics     import *
from pScientific.Arrays         import *
from pSimulation                import *
#=====================================================================
class TrajectoryAnalysis:
	'''
	Concentre functions to perform analysis from molecular dynamics trajectories
	'''
	#-----------------------------------------
	def __init__(self,_trajFolder,_system,t_time):
		'''
		Default constructor. Initializa the atributes. 
		'''
		self.trajFolder = _trajFolder
		self.molecule   = _system
		self.RG         = []
		self.RMS        = []
		self.distances1 = []
		self.distances2 = []
		self.total_time = t_time

		self.rc1_MF     = 0.0
		self.rc2_MF     = 0.0
		self.rg_MF      = 0.0
		self.rms_MF     = 0.0
		self.energies   = []

		if self.trajFolder[-4:] == ".dcd":			
			Duplicate(self.trajFolder,self.trajFolder[:-4]+".ptGeo",self.molecule)
			self.trajFolder = self.trajFolder[:-4]+".ptGeo"

		self.trajectory = ImportTrajectory( self.trajFolder , self.molecule )
		self.trajectory.ReadHeader()
        	
	#=================================================
	def CalculateRG_RMSD(self):
		'''
		Get Radius of Gyration and Root Mean Square distance for the trajectory
		'''
		masses  = Array.FromIterable ( [ atom.mass for atom in self.molecule.atoms ] )
		crd3    = ImportCoordinates3( os.path.join(self.trajFolder,"frame0.pkl") )
		system  = AtomSelection.FromAtomPattern ( self.molecule, "*:*:CA" )
		#------------------------------------------------------------------------------
		# . Calculate the radius of gyration.
		rg0 = crd3.RadiusOfGyration(selection = system, weights = masses)
		#------------------------------------------------------------------------------
		# . Save the starting coordinates.
		reference3 = Clone(crd3)  
		#------------------------------------------------------------------------------
		n = []
		m = 0             
		#-------------------------------------------------------------------------------
		while self.trajectory.RestoreOwnerData ( ):
			self.molecule.coordinates3.Superimpose ( reference3, selection = system, weights = masses )
			self.RG.append  ( self.molecule.coordinates3.RadiusOfGyration( selection = system, weights = masses ) )
			self.RMS.append ( self.molecule.coordinates3.RootMeanSquareDeviation( reference3, selection = system, weights = masses ) )
			n.append(m)
			m+=1
		# . Set up the statistics calculations.        
		rgStatistics  = Statistics(self.RG)
		rmsStatistics = Statistics(self.RMS)
		#-------------------------------------------------------------------------------
		# . Save the results.        
		textLog = open( self.trajFolder+"_MDanalysis", "w" ) 
		#-------------------------------------------------------------------------------
		_Text = "rg0 rgMean rgSD rgMax rgMin\n"
		_Text += "{} {} {} {} {}\n".format(rg0,rgStatistics.mean,rgStatistics.standardDeviation,rgStatistics.maximum,rgStatistics.minimum )
		_Text += "rmsMean rmsSD rmsMax rmsMin\n"
		_Text += "{} {} {} {}\n".format(rmsStatistics.mean,rmsStatistics.standardDeviation,rmsStatistics.maximum,rmsStatistics.minimum )
		#-------------------------------------------------------------------------------
		_Text += "Frame RG RMS\n"
		for i in range(len(self.RG)):
			_Text += "{} {} {}\n".format(i,self.RG[i],self.RMS[i])
		#--------------------------------------------------------------------------------
		textLog.write(_Text)
		textLog.close()
	#=================================================
	def ExtractFrames(self):
		'''
		'''	
		'''
		self.rc1_MF = Counter(self.distances1).most_common(1)[0][0]
		self.rc2_MF = Counter(self.distances2).most_common(1)[0][0]
		self.rms_MF = Counter(self.RMS).most_common(1)[0][0]
		self.rg_MF  = Counter(self.RG).most_common(1)[0][0]
        '''
		try:
			from sklearn.neighbors import KernelDensity
		except:
			pass
		kde = KernelDensity(bandwidth=1.0, kernel='gaussian')
		self.distances1 = np.array(self.distances1, dtype=np.float32)
		self.distances2 = np.array(self.distances2, dtype=np.float32)
		self.RMS        = np.array(self.RMS, dtype=np.float32)
		self.RG         = np.array(self.RG, dtype=np.float32)
		self.distances1.reshape(-1,1)
		self.distances2.reshape(-1,1)
		self.RMS.reshape(-1,1)
		self.RG.reshape(-1,1)
		kde.fit(self.distances1[:, None])
		density_rc1 = kde.score_samples(self.distances1[:,None])
		density_rc1 = np.exp(density_rc1)
		self.rc1_MF = max(density_rc1)
		self.distances2.reshape(-1,1)
		kde.fit(self.distances2[:,None])
		density_rc2 = np.exp(kde.score_samples(self.distances2[:,None]))
		self.rc2_MF = max(density_rc2)
		kde.fit(self.RMS[:,None])
		density_rms = np.exp(kde.score_samples(self.RMS[:,None]))
		self.rms_MF = max(density_rms[:,None])
		kde.fit(self.RG[:,None])
		density_rg  = np.exp(kde.score_samples(self.RG[:,None]))
		self.rg_MF  = max(density_rg[:,None])
		
		#------------------------------------------------------------------------------
		distold = abs(density_rms[0] - self.rms_MF)
		distnew = 0.0
		fn      = 0 
		for i in range( len(density_rms) ):
			distnew = abs(density_rms[i] - self.rms_MF)
			if distnew < distold:
				distold = distnew
				fn = i
		#------------------------------------------------		
		self.molecule.coordinates3 = ImportCoordinates3( os.path.join(self.trajFolder,"frame{}.pkl".format(fn) ) )
		ExportSystem( os.path.join( self.trajFolder, "mostFrequentRMS.pdb" ),self.molecule,log=None )
		ExportSystem( os.path.join( self.trajFolder, "mostFrequentRMS.pkl" ),self.molecule,log=None )
		#------------------------------------------------------------------------------
		input()
		if len(self.distances2) > 0:
			distoldRC1 = abs(density_rc1[0] - self.rc1_MF)
			distoldRC2 = abs(density_rc2[0] - self.rc2_MF)
			distold    = abs(distoldRC1-distoldRC2)
			distnew    = 0.0
			fn         = 0 
			for i in range( len(self.distances1) ):
				distnew = abs( abs(density_rc1[i] - self.rc1_MF) -  abs(density_rc2[i] - self.rc2_MF) )
				if distnew < distold:
					distold = distnew
					fn = i			
			self.molecule.coordinates3 = ImportCoordinates3( os.path.join(self.trajFolder,"frame{}.pkl".format(fn) ) )
			ExportSystem( os.path.join( self.trajFolder,"mostFrequentRC1RC2.pdb"), self.molecule,log=None  )
			ExportSystem( os.path.join( self.trajFolder,"mostFrequentRC1RC2.pkl"), self.molecule,log=None )
		
	#=================================================
	def PlotRG_RMS(self,SHOW=False):
		'''
		Plot graphs for the variation of Radius of Gyration and RMSD
		'''
		fig1, (ax1) = plt.subplots(nrows=1)

		n = np.linspace( 0, self.total_time, len(self.RG) )
		plt.plot(n, self.RG)
		ax1.set_xlabel("Time (ps)")
		ax1.set_ylabel("Radius of Gyration $\AA$")
		plt.savefig( os.path.join( self.trajFolder,"analysis_mdRG.png") )
		if SHOW: 
			plt.show()

		fig2, (ax2) = plt.subplots(nrows=1)
		#--------------------------------------------------------------------------
		plt.plot(n, self.RMS)
		ax2.set_xlabel("Time (ps)")
		ax2.set_ylabel("RMSD $\AA$")
		plt.savefig( os.path.join( self.trajFolder,"analysis_mdRMSD.png") )
		if SHOW:
			plt.show()        
		#---------------------------------------------------------------------------
		try:
			import seaborn as sns
			g = sns.jointplot(x=self.RG,y=self.RMS,kind="kde",cmap="plasma",shade=True,height=4)
			g.set_axis_labels("Radius of Gyration $\AA$","RMSD $\AA$",fontsize=4)
			plt.savefig( os.path.join( self.trajFolder,"rg_rmsd_biplot.png") )
			if SHOW:
				plt.show()
		except:
			print("Error in importing seaborn package!\nSkipping biplot distribution plot!")
			pass

	#=========================================================================
	def DistancePlots(self,RCs,SHOW=False):
		'''
		Calculate distances for the indicated reaction coordinates.
		'''		
		if len(RCs) == 2:
			while self.trajectory.RestoreOwnerData():
				self.energies.append( self.molecule.Energy(log=None) )
				if RCs[0].nAtoms == 3:
					self.distances1.append( self.molecule.coordinates3.Distance(RCs[0].atoms[0], RCs[0].atoms[1]) - self.molecule.coordinates3.Distance(RCs[0].atoms[1], RCs[0].atoms[2]) )
				elif RCs[0].nAtoms == 2:
					self.distances1.append( self.molecule.coordinates3.Distance(RCs[0].atoms[0], RCs[0].atoms[1]) )
				if RCs[1].nAtoms == 3:                    
					self.distances2.append( self.molecule.coordinates3.Distance(RCs[1].atoms[0], RCs[1].atoms[1]) - self.molecule.coordinates3.Distance(RCs[1].atoms[1], RCs[1].atoms[2]) )
				elif RCs[1].nAtoms == 2:
					self.distances2.append( self.molecule.coordinates3.Distance(RCs[1].atoms[0], RCs[1].atoms[1]) )
 				
		if len(RCs) == 1:
			while self.trajectory.RestoreOwnerData():
				self.energies.append( self.molecule.Energy(log=None) )
				if RCs[0].nAtoms == 3:
					self.distances1.append( self.molecule.coordinates3.Distance( RCs[0].atoms[0], RCs[0].atoms[1]) - self.molecule.coordinates3.Distance(RCs[0].atoms[1], RCs[0].atoms[2]) )
				elif RCs[0].nAtoms == 2:
					self.distances1.append( self.molecule.coordinates3.Distance(RCs[0].atoms[0], RCs[0].atoms[1]) )		
		#------------------------------------------------------------------------
		# . Save the results.        
		textLog = open( self.trajFolder+"_MDdistAnalysis", "w" )         
		_Text = ""
		if len(RCs) > 1:
			_Text = "Frame RC1 RC2 Energy\n"
			for i in range( len(self.distances1) ):
				_Text += "{} {} {} {}\n".format(i,self.distances1[i],self.distances2[i],self.energies[i])
		else:
			_Text = "Frame RC1 Energy\n"
			for i in range( len(rc1) ):
				_Text += "{} {} {}\n".format(i,self.distances1[i],self.energies[i])
		#-------------------------------------------------------------------------
		n = np.linspace( 0, self.total_time, len(self.distances1) )

		fig1, (ax1) = plt.subplots(nrows=1)
		plt.plot(n, self.energies)
		ax1.set_xlabel("Time (ps)")
		ax1.set_ylabel("Energy kJ/mol")
		plt.savefig(self.trajFolder+"_MDenergy.png")
		if SHOW:
			plt.show()
		#-------------------------------------------------------------------------
		fig2, (ax2) = plt.subplots(nrows=1)
		plt.plot(n, self.distances1,label=RCs[0].label,linestyle="-." )
		if len(RCs) ==2:
			plt.plot(n, self.distances2,label=RCs[1].label,linestyle="-.")
		plt.legend()
		ax2.set_xlabel("Time (ps)")
		ax2.set_ylabel("Distances $\AA$")			
		plt.savefig(self.trajFolder+"_MDdistAnalysis.png")
		if SHOW:
			plt.show()
		#-------------------------------------------------------------------------
		if len(RCs) == 2:
			try:
				import seaborn as sns
				g=sns.jointplot(x=self.distances1,y=self.distances2,kind="kde",cmap="plasma",shade=True,height=4)
				g.set_axis_labels(RCs[0].label,RCs[1].label)
				plt.savefig( os.path.join( self.trajFolder,"distanceBiplot.png") )
				if SHOW:
					plt.show()
			except:
				print("Error in importing seaborn package!\nSkipping biplot distribution plot!")
				pass
		
		textLog.write(_Text)
		textLog.close()
	#=========================================================================
	def Print(self):
		'''
		'''
		print("Claas printing information for Debug!")
		print( "Printing trajectory folder path: {}".format(self.trajFolder) )
		print( "RG array lenght: {}".format( len(self.RG) ) )
		print( "RMS array lenght: {}".format( len(self.RMS) ) )
		print( "RC1 most frequent:{}".format( self.rc1_MF) ) 
		print( "RC2 most frequent:{}".format( self.rc2_MF) ) 
		print( "RG most frequent:{}".format( self.rg_MF) ) 
		print( "RMS most frequent:{}".format( self.rg_MF) ) 
		
#=================================================================================

