import pickle
from vModel import VismolObject
from OpenGL import GL
import ctypes

class LoadAndSaveFiles:
    """ Class doc """
    
    def __init__ (self, vm_session, p_session):
        """ Class initialiser """
        
        self.p_session = self.main_session.p_session
        self.main_session    = self.main_session
        
    def save_session (self, filename):
        """ Function doc """
  
        self.p_session = self.main_session.p_session
        
        vobjects_dic = {}
        
        #********************************************************************** 
        
        #---------------------------------------------------------------
        #                 V I S M O L    O B J E C T S
        #---------------------------------------------------------------
        
        for vobj_id, vobj in self.vobjects_dic.items():
            
            vobjects_dic[vobj_id] = {}
            '''-------------------------------------------------------'''
            '''Exporting atom list'''
            '''-------------------------------------------------------'''
            atoms = []
            for atom in vobj.atoms:
                
                atoms.append({
                              'index'      : atom.index-1    , 
                              'name'       : atom.name       , 
                              'resi'       : atom.resi       , 
                              'resn'       : atom.resn       , 
                              'chain'      : atom.chain      , 
                              'symbol'     : atom.symbol     , 
                              'occupancy'  : atom.occupancy  , 
                              'bfactor'    : atom.bfactor    , 
                              'charge'     : atom.charge     ,
                              'color'      : atom.color      ,
                              })
            
            representations = {}
            
            for rep_name, rep_data in vobj.representations.items():
                if rep_data == None:
                    pass
                
                else:
                    try:
                        if rep_data.active:
                            representations[rep_name] = list(rep_data.indexes)               
                    except:
                        representations[rep_name] = None
                    #if rep_name == 'spheres':
                    #    representations[rep_name] =  rep_data.indexes
                    #else:
                    #    pass
                    #    # this try / except  should be replaced later
                    #    
                    #    try:#else:
                    #        #print(vobj.name, vobj.index, rep_name, rep_data.indexes )
                    #        representations[rep_name] = list(rep_data.indexes)
                    #    except:
                    #        
                    #        #print()
                    #        pass
            

            #'''
            vobjects_dic[vobj_id] = {'name'                    : vobj.name                 ,
                                     'atoms'                   : atoms                     ,
                                     'index_bonds'             : list(vobj.index_bonds)    ,
                                     'dynamic_bonds'            : list(vobj.dynamic_bonds) ,
                                     'active'                  : vobj.active               ,
                                     'frames'                  : vobj.frames               ,
                                     'vobj_id'                 : vobj_id                   ,
                                     'easyhybrid_system_id'    : vobj.easyhybrid_system_id ,
                                     'representations'         : representations           ,
                                     'color_palette'           : vobj.color_palette        ,
                                     #'trajectory2D_xy_indexes' : vobj.trajectory2D_xy_indexes
                                           }
            
            try:
                #if vobj.trajectory_type == 2:
                #    vobjects_dic[vobj_id]['trajectory_type']         =  vobj.trajectory_type
                #    vobjects_dic[vobj_id]['trajectory2D_xy_indexes'] =  vobj.trajectory2D_xy_indexes
                #    vobjects_dic[vobj_id]['trajectory2D_f_indexes']  =  vobj.trajectory2D_f_indexes 
                #    vobjects_dic[vobj_id]['trajectory2D_x_size']     =  vobj.trajectory2D_x_size    
                #    vobjects_dic[vobj_id]['trajectory2D_y_size']     =  vobj.trajectory2D_y_size    
                #
                #else:
                #    vobjects_dic[vobj_id]['trajectory_type']         =  vobj.trajectory_type = 1
                #
                
                vobjects_dic[vobj_id]['trajectory2D_xy_indexes'] = vobj.trajectory2D_xy_indexes
            except:
                pass
            
        #********************************************************************** 
        
        
        
        #---------------------------------------------------------------
        #                 P D Y N A M O    P R O J E C T S
        #---------------------------------------------------------------
        pdynamo_projects = {
                            'name'                   : self.p_session.name,
                            'nbModel_default'        : self.p_session.nbModel_default,
                            'fixed_color'            : self.p_session.fixed_color,
                            'pdynamo_distance_safety': self.p_session.pdynamo_distance_safety,
                            'active_id'              : self.p_session.active_id,
                            'counter'                : self.p_session.counter  ,
                            'color_palette_counter'  : self.p_session.color_palette_counter,
                            'systems'                : {0:None},
                            }
        
        
        for system_id, system in self.p_session.systems.items():
            pdynamo_projects['systems'][system_id] = {}
            if system:
                for key in system.keys():
                    
                    if key == 'vobject':
                        pdynamo_projects['systems'][system_id]['vobject'] = system['vobject'].index
                    
                    elif key == 'vobjects':
                        pdynamo_projects['systems'][system_id]['vobjects'] = {}
                    
                    else:
                        pdynamo_projects['systems'][system_id][key] = system[key]
                
                '''
                pdynamo_projects['systems'][system_id] = {
                                                        'id'            : system['id'           ],
                                                        'name'          : system['name'         ],
                                                        'system'        : system['system'       ],
                                                        'vobject' : system['vobject'].index,
                                                        'active'        : system['active'       ],
                                                        'bonds'         : system['bonds'        ],
                                                        'sequence'      : system['sequence'     ],
                                                        'qc_table'      : system['qc_table'     ],
                                                        'fixed_table'   : system['fixed_table'  ],
                                                        'color_palette' : system['color_palette'],
                                                        }
                '''
            else:
                pass
        #---------------------------------------------------------------
        #               V I S M O L   S E S S I O N
        #---------------------------------------------------------------
        
        vm_session = {'vobj_counter' : self.vobj_counter}
        vm_session['selected_path'] = self.main_session.treeview.selected_path #An integer that indicates which radio button is active in the tree 

        easyhybrid_session_data = { 
                                    'pdynamo_projects'   : pdynamo_projects  ,
                                    'vobjects_dic' : vobjects_dic,
                                    'vm_session'         : vm_session    ,
                                    }
        
        with open(filename,'wb') as outfile:
            pickle.dump(easyhybrid_session_data, outfile)
        



    def load_session (self, infile):
        """ Function doc """
        self.p_session = self.main_session.p_session
        infile             = open(infile,'rb')
        easyhybrid_session_data = pickle.load(infile)
        
        '''
        self.main_session.vm_session.vobjects = []
        #---------------------------------------------------------------
        print(self.main_session.vm_session.vm_session_vbos)
        for index in self.main_session.vm_session.vm_session_vbos:
            #GL.glDeleteBuffers(1, index)
            idn_array = []
            idn_array.append(index)
            array = (ctypes.c_int * len(idn_array))(*idn_array)
            GL.glDeleteBuffers( 1 , ctypes.byref( array) )
        
        
        #for vobject in self.main_session.vm_session.vobjects:
            
        #---------------------------------------------------------------
        #'''
        

        
        self.vobj_counter = easyhybrid_session_data['vm_session']['vobj_counter']
        self.main_session.treeview.selected_path = easyhybrid_session_data['vm_session']['selected_path'] #An integer that indicates which radio button is active in the tree
        
        
        self.p_session.name            = easyhybrid_session_data['pdynamo_projects']['name']
        self.p_session.nbModel_default = easyhybrid_session_data['pdynamo_projects']['nbModel_default']
        self.p_session.fixed_color     = easyhybrid_session_data['pdynamo_projects']['fixed_color']
        
        
        self.p_session.pdynamo_distance_safety = easyhybrid_session_data['pdynamo_projects']['pdynamo_distance_safety']
        self.p_session.active_id               = easyhybrid_session_data['pdynamo_projects']['active_id']
        self.p_session.counter                 = easyhybrid_session_data['pdynamo_projects']['counter']
        self.p_session.systems                 = easyhybrid_session_data['pdynamo_projects']['systems']
        self.p_session.color_palette_counter   = easyhybrid_session_data['pdynamo_projects']['color_palette_counter']
        
        
        
        
        for vobj_id, vobject_data in easyhybrid_session_data['vobjects_dic'].items():

            frames          = vobject_data['frames']
            name            = vobject_data['name']
            bonds           = vobject_data['index_bonds']
            dynamic_bonds   = vobject_data['dynamic_bonds']
            atoms           = vobject_data['atoms']
            representations = vobject_data['representations']
            color_palette   = vobject_data['color_palette']
        
            vobject  = VismolObject.VismolObject(
                                                       #active                         = easyhybrid_session_data['vobjects_dic'][vobj_id]['active']
                                                       name                           = name, 
                                                       atoms                          = atoms, 
                                                       vm_session                     = self, 
                                                       bonds_pair_of_indexes          = list(bonds),
                                                       auto_find_bonded_and_nonbonded = False,
                                                       trajectory                     = frames,
                                                       color_palette                  = color_palette,
                                                       )
                
            vobject.index                = vobj_id
            vobject.active               = vobject_data['active']
            vobject.dynamic_bonds        = vobject_data['dynamic_bonds']
            vobject.easyhybrid_system_id = vobject_data['easyhybrid_system_id']
            vobject.set_model_matrix(self.glwidget.vm_widget.model_mat)


            
            #try:
            #    if vobjects_dic[vobj_id]['trajectory_type']  == 2:
            #        vobject.trajectory_type         = vobjects_dic[vobj_id]['trajectory_type']              
            #        vobject.trajectory2D_xy_indexes = vobjects_dic[vobj_id]['trajectory2D_xy_indexes']      
            #        vobject.trajectory2D_f_indexes  = vobjects_dic[vobj_id]['trajectory2D_f_indexes']       
            #        vobject.trajectory2D_x_size     = vobjects_dic[vobj_id]['trajectory2D_x_size']          
            #        vobject.trajectory2D_y_size     = vobjects_dic[vobj_id]['trajectory2D_y_size']          
            #    
            #    else:
            #        vobject.trajectory_type         = vobjects_dic[vobj_id]['trajectory_type']
            #
            #except:
            #    try:
            #        vobject.trajectory_type         = 2
            #        vobject.trajectory2D_xy_indexes = vobject_data['trajectory2D_xy_indexes']
            #    except:
            #        print('no trajectory2D_xy_indexes  found')
            
            try:
                #vobject.trajectory_type         = 2
                vobject.trajectory2D_xy_indexes = vobject_data['trajectory2D_xy_indexes']
            except:
                print('no trajectory2D_xy_indexes  found')# - - - - - - - - - R E P R E S E N T A T I O N - - - - - - - - - - - - - - - 
            #for rep_key in representations.keys():
                
            self.add_vobject_to_vismol_session (pdynamo_session    = self.p_session, 
                                                      rep                = representations, 
                                                      vobject      = vobject, 
                                                      vobj_count         = False,
                                                      autocenter         = True,
                                                      find_dynamic_bonds = False)
        
            
            
            
            
            #self.main_session.vm_session.glwidget.queue_draw()
            self.main_session.vm_session.vobjects_dic[vobj_id].active = vobject_data['active']
        
        
        
        
        
        #
        #self.p_session.refresh_qc_and_fixed_representations(       _all = True       ,
        #                                                           # system_id = system['id'], 
        #                                                          fixed_atoms = True        , 
        #                                                             QC_atoms = False       ,
        #                                                               static = False       )
        #
        
        
        
        #'''-----------------------------------------------------------------------------------
        for key, system in self.p_session.systems.items():
        #    #print(key, system)
            if system:
                system['vobject'] = self.vobjects_dic[system['vobject']]
        #'''#----------------------------------------------------------------------------------        
        
        
        #        self.p_session.refresh_qc_and_fixed_representations(      _all = False       , 
        #                                                                   system_id = system['id'], 
        #                                                                 fixed_atoms = True        , 
        #                                                                    QC_atoms = False        , 
        #                                                                      static = False       )
        #    else:
        #        pass
        
        '''Here we will select the radio button corresponding to the system that is active. 
        When "path" = None, we select the first system from the treeview''' 
        path   = easyhybrid_session_data['vm_session']['selected_path']
        widget = self.main_session.treeview.treestore
        if path:
            self.main_session.treeview.on_cell_radio_toggled(widget, path)
        else:
            self.main_session.treeview.on_cell_radio_toggled(widget, 0)
        
        
        
        self.main_session.vm_session.center(self.p_session.systems[self.p_session.active_id]['vobject'])
        
        if self.main_session.selection_list_window.visible:
            self.main_session.selection_list_window.update_window(system_names = True, coordinates = False,  selections = False)
        
        self.p_session.refresh_qc_and_fixed_representations(       _all = True       ,
                                                                   # system_id = system['id'],
                                                                  fixed_atoms = True        , 
                                                                     QC_atoms = False       ,
                                                                       static = True       )
        
        #self.p_session.refresh_qc_and_fixed_representations(_all = True)#_all = True)
        
        #for index, vobject in self.main_session.vm_session.vobjects_dic.items():
        #    # for all the vobject in all created vobjects  
        #    for rep_name in vobject.representations:
        #        print (rep_name)
        #        
        #        if vobject.representations[rep_name]  != None:
        #            vobject.representations[rep_name].draw_representation()
