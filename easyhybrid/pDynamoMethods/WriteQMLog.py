#LDL QC/MM simulations of its catalysis reaction path

#-------------------------------------------------------------------
import sys                                                                                
sys.path.append("/home/igorchem/VisMol/easyhybrid/pDynamoMethods") 
import pymp
#--------------------------------------------------------------------
import os, glob
from commonFunctions import *
from CoreInterface import *
import SimulationsPreset

#==================================================
class WriteQMLog:
	'''
	'''
	def __init__(self,_system,_outFile):
		'''
		'''
		_system.qcModel.GetOrthogonalizer(_system)
		self.scratch = _system.scratch
		self.outname = _outFile

		self.text    = "{}".format( self.scratch.energyTerms["Potential Energy"] )
		self.charges = _system.AtomicCharges()

		self.outFile = open(_outFile,"w")

	#==============================================
	def write(self):
		'''
		'''
		#fill energy terms
		#number of atoms
		#fill atom labels, cooordinartes and charges
		#number of orbitals
		#basis set information
		#obital energies and occupancies 
		norbitals    = self.scratch.orbitalsP.numberOrbitals
		occupancies  = self.scratch.orbitalsP.occupancies
		energies     = self.scratch.orbitalsP.energies	
		overlap      = self.scratch.Get( "overlapMatrix", None )
		block        = overlap.block
		coordinates3 = self.scratch.qcCoordinates3AU
		orbitals     = self.scratch.orbitalsP.orbitals

		self.text += "\nATOMS_COORD_CHARGE[{}]".format(len(coordinates3[0]))

		self.text += "\nOVERLAP_MATRIX[{}]".format(len(block))
		for i in range(len(block)):
			if i % 6 == 0:
				self.text += "\n"
			self.text += "{0:10.6f} ".format(block[i])
		#molecular orbitals 
		'''
		print(orbitals)
		print(orbitals[0])
		print(len(orbitals))
		print(len(orbitals[0]))
		input()
		for i in range(len(orbitals)):
			if i % 6 == 0:
				self.text += "\n"
			self.text += "{0:10.6f} ".format(orbitals[i])
		'''
		outFile = open(self.outname,"w")
		outFile.write(self.text)
		outFile.close()
	
	#==============================================
	
#==================================================

#==================================================
#Scans 1D with the broken nad and arg 106
#--------------------------------------------------
#Setting reaction coordinates


