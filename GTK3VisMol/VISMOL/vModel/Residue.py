class Residue:
    """ Class doc """
    
    def __init__ (self, atoms   = None, 
                        name    = 'UNK', 
                        index   = None,
                        chain   = None,
                        Vobject = None):
        """ Class initialiser """
        self.atoms    = []
        self.resi     = index
        self.resn     = name
        self.chain    = chain
        self.Vobject  = Vobject
