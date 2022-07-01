class Bond:
	""" Class doc """
	
	def __init__ (self, atom_i       = None ,
						atom_index_i = None ,
						atom_j       = None ,
						atom_index_j = None , 
						bond_order = 1):
							
		""" Class initialiser """
		self.atom_i = atom_i
		self.atom_j = atom_j
		
		
		# - Remember that the "index" attribute refers to the numbering of atoms 
		# (it is not a zero base, it starts at 1 for the first atom)
		
		
		
		# these indices are zero base numbering (it starts at 0 for the first atom)
		self.atom_index_i = None
		self.atom_index_j = None
		
		if atom_index_i:
			self.atom_index_i = atom_index_i
		else:
			self.atom_index_i = atom_i.index-1
		
		
		if atom_index_j:
			self.atom_index_j = atom_index_j
		else:
			self.atom_index_j = atom_j.index-1
		
		self.bond_order = bond_order 
		
		self.line_active  = True
		self.stick_active = False
		pass
	
	def distance (self, frame = 0):
		""" Function doc """
		
		coords_i = self.atom_i.coords (frame)
		coords_j = self.atom_j.coords (frame)
		
		dX2  = (coords_i[0] - coords_j[0])**2
		dY2  = (coords_i[1] - coords_j[1])**2
		dZ2  = (coords_i[2] - coords_j[2])**2
		
		distance = (dX2 + dY2 + dZ2)**0.5
		return distance
		
		
