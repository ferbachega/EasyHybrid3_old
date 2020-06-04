class Chain:
    """ Class doc """
    
    def __init__ (self, name=None, residues=None, label=None, Vobject = None):
        """ Class initialiser """
        #self.residues = {}
        self.residues = []
        
        self.backbone = []
        self.name     = ''
        #self.label    = None
        
        self.Vobject  = Vobject
        self.backbone_pair_indices_full = []
        self.backbone_pair_indices_show = []
    
    '''
    def generate_backbone_indices (self):
        """ Function doc """
        bonds_indices = [] 
        
        for pair in self.backbone_pair_indices_show:
            self.Vobject.backbone_full_indices.append(pair[0])
            self.Vobject.backbone_full_indices.append(pair[1])
          
            
        bonds_indices = np.array(bonds_indices, dtype=np.uint32)
        chain.backbone_pair_indices = bonds_pairs
        chain.backbone_full_indices = bonds_indices           
        chains_list.append(chain_list)
        
        self.ribbons_Calpha_pairs_full  = bonds_pairs
        self.ribbons_Calpha_pairs_rep   = bonds_pairs
        self.ribbons_Calpha_indices_rep = bonds_indices
    '''
    
