#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#FILE = MopacQCMMinput.py

##############################################################
#-----------------...EasyHybrid 3.0...-----------------------#
#-----------Credits and other information here---------------#
##############################################################

from commonFunctions import *

#************************************************************
class MopacQCMMinput:
	'''
	Class to set methods to creat inputs for run QC/MM in mopac
	'''
	#---------------------------------------------------------
	def __init__(self,_system,_baseName,_coordName,_keyWords,_hamiltonian):
		'''
		'''
		self.molecule 		= _system
		self.baseName       = _baseName
		self.coordName      = _coordName
		self.keywords 		= _keyWords
		self.QCatoms  		= []
		self.QCcharge 		= 0
		self.multiplicity 	= 1
		self.gradVectors 	= []
		self.molinFile      = None 
		self.inputFile 		= None
		self.atomsDict		= {}
		self.Hamiltonian    = _hamiltonian
		if _coordName[:-4] == ".plk":
			self.molecule.coordinates3 = ImportCoordinates3(_coordName,log=None)

		self.charges = self.molecule.mmState.charges
		
		for i in self.molecule.atoms.items:
			symbol = GetAtomicSymbol( i.atomicNumber )
			index  = i.index
			x      = self.molecule.coordinates3[i.index, 0]
			y      = self.molecule.coordinates3[i.index, 1]
			z      = self.molecule.coordinates3[i.index, 2]
			self.atomsDict[index] = [ symbol,x,y,z,self.charges[index] ]

		self.QCatoms		= list(self.molecule.qcState.qcAtoms)
		self.BAatoms		= list(self.molecule.qcState.boundaryAtoms)
	#==================================================================
	def CalculateGradVectors(self):
		'''
		Calculate the grad vectors for the mol.in
		'''
		PHI      = 0.0 
		distance = 0.0
		indx     = 0		
		#----------------------------------		
		for j in range( len(self.QCatoms) ):
			indx = 0 
			for i in self.molecule.atoms.items:						 
				distance = self.molecule.coordinates3.Distance( indx, self.QCatoms[j] )
				if not indx == self.QCatoms[j]:
					PHI 	+= self.charges[indx]/ distance
					indx    += 1
			
			PHI *= 332
			self.gradVectors.append(PHI)
			PHI=0		
		
	#===================================================================
	def write_input(self,_chg,_mult):
		'''
		Write the input files and grad vectors file
		'''
		MULT        = "singlet"
		if 	 _mult == 2: MULT = "doublet"
		elif _mult == 3: MULT = "triplet"
		elif _mult == 4: MULT = "quartet"
		elif _mult == 5: MULT = "quintet"
		
		sequence = getattr( self.molecule, "sequence", None )
		mol_file_name = os.path.join( os.getcwd(),"mol.in")
		self.mop_file_name = os.path.join(self.baseName, os.path.basename(self.coordName) + "_" + self.Hamiltonian+ ".mop" )
		mol_file  = open( mol_file_name, "w" )
		mop_file  = open( self.mop_file_name, "w" )
		if sequence is not None: pdb_file  = open( self.mop_file_name[:-4]+".pdb","w")
		molInText = "\n{} 0\n".format( len(self.QCatoms) )
		mop_text  = self.Hamiltonian + " 1SCF charge={} {} ".format(_chg,MULT)
		pdb_text  = ""
		for _key in self.keywords:
			mop_text += _key
			mop_text += " "
		#-------------------
		cnt = 1
		mop_text+="\n\n\n"

		a1    = ""
		a2    = ""
		A1res = "UKN" 
		A2res = "UKN"
		for i in self.QCatoms:
			if sequence is not None:
				a1    = self.molecule.atoms.items[i]
				A1res = a1.parent.label.split(".")
				if i in self.BAatoms:
					a2    = self.molecule.atoms.items[ self.QCatoms[cnt+1] ]
					A2res = a2.parent.label.split(".")	
					pdb_text +=  "ATOM {0:6} {1:4} {2:2} {3:<1} {4:<7} {5:7.3f} {6:7.3f} {7:7.3f} {8:>5.2f} {9:>4.2f} \n".format(cnt,"H",A2res[0],"A",A2res[1],self.atomsDict[i][1],self.atomsDict[i][2],self.atomsDict[i][3],1.00,0.00)
				else:
					pdb_text +=  "ATOM {0:6} {1:4} {2:2} {3:<1} {4:<7} {5:7.3f} {6:7.3f} {7:7.3f} {8:>5.2f} {9:>4.2f} \n".format(cnt,a1.label,A1res[0],"A",A1res[1],self.atomsDict[i][1],self.atomsDict[i][2],self.atomsDict[i][3],1.00,0.00)
			if i in self.BAatoms:								
				mop_text += "{} {} 1 {} 1 {} 1\n".format("H",self.atomsDict[i][1],self.atomsDict[i][2],self.atomsDict[i][3])
			else:
				mop_text += "{} {} 1 {} 1 {} 1\n".format(self.atomsDict[i][0],self.atomsDict[i][1],self.atomsDict[i][2],self.atomsDict[i][3])
			cnt+=1
		idx = 0 
		for i in self.QCatoms:
			molInText += "{} {} {} {} {}\n".format(self.atomsDict[i][0],self.atomsDict[i][1],self.atomsDict[i][2],self.atomsDict[i][3],self.gradVectors[idx])
			idx += 1

		mop_file.write(mop_text)
		mop_file.close()
		mol_file.write(molInText)
		mol_file.close()
		if sequence is not None:
			pdb_file.write(pdb_text)
			pdb_file.close()
	#--------------------------------------------------------
	def Execute(self, mopac_path="/opt/mopac/MOPAC2016.exe"):
		'''
		'''
		command = mopac_path + " " + self.mop_file_name 		
		os.system(command)
	#--------------------------------------------------------
	def GetEnergy(self):
		'''
		Read ARC file to get and return the total energy
		'''
		arcfile = open(self.mop_file_name[:-4]+".arc","r")
		energy = 0.0 		
		for line in arcfile:
			line2 = line.split()
			if len(line2) == 9:
				if line2[0] == "HEAT" and line2[2] == "FORMATION":
					energy = 4.184*float(line2[4])
					break

		arcfile.close()
		return(energy)

	#--------------------------------------------------------






#======================================================================================================#
#======================================END OF FILE=====================================================#
#======================================================================================================#