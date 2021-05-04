import VISMOL.vModel.Vectors as vectors

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
        self.isSolvent = False
        
        self.is_protein ()


        self.topology = {
                         
                        }
        
        

    def is_protein (self):
        """ Function doc """
        residues_dictionary = self.Vobject.vismol_session.vConfig.residues_dictionary
        solvent_dictionary  = self.Vobject.vismol_session.vConfig.solvent_dictionary
        # is it a protein residue?
        if self.resn in residues_dictionary.keys():
            self.isProtein = True
        else:
            self.isProtein = False
        
        # is it a salvent molecule?
        if self.resn in solvent_dictionary.keys():
            self.isSolvent = True
        else:
            self.isSolvent = False
        
        #return self.isProtein
    
    def get_phi_and_psi (self):
        """ Function doc """
        if self.isProtein:
            
            dihedral_atoms = { 
                              
            
                             } 
            print(self.resn,self.resi) 
            for atom in self.atoms:
                print(self.resn, atom.name, atom.symbol, atom.coords(), atom.bonds, atom.connected2 )
        
        else:
            pass
            
