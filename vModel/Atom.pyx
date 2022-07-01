#import vModel.atom_types as at 

#GTK3EasyMol/VISMOL/Model/atom_types.py
from   vModel import MolecularProperties
from   vModel.MolecularProperties import ATOM_TYPES , ATOM_TYPES_list , ATOM_TYPES_BY_ATOMICNUMBER, NON_METAL_LIST



class AtomDict(dict):
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        pass







class Atom:
    """ Class doc """
    
    def __init__ (self, name         = 'Xx',
                        index        = None, 
                        symbol       = None, 
                        pos          = None, 
                        resi         = None, 
                        resn         = None, 
                        chain        = ''  , 
                        atom_id      = 0   , 
                        residue      = 'X' ,
                        
                        
                        color        = []  ,
                        color_id     = None,
                        
                        radius       = None,
                        vdw_rad      = None,
                        cov_rad      = None,
                        ball_radius  = None,
                        
                        
                        occupancy    = 0.0 ,
                        bfactor      = 0.0 , 
                        charge       = 0.0 ,
						bonds_indexes= []  ,
                        vobject      = None):
 
        #if pos is None:
        #    pos = np.array([0.0, 0.0, 0.0])
		
        
        self.pos        = pos     # - coordinates of the first frame
        self.index      = index   # - Remember that the "index" attribute refers to the numbering of atoms 
                                  # (it is not a zero base, it starts at 1 for the first atom)
					    
        self.name       = name    #
        
        if symbol:
            self.symbol = symbol  #
            print("Hey, symbol:", symbol )
        else:
            self.symbol = self.get_symbol(self.name)
            print("Hey, symbol:",self.symbol )
        
        self.is_metal   = self.is_metal_check(self.symbol)
        
        self.resi       = resi    #
        self.resn       = resn    #
        self.chain      = chain   #
        self.vobject    = vobject
        self.residue    = residue    
        
        
        self.occupancy  = occupancy
        self.bfactor    = bfactor  
        self.charge     = charge   
        
        
        #self.at = MolecularProperties.AtomTypes()

        self.atom_id = atom_id        # An unique number
        #----------------------------------------------        
        if color == []:# or color == None:
            self.color   = self.init_color (self.symbol)
        else:
            self.color = color
        #----------------------------------------------        
        if color_id:
            self.color_id = color_id
        else:
            self._generate_atom_unique_color_id ()
        #----------------------------------------------
        
        #self.col_rgb      = self.init_color_rgb(self.symbol)
        if radius:
            self.radius = radius
        else:
            self.radius       = self.init_radius   (self.symbol)
        

        if vdw_rad:
            self.vdw_rad = vdw_rad
        else:
            self.vdw_rad = self.init_vdw_rad  (self.symbol)
        
        
        if cov_rad:
            self.cov_rad = cov_rad
        else:
            self.cov_rad = self.init_cov_rad  (self.symbol)
        

        if ball_radius:
            self.ball_radius = ball_radius
        else:
            self.ball_radius  = self.init_ball_rad (self.symbol)


        self.selected       = False
        self.lines          = True
        self.dotted_lines   = False
        self.dots           = False
        self.nonbonded      = False
        self.ribbons        = False
        self.ball_and_stick = False
        self.sticks         = False
        self.spheres        = False
        self.surface        = False
        self.bonds_indexes  = bonds_indexes
        self.bonds          = []

        self.dynamic_bonds  = False  # represent dynamic bonds True/False

        self.isfree         = True
        #self.sphere_data    = self.get_sphere_data(self.symbol)
        


    
    def coords (self, frame = None):
        """
        This method returns the atom's coordinates. If a frame (integer) 
        is not given as an argument, the value of the trajectory bar is used. 
        If the value of the trajectory bar exceeds the number of frames of 
        the vobject, the last frame of the vobject is used.
        """
        
        if frame is None:
            frame  = self.vobject.vm_session.glwidget.vm_widget.frame

            if frame > len(self.vobject.frames)-1:
                frame = -1
            else:
                pass
        #print(self.index, frame )
        coords = [self.vobject.frames[frame][(self.index-1)*3  ],
                  self.vobject.frames[frame][(self.index-1)*3+1],
                  self.vobject.frames[frame][(self.index-1)*3+2],]

        return coords

    def get_grid_position (self, gridsize = 3, frame = None):
        """ Function doc """
        coords = self.coords (frame)
        gridpos  = (int(coords[0]/gridsize), int(coords[1]/gridsize), int(coords[2]/gridsize))
        return gridpos

    
    def get_cov_rad (self):
        """ Function doc """
        return self.cov_rad 

    #def get_color (self):
    #    """ Function doc """
    #    #self.at = vobject.vm_session.vConfig.atom_types
    #
    #    self.color   = self.at.get_color(self.symbol)
 
    def _generate_atom_unique_color_id (self): #, vm_session = None):
        """ Function doc """
        i = self.atom_id
        r = (i & 0x000000FF) >>  0
        g = (i & 0x0000FF00) >>  8
        b = (i & 0x00FF0000) >> 16
       
        pickedID = r + g * 256 + b * 256*256
        self.color_id = [r/255.0, g/255.0, b/255.0]
        #print ('pickedID',pickedID, self.atom_id)
        #return pickedID
        #self.vobject.vm_session.atom_dic_id[pickedID] = self



    def is_metal_check (self, symbol = None): #, vm_session = None):
        """ Function doc """
        if symbol in NON_METAL_LIST:
            return False
        else:
            return True








    def init_color_rgb(self, name):
        """ Return the color of an atom in RGB. Note that the returned
            value is in scale of 0 to 1, but you can change this in the
            index. If the atomname does not match any of the names
            given, it returns the default dummy value of atom X.
        """
        try:
            color = color =self.vobject.color_palette[name]
            #color = ATOM_TYPES[name][1]
        except KeyError:
            if name[0] == 'H':# or name in self.hydrogen:
                #color = ATOM_TYPES['H'][1]
                color = self.vobject.color_palette['H']
            
            elif name[0] == 'C':
                #color = ATOM_TYPES['C'][1]
                color = self.vobject.color_palette['C']
            
            elif name[0] == 'O':
                #color = ATOM_TYPES['O'][1]
                color = self.vobject.color_palette['O']
            
            elif name[0] == 'N':
                #color = ATOM_TYPES['N'][1]
                color = self.vobject.color_palette['N']
                
            elif name[0] == 'S':
                #color = ATOM_TYPES['S'][1]
                color = self.vobject.color_palette['S']
            else:
                #color = ATOM_TYPES['X'][1]
                color = self.vobject.color_palette['X']
                
        color = [int(color[0]*250), int(color[1]*250), int(color[2]*250)]
        return color

    def init_color(self, name):
        """ Return the color of an atom in RGB. Note that the returned
            value is in scale of 0 to 1, but you can change this in the
            index. If the atomname does not match any of the names
            given, it returns the default dummy value of atom X.
        """
        try:
            color = color =self.vobject.color_palette[name]
            #color = ATOM_TYPES[name][1]
        except KeyError:
            if name[0] == 'H':# or name in self.hydrogen:
                #color = ATOM_TYPES['H'][1]
                color = self.vobject.color_palette['H']
            
            elif name[0] == 'C':
                #color = ATOM_TYPES['C'][1]
                color = self.vobject.color_palette['C']
            
            elif name[0] == 'O':
                #color = ATOM_TYPES['O'][1]
                color = self.vobject.color_palette['O']
            
            elif name[0] == 'N':
                #color = ATOM_TYPES['N'][1]
                color = self.vobject.color_palette['N']
                
            elif name[0] == 'S':
                #color = ATOM_TYPES['S'][1]
                color = self.vobject.color_palette['S']
            else:
                #color = ATOM_TYPES['X'][1]
                color = self.vobject.color_palette['X']
                ##print(name)
        return color

    def init_cov_rad(self, name):
        """
        """
        
        
        try:
            rad = ATOM_TYPES[name][5]
        except KeyError:
            if name[0] == 'H' or name in self.hydrogen:
                rad = ATOM_TYPES['H'][5]
            elif name[0] == 'C':
                rad = ATOM_TYPES['C'][5]
            elif name[0] == 'O':
                rad = ATOM_TYPES['O'][5]
            elif name[0] == 'N':
                rad = ATOM_TYPES['N'][5]
            elif name[0] == 'S':
                rad = ATOM_TYPES['S'][5]
            else:
                rad = 0.30
        #if name[0] == "P":
        #    print (name, rad)
        return rad

    def init_radius(self, name):
        """
        """
        try:
            rad = ATOM_TYPES[name][6]/5.0
        except KeyError:
            if name[0] == 'H' or name in self.hydrogen:
                rad = ATOM_TYPES['H'][6]/5.0
            elif name[0] == 'C':
                rad = ATOM_TYPES['C'][6]/5.0
            elif name[0] == 'O':
                rad = ATOM_TYPES['O'][6]/5.0
            elif name[0] == 'N':
                rad = ATOM_TYPES['N'][6]/5.0
            elif name[0] == 'S':
                rad = ATOM_TYPES['S'][6]/5.0
            else:
                rad = 0.30
        return rad

    def init_vdw_rad(self, name):
        """
        """
        try:
            vdw = ATOM_TYPES[name][6]
        except KeyError:
            if name[0] == 'H' or name in self.hydrogen:
                vdw = ATOM_TYPES['H'][6]
            elif name[0] == 'C':      
                vdw = ATOM_TYPES['C'][6]
            elif name[0] == 'O':      
                vdw = ATOM_TYPES['O'][6]
            elif name[0] == 'N':      
                vdw = ATOM_TYPES['N'][6]
            elif name[0] == 'S':      
                vdw = ATOM_TYPES['S'][6]
            else:
                vdw = 0.40
        return vdw

    def init_ball_rad(self, name):
        """
        """
        try:
            ball = ATOM_TYPES[name][4]
        except KeyError:
            if name[0] == 'H' or name in self.hydrogen:
                ball = ATOM_TYPES['H'][4]
            elif name[0] == 'C':
                ball = ATOM_TYPES['C'][4]
            elif name[0] == 'O':
                ball = ATOM_TYPES['O'][4]
            elif name[0] == 'N':
                ball = ATOM_TYPES['N'][4]
            elif name[0] == 'S':
                ball = ATOM_TYPES['S'][4]
            else:
                ball = 0.30
        return ball/2.0

    def get_symbol (self, name):
        """ Function doc """
        
        name  =  name.strip()
        
        
        if name == '':
            return ''
        
        name2 = name
        for char in name:
            if char.isnumeric():
                name2 = name2.replace(char,'')
                #print ('replace', name)
            else:
                #print (name)
                pass
        name = name2
        #print (name)
        if len(name) >=3:
            name  = name[:2]
        
        if len(name) == 2:
            if name[1].isnumeric():
                symbol  =  name[0]
            else:
                pass
                
        
        
        if name in ATOM_TYPES.keys():
            return name
        
        else:
           
            if name[0] == 'H':
                
                if name[1] == 'g':
                    symbol =  'Hg'
               
                elif  name[-1] =='e':
                    symbol = 'He'                    
                
                else:
                    symbol =  'H'

            
            
            elif name[0] == 'C':
                
                if name[1] == 'a':
                    symbol =  'Ca'
                    
                elif  name[-1] =='l':
                    symbol = 'Cl'
                
                elif  name[-1] =='L':
                    symbol = 'Cl'
                   
                elif  name[-1] =='d':
                    symbol = 'Cd'
                
                elif  name[-1] =='u':
                    symbol = 'Cu'
                
                else:
                    symbol =  'C'
        
            
            
            
            
            elif name[0] == 'N':
                
                if name[1] == 'i':
                    symbol =  'Ni'
                
                elif name[1] == 'a':
                    symbol =  'Na'
                
                elif name[1] == 'A':
                    symbol =  'Na'
                
                elif name[1] == 'e':
                    symbol =  'Ne'
                elif name[1] == 'b':
                    symbol =  'Nb'
                
                else:
                    symbol =  'N'
                    
            
            
            
            elif name[0] == 'O':
                
                if name[1] == 'g':
                    symbol =  'Og'
                
                if name[1] == 's':
                    symbol =  'Os'
                
                else:
                    symbol =  'O'                        
            
            
            
            elif name[0] == 'S':           
                if name[1] == 'I':
                    symbol =  'Si'
                
                elif name[1] == 'e':
                    symbol =  'Se'
                else:
                    symbol =  'S'   
            
            
            
            
            
            elif name[0] == 'P':
                
                if name[1] == 'd':
                    symbol =  'Pd'
                    
                elif  name[1] == 'b':
                    symbol =  'Pb'
                
                elif  name[1] == 'o':
                    symbol =  'Po'
                
                else:
                    symbol =  'P' 
            
            
            elif name[0] == 'O':
                
                if name[1] == 'g':
                    symbol =  'Og'
                else:
                    symbol =  'O' 


            elif name[0] == 'M':
                
                if name[1] == 'n':
                    symbol =  'Mn'
                    
                elif name[1] == 'N':
                    symbol =  'Mn'
                
                elif name[1] == 'o' or name[1] == 'O':
                    symbol =  'Mo'
                
                elif name[1] == 'G':
                    symbol =  'Mg'
                    
                else:
                    symbol =  'X' 

        
            else:
                #print (name)
                #if returnX:
                symbol = 'X'
                #else:
                #symbol = ''
    
        return symbol
            
        
        
        
        
        
        


   
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        

    



























