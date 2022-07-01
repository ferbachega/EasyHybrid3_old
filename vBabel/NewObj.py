from   vModel import VismolObject



def create_empty_vismol_obj (infile = None, vm_session =  None, gridsize = 3):
    """ Function doc """
    print ('\nstarting: parse_mol2')
    at  =  vm_session.vConfig.atom_types

    frames = []
    atoms  = []
    
    #-------------------------------------------------------------------------------------------
    #                         Building   V I S M O L    O B J
    #-------------------------------------------------------------------------------------------
    #name = os.path.basename(infile)
    vobject  = VismolObject.VismolObject(name                           = 'UNK', 
                                               atoms                          = atoms, 
                                               vm_session                      = vm_session, 
                                               trajectory                     = frames,
                                               auto_find_bonded_and_nonbonded = False)
    
    #-------------------------------------------------------------------------------------------
    return vobject




