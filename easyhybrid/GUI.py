import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from GTKGUI.gtkWidgets.filechooser import FileChooser
from easyhybrid.pDynamoMethods.pDynamo2Vismol import *

from easyhybrid.gui.easyhybrid_pDynamo_selection            import  PDynamoSelectionWindow
from easyhybrid.gui.ImportNewSystem                         import  ImportANewSystemWindow 
from easyhybrid.gui.easyhybrid_import_trajectory_window     import  ImportTrajectoryWindow 
from easyhybrid.gui.easyhybrid_export_systems               import  ExportDataWindow 
from easyhybrid.gui.PES_scan_window                         import  PotentialEnergyScanWindow 
from easyhybrid.gui.molecular_dynamics_window               import  MolecularDynamicsWindow 
from easyhybrid.gui.umbrella_sampling_window                import  UmbrellaSamplingWindow 
from easyhybrid.gui.geometry_optimization_window            import  GeometryOptimizatrionWindow 
from easyhybrid.gui.QCSetup_window                          import  EasyHybridSetupQCModelWindow 
from easyhybrid.gui.merge_systems                           import  MergeSystemsWindow 
from easyhybrid.gui.selection_list_window                   import  SelectionListWindow 
from easyhybrid.gui.PES_analisys_window                     import  PotentialEnergyAnalysisWindow 
from easyhybrid.gui.easyhybrid_terminal                     import  TerminalWindow 
from easyhybrid.gui.easyhybrid_energy_refinement            import  EnergyRefinementWindow 

import gc
import os
EASYHYBRID_VERSION = '3.0'
VISMOL_HOME        = os.environ.get('VISMOL_HOME')
HOME               = os.environ.get('HOME')



class EasyHybridDialogGeneric(Gtk.Dialog):
    def __init__(self, parent, message):
        super().__init__(title="New QC list", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_YES, Gtk.ResponseType.YES
        )
        
        label = Gtk.Label(label=message)
        box = self.get_content_area()
        box.add(label)
        self.show_all()

        
class EasyHybridDialogSetQCAtoms(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="New QC list", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_YES, Gtk.ResponseType.YES
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label="A new quantum region has been defined. Would you like to set up your QC parameters now?")

        box = self.get_content_area()
        box.add(label)
        self.show_all()


class EasyHybridDialogEnergy(Gtk.Dialog):
    def __init__(self, parent, energy = None):
        super().__init__(title="Energy Dialog", transient_for=parent, flags=0)
        self.add_buttons(
             Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(300, 100)
        
        label = Gtk.Label(label="Energy = {0:.5f} (KJ/mol)".format(energy))

        box = self.get_content_area()
        box.add(label)
        self.show_all()






class EasyHybridMainWindow ( ):
    """ Class doc """

    def __init__ (self, vm_session = None):
        """ Class initialiser """
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.join(VISMOL_HOME,'easyhybrid/MainWindow.glade'))
        #self.builder.add_from_file(os.path.join(VISMOL_HOME,'GTKGUI/toolbar_builder.glade'))
        self.builder.connect_signals(self)
        self.window = self.builder.get_object('window1')
        self.window.set_default_size(1200, 600)                          
        self.window.set_title('EasyHybrid {}'.format(EASYHYBRID_VERSION))                          
        
        #self.toolbar_builder = self.builder.get_object('toolbar_builder') 
        #self.builder.get_object('box1').pack_start(self.toolbar_builder, True, True, 1)
        
        # Status Bar
        self.statusbar_main = self.builder.get_object('statusbar1')
        #self.statusbar_main.push(0,'wellcome to EasyHydrid')
        self.statusbar_main.push(1,'Welcome to EasyHybrid version {}, a pDynamo3 graphical tool'.format(EASYHYBRID_VERSION))
        
        self.paned_V = self.builder.get_object('paned_V')
        #self.nootbook  =  self.builder.get_object('notebook2')
        #self.window = Gtk.Window(title="VisMol window")
        #self.main_box = Gtk.Box()
        self.vm_session = vm_session#( main_session = None)
        self.vm_session.main_session = self
        
        self.window.connect("key-press-event",   self.vm_session.glwidget.key_pressed)
        self.window.connect("key-release-event", self.vm_session.glwidget.key_released)
        
                
        
        self.menu_box = self.builder.get_object('toolbutton_selection_box')
        self.box2 = self.builder.get_object('box2')
        self.selection_box = self.vm_session.selection_box
        #self.box2.pack_start(self.selection_box, True, True, 0)
        self.menu_box.add(self.selection_box)
        #remove this combobox for vismol tools after
        #self.combobox1 = self.builder.get_object('combobox1')
        #self.combobox1.set_model(self.vm_session.Vismol_selection_modes_ListStore)
        #self.renderer_text = Gtk.CellRendererText()
        #self.combobox1.pack_start(self.renderer_text, True)
        #self.combobox1.add_attribute(self.renderer_text, "text", 0)        
        '''This gtk list is declared in the VismolGLWidget file 
           (it does not depend on the creation of Treeview)'''
        #self.Vismol_Objects_ListStore = self.vm_session.Vismol_Objects_ListStore
        
        #self.box2.pack_start(self.toolbar_builder, True, True, 1)
        
        #-------------------------------------------------------------------      
        #                         notebook_V1
        #-------------------------------------------------------------------
        #self.notebook_V1 = Gtk.Notebook()
        #print (self.notebook_V1.set_tab_pos(Gtk.PositionType.LEFT))
        #self.page1 = Gtk.Box()
        #self.page1.set_border_width(5)
        
        #self.text_view = Gtk.TextView()
        #self.text_view.set_editable(True)
        #self.page1.add( self.text_view)
        
        #self.page1.add(Gtk.Label('Here is the content of the first section.'))
        #self.notebook_V1.append_page(self.page1, Gtk.Label('Logs'))
        
        #-------------------------------------------------------------------      
        #                         notebook_H1
        #-------------------------------------------------------------------
        self.notebook_H1 = Gtk.Notebook()
        self.ScrolledWindow_notebook_H1 = Gtk.ScrolledWindow()
        
        #self.Tree_notebook_H1           = Gtk.TreeView()
        #self.treeview = GtkMainTreeView(vm_session)
        self.treeview = GtkEasyHybridMainTreeView(self, vm_session)
        
        #self.treeview  = self.gtkTreeViewObj.treeview
        self.ScrolledWindow_notebook_H1.add(self.treeview)
        self.notebook_H1.append_page(self.ScrolledWindow_notebook_H1, Gtk.Label('Objects'))
        


        # the label we use to show the selection
        self.label = Gtk.Label()
        self.label.set_text("")

        
        #-------------------------------------------------------------------
        #                         notebook_H2
        #-------------------------------------------------------------------
        self.notebook_H2 = Gtk.Notebook()
        #-------------------------------------------------------------------
        
        self.paned_H = Gtk.Paned(orientation = Gtk.Orientation.HORIZONTAL)
        self.button = Gtk.Button(label="Click Here")
        #-------------------------------------------------------------------
        self.vm_session = vm_session#( main_session = None)
        self.filechooser   = FileChooser()
        #-------------------------------------------------------------------
        
        
        self.container = Gtk.Box (orientation = Gtk.Orientation.VERTICAL)
        self.command_line_entry = Gtk.Entry()

        
        if self.vm_session is not None:
            #player

            self.container.pack_start(self.vm_session.glwidget, True, True, 0)
            
            self.traj_frame = self.vm_session.trajectory_frame
            #self.container.pack_start(self.traj_frame, False, False, 1)
            #self.container.pack_start(self.command_line_entry, False, False, 0)

            self.notebook_H2.append_page(self.container, Gtk.Label('view'))
            self.notebook_H2.append_page(Gtk.TextView(), Gtk.Label('logs'))
            
            
            #self.HBOX = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
            self.HBOX = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 0)
            self.HBOX.pack_start(self.notebook_H1, True, True, 0)
            self.HBOX.pack_start(self.traj_frame, False, False, 1)

            #self.paned_H.add(self.notebook_H1)
            self.paned_H.add(self.HBOX)
            self.paned_H.add(self.notebook_H2)

            self.paned_V.add(self.paned_H)
            #self.paned_V.add(Gtk.TextView())
            
            #self.paned_V.add(self.traj_frame)
        

        #self.player_frame = self.vm_session.player_frame
        #self.player_frame.show_all()
        
        
        '''#- - - - - - - - - - - -  pDynamo - - - - - - - - - - - - - - -#'''
        
        self.p_session = pDynamoSession(vm_session = vm_session)

        '''#- - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - -#'''
        self.system_liststore      = Gtk.ListStore(str, int)
        
        '''#- - - - - - - - - - G T K  W I N D O W S - - - - - - - - - - -#'''
        self.NewSystemWindow              = ImportANewSystemWindow(main = self)
        self.setup_QCModel_window         = EasyHybridSetupQCModelWindow(main = self)
        self.import_trajectory_window     = ImportTrajectoryWindow(main = self)
        self.geometry_optimization_window = GeometryOptimizatrionWindow(main = self)
        self.molecular_dynamics_window    = MolecularDynamicsWindow(main = self)
        self.merge_pdynamo_systems_window = MergeSystemsWindow(main = self)
        self.pDynamo_selection_window     = PDynamoSelectionWindow(main = self)
        self.PES_scan_window              = PotentialEnergyScanWindow(main=  self)
        self.umbrella_sampling_window     = UmbrellaSamplingWindow (main=  self)
        self.export_data_window           = ExportDataWindow(main=  self)
        self.selection_list_window        = SelectionListWindow     (main=  self, system_liststore = self.system_liststore)
        self.go_to_atom_window            = EasyHybridGoToAtomWindow(main=  self, system_liststore = self.system_liststore)
        self.PES_analysis_window          = PotentialEnergyAnalysisWindow(main = self)#, coor_liststore = self.system_liststore)
        self.energy_refinement_window     = EnergyRefinementWindow(main = self)#, coor_liststore = self.system_liststore)
        self.terminal_window              = TerminalWindow(main = self)
        '''#- - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - -#'''

        self.save_vismol_file = None

        self.window.connect("destroy", Gtk.main_quit)
        self.window.connect("delete-event",    Gtk.main_quit)
        self.window.show_all()

    
    def refresh_main_statusbar(self, _type = 'summary', psystem = None):
        """ Function doc """
        if psystem:
            pass
        else:
            psystem = self.p_session.systems[self.p_session.active_id]
            
        if _type == 'summary':
            
            #string = 'System: {}  Size: {}  '.format()
            name    = psystem['name']
            size    = len(psystem['system'].atoms)
            string = 'system: {}    atoms: {}    '.format(name, size)

            if psystem['system'].qcModel:
                hamiltonian = psystem['system'].qcModel.hamiltonian
                n_QC_atoms  = len(psystem['qc_table'])
                
                
                summary_items = psystem['system'].electronicState.SummaryItems()
                
                string += 'hamiltonian: {}    QC atoms: {}    QC charge: {}    spin multiplicity {}    '.format(hamiltonian, 
                                                                                                               n_QC_atoms,
                                                                                                               summary_items[1][1],
                                                                                                               summary_items[2][1],
                                                                                                                 )
                
            n_fixed_atoms = len(psystem['fixed_table'])
            string += 'fixed_atoms: {}    '.format(n_fixed_atoms)
            
            if psystem['system'].mmModel:
                forceField = psystem['system'].mmModel.forceField
                string += 'forceField: {}    '.format(forceField)
            
                if psystem['system'].nbModel:
                    nbmodel = psystem['system'].mmModel.forceField
                    string += 'nbModel: True    '
                    
                    summary_items = psystem['system'].nbModel.SummaryItems()
                    
                
                else:
                    string += 'nbModel: False    '
            
            
            #if len(psystem['fixed_table'] > 0:

            
            self.statusbar_main.push(1,string)

    def refresh_system_liststore (self):
        """ Function doc """
        self.system_liststore     .clear()
        #self.selection_liststore  .clear()
        for key, system  in self.p_session.systems.items():
            try:
                self.system_liststore.append([system['name'], key])
            except:
                print(system)

    def run (self):
        """ Function doc """
        Gtk.main()
    
    def run_dialog_set_QC_atoms (self, _type = None):
        """ Function doc """
        dialog = EasyHybridDialogSetQCAtoms(self.window)
        response = dialog.run()

        if response == Gtk.ResponseType.YES:
            #print("The OK button was clicked")
            self.setup_QCModel_window.OpenWindow()
        elif response == Gtk.ResponseType.CANCEL:
            
            print("The Cancel button was clicked")

        dialog.destroy()
    
    def gtk_load_files (self, button):
        '''Easyhybrid and pkl pdynamo file search '''
        filters = []        
        ''' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - '''
        filter = Gtk.FileFilter()  
        filter.set_name("EasyHybrid3 files - *.easy")
        filter.add_mime_type("Easy files files")
        filter.add_pattern("*.easy")
        filters.append(filter)
        
        filter = Gtk.FileFilter()  
        filter.set_name("pDynamo3 files - *.pkl")
        filter.add_mime_type("PKL files")
        filter.add_pattern("*.pkl")
        filters.append(filter)
        
        filter = Gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        filters.append(filter)
        ''' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - '''
        
        
        ''' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - '''
        filename = self.filechooser.open(filters = filters)
        ''' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - '''
    
        if filename:
            if filename[-4:] == 'easy':
                print('ehf file')            
                self.save_vismol_file = filename
                self.vm_session.load_easyhybrid_serialization_file(filename)            
            else:
                files = {'coordinates': filename}
                systemtype = 3
                self.p_session.load_a_new_pDynamo_system_from_dict(files, systemtype)
        else:
            pass

    def gtk_save_file (self, widget = None):
        """ Function doc """
        if self.save_vismol_file:
            print('saving easyhybrid session - file: ', self.save_vismol_file)
            self.vm_session.save_serialization_file(self.save_vismol_file)
            
        else:
            dialog = Gtk.FileChooserDialog("Save", self.window,
                Gtk.FileChooserAction.SAVE,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

            #self.win.add_filters(dialog)

            filter = Gtk.FileFilter()  
            filter.set_name("EasyHybrid files - *.easy")

            filter.add_mime_type("Easy files files")
            filter.add_pattern("*.easy")
            #
            dialog.add_filter(filter)
            filter = Gtk.FileFilter()
            filter.set_name("All files")
            filter.add_pattern("*")
            #
            dialog.add_filter(filter) 



            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                file_path = dialog.get_filename()
                file_path = file_path+'.easy'
                
                print("Save clicked")
                print("File selected: " + file_path)
                
                self.save_vismol_file = file_path

                print('saving easyhybrid session - file: ', self.save_vismol_file)
                self.vm_session.save_serialization_file(self.save_vismol_file)

            elif response == Gtk.ResponseType.CANCEL:
                print("Cancel clicked")

            dialog.destroy()

    def gtk_save_as_file (self, widget):
        """ Function doc """
        dialog = Gtk.FileChooserDialog("Save as", self.window,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        filter = Gtk.FileFilter()  
        filter.set_name("EasyHybrid files - *.easy")

        filter.add_mime_type("Easy files files")
        filter.add_pattern("*.easy")
        #
        dialog.add_filter(filter)
        filter = Gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        #
        dialog.add_filter(filter) 

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
            file_path = file_path+'.easy'
            
            print("Save clicked")
            print("File selected: " + file_path)
            
            self.save_vismol_file = file_path

            print('saving easyhybrid session - file: ', self.save_vismol_file)
            self.vm_session.save_serialization_file(self.save_vismol_file)

        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def gtk_get_energy (self, widget):
        """ Function doc """
        energy = self.p_session.get_energy()
        dialog = EasyHybridDialogEnergy(parent = self.window, energy = energy)
        response = dialog.run()
        dialog.destroy()

    def on_main_toolbar_clicked (self, button):
        """ Function doc """
        if button  == self.builder.get_object('toolbutton_new_system'):
            self.NewSystemWindow.OpenWindow()
        
        if button  == self.builder.get_object('toolbutton_save'):
            self.gtk_save_file (button)
             
        if button  == self.builder.get_object('toolbutton_save_as'):
            self.gtk_save_as_file (button)
            
        if button == self.builder.get_object('toolbutton_terminal'):
            if button.get_active ():
                self.terminal_window.OpenWindow()
            else:
                self.terminal_window.CloseWindow(None, None)
        
        if button == self.builder.get_object('toolbutton_trajectory_tool1'):
            if button.get_active ():
                self.traj_frame.hide()
                #window = Gtk.Window()
                #window.add(self.traj_frame)
                #window.show_all()
                #self.traj_frame
                #print('ativo')
            else:
                print('desativo')
                self.traj_frame.show()
        if button == self.builder.get_object('button_go_to_atom'):
            self.treeview.main_session.go_to_atom_window.OpenWindow()

        if button  == self.builder.get_object('selections'):
            #print('OpenWindow')
            self.selection_list_window.OpenWindow()

        if button  == self.builder.get_object('toolbutton_energy'):
            self.energy_refinement_window.OpenWindow()
            #self.gtk_get_energy(button)
            
        if button  == self.builder.get_object('toolbutton_setup_QCModel'):
            #self.dialog_import_a_new_systen = EasyHybridImportANewSystemDialog(self.p_session, self)
            #self.dialog_import_a_new_systen.run()
            #self.dialog_import_a_new_systen.hide()
            #self.NewSystemWindow.OpenWindow()
            self.setup_QCModel_window.OpenWindow()
        
        if button  == self.builder.get_object('toolbutton_system_check'): 
            self.p_session.systems[self.p_session.active_id]['vobject'].get_backbone_indexes ()
            print(self.p_session.systems[self.p_session.active_id]['vobject'].c_alpha_bonds)          
            print(self.p_session.systems[self.p_session.active_id]['vobject'].c_alpha_atoms)
        
        
        if button  == self.builder.get_object('toolbutton_geometry_optimization'):
            self.geometry_optimization_window.OpenWindow()
        
        if button  == self.builder.get_object('toolbutton_pDynamo_selections'):
            #print('toolbutton_pDynamo_selections')
            #print('self.p_session.picking_selections_list', self.vm_session.picking_selections.picking_selections_list)
            self.pDynamo_selection_window.OpenWindow()
            
            '''
            atom1 = self.vm_session.picking_selections.picking_selections_list[0]
            #print (atom1.chain, atom1.resn, atom1.resi, atom1.name)
            print ("%s:%s.%s:%s" %(atom1.chain, atom1.resn, atom1.resi, atom1.name))
            
            _centerAtom ="%s:%s.%s:%s" %(atom1.chain, atom1.resn, atom1.resi, atom1.name)
            _radius =  10.0
            
            self.p_session.selections (_centerAtom, _radius)
            '''
       
        if button  == self.builder.get_object('toolbutton_pes_scan'):
            self.PES_scan_window.OpenWindow()
        
        if button  == self.builder.get_object('toolbutton_molecular_dynamics'):
            self.molecular_dynamics_window.OpenWindow()

        if button  == self.builder.get_object('toolbutton_umbrella_sampling'):
            #print('toolbutton_umbrella_sampling')
            self.umbrella_sampling_window.OpenWindow()

            
    def menubar_togglebutton1 (self, button):
        """ Function doc """
        if button.get_active():
            state = "on"
            self.vm_session._picking_selection_mode = True
            button.set_label('Picking')
            
            
        else:
            state = "off"
            self.vm_session._picking_selection_mode = False
            button.set_label('Viewing')

    
    def test (self, widget):
        """ Function doc """
        container = Gtk.Box (orientation = Gtk.Orientation.VERTICAL)
        container.pack_start(self.notebook_V1, True, True, 0)
        container.pack_start(self.command_line_entry, False, False, 0)
        self.paned_V.add(container)
        self.paned_V.show()
        self.window.show_all()


    def on_toolbutton_trajectory_tool (self, button):
        """ Function doc """
        print (button)
        
    def on_main_menu_activate (self, menuitem):
        """ Function doc """
        #print(menuitem)
        
        if menuitem == self.builder.get_object('menuitem_new'):
            self.NewSystemWindow.OpenWindow()
        
        elif menuitem == self.builder.get_object('menuitem_open'):
            self.gtk_load_files (menuitem)
            
        elif menuitem == self.builder.get_object('menuitem_save'):
            self.gtk_save_file (menuitem)
            
        elif menuitem == self.builder.get_object('menuitem_save_as'):
            self.gtk_save_as_file (menuitem)

        elif menuitem == self.builder.get_object('menuitem_export'):
            self.treeview.main_session.export_data_window.OpenWindow()
            
        elif menuitem == self.builder.get_object('menuitem_quit'):
            #print(menuitem, 'menu_item_merge_system')
            pass
        
        
        
        
        elif menuitem == self.builder.get_object('menuitem_energy'):
            self.gtk_get_energy(button)
            
        elif menuitem == self.builder.get_object('menuitem_geometry_optimization'):
            self.geometry_optimization_window.OpenWindow()
            
        elif menuitem == self.builder.get_object('menuitem_molecular_dynamics'):
            self.molecular_dynamics_window.OpenWindow()
            
        elif menuitem == self.builder.get_object('menuitem_normal_modes'):
            pass
            
        elif menuitem == self.builder.get_object('menuitem_rection_coordinate_scans'):
            self.PES_scan_window.OpenWindow()
            
        elif menuitem == self.builder.get_object('menuitem_nudged_elastic_band'):
            pass
            
        elif menuitem == self.builder.get_object('menuitem_umbrella_sampling'):
            self.umbrella_sampling_window.OpenWindow()
        
        elif menuitem == self.builder.get_object('menuitem_check_pDynamo_tools_bar'):
            if menuitem.get_active():
                self.builder.get_object('toolbar4_pdynamo_tools').show()
            else:
                self.builder.get_object('toolbar4_pdynamo_tools').hide()
        
        elif menuitem == self.builder.get_object('menuitem_check_selection_toolbar'):
            if menuitem.get_active():
                self.builder.get_object('toolbar2_selections').show()
            else:
                self.builder.get_object('toolbar2_selections').hide()

            #self.umbrella_sampling_window.OpenWindow()
        
        
        
        
        
        
        
        
        elif menuitem == self.builder.get_object('menuitem_merge_system'):
            #print(menuitem, 'menu_item_merge_system')
            self.merge_pdynamo_systems_window.OpenWindow()
        elif menuitem == self.builder.get_object('menuitem_energy_analysis'):
            #print(menuitem, 'menu_item_merge_system')
            self.PES_analysis_window.OpenWindow()
        
        elif menuitem == self.builder.get_object('menuitem_about'):
            dialog = Gtk.AboutDialog()
            dialog.set_title("About")
            dialog.set_name("EasyHybrid")
            dialog.set_version(EASYHYBRID_VERSION)
            dialog.set_comments("EasyHybrid, a pDynamo Graphical Tool")
            dialog.set_website("https://sites.google.com/site/gtkdynamo/home")
            dialog.set_website_label("EasyHybrid Website")
            dialog.set_authors(["Fernando Bachega, Carlos Sequeiros, Igor Barden and Martin Field"])
            #dialog.set_logo('easyhybrid/icons/easyhybrid_solo_100x100.png')
            dialog.connect('response', lambda dialog, data: dialog.destroy())
            dialog.show_all()




    def update_gui_widgets (self, update_folder = True, update_coords = True):
        """ Function doc """
        self.refresh_main_statusbar()
        # should be a function . in the future!!!
        if update_coords:
            #print(self.vm_session.starting_coords_liststore)
            starting_coords = []
            #self.easyhybrid_main.p_session
            self.vm_session.starting_coords_liststore.clear()
            for key, vobject in self.vm_session.vobjects_dic.items():
                
                #print(vobject.name, vobject.easyhybrid_system_id, vobject.active)
                
                if vobject.easyhybrid_system_id == self.p_session.active_id:
                    starting_coords.append([vobject.name, key])
            
            for item in starting_coords:
                self.vm_session.starting_coords_liststore.append(list(item))
                #print (item)
                
            
        
        '''--------------------------------------------------------------------------------------------'''
        if update_folder:
            active_id = self.p_session.active_id
            working_folder = self.p_session.systems[active_id]['working_folder']
            
            if self.geometry_optimization_window.Visible:
                self.geometry_optimization_window.update_working_folder_chooser(folder = working_folder)
            
            if self.molecular_dynamics_window.Visible:
                self.molecular_dynamics_window.update_working_folder_chooser(folder = working_folder)
        




class GtkEasyHybridMainTreeView(Gtk.TreeView):
    
    def __init__ (self,  main, vm_session):
        Gtk.TreeView.__init__(self)
        self.main_session  = main
        self.vm_session    = vm_session
        self.treeview_menu = TreeViewMenu(self)
        self.treestore     = self.vm_session.treestore
        #--------------------------------------------------------------                                  
                                                                                                         
        self.set_model(self.treestore)                                                                   
                                                                                                         
                                                                                                         
        #------------------ r a d i o  ------------------                                                
        renderer_radio = Gtk.CellRendererToggle()                                                        
        renderer_radio.set_radio(True)                                                                   
        renderer_radio.connect("toggled", self.on_cell_radio_toggled)                                    
        column_radio = Gtk.TreeViewColumn("active", renderer_radio,    active=3, visible = 4)            
        self.append_column(column_radio)                                                                 
                                                                                                         
                                                                                                         
        
        #------------------  t e x t  ------------------
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Object", renderer_text, text=0)
        column_text.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        column_text.set_resizable(True)
        self.append_column(column_text)  
        

        
        #----------------- t o g g l e ------------------
        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_toggled)
        #column_toggle = Gtk.TreeViewColumn("Visible", renderer_toggle, active=1, visible = 3)
        column_toggle = Gtk.TreeViewColumn("V", renderer_toggle, active=1, visible = 2)
        self.append_column(column_toggle)


        #------------------ r a d i o ------------------

        renderer_radio2 = Gtk.CellRendererToggle()
        renderer_radio2.set_radio(True)
        renderer_radio2.connect("toggled", self.on_cell_radio_toggled2)
        column_radio2 = Gtk.TreeViewColumn("T", renderer_radio2, active = 5, visible = 6)
        self.append_column(column_radio2) 


        #'''
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("F", renderer_text, text=9,  visible = 6)
        self.append_column(column_text)  
        #'''


        self.connect('button-release-event', self.on_treeview_Objects_button_release_event )
        
        
        self.selected_path = None
        #self.expand_all()
    def on_cell_toggled(self, widget, path):
        
        self.treestore[path][1] = not self.treestore[path][1]
        #for i in path:
        print(self.treestore[path][1], path, self.treestore[path][0],self.treestore[path][-1] )


        if self.treestore[path][1]:
            obj_index = self.treestore[path][7]
            #print('obj_index', obj_index)
            self.vm_session.enable_by_index(index = int(obj_index))
            self.vm_session.glwidget.queue_draw()
        else:
            obj_index = self.treestore[path][7]
            print ('obj_index:', obj_index)
            self.vm_session.disable_by_index(index = int(obj_index))
            self.vm_session.glwidget.queue_draw()


    def on_cell_radio_toggled2(self, widget, path):
        '''
        Change the radio button relative to the 'T' 
        collumn of the vismol objects treeview 
        '''

        #'''
        #print('\n\n\path1:', path)
        
        #print('\n\n\path:', 'AQUI')
        #print(widget)
        
        for treeview_iter in self.vm_session.gtk_treeview_iters:
            self.treestore[treeview_iter][5] = False
            #print(self.treestore[treeview_iter][0],self.treestore[treeview_iter][-1],self.treestore[treeview_iter][-2] )
        self.treestore[path][5] = True
        
        
        vob_id = self.treestore[path][-3]
        size = len(self.main_session.vm_session.vobjects_dic[vob_id].frames)
        self.treestore[path][-1] = size
        size = self.treestore[path][-1]
        #print (path, type(path),self.treestore['0:1'][0] ,  self.treestore[path][0], self.treestore[path][-3],  self.treestore[path][-1])
        self.main_session.vm_session.TrajectoryFrame.change_range(upper = size)
        
        #print('\n\n\path2:', path)
        #'''
        
  
    def on_cell_radio_toggled(self, widget, path):
        '''This function changes the status of radio buttons in the main tree. 
        
        It must also change the working directory and the list of coordinates 
        that will be available in each system.
        
        see:
        
        self.vm_session.combobox_initial_coordinates
        self.vm_session.filechooser_working_folder  
        
        '''
    
        #print('\n\n\path:', 'AQUI')
        #print('\n\n\path:', path)
        #
        #selected_path = path
        self.selected_path = path
        selected_path      = Gtk.TreePath(path)
        
        #print(widget, selected_path)
        
        for row in self.treestore:
            row[3] = row.path == selected_path
            if row[3]:
                self.main_session.p_session.active_id = row[8]
            else:
                pass
        
        #print('\n\nactive_id', self.main_session.p_session.active_id,'\n\n')
        
        self.main_session.update_gui_widgets()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def on_treeview_Objects_button_release_event(self, tree, event):
        '''
         str  ,   #                                   # 0
         bool ,   # toggle active=1                   # 1
         bool ,   # toggle visible = 3                # 2 
                                                      
         bool ,   # radio  active  = 2                # 3 
         bool ,   # radio  visible = 4                # 4 
                                                      
         bool  ,  # traj radio  active = 5            # 5 
         bool  ,  # is trajectory radio visible?      # 6 
                                                      
         int,     #                                   # 7
         int,     # pdynamo system index              # 8
         int,)    # frames  # 9
        '''

        if event.button == 3:
        
            
            selection     = self.get_selection()
            #print(selection)
            model         = self.get_model()
            #print(model)
            #print(self.treestore)
            
            (model, iter) = selection.get_selected()
            for item in model:
                pass
                #print (item[0], model[iter][0])
            if iter != None:
                vobject_id = str(model.get_value(iter, 7))
                system_id  = str(model.get_value(iter, 8))
                
                self.selectedID  = str(model.get_value(iter, 1))
                self.selectedObj = str(model.get_value(iter, 2))
                #print(self.selectedID, self.selectedObj)
                self.treeview_menu.open_menu(vobject_id)



        if event.button == 2:
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            #pymol_object = model.get_value(iter, 0)
            #self.refresh_gtk_main_self.treeView()
            print ('button == 2')
            
            self.selectedID  = int(model.get_value(iter, 7))  # @+
            #print(self.selectedID, model.get_value(iter, 7))
            #print (model[iter][:], iter)
            vobject = self.vm_session.vobjects_dic[self.selectedID]
            self.vm_session.center(vobject)

        if event.button == 1:
            print ('event.button == 1:')
        
        
class TreeViewMenu:
    """ Class doc """
    
    def __init__ (self, treeview):
        """ Class initialiser """
        pass
        self.treeview = treeview
        self.filechooser   = FileChooser()
        functions = {
                    'Rename'                : self.f2 ,
                    'Info'                  : self.f2 ,
                    'Load Data Into System' : self.load_data_to_a_system ,
                    'Define Color Palette'  : self.f2 ,
                    'Edit Parameters'       : self.f2 ,
                    'Export As...'          : self.menu_export_data_window ,
                    'Merge System With...'  : self.f3 ,
                    'Delete'                : self.delete_system ,
                    #'test'  : self.f1 ,
                    #'f1'    : self.f1 ,
                    #'f2'    : self.f2 ,
                    #'gordão': self.f3 ,
                    #'delete': self.f3 ,
                    }
        self.build_tree_view_menu(functions)



    def menu_export_data_window (self,vobject = None ):
        """ Function doc """
        self.treeview.main_session.export_data_window.OpenWindow()
    
    def load_data_to_a_system (self, vobject = None ):
        """ Function doc """
        selection        = self.treeview.get_selection()
        model, iter      = selection.get_selected()
        self.treeview.main_session.import_trajectory_window.OpenWindow(sys_selected = model.get_value(iter, 8))

    def f2 (self, vobject = None):
        """ Function doc """
        #print('f2')
        #self._show_lines(vobject = self.vobjects[0], indices = [0,1,2,3,4] )
        self.treeview.main_session.go_to_atom_window.OpenWindow()
        #self.treeview.vm_session.go_to_atom_window.OpenWindow()

    def f3 (self, vobject = None):
        """ Function doc """
        
        selection     = self.treeview.get_selection()
        (model, iter) = selection.get_selected()


        self.selectedID  = int(model.get_value(iter, 1))  # @+
        
        
        
        del self.treeview.vm_session.vobjects_dic[self.selectedID]
        '''
        vobject = self.treeview.vm_session.vobjects_dic.pop(self.selectedID)
        del vobject
        '''
        self.treeview.store.clear()
        for vobj_index ,vis_object in self.treeview.vm_session.vobjects_dic.items():
            data = [vis_object.active          , 
                    str(vobj_index),
                    vis_object.name            , 
                    str(len(vis_object.atoms)) , 
                    str(len(vis_object.frames)),
                   ]
            model.append(data)
        self.treeview.vm_session.glwidget.queue_draw()

    def delete_system (self,vobject = None ):
        """ Function doc """
        selection = self.treeview.get_selection()
        # get_selected_rows() returns a tuple
        # The first element is a ListStore
        # The second element is a list of tree paths
        # of all selected rows
        model, paths = selection.get_selected_rows()
        remove_list  = [] 
        
        # Get the TreeIter instance for each path
        for path in paths:
            iter = model.get_iter(path)
            
            
            system_id = model.get_value(iter, 8)
            '''
            print("\niter0:" ,model.get_value(iter, 0),
                  "\niter1:" ,model.get_value(iter, 1),
                  "\niter2:" ,model.get_value(iter, 2),
                  "\niter3:" ,model.get_value(iter, 3),
                  "\niter4:" ,model.get_value(iter, 4),
                  "\niter5:" ,model.get_value(iter, 5),
                  "\niter6:" ,model.get_value(iter, 6),
                  "\niter7:" ,model.get_value(iter, 7),
                  "\niter8:" ,model.get_value(iter, 8)
                  )
            '''
            #'''
            
        
            if model.get_value(iter, 4):
                """model.get_value(iter, 4) = True , it means that it is a header 
                referring to a pdynamo system (containing several associated vobjects), 
                in which case the entire system will be removed."""
                for key , vobject in self.treeview.main_session.vm_session.vobjects_dic.items():
                    if vobject.easyhybrid_system_id == system_id:
                        remove_list.append(key)
                        vobject.active = False
                        self.treeview.main_session.vm_session.glwidget.queue_draw()
                        
                for key in remove_list:
                    self.treeview.main_session.vm_session.vobjects_dic.pop(key)
                self.treeview.main_session.update_gui_widgets()

                self.treeview.main_session.p_session.systems.pop(system_id)
                self.treeview.main_session.vm_session.parents.pop(system_id)
                #self.treeview.main_session.vm_session.gtk_treeview_iters.pop(self.treeview.main_session.vm_session.parents[system_id])
                #model.remove(iter)
        
        
        
        
        
        
            else:
                """model.get_value(iter, 4) = False , it means that it is vobject, 
                in this case, only the coordinates will be removed.""" 
                vobj_id = model.get_value(iter, 7)
                self.treeview.main_session.vm_session.vobjects_dic[vobj_id].active = False
                self.treeview.main_session.vm_session.glwidget.queue_draw()
                self.treeview.main_session.vm_session.vobjects_dic.pop(vobj_id)
                # Remove the ListStore row referenced by iter
                #self.treeview.main_session.update_gui_widgets()
            
        
                # Remove the ListStore row referenced by iter
                #model.remove(iter)
                self.treeview.main_session.update_gui_widgets()
        
        
        
        '''The best way to guarantee the deletion of objects is to rebuild the treeview'''
        #'''
        self.treeview.main_session.vm_session.gtk_treeview_iters = []
        self.treeview.main_session.vm_session.parents = {}
        self.treeview.treestore.clear()

        for key , vobject in self.treeview.main_session.vm_session.vobjects_dic.items():
            self.treeview.main_session.vm_session.add_vobject_to_vismol_session (pdynamo_session = self.treeview.main_session.p_session, 
                                                      rep             = None, 
                                                      vobject   = vobject, 
                                                      vobj_count      = False,
                                                      autocenter      = False)

        #'''
        self.treeview.expand_all()
        
        
        '''This loop guarantees the correct assignment of "true" 
        to the radiobutton of the system that is in memory.
        
        system that is in memory = self.treeview.main_session.p_session.active_id
        
        '''
        for row in self.treeview.treestore:
            #row[3] = row.path == selected_path
            if self.treeview.main_session.p_session.active_id == row[8]:
                row[3] = True
            else:
                row[3] = False
            #print(list(row))
            #if row[3]:
            #    self.main_session.p_session.active_id = row[8]
            #else:
            #    pass
        
        
        
        
        
        
        
        
        
        
        
    def build_tree_view_menu (self, menu_items = None):
        """ Function doc """
        self.tree_view_menu = Gtk.Menu()
        for label in menu_items:
            mitem = Gtk.MenuItem(label)
            mitem.connect('activate', menu_items[label])
            self.tree_view_menu.append(mitem)
            #mitem = Gtk.SeparatorMenuItem()
            #self.tree_view_menu.append(mitem)

        self.tree_view_menu.show_all()

    def open_menu (self, vobject = None):
        """ Function doc """
        #print (vobject)
        
        #print('AQ?UIIIIIIIIIIII')
        self.tree_view_menu.popup(None, None, None, None, 0, 0)




def check_filetype(filein):
    """ Function doc """
    
    data =  open(filein)




class EasyHybridGoToAtomWindow(Gtk.Window):
    def OpenWindow (self):
        """ Function doc """
        if self.visible  ==  False:
            
            #self.vm_session.Vismol_Objects_ListStore
            
            #------------------------------------------------------------------#
            #                  SYSTEM combobox and Label
            #------------------------------------------------------------------#
            self.box_vertical    = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,   spacing = 10)
            self.box_horizontal1 = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 10)
             

            
            self.label1  = Gtk.Label()
            self.label1.set_text('System:')
            self.box_horizontal1.pack_start(self.label1, False, False, 0)

            
            self.combobox_systems = Gtk.ComboBox.new_with_model(self.system_liststore)
            self.combobox_systems.connect("changed", self.on_combobox_systems_changed)
            renderer_text = Gtk.CellRendererText()
            self.combobox_systems.pack_start(renderer_text, True)
            self.combobox_systems.add_attribute(renderer_text, "text", 0)
            
            self.box_horizontal1.pack_start(self.combobox_systems, False, False, 0)
            #------------------------------------------------------------------#
            
            
            
            
            
            #------------------------------------------------------------------#
            #                  COORDINATES combobox and Label
            #------------------------------------------------------------------#
            self.label1  = Gtk.Label()
            self.label1.set_text('Coordinates:')
            self.box_horizontal1.pack_start(self.label1, False, False, 0)
            self.coordinates_combobox = Gtk.ComboBox.new_with_model(self.coordinates_liststore)
            #self.coordinates_combobox.connect("changed", self.on_self.coordinates_combobox_changed)
            renderer_text = Gtk.CellRendererText()
            self.coordinates_combobox.pack_start(renderer_text, True)
            self.coordinates_combobox.add_attribute(renderer_text, "text", 0)
            self.box_horizontal1.pack_start(self.coordinates_combobox, False, False, 0)
            #------------------------------------------------------------------#
            
            


            
            #------------------------------------------------------------------#
            #                  CHAIN combobox and Label
            #------------------------------------------------------------------#
            self.box_horizontal2 = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 6)
            
            
            self.label2  = Gtk.Label()
            self.label2.set_text('Chain:')
            self.box_horizontal2.pack_start(self.label2, False, False, 0)

            self.liststore_chains = Gtk.ListStore(str)
            
            self.combobox_chains = Gtk.ComboBox.new_with_model(self.liststore_chains)
            self.combobox_chains.connect("changed", self.on_combobox_chains_changed)
            renderer_text = Gtk.CellRendererText()
            self.combobox_chains.pack_start(renderer_text, True)
            self.combobox_chains.add_attribute(renderer_text, "text", 0)
            #vbox.pack_start(self.combobox_chains, False, False, True)
            self.box_horizontal2.pack_start(self.combobox_chains, False, False, 0)
            
            
            
            
            #------------------------------------------------------------------#
            #                  RESIDUES combobox and Label
            #------------------------------------------------------------------#
            
            self.label3  = Gtk.Label()
            self.label3.set_text('Residue type:')
            self.box_horizontal2.pack_start(self.label3, False, False, 0)

            self.liststore_residues = Gtk.ListStore(str)
            
            self.combobox_residues = Gtk.ComboBox.new_with_model(self.liststore_residues)
            self.combobox_residues.connect("changed", self.on_combobox_residues_changed)
            renderer_text = Gtk.CellRendererText()
            self.combobox_residues.pack_start(renderer_text, True)
            self.combobox_residues.add_attribute(renderer_text, "text", 0)
            #vbox.pack_start(self.combobox_chains, False, False, True)
            self.box_horizontal2.pack_start(self.combobox_residues, False, False, 0)
            
            
            #------------------------------------------------------------------#
            
            
            
            
            
            self.treeviewbox_horizontal = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 6)
            
            #------------------------------------------------------------------------------------------
            #self.treeview = Gtk.TreeView(model =self.residue_liststore)
            
            
            #-----------------------------------------------------------------------------------------
            #                                      Chain filter
            #-----------------------------------------------------------------------------------------
            self.current_filter_chain = None
            # Creating the filter, feeding it with the liststore model
            self.chain_filter = self.residue_liststore.filter_new()
            # setting the filter function, note that we're not using the
            self.chain_filter.set_visible_func(self.chain_filter_func)
            #-----------------------------------------------------------------------------------------
            
            
            self.treeview = Gtk.TreeView(model = self.chain_filter)
            self.treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
            
            self.treeview.connect("button-release-event", self.on_treeview_Objects_button_release_event)
            self.treeview.connect("row-activated", self.on_treeview_row_activated_event)
            
            for i, column_title in enumerate(
                ['', "index", "Residue",  "Chain", 'size']
            ):
                if i == 0:
                    cell = Gtk.CellRendererToggle()
                    cell.set_property('activatable', True)
                    cell.connect('toggled', self.on_chk_renderer_toggled, self.residue_liststore)
                    column = Gtk.TreeViewColumn(column_title, cell )
                    column.add_attribute(cell, 'active', 0)
                    self.treeview.append_column(column)
                    #print ('aqui')
                else:
                    renderer = Gtk.CellRendererText()
                    #renderer.connect('toggled', self.on_chk_renderer_toggled, self.residue_liststore)
                    column = Gtk.TreeViewColumn(column_title, renderer, text=i)
                    self.treeview.append_column(column)

            
            self.current_filter_chain = None
            

            self.scrollable_treelist = Gtk.ScrolledWindow()
            self.scrollable_treelist.set_vexpand(True)
            self.scrollable_treelist.add(self.treeview)
            #------------------------------------------------------------------------------------------
            


            
            
            #------------------------------------------------------------------------------------------
            self.treeview_atom = Gtk.TreeView(model =self.atom_liststore)
            self.treeview_atom.connect("button-release-event", self.on_treeview_atom_button_release_event)
            self.treeview_atom.connect("row-activated", self.on_treeview_atom_row_activated_event)

            for i, column_title in enumerate(
                ['', "index", "name", "MM atom", 'MM charge']
            ):
                if i == 0:
                    cell = Gtk.CellRendererToggle()
                    cell.set_property('activatable', True)
                    cell.connect('toggled', self.on_chk_renderer_toggled, self.atom_liststore)
                    column = Gtk.TreeViewColumn(column_title, cell )
                    column.add_attribute(cell, 'active', 0)
                    self.treeview_atom.append_column(column)
                    #print ('aqui')
                else:
                    renderer = Gtk.CellRendererText()
                    column = Gtk.TreeViewColumn(column_title, renderer, text=i)
                    self.treeview_atom.append_column(column)

            self.scrollable_treelist2 = Gtk.ScrolledWindow()
            self.scrollable_treelist2.set_vexpand(True)
            self.scrollable_treelist2.add(self.treeview_atom)
            #------------------------------------------------------------------------------------------
            
            
            
            
            
            
            
            
            
            
            
            self.box_vertical.pack_start(self.box_horizontal1, False, True, 0)
            self.box_vertical.pack_start(self.box_horizontal2, False, True, 0)
            self.treeviewbox_horizontal.pack_start(self.scrollable_treelist, True, True, 0)
            self.treeviewbox_horizontal.pack_start(self.scrollable_treelist2, True, True, 0)
            
            self.box_vertical.pack_start(self.treeviewbox_horizontal, False, True, 0)
            
            self.refresh_system_liststore()
            self.update_window (system_names = True, coordinates = True)
            
            self.combobox_systems.set_active(0)
            self.window =  Gtk.Window()
            self.window.set_border_width(10)
            self.window.set_default_size(600, 600)  
            self.window.add(self.box_vertical)
            self.window.connect("destroy", self.CloseWindow)
            self.window.set_title('Go to Atom Window') 
            self.window.show_all() 
                                                          
            #                                                                
            #self.builder.connect_signals(self)                                   
            
            self.visible  =  True
            #self.PutBackUpWindowData()
            #gtk.main()
            #----------------------------------------------------------------

    def CloseWindow (self, button):
        """ Function doc """
        #self.BackUpWindowData()
        self.window.destroy()
        self.visible    =  False
        #print('self.visible',self.visible)
    
    def __init__(self, main = None, system_liststore = None):
        """ Class initialiser """
        
        self.main_session  = main
        self.vm_session    = self.main_session.vm_session
        self.p_session     = self.main_session.p_session
        self.system_liststore      = system_liststore
        self.coordinates_liststore = Gtk.ListStore(str, int)
        
        
        self.residue_liststore = Gtk.ListStore(bool, int, str, str, int)
        self.atom_liststore    = Gtk.ListStore(bool, int, str, str, float, int, )
        self.residue_filter    = False
        self.visible           = False

    
    def update_window (self, system_names = False, coordinates = True,  selections = False ):
        """ Function doc """

        if self.visible:
            
            _id = self.combobox_systems.get_active()
            if _id == -1:
                '''_id = -1 means no item inside the combobox'''
                return None
            else:    
                _, system_id = self.system_liststore[_id]
            
            if system_names:
                self.refresh_system_liststore ()
                self.combobox_systems.set_active(_id)
            
            if coordinates:
                self.refresh_coordinates_liststore ()
                
            
            #if selections:
            #    _, system_id = self.system_liststore[_id]
            #    self.refresh_selection_liststore(system_id)
        else:
            if system_names:
                self.refresh_system_liststore ()
            if coordinates:
                self.refresh_coordinates_liststore ()
            
    
    def refresh_coordinates_liststore(self, system_id = None):
        """ Function doc """
        cb_id =  self.coordinates_combobox.get_active()
        if system_id:
            pass
        else:
            _id = self.combobox_systems.get_active()
            if _id == -1:
                return False
            else:
                #print('_id', _id)
                _, system_id = self.system_liststore[_id]
        
        self.coordinates_liststore.clear()
        n = 0
        for key , vobject in self.vm_session.vobjects_dic.items():
            if vobject.easyhybrid_system_id == system_id:
                self.coordinates_liststore.append([vobject.name, key])
                n += 1
        
        self.coordinates_combobox.set_active(n-1)
        
    def refresh_system_liststore (self):
        """ Function doc """
        self.main_session.refresh_system_liststore()
        #self.system_liststore     .clear()
        ##self.selection_liststore  .clear()
        #'''--------------------------------------------------------------------------------------------'''
        ##self.combobox_systems =self.builder.get_object('systems_combobox')
        #for key, system  in self.p_session.systems.items():
        #    try:
        #        self.system_liststore.append([system['name'], key])
        #    except:
        #        print(system)

    def on_combobox_residues_changed (self, widget):
        """ Function doc """
        tree_iter = widget.get_active_iter()
        if tree_iter is not None:
            model = widget.get_model()
            residue = model[tree_iter][0]
            #print("Selected: country=%s" % country)
        
            self.current_filter_residue = residue
            
            #print("%s Chain selected!" % self.current_filter_residue)
            
            # we update the filter, which updates in turn the view
            if self.residue_filter:
                self.residue_filter.refilter()
        
        
    def on_combobox_chains_changed (self, widget):
        """ Function doc """
        ##---------------------------------------------------------------
        #self.current_filter_chain = None
        ## Creating the filter, feeding it with the liststore model
        #self.chain_filter = self.residue_liststore.filter_new()
        ## setting the filter function, note that we're not using the
        #self.chain_filter.set_visible_func(self.chain_filter_func)
        ##---------------------------------------------------------------
        
        tree_iter = self.combobox_chains.get_active_iter()
        if tree_iter is not None:
            model = self.combobox_chains.get_model()
            chain = model[tree_iter][0]
            #print("Selected: country=%s" % country)
        
        self.current_filter_chain = chain
        #print("%s Chain selected!" % self.current_filter_chain)
        # we update the filter, which updates in turn the view
        self.chain_filter.refilter()
    
    
    def on_combobox_systems_changed (self, widget):
        """ Function doc """
        #print(widget)
        #print(widget.get_active())
        
        #print(widget.get_active_id())
        #print(widget.get_active_iter())
        
        #self.vm_session.vobjects_dic.items()
        
        #self.vm_session.vobjects_dic.items()
        cb_id = widget.get_active()
        if cb_id == -1:
            return None
        else:
            
            self.update_window (coordinates = True)
            
            cb_id =  self.coordinates_combobox.get_active()
            _, key = self.coordinates_liststore[cb_id]
            
            self.VObj = self.vm_session.vobjects_dic[key]
            
            
            self.liststore_chains = Gtk.ListStore(str)
            self.liststore_chains.append(['all'])
            chains = self.VObj.chains.keys()
            
            #self.chain_liststore = Gtk.ListStore(str)
            
            for chain in chains:
                self.liststore_chains.append([chain])
            self.combobox_chains.set_model(self.liststore_chains)
            self.combobox_chains.set_active(0)
            
            
            self.residue_liststore = Gtk.ListStore(bool, int, str, str, int)
            for chain in self.VObj.chains:
                for res in self.VObj.chains[chain].residues:
                    #print(res.resi, res.resn, chain,  len(res.atoms) ) 
                    
                    self.residue_liststore.append(list([True, res.resi, res.resn, chain,  len(res.atoms)]))
            #-----------------------------------------------------------------------------------------
            #                                      Chain filter
            #-----------------------------------------------------------------------------------------
            self.current_filter_chain = None
            # Creating the filter, feeding it with the liststore model
            self.chain_filter = self.residue_liststore.filter_new()
            # setting the filter function, note that we're not using the
            self.chain_filter.set_visible_func(self.chain_filter_func)
            #-----------------------------------------------------------------------------------------
            
            
            
            
            
            
            #-----------------------------------------------------------------------------------------
            #                                      Residue combobox
            #-----------------------------------------------------------------------------------------
            self.liststore_residues = Gtk.ListStore(str)
            self.liststore_residues.append(['all'])
            
            resn_labels = {}
            
            for residue in self.VObj.residues:
                resn_labels[residue.resn] = True
            
            for resn in resn_labels.keys():
                #print (resn)
                self.liststore_residues.append([resn])
            
            self.combobox_residues.set_model(self.liststore_residues)
            self.combobox_residues.set_active(0)
            
            #-----------------------------------------------------------------------------------------
            #                                      Residue filter
            #-----------------------------------------------------------------------------------------
            self.current_filter_residue = None
            # Creating the filter, feeding it with the liststore model
            self.residue_filter = self.chain_filter.filter_new()
            # setting the filter function, note that we're not using the
            self.residue_filter.set_visible_func(self.residue_filter_func)
            #-----------------------------------------------------------------------------------------        
            
            
            #self.treeview.set_model(self.residue_liststore)
            #self.treeview.set_model(self.chain_filter)
            self.treeview.set_model(self.residue_filter)
            
        
    def on_treeview_atom_button_release_event(self, tree, event):
        if event.button == 2:
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            
            
            if iter != None:
                self.selectedID  = int(model.get_value(iter, 1))-1  # @+
                atom = self.VObj.atoms[self.selectedID]
                self.vm_session.glwidget.vm_widget.center_on_atom(atom)
       
    def on_treeview_atom_row_activated_event (self, tree, rowline , column):
        """ Function doc """
        #print (A,B,C)
        selection     = tree.get_selection()
        model         = tree.get_model()
        
        #print(model)
        #print(rowline, list(model[rowline]))
        
        data  = list(model[rowline])
        #print(data)
        #self.selectedID  = int(data[1])  # @+
        #self.selectedObj = str(data[2])
        pickedID = data[-1]
        
        atom_picked = self.vm_session.atom_dic_id[pickedID]
        
        
        #res = self.VObj.chains[self.selectedChn].residues_by_index[self.selectedID]
        #
        ##print('Selecting by doble click')
        ##self.vm_session.selections[self.vm_session.current_selection].selecting_by_residue (res.atoms[0])
        ##self.vm_session.selections[self.vm_session.current_selection].selection_function_viewing (res.atoms[0])
       
        self.vm_session._selection_function (atom_picked, _type = 'atom')
        self.vm_session.glwidget.queue_draw()
        #
        #self.atom_liststore.clear()
        #for atom in res.atoms:
        #    self.atom_liststore.append(list([True, int(atom.index), atom.name, atom.symbol, atom.charge]))
    
    
    def on_treeview_row_activated_event(self, tree, rowline , column ):
        #print (A,B,C)
        selection     = tree.get_selection()
        model         = tree.get_model()
        
        #print(model)
        #print(rowline, list(model[rowline]))
        
        data  = list(model[rowline])
        self.selectedID  = int(data[1])  # @+
        self.selectedObj = str(data[2])
        self.selectedChn = str(data[3])
        
        cb_id =  self.coordinates_combobox.get_active()
        _, key = self.coordinates_liststore[cb_id]
        self.VObj = self.vm_session.vobjects_dic[key]
        
        res = self.VObj.chains[self.selectedChn].residues_by_index[self.selectedID]
        
        
        '''centering and selecting'''
        frame = self.vm_session.get_frame ()
        res.get_center_of_mass(frame = frame)
        self.vm_session.glwidget.vm_widget.center_on_coordinates(res.vobject, res.mass_center)
        
        self.vm_session._selection_function (res.atoms[0], _type = 'residue')
        self.vm_session.glwidget.queue_draw()
        
        self.atom_liststore.clear()
        
        for atom in res.atoms:
            self.atom_liststore.append(list([True, int(atom.index), atom.name, atom.symbol, atom.charge, atom.atom_id ]))

        #self.treeview_atom.set_model(self.atom_liststore)
  
    
    def on_treeview_Objects_button_release_event(self, tree, event):
        #print ( tree, event)
        
        if event.button == 3:
            print ("button 3")
            #selection     = tree.get_selection()
            #model         = tree.get_model()
            #(model, iter) = selection.get_selected()
            #
            #
            #
            #if iter != None:
            #    self.selectedID  = int(model.get_value(iter, 1))  # @+
            #    self.selectedObj = str(model.get_value(iter, 2))
            #    print(self.selectedID, self.selectedObj, self.VObj.residues[self.selectedID])
            #    #self.builder.get_object('TreeViewObjLabel').set_label('- ' +self.selectedObj+' -' )
            #
            #    #widget = self.builder.get_object('treeview_menu')
            #    #widget.popup(None, None, None, None, event.button, event.time)
            #    #print ('button == 3')


        if event.button == 2:
            #print ('button == 2')
            self.treeview.get_selection().set_mode(Gtk.SelectionMode.SINGLE)

            
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()

            if iter != None:
                self.selectedID  = int(model.get_value(iter, 1))  # @+
                self.selectedObj = str(model.get_value(iter, 2))
                self.selectedChn = str(model.get_value(iter, 3))
                res = self.VObj.chains[self.selectedChn].residues_by_index[self.selectedID]
                frame = self.vm_session.get_frame ()
                res.get_center_of_mass(frame = frame)
                
                self.vm_session.glwidget.vm_widget.center_on_coordinates(res.vobject, res.mass_center)
        
                self.atom_liststore.clear()
                for atom in res.atoms:
                     self.atom_liststore.append(list([True, int(atom.index), atom.name, atom.symbol, atom.charge, atom.atom_id ]))
            
            
            
            self.treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)

        
        if event.button == 1:
            self.treeview.get_selection().set_mode(Gtk.SelectionMode.SINGLE)

            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            
            
            if iter != None:
                self.selectedID  = int(model.get_value(iter, 1))  # @+
                self.selectedObj = str(model.get_value(iter, 2))
                self.selectedChn = str(model.get_value(iter, 3))
                res = self.VObj.chains[self.selectedChn].residues_by_index[self.selectedID]
                
                
                self.atom_liststore.clear()
                #self.atom_liststore = Gtk.ListStore(bool, int, str, str, float)
                try:
                    #charges = list(self.p_session.systems[self.VObj.easyhybrid_system_id]['system'].AtomicCharges())
                    charges         = list(self.p_session.systems[self.VObj.easyhybrid_system_id]['system'].mmState.charges)
                    atomTypes       = self.p_session.systems[self.VObj.easyhybrid_system_id]['system'].mmState.atomTypes
                    atomTypeIndices = list(self.p_session.systems[self.VObj.easyhybrid_system_id]['system'].mmState.atomTypeIndices)

                    for atom in res.atoms:
                         #self.atom_liststore.append(list([True, int(atom.index), atom.name, atom.symbol,  charges[atom.index-1] , int(atom.atom_id)]))
                         self.atom_liststore.append(list([True, int(atom.index), atom.name, atomTypes[atomTypeIndices[atom.index-1]] ,  charges[atom.index-1] , int(atom.atom_id)]))
                except:
                    charges = [0]*len(self.VObj.atoms)
                    for atom in res.atoms:
                         self.atom_liststore.append(list([True, int(atom.index), atom.name, 'UNK',  charges[atom.index-1] , int(atom.atom_id)]))
                
                
                
                #self.treeview_atom.set_model(self.atom_liststore)
            self.treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)

        
      
    
    def on_chk_renderer_toggled(self, cell, path, model):
        print(model[path][0])

   
   
    def residue_filter_func(self, model, iter, data):
        """Tests if the language in the row is the one in the filter"""
        if (
            self.current_filter_residue is None
            or self.current_filter_residue == "all"
        ):
            return True
        else:
            return model[iter][2] == self.current_filter_residue
   
            
    def chain_filter_func(self, model, iter, data):
        """Tests if the language in the row is the one in the filter"""
        if (
            self.current_filter_chain is None
            or self.current_filter_chain == "all"
        ):
            return True
        else:
            return model[iter][3] == self.current_filter_chain

    #def on_selection_button_clicked(self, widget):
    #    """Called on any of the button clicks"""
    #    # we set the current language filter to the button's label
    #    self.current_filter_language = widget.get_label()
    #    print("%s language selected!" % self.current_filter_language)
    #    # we update the filter, which updates in turn the view
    #    self.language_filter.refilter()
    #
    #def on_button1_clicked(self, widget):
    #    print("Hello")
    #
    #def on_button2_clicked(self, widget):
    #    print("Goodbye")
    def update (self):
        """ Function doc """
        print('VismolGoToAtomWindow2 update')
        pass
        #self.self.combobox_systems.set_active(-1)





