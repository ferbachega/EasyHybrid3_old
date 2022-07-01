#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#FILE = ReactionCoordinate.py

##############################################################
#-----------------...EasyHybrid 3.0...-----------------------#
#-----------Credits and other information here---------------#
##############################################################
#=============================================================================
from commonFunctions import *
from pMolecule import *
#*****************************************************************************
class ReactionCoordinate:
	'''
	Class to set up and store reaction coordinate information
	'''
	def __init__(self,_atoms,_massConstraint,_type="Distance"):
		'''
		Types:
			distance
			multipleDistance
			Angle
			Dihedral
		'''
		self.atoms	        = _atoms
		self.nAtoms 		= len(_atoms)
		self.massConstraint = _massConstraint
		self.Type 			= _type
		self.weight13 		=  1.0
		self.weight31 		= -1.0
		self.period 		= 360.0
		self.increment      = 0.0
		self.minimumD  		= 0.0
		self.label 			= "Reaction Coordinate"

		if self.Type == "Distance":
			if self.nAtoms == 3:
				self.Type = "multipleDistance"
	#==========================================================================================================
	def GetRCLabel(self,_molecule):
		'''
		Get the names of atoms and its residues from the molecule sequence object
		'''
		sequence = getattr( _molecule, "sequence", None )		
		if self.Type == "multipleDistance":
			A1 = _molecule.atoms.items[ self.atoms[0] ]
			A2 = _molecule.atoms.items[ self.atoms[1] ]
			A3 = _molecule.atoms.items[ self.atoms[2] ]
			if not sequence == None:
				A1res = A1.parent.label.split(".")
				A2res = A2.parent.label.split(".")
				A3res = A3.parent.label.split(".")
				#resName1 
				self.label =  A1.label + "(" + A1res[0] + A1res[1] + ")-"
				self.label += A2.label + "(" + A2res[0] + A2res[1] + ")--"
				self.label += A3.label + "(" + A3res[0] + A3res[1] + ") $\AA$"
			else: 
				self.label = A1.label + "-" + A2.label +"-"+ A3.label              
		elif self.Type == "Distance":
			A1 = _molecule.atoms.items[ self.atoms[0] ]
			A2 = _molecule.atoms.items[ self.atoms[1] ]
			if not sequence == None:
				A1res = A1.parent.label.split(".")
				A2res = A2.parent.label.split(".")
				self.label =  A1.label + "(" + A1res[0] + A1res[1] + ")--"
				self.label += A2.label + "(" + A2res[0] + A2res[1] + ") $\AA$"	
			else: self.label = A1.label + "-" + A2.label 	
		#.--------------------------
		elif self.Type == "Dihedral":
			A1 = _molecule.atoms.items[ self.atoms[0] ]
			A2 = _molecule.atoms.items[ self.atoms[1] ]
			A3 = _molecule.atoms.items[ self.atoms[2] ]
			A4 = _molecule.atoms.items[ self.atoms[3] ]
			if not sequence == None:
				A1res = A1.parent.label.split(".")
				A2res = A2.parent.label.split(".")
				A3res = A3.parent.label.split(".")
				A4res = A4.parent.label.split(".")
				self.label =  A1.label + "(" + A1res[0] + A1res[1] + ")-"
				self.label += A2.label + "(" + A2res[0] + A2res[1] + ")-"
				self.label += A3.label + "(" + A3res[0] + A3res[1] + ")-"
				self.label += A4.label + "(" + A4res[0] + A4res[1] + ") $\AA$"
			else: self.label =  A1.label + "-" + A2.label +"-" + A3.label +"-"+A4.label + "$\AA$"
	#==================================================================================================
	def SetInformation(self,_molecule,_dincre,_dminimum=None,_sigma_pk1_pk3=None,_sigma_pk3_pk1=None):
		'''
		Define the values required for the reaction coordinate		
		'''	
		self.increment = _dincre		
		set_pars = True
		if not _dminimum == None:  
			self.minimumD = _dminimum
			set_pars      = False
		if not _sigma_pk1_pk3 == None: 	self.weight13 = _sigma_pk1_pk3
		if not _sigma_pk3_pk1 == None:	self.weight31 = _sigma_pk3_pk1		
		if set_pars: 
			if self.Type == "multipleDistance":
				#.-------------------------------------------------
				if self.massConstraint:			
					#------------------------------------------------
					atomic_n1 = _molecule.atoms.items[ self.atoms[0] ].atomicNumber
					atomic_n3 = _molecule.atoms.items[ self.atoms[2] ].atomicNumber
					mass_a1 = GetAtomicMass(atomic_n1)
					mass_a3 = GetAtomicMass(atomic_n3)
					self.weight13 = mass_a1/(mass_a1+mass_a3)
					self.weight31 = mass_a3/(mass_a1+mass_a3)
					self.weight31 = self.weight31*-1
					dist_a1_a2 = _molecule.coordinates3.Distance( self.atoms[0], self.atoms[1] )
					dist_a2_a3 = _molecule.coordinates3.Distance( self.atoms[1], self.atoms[2] )
					self.minimumD = ( self.weight13 * dist_a1_a2 ) - ( self.weight31 * dist_a2_a3*-1)				
            		#.------------------------------------------------
				else:
					dist_a1_a2 = _molecule.coordinates3.Distance( self.atoms[0], self.atoms[1] )
					dist_a2_a3 = _molecule.coordinates3.Distance( self.atoms[1], self.atoms[2] )
					self.minimumD =  dist_a1_a2 - dist_a2_a3
				#.-------------------------------------------------------------      
			elif self.Type == "Distance": self.minimumD = _molecule.coordinates3.Distance( self.atoms[0], self.atoms[1] )
			#.--------------------------
			elif self.Type == "Dihedral": self.minimumD = _molecule.coordinates3.Dihedral(self.atoms[0],self.atoms[1],self.atoms[2],self.atoms[3])
	#==================================================================================================
	def Print(self):
		'''
		Printing information to the screen.
		'''
		print( "Printing reaction coordinate information:")
		print( "\tAtoms Indices: {}".format(self.atoms) )
		print( "\tType: {}".format(self.Type) )
		print( "\tWeight N1:{} ".format(self.weight13) )
		print( "\tWeight N2:{} ".format(self.weight31) )
		print( "\tIncrement:{} ".format(self.increment) )
		print( "\tInitial distance:{}".format(self.minimumD) )		

#=======================================================================================================================
