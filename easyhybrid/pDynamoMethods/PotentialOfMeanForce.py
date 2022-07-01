#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#FILE = PotentialOfMeanForce.py

##############################################################
#-----------------...EasyHybrid 3.0...-----------------------#
#-----------Credits and other information here---------------#
##############################################################

import os, sys, glob

from pBabel                    	import *                                     
from pCore                     	import *                                     
from pMolecule                 	import *            
from pScientific               	import *                 
         
from pSimulation               	import *
from commonFunctions 			import GetFrameIndex
#-----------------------------------------------------
import pymp

#-----------------------------------------------------

#==============================================================================
class PMF:
	'''
	Class to setup and execute WHAN method in pDynamo to obtain the potential of mean force and
	the free energies from umbrella sampling simulations.
	'''
	#-----------------------------------------------------------------------------------
	def __init__(self,_system,_sourceFolder,_name):
		'''
		Class constructor
		'''
		self.molecule 	= _system
		self.baseName	= _name
		
		self.srcFolder	= _sourceFolder
		self.fileNames	= []
		
		self.text		= ""
		self.LOG		= open( os.path.join(self.baseName,"FreeEnergy.log") ,"w" ) # free energy log
		
		pat = os.path.join( self.srcFolder, "*.ptRes" )
		self.fileNames = glob.glob ( pat ) # ver como fica o nome dos arquivos de trejetória na nova versão
		self.fileNames.sort()
		
	#=================================================================================
	def CalculateWHAM(self,_nbins_x,_nbins_y,_temperature):
		'''
		Perform Window histogram calculations from a productuion restricted molecular dynamics
		'''
		
		#-----------------------------------------------------------------------------------------------
		binslist = []
		binslist.append(_nbins_x)		
		if _nbins_y > 0:
			binslist.append(_nbins_y)	
		#-----------------------------------------------------------------------------------------------
		state = WHAM_ConjugateGradientMinimize(	self.fileNames 					  ,
                                         		bins          		= binslist	  ,
                                         		logFrequency        =      1  	  ,
                                         		maximumIterations   =   1000  	  ,
                                         		rmsGradientTolerance= 1.0e-3  	  ,
                                         		temperature         = _temperature)
		#-----------------------------------------------------------------------------------------------
		histogram = state["Histogram"]
		pmf       = state["PMF"      ]
		FE		  = state["Free Energies"]
		if _nbins_y > 0:
			histogram.ToTextFileWithData ( os.path.join(self.baseName,"PotentialOfMeanForce.dat") , [ pmf ], format = "{:20.3f} {:20.3f} {:20.3f}\n" )
		else: 
			histogram.ToTextFileWithData ( os.path.join(self.baseName,"PotentialOfMeanForce.dat") , [ pmf ], format = "{:20.3f} {:20.3f} \n" )
		#-----------------------------------------------------------------------------------------------
		text = ""
		for i in range(len(FE)):
			lsFrames = GetFrameIndex( self.fileNames[i][:-16] )
			if len(lsFrames) > 1:
				text += "{} {} {}\n".format( lsFrames[0], lsFrames[1] , FE[i] )
			elif len(lsFrames) == 1:
				text += "{} {}\n".format( lsFrames[0] , FE[i] )
		#-----------------------------------------------------------------------------------------------
		print(pmf)
		self.LOG.write(text)
		self.LOG.close()

#==================================================================================
#=============================END OF FILE==========================================
#==================================================================================

