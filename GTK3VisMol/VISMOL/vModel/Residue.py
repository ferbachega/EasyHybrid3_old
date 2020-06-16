class Residue:
    """ Class doc """
    
    def __init__ (self, atoms   = None, 
                        name    = 'UNK', 
                        index   = None,
                        chain   = None,
                        Vobject = None):
        """ Class initialiser """
        self.atoms     = []
        self.resi      = index
        self.resn      = name
        self.chain     = chain
        self.Vobject   = Vobject
	self.isProtein = False
	
	
	
	self.residues_dictionary = {'CYS': 'C', 
	                            'ASP': 'D', 
	                            'SER': 'S', 
	                            'GLN': 'Q', 
	                            'LYS': 'K',
                                    'ILE': 'I', 
	                            'PRO': 'P', 
	                            'THR': 'T', 
	                            'PHE': 'F', 
	                            'ASN': 'N', 
                                    'GLY': 'G', 
	                            'HIS': 'H', 
	                            
	                            # amber
	                            "HID": "H",
	                            "HIE": "H",
	                            "HIP": "H",
	                            "ASH": "D",
	                            "GLH": "E",
	                            "CYX": "C",
	                            
	                            # charmm
	                            "HSD": "H", 
	                            "HSE": "H", 
	                            "HSP": "H", 
	                            
	                            
	                            'LEU': 'L', 
	                            'ARG': 'R', 
	                            'TRP': 'W', 
                                    'ALA': 'A', 
	                            'VAL': 'V', 
	                            'GLU': 'E', 
	                            'TYR': 'Y', 
	                            'MET': 'M'}
	
	
    def is_protein (self):
	""" Function doc """
	if self.name in  self.residues_dictionary.keys():
	    self.isProtein = True
	else:
	    self.isProtein = False
	return self.isProtein
	    
	    
