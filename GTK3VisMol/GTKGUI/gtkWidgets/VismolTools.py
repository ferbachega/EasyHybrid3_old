import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk




class VismolGoToAtomWindow2(Gtk.Window):
    def OpenWindow (self):
        """ Function doc """
        if self.Visible  ==  False:
            
            self.VMSession.Vismol_Objects_ListStore
            
            #------------------------------------------------------------------#
            #                  VISOBJ combobox and Label
            #------------------------------------------------------------------#
            self.box_vertical    = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,   spacing = 6)
            self.box_horizontal1 = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 6)
            
            
            self.label1  = Gtk.Label()
            self.label1.set_text('Object:')
            self.box_horizontal1.pack_start(self.label1, False, False, 0)

            combobox_vobjects = Gtk.ComboBox.new_with_model(self.VMSession.Vismol_Objects_ListStore)
            combobox_vobjects.connect("changed", self.on_combobox_vobjects_changed)
            renderer_text = Gtk.CellRendererText()
            combobox_vobjects.pack_start(renderer_text, True)
            combobox_vobjects.add_attribute(renderer_text, "text", 2)
            #vbox.pack_start(combobox_vobjects, False, False, True)

            self.box_horizontal1.pack_start(combobox_vobjects, False, False, 0)
            #------------------------------------------------------------------#
            
            
            
            #------------------------------------------------------------------#
            #                  CHAIN combobox and Label
            #------------------------------------------------------------------#
            self.box_horizontal2 = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 6)
            
            
            self.label2  = Gtk.Label()
            self.label2.set_text('Chain:')
            self.box_horizontal2.pack_start(self.label2, False, False, 0)

            liststore_chains = Gtk.ListStore(str)
            
            combobox_chains = Gtk.ComboBox.new_with_model(liststore_chains)
            combobox_chains.connect("changed", self.on_combobox_vobjects_changed)
            renderer_text = Gtk.CellRendererText()
            combobox_chains.pack_start(renderer_text, True)
            combobox_chains.add_attribute(renderer_text, "text", 0)
            #vbox.pack_start(combobox_chains, False, False, True)
            self.box_horizontal2.pack_start(combobox_chains, False, False, 0)

            #------------------------------------------------------------------#
            
            
            
            
            
            self.treeviewbox_horizontal = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 6)
            
            #------------------------------------------------------------------------------------------
            self.treeview = Gtk.TreeView(model =self.residue_liststore)
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

            self.scrollable_treelist = Gtk.ScrolledWindow()
            self.scrollable_treelist.set_vexpand(True)
            self.scrollable_treelist.add(self.treeview)
            #------------------------------------------------------------------------------------------
            
            
            
            
            
            #------------------------------------------------------------------------------------------
            self.treeview_atom = Gtk.TreeView(model =self.atom_liststore)
            self.treeview_atom.connect("button-release-event", self.on_treeview_atom_button_release_event)
            
            for i, column_title in enumerate(
                ['', "index", "name",  "type", 'mass']
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

            #self.project          = self.EasyHybridSession.project
            #self.builder = gtk.Builder()
            #self.builder.add_from_file(
            #    os.path.join(EasyHybrid_GUI,'WindowScan1D', 'ScanWindow.glade'))
            #
            #self.builder.connect_signals(self)
            #self.window = self.builder.get_object('ScanWindow')
            #self.sigma_pk1_pk3 = None
            #self.sigma_pk3_pk1 = None
            #self.builder.get_object("ScanDialog_SCAN_entry_trajectory_name").set_text(text)
            #
            #
            #'''
            #--------------------------------------------------
            #-                                                -
            #-	              WindowControl                  -
            #-                                                -
            #--------------------------------------------------
            #'''        
            #self.window_control = WindowControl(self.builder)
            #
            ##--------------------- Setup ComboBoxes -------------------------
            #combobox  = 'ScanDialog_combobox_SCAN_reaction_coordiante_type'                     
            #combolist = ['simple-distance', 'multiple-distance']
            #self.window_control.SETUP_COMBOBOXES(combobox, combolist, self.distanceType)     
            #
            #combobox  = 'ScanDialog_combobox_optimization_method'                     
            #combolist = ['Conjugate Gradient', 'Steepest Descent','LBFGS']
            #self.window_control.SETUP_COMBOBOXES(combobox, combolist, self.minitype )     
            #                                                                                                 
            #
            self.window =  Gtk.Window()
            self.window.set_border_width(10)
            self.window.set_default_size(600, 600)  
            self.window.add(self.box_vertical)
            self.window.connect("destroy", self.CloseWindow)
            self.window.show_all()                                               
            #                                                                
            #self.builder.connect_signals(self)                                   
            
            self.Visible  =  True
            #self.PutBackUpWindowData()
            #gtk.main()
            #----------------------------------------------------------------

    def CloseWindow (self, button):
        """ Function doc """
        #self.BackUpWindowData()
        self.window.destroy()
        self.Visible    =  False
        print('self.Visible',self.Visible)
    
    def __init__(self, VMSession = None):
        """ Class initialiser """
        self.VMSession = VMSession
        #if EasyHybridSession != None:
        #    self.project          = EasyHybridSession.project
        #    self.main_builder     = EasyHybridSession.builder
        #    self.EasyHybridSession = EasyHybridSession        
        #    self.window_control   = EasyHybridSession.window_control
        #
        #self.atom1_index = ''
        #self.name1       = ''
        #self.atom2_index = ''
        #self.name2       = ''
        #self.atom3_index = ''
        #self.name3       = ''
        #
        #
        #self.distanceType  = 0
        #self.DMINIMUM      = ''
        #self.minitype      = 0
        #
        #self.DINCREMENT    = '0.1'
        #self.NWINDOWS      = '10'
        #self.FORCECONSTANT = '4000'
        #self.max_int       = '500'
        #self.rms_grad      = '0.1'
        #
        #self._mass_weight_check = False
        #
        #
        #self.project   =  project
        self.Visible    =  False
        
        self.residue_liststore = Gtk.ListStore(bool, int, str, str, int)
        self.atom_liststore    = Gtk.ListStore(bool, int, str, str, int)




    
    def on_combobox_vobjects_changed (self, widget):
        """ Function doc """
        print(widget)
        print(widget.get_active())
        #print(widget.get_active_id())
        #print(widget.get_active_iter())
        self.VObj = self.VMSession.vismol_objects[widget.get_active()]
        
        
        self.residue_liststore = Gtk.ListStore(bool, int, str, str, int)
        for chain in self.VObj.chains:
            for res in self.VObj.chains[chain].residues:
                #print(res.resi, res.resn, chain,  len(res.atoms) ) 
                
                self.residue_liststore.append(list([True, res.resi, res.resn, chain,  len(res.atoms)]))
        self.treeview.set_model(self.residue_liststore)
        

        
        
    def on_treeview_atom_button_release_event(self, tree, event):
        if event.button == 2:
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            
            
            if iter != None:
                self.selectedID  = int(model.get_value(iter, 1))-1  # @+
                atom = self.VObj.atoms[self.selectedID]
                self.VMSession.glwidget.vm_widget.center_on_atom(atom)
                #self.selectedObj = str(model.get_value(iter, 2))
                #res = self.VObj.residues[self.selectedID]
                
                #self.atom_liststore = Gtk.ListStore(bool, int, str, str, float)
                #for atom in res.atoms:
                #     self.atom_liststore.append(list([True, int(atom.index), atom.name, atom.symbol, atom.charge]))
                
                #self.treeview_atom.set_model(self.atom_liststore)        
        
    
    def on_treeview_row_activated_event(self, tree, rowline , column ):
        #print (A,B,C)
        selection     = tree.get_selection()
        model         = tree.get_model()
        
        print(model)
        print(rowline, list(model[rowline]))
        
        data  = list(model[rowline])
        self.selectedID  = int(data[1])  # @+
        self.selectedObj = str(data[2])
        self.selectedChn = str(data[3])
        res = self.VObj.chains[self.selectedChn].residues_by_index[self.selectedID]

        self.atom_liststore = Gtk.ListStore(bool, int, str, str, float)
        for atom in res.atoms:
            self.atom_liststore.append(list([True, int(atom.index), atom.name, atom.symbol, atom.charge]))

        self.treeview_atom.set_model(self.atom_liststore)
        
        #for item in model:
        #    print(item)
        #(model, iter) = selection.get_selected()
        
        #if iter != None:
        #    self.selectedID  = int(model.get_value(iter, 1))-1  # @+
            
        #    print (self.selectedID)
            #atom = self.VObj.atoms[self.selectedID]
            #self.VMSession.glwidget.vm_widget.center_on_atom(atom)
    
    
    
    def on_treeview_Objects_button_release_event(self, tree, event):
        print ( tree, event)
        
        if event.button == 3:
            print (3)
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
            print ('button == 2')
            self.treeview.get_selection().set_mode(Gtk.SelectionMode.SINGLE)

            
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()

            if iter != None:
                self.selectedID  = int(model.get_value(iter, 1))  # @+
                self.selectedObj = str(model.get_value(iter, 2))
                self.selectedChn = str(model.get_value(iter, 3))
                res = self.VObj.chains[self.selectedChn].residues_by_index[self.selectedID]
                frame = self.VMSession.get_frame ()
                res.get_center_of_mass(frame = frame)
                
                self.VMSession.glwidget.vm_widget.center_on_coordinates(res.Vobject, res.mass_center)
        
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
                
                self.atom_liststore = Gtk.ListStore(bool, int, str, str, float)
                for atom in res.atoms:
                     self.atom_liststore.append(list([True, int(atom.index), atom.name, atom.symbol, atom.charge]))
                
                self.treeview_atom.set_model(self.atom_liststore)
            self.treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)

        
        

    
    def on_chk_renderer_toggled(self, cell, path, model):
        print(model[path][0])

            
    def language_filter_func(self, model, iter, data):
        """Tests if the language in the row is the one in the filter"""
        if (
            self.current_filter_language is None
            or self.current_filter_language == "None"
        ):
            return True
        else:
            return model[iter][2] == self.current_filter_language

    def on_selection_button_clicked(self, widget):
        """Called on any of the button clicks"""
        # we set the current language filter to the button's label
        self.current_filter_language = widget.get_label()
        print("%s language selected!" % self.current_filter_language)
        # we update the filter, which updates in turn the view
        self.language_filter.refilter()

    def on_button1_clicked(self, widget):
        print("Hello")

    def on_button2_clicked(self, widget):
        print("Goodbye")



class VismolTrajectoryFrame(Gtk.Box):
    """ Class doc """
    
    def __init__ (self, VMSession = None):
        """ Class initialiser """
        self.VMSession = VMSession 
        
        self.box        = Gtk.Box() 
        self.value      = 0
        self.scale      = Gtk.Scale()
        self.adjustment = Gtk.Adjustment(self.value, 0, 100, 0, 10, 0)
        self.scale.set_adjustment ( self.adjustment)
        
        #self.box.add(self.scale)
        self.box.pack_start(self.scale, True, True, 0)
        
        
        
        win = Gtk.Window()
        win.add(self.box)
        win.show_all()        
        Gtk.main()

#VismolTrajectoryFrame()





