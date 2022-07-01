#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#FILE = Analysis.py

##############################################################
#-----------------...EasyHybrid 3.0...-----------------------#
#-----------Credits and other information here---------------#
##############################################################

#==============================================================================

import os, sys, glob
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.colors as colors
from matplotlib.colors import BoundaryNorm

from commonFunctions import *

from pBabel                    import *                                     
from pCore                     import *                                     
from pMolecule                 import *                   
from pScientific               import *                                                             
from pScientific.Statistics    import *
from pScientific.Arrays        import *
from pSimulation               import *

#*********************************************************************
class EnergyAnalysis:
	'''
	Centralize all plot functions for energy alaysis, one and two-dimensional
	'''
	#------------------------------------------------
	def __init__(self, x, y, _type="1D"):
		'''
		Desfault constructor initializing the atributes.
		'''
		self.energies1D 	= []						  # array for energy values from one-dimension coordinate simulation 
		self.energiesMatrix = np.zeros( (y, x), dtype=float ) # array for energy values from two-dimension coordinate simulation
		self.multiple1Dplot = []							  # List of one-dimension energy arrays, each one for a different energy method
		self.multiple2Dplot = []							  # List of two-dimension energy arrays, 
		self.RC1            = []							  # Array with the first reaction coordinate values
		self.RC2            = []							  # Array with the second reaction coordinate values
		self.dimensions     = 0								  # Number of coordinates used in the analysis
		self.nplots1D       = 0								  # Number of one-dimension energy plots to do 
		self.nplots2D 		= 0								  # Number of two-dimension energy plots to do
		self.xlen 			= x 							  # Number of steps in the first coordinate
		self.ylen  			= y         					  # Number of steps in the seconf coordinate
		self.Type 			= _type                           # Type of the plot, could be of: Free Energy, PMF, Potential Energy 
		self.labely         = ""                              # String holding the name of Y axis  
		self.baseName 		= ""							  # string holding the path of the folder
		self.identifiers    = []                              # List of string identifiers 
		
		if self.ylen > 0:
			self.dimensions = 2
		else:
			self.dimensions = 1
	#================================================
	def ReadLog(self, _fileName):
		'''
		Parse energy logs.
		'''
		self.baseName = _fileName[:-4]
		reading       = open(_fileName,'r')
		i = 0 
		energyTmp = []
		#----------------------------------
		if 	self.Type == "1D":
			for line in reading:
				if i > 0:
					lns = line.split()
					self.RC1.append( float(lns[1] ) )
					energyTmp.append( float(lns[2]) )
					self.energies1D.append( float(lns[2]) )
				i += 1
			self.multiple1Dplot.append(energyTmp)
			self.labely = "Potential Energy (kJ/mol)"
		#-----------------------------------
		elif self.Type == "1DRef":
			oldMethod = "none"
			method    = "none"
			for line in reading:
				lns = line.split()
				if oldMethod == "none":
					oldMethod = lns[2]
				method = lns[2]
				if not method == oldMethod:
					self.multiple1Dplot.append(energyTmp)
					self.identifiers.append(oldMethod)
					oldMethod = method
					self.nplots1D += 1	
					energyTmp = []		
				energyTmp.append( float(lns[1]) )
				self.energies1D.append( float(lns[1]) )
			self.multiple1Dplot.append(energyTmp)
			self.identifiers.append(method)
			self.labely = "Potential Energy (kJ/mol)"
		#----------------------------------
		elif self.Type == "2D":
			for line in reading:
				if i > 0:
					lns = line.split()
					self.RC1.append( float(lns[2] ) )
					self.RC2.append( float(lns[3] ) )
					m = int(lns[0])				
					n = int(lns[1])	
					self.energiesMatrix[n][m] = float(lns[4]) 
				i += 1		
		#----------------------------------
		elif self.Type == "2DRef":
			oldMethod = "none"
			method    = "none"
			for line in reading:
				lns = line.split()
				if oldMethod == "none":
					oldMethod = lns[3]
				method = lns[3]
				if not method == oldMethod:
					self.multiple2Dplot.append(self.energiesMatrix)
					self.identifiers.append(oldMethod)
					oldMethod = method
					self.nplots2D += 1
					self.energiesMatrix = np.zeros( (self.ylen, self.xlen), dtype=float )
				m = int( lns[0])				
				n = int( lns[1])				
				self.energiesMatrix[m][n] = float(lns[2])
			
			self.multiple2Dplot.append(self.energiesMatrix)
			self.identifiers.append(method)
			self.nplots2D += 1
		#----------------------------------
		elif self.Type == "WHAM1D":
			MaX = 0.0
			for line in reading:
				lns = line.split()
				pmf = float(lns[1])
				if pmf > MaX: MaX = pmf
				self.RC1.append( float(lns[0]) )
				if lns[1] == "inf": self.energies1D.append( 43434.0000 )
				else:       		self.energies1D.append( float(lns[1]) )

			for i in range(len(self.energies1D)):
				if self.energies1D[i] == 43434.0000:
					self.energies1D[i] = MaX
		#----------------------------------
		elif self.Type == "WHAM2D":
			m = 0
			n = 0
			MaX = 0.0
			for line in reading:
				lns = line.split()				
				self.RC1.append( float(lns[0]) )
				self.RC2.append( float(lns[1]) )
				if lns[2] == "inf":
					self.energiesMatrix[m][n] = 43434.0000
				else:
					self.energiesMatrix[m][n] = float(lns[2])	
					pmf = float(lns[2])
					if pmf > MaX:
						MaX = pmf			
				i +=1
				n +=1 				
				if i % self.xlen == 0:
					m += 1
					n = 0	
			for j in range(self.xlen):
				for i in range(self.ylen):
					if self.energiesMatrix[i][j] == 43434.0000:
						self.energiesMatrix[i][j] = MaX
		#----------------------------------
		elif self.Type == "FE1D":
			energyTmp = np.zeros( (self.xlen), dtype=float )
			for line in reading:
				lns = line.split()
				m = int( lns[0] )
				energyTmp[m]  = float(lns[1]) 
			self.energies1D = energyTmp		
		#----------------------------------
		elif self.Type == "FE2D":
			for line in reading:
				lns = line.split()
				m = int( lns[0])				
				n = int( lns[1])
				self.energiesMatrix[n][m] = float(lns[2])
		#----------------------------------
		self.nplots1D += 1	
	#================================================
	def ReadLogs(self,_folder):
		'''
		'''
		_path = os.path.join(_folder,"")
		logs = glob.glob( _path + "*.log" )
		for log in logs:
			self.ReadLog(log)
			self.identifiers.append( os.path.basename(log[:-4]) )
	#==============================================
	def NormalizeEnergies(self):
		'''
		Normalize energy arrays
		'''
		#------------------------------------------
		if self.Type == "1D":
			Min = 0
			if self.nplots1D == 1:
				Min = self.energies1D[0]
				for i in range( len(self.energies1D) ):
					self.energies1D[i] = self.energies1D[i] - Min
			elif self.nplots1D > 2:
				for k in range( self.nplots1D ):
					Min = self.multiple1Dplot[k][0]
					for i in range(len(self.multiple1Dplot)):
						self.multiple1Dplot[k][i] = self.multiple1Dplot[k][i] - Min		
		#------------------------------------------
		if self.Type == "2D" or self.Type == "WHAM2D" or self.Type == "FE2D" or self.Type == "2DRef":
			if not self.energiesMatrix[0][0] == 0.0:
				self.energiesMatrix = self.energiesMatrix - np.min(self.energiesMatrix)
	#===============================================
	def FES_HL_SMO(self, logPES, logSMO, logFE):
		'''
		Free energy surface from a combination of High level QC method PES and semiempirical free energy
		Parameters:
			logPES:
			logSMO:
			logFE:
		'''
		pass
	#===============================================
	def Plot1D(self,label,XLIM=None,SHOW=False):
		'''
		Plot one dimensional energy plot.
		'''
		self.NormalizeEnergies()
		if self.Type == "FE1D" or self.Type == "1DRef":
			if XLIM == None:
				self.RC1 = np.linspace( 0,len(self.energies1D),len(self.energies1D) )
			else:
				self.RC1 = np.linspace( XLIM[0],XLIM[1],len(self.energies1D) )
			self.labely = "Free Energy (kJ/mol)"			
		elif self.Type == "WHAM1D":
			self.RC1 = np.linspace( np.min(self.RC1), np.max(self.RC1), len(self.RC1) )
			self.labely = "Potential of Mean Field (kJ/mol)"
		
		#--------------------------------------------
		plt.plot(self.RC1,self.energies1D,'-ok')
		plt.xlabel(label)
		plt.ylabel(self.labely)		
		#--------------------------------------------
		plt.savefig(self.baseName+".png",dpi=1000)
		#---------------------------------------------
		if SHOW: plt.show()	
		plt.close()
	#===============================================
	def MultPlot1D(self,label,SHOW=False):
		'''
		Plot one-dimensinal energy plot for several methods
		'''
		#---------------------------------------------
		self.NormalizeEnergies()
		x = np.linspace(0, self.xlen, self.xlen )
		for i in range(self.nplots1D):
			plt.plot(x,self.multiple1Dplot[i],label=self.identifiers[i])
		#---------------------------------------------
		plt.xlabel(label)
		plt.ylabel(self.labely)
		plt.legend()
		plt.savefig(self.baseName+".png",dpi=1000)
		#---------------------------------------------
		if SHOW: plt.show()		
		plt.close()
	#===============================================
	def Plot2D(self,contourlines,crd1label,crd2label,_xlim=None,_ylim=None,SHOW=False,_figS=[7,5]):
		'''
		Plot contour plot for potential, free energy and potential of mean field
		'''			
		#-----------------------------------------------------
		self.NormalizeEnergies()
		if len(self.RC1) > 0:
			X = np.linspace( np.min(self.RC1) , np.max(self.RC1), self.xlen )
			Y = np.linspace( np.min(self.RC2) , np.max(self.RC2), self.ylen )
		#------------------------------------------------------
		else:
			if _xlim == None:
				_xlim = [ 0, self.xlen ]
				_ylim = [ 0, self.ylen ]
			X = np.linspace(_xlim[0],_xlim[1],self.xlen)
			Y = np.linspace(_xlim[0],_xlim[1],self.ylen)
		#------------------------------------------------------
		z = self.energiesMatrix
		#------------------------------------------------------
		fig, (ax0) = plt.subplots( nrows=1, figsize=(_figS[0],_figS[1]) )
		vmin=z.min()
		vmax=z.max()
		#------------------------------------------------------
		levels = MaxNLocator(nbins=20).tick_values( z.min(), z.max() )
		cmap = plt.get_cmap("jet")
		#------------------------------------------------------
		norm = BoundaryNorm(levels, ncolors=cmap.N,	clip=True)
		norm= colors.PowerNorm(gamma=1./2.)
		norm= colors.Normalize(vmin=vmin, vmax=vmax)
		#------------------------------------------------------
		im = ax0.pcolormesh(X,Y,z, cmap=cmap, norm=norm, shading = "gouraud")
		am = ax0.contour(X,Y,z,contourlines, colors='k')		
		ax0.clabel(am, inline=1, fontsize=8, fmt='%1.1f',colors="k")		
		cbar = fig.colorbar(im, ax=ax0)
		cbar.ax.tick_params()
		#---------------------------------------------
		# Set the tick labels font
		axis_font = {'fontname':'Michroma', 'size':14}
		for tick in (ax0.xaxis.get_major_ticks()):
			tick.label.set_fontname('Arial')
			tick.label.set_fontsize(14)

		for tick in (ax0.yaxis.get_major_ticks()):
			tick.label.set_fontname('Dejavu')
			tick.label.set_fontsize(14) 
		#---------------------------------------------				
		ax0.set_xlabel(crd1label, **axis_font)
		ax0.set_ylabel(crd2label, **axis_font)
		fig.tight_layout()
		_method = ""
		if len(self.identifiers) > 0: 
			_method = "_" + self.identifiers[-1]

		plotName = self.baseName + _method
		plt.savefig(plotName+".png",dpi=1000)
		if SHOW: plt.show()
		plt.close()
	#----------------------------------------------------------------------------------------
	def MultPlot2D(self,contourlines,crd1label,crd2label,_xlim=None,_ylim=None,SHOW=False):
		'''
		'''
		for i in range(self.nplots2D):
			self.identifiers.append( self.identifiers[i] )
			self.energiesMatrix = self.multiple2Dplot[i]
			self.Plot2D(contourlines,crd1label,crd2label,_xlim=None,_ylim=None,SHOW=False)
	#----------------------------------------------------------------------------------------
	def Plot1D_FreeEnergy(self,crd1label,crd2label,SHOW=False):
		'''
		'''
		self.NormalizeEnergies()
		if 	 self.Type == "FE2D"   or self.Type == "FE1D"  : self.labely = "Free Energy (kJ/mol)"
		elif self.Type == "WHAM1D" or self.Type == "WHAM2D": self.labely = "Potential of Mean Field (kJ/mol)"
		
		rc0 = np.linspace( 0, len(self.energies1D)-1, len(self.energies1D) )
		#--------------------------------------------
		plt.plot(rc0,self.energies1D,'-ok')
		plt.xlabel("Frame Window (n)")
		plt.ylabel(self.labely)	
		plt.savefig(self.baseName+".png",dpi=1000)
		#---------------------------------------------
		if SHOW: plt.show()	
		plt.close()
#=====================================================================




