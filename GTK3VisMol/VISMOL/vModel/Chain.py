class Chain:
    """ Class doc """
    
    def __init__ (self, name=None, residues=None, label=None, Vobject = None):
        """ Class initialiser """
        #self.residues = {}
        self.residues = []
        
        self.residues_by_index = {}
        
        
        self.backbone = []
        self.name     = ''
        #self.label    = None
        
        self.Vobject  = Vobject
        self.backbone_pair_indexes_full = []
        self.backbone_pair_indexes_show = []
    
    def get_CA_list (self):
        """ Function doc """
        self.backbone = []
        
        for residue in self.residues:
            if residue.isProtein:
                for atom in residue.atoms:
                    if atom.name == 'CA':
                        self.backbone.append(atom)
                    else:
                        pass
                        
                        
        
        return self.backbone
    
    def get_secundary_structure (_):
        """ Function doc """
        return None
    
    
    def return_name (self):
        """ Function doc """
        return self.name
    '''
    def generate_backbone_indexes (self):
        """ Function doc """
        bonds_indexes = [] 
        
        for pair in self.backbone_pair_indexes_show:
            self.Vobject.backbone_full_indexes.append(pair[0])
            self.Vobject.backbone_full_indexes.append(pair[1])
          
            
        bonds_indexes = np.array(bonds_indexes, dtype=np.uint32)
        chain.backbone_pair_indexes = bonds_pairs
        chain.backbone_full_indexes = bonds_indexes           
        chains_list.append(chain_list)
        
        self.ribbons_Calpha_pairs_full  = bonds_pairs
        self.ribbons_Calpha_pairs_rep   = bonds_pairs
        self.ribbons_Calpha_indexes_rep = bonds_indexes
    '''
    
