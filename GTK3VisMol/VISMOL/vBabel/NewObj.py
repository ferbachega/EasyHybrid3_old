from   VISMOL.vModel import VismolObject



def create_empty_vismol_obj (infile = None, vismolSession =  None, gridsize = 3):
    """ Function doc """
    print ('\nstarting: parse_mol2')
    at  =  vismolSession.vConfig.atom_types

    frames = []
    atoms  = []
    
    #-------------------------------------------------------------------------------------------
    #                         Building   V I S M O L    O B J
    #-------------------------------------------------------------------------------------------
    #name = os.path.basename(infile)
    vismol_object  = VismolObject.VismolObject(name                           = 'UNK', 
                                               atoms                          = atoms, 
                                               vismolSession                      = vismolSession, 
                                               trajectory                     = frames,
                                               auto_find_bonded_and_nonbonded = False)
    
    #-------------------------------------------------------------------------------------------
    return vismol_object




