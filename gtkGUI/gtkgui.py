import gi, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from gtkGUI.gtkWidgets.AnimateTrajectory import AnimatedWindow
from gtkGUI.gtkWidgets.console import ConsoleWindow
#from VISMOL.gtkWidgets.main_treeview import GtkMainTreeView


class FileChooser:
    """ Class doc """
    
    def __init__ (self, main_window = None):
        """ Class initialiser """
        self.main_window = main_window

    
    def open (self):

        """ Function doc """
        #main = gtkmain
        main = self.main_window
        filename = None
        
        chooser = Gtk.FileChooserDialog("Open File...", main,0,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OK, Gtk.ResponseType.OK))

        filter = Gtk.FileFilter()  
        filter.set_name("PDB files - *.pdb")
        #
        filter.add_mime_type("PDB files")
        filter.add_pattern("*.pdb")
        #
        chooser.add_filter(filter)
        filter = Gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        #
        chooser.add_filter(filter)  

        response = chooser.run()
        if response == Gtk.ResponseType.OK:
            filename = chooser.get_filename()
        chooser.destroy()
        return filename
       

class GtkMainTreeView():
    """ 
    """
    
    def __init__(self, vismolSession):
        """ 
        """
        self.builder = Gtk.Builder()
        self.builder.add_from_file('gtkGUI/gtkWidgets/main_treeview.glade')
        self.builder.connect_signals(self)
        self.vismolSession = vismolSession
        self.treeView = self.builder.get_object('treeview1')
        
        #self.liststore = self.builder.get_object('liststore1')
        self.liststore = Gtk.ListStore(bool, str, str, str, str)
        
        
        self.treeView.set_model(self.liststore)

    def refresh_gtk_main_treeview (self):
        """ Function doc """
        #print ('refresh_gtk_main_self.treeView',)
        #print (widget)
        #liststore = self.builder.get_object('liststore1')
        model = self.liststore  
        model.clear()
        n = 0
        i = 1
        
        for vis_object in self.vismolSession.vismol_objects:
            print ('\n\n',vis_object.name,'\n\n')
            
            if vis_object.actived:
                actived = True
            else:
                actived = False
        
            data = [actived, str(i)        ,
                   vis_object.name      , 
                   str(len(vis_object.atoms)) , 
                   str(len(vis_object.frames)),
                   ]
            model.append(data)
            i +=1
            n = n + 1
        self.treeView.set_model(model)
        print ('load fuction finished')
        
    
    
    def on_treeview_Objects_button_release_event(self, tree, event):
        if event.button == 3:
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            if iter != None:
                self.selectedID  = str(model.get_value(iter, 1))  # @+
                self.selectedObj = str(model.get_value(iter, 2))
    
                self.builder.get_object('TreeViewObjLabel').set_label('- ' +self.selectedObj+' -' )

                widget = self.builder.get_object('treeview_menu')
                widget.popup(None, None, None, None, event.button, event.time)
                print ('button == 3')


        if event.button == 2:
            #selection     = tree.get_selection()
            #model         = tree.get_model()
            #(model, iter) = selection.get_selected()
            #pymol_object = model.get_value(iter, 0)
            self.refresh_gtk_main_self.treeView()
            print ('button == 2')
            
            #self.selectedID  = int(model.get_value(iter, 1))  # @+
            #self.vismolSession.center(Vobject_index = self.selectedID -1)

        if event.button == 1:
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            print ('button == 1')

            if iter != None:
                #print model, iter
                pymol_object  = model.get_value(iter, 2)  # @+
                true_or_false = model.get_value(iter, 0)
                obj_index     = model.get_value(iter, 1)
                #print pymol_object
                if true_or_false == False:
                    self.vismolSession.enable_by_index(int(obj_index)-1)
                    true_or_false = True
                    model.set(iter, 0, true_or_false)
                    # print true_or_false
                    self.vismolSession.glwidget.queue_draw()
                
                else:
                    self.vismolSession.disable_by_index(int(obj_index)-1)
                    true_or_false = False
                    model.set(iter, 0, true_or_false)
                    self.vismolSession.glwidget.queue_draw()
       
    def on_treemenu_item_selection (self, widget, event = None , data = None):
        """ Function doc """
        
        if widget == self.builder.get_object('menuitem5_rename'):
            tree = self.builder.get_object('treeview1')
            selection = tree.get_selection()
            model = tree.get_model()
            (model, iter) = selection.get_selected()
            obj_index = model.get_value(iter, 1)
            self.vismolSession.edit_by_index(int(obj_index)-1)
            self.vismolSession.glwidget.vm_widget.editing_mols = not self.vismolSession.glwidget.vm_widget.editing_mols
    


        tree = self.builder.get_object('treeview1')
        selection = tree.get_selection()
        model = tree.get_model()
        (model, iter) = selection.get_selected()
        obj_index = model.get_value(iter, 1)
        visObj = self.vismolSession.vismol_objects[(int(obj_index)-1)]

        
        if widget == self.builder.get_object('menuitem_center'):
            self.vismolSession.glwidget.vm_widget.center_on_coordinates(visObj, visObj.mass_center)

        
        if widget == self.builder.get_object('menu_show_lines'):
            visObj.lines_actived     =  True
            #self.vismolSession._show_lines (visObj = visObj)


        if widget == self.builder.get_object('menu_show_sticks'):
            visObj.sticks_actived =  True

        if widget == self.builder.get_object('menu_show_spheres'):
            visObj.spheres_actived   =  True

        if widget == self.builder.get_object('menu_show_ribbons'):
            visObj.ribbons_actived   =  True

        if widget == self.builder.get_object('menu_show_dots'):
            visObj.dots_actived      =  True
            self.vismolSession.glwidget.vm_widget.queue_draw()


        
        
        if widget == self.builder.get_object('menu_hide_lines'):
            visObj.lines_actived     = False
            #self.vismolSession._hide_lines (visObj = visObj)

        if widget == self.builder.get_object('menu_hide_sticks'):
            visObj.sticks_actived = False

        if widget == self.builder.get_object('menu_hide_spheres'):
            visObj.spheres_actived   = False

        if widget == self.builder.get_object('menu_hide_ribbons'):
            visObj.ribbons_actived   = False
            
        if widget == self.builder.get_object('menu_hide_dots'):
            visObj.dots_actived      = False
            self.vismolSession.glwidget.vm_widget.queue_draw()
        


class GTKTerminalGUI():
    def __init__ (self, vismolSession = None):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('GTK3VisMol/GTKGUI/GTKTerminalGUI.glade')
        self.builder.connect_signals(self)
        self.TerminalLabel = Gtk.Label('Terminal')
        self.TerminalBox   = self.builder.get_object('box4')
        self.vismolSession = vismolSession
        
        
        self.command_list  = [] 
        self.counter       = 0
        
    def on_entry1_activate (self, widget, click=None):
        """ Function doc """
        text =  self.builder.get_object('entry1').get_text()
        self.command_list.append(text)

        self.vismolSession.command_line(text)
        self.builder.get_object('entry1').set_text('')
        self.counter       += 1

    def on_key_pressed (self, widget, click=None):
        print (click)
        




class MainMenu:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        pass

class ToolBar:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        pass
    
    def on_button_pDynamo (self, widget, click=None):
        """ Function doc """
        print ("Save")
        #'''
        
        import glob, math, os.path

        from pBabel                    import ExportSystem                                 , \
                                              ImportCoordinates3                           , \
                                              ImportSystem                                 , \
                                              SMILES_ToSystem                              , \
                                              SystemGeometryTrajectory                     , \
                                              SystemRestraintTrajectory
        from pCore                     import Clone                                        , \
                                              logFile                                      , \
                                              Selection                                    , \
                                              TestScript_InputDataPath                     , \
                                              TestScript_OutputDataPath                    , \
                                              XHTMLLogFileWriter
        from pMolecule                 import RestraintDistance                            , \
                                              RestraintEnergyModelHarmonic                 , \
                                              RestraintEnergyModelHarmonicRange            , \
                                              RestraintModel                               , \
                                              RestraintTether                              , \
                                              System                                       , \
                                              SystemGeometryObjectiveFunction
        from pMolecule.MMModel         import MMModelOPLS
        from pMolecule.NBModel         import NBModelCutOff                                , \
                                              NBModelFull                                  , \
                                              NBModelMonteCarlo                            , \
                                              NBModelORCA                                  , \
                                              PairwiseInteractionABFS
        from pMolecule.QCModel         import DIISSCFConverger                             , \
                                              QCModelMNDO
        from pScientific               import Constants                                    , \
                                              Units
        from pScientific.Arrays        import ArrayPrint2D
        from pScientific.Geometry3     import PairListGenerator                            , \
                                              Vector3
        from pScientific.RandomNumbers import NormalDeviateGenerator                       , \
                                              RandomNumberGenerator
        from pScientific.Statistics    import Statistics
        from pScientific.Symmetry      import CrystalSystemCubic                           , \
                                              PeriodicBoundaryConditions                   , \
                                              SymmetryParameters
        from pSimulation               import BakerSaddleOptimize_SystemGeometry           , \
                                              BuildCubicSolventBox                         , \
                                              BuildHydrogenCoordinates3FromConnectivity    , \
                                              BuildSolventBox                              , \
                                              ChainOfStatesOptimizePath_SystemGeometry     , \
                                              ConjugateGradientMinimize_SystemGeometry     , \
                                              GrowingStringInitialPath                     , \
                                              LeapFrogDynamics_SystemGeometry              , \
                                              MergeByAtom                                  , \
                                              MonteCarlo_IsolateInteractionEnergy          , \
                                              MonteCarlo_ScaleIsolateInteractionParameters , \
                                              MonteCarlo_SystemGeometry                    , \
                                              NormalModes_SystemGeometry                   , \
                                              NormalModesTrajectory_SystemGeometry         , \
                                              PruneByAtom                                  , \
                                              RadialDistributionFunction                   , \
                                              SelfDiffusionFunction                        , \
                                              SolventCubicBoxDimensions                    , \
                                              SolvateSystemBySuperposition                 , \
                                              SteepestDescentPath_SystemGeometry           , \
                                              SystemDensity                                , \
                                              ThermodynamicsRRHO_SystemGeometry            , \
                                              VelocityVerletDynamics_SystemGeometry        , \
                                              WHAM_ConjugateGradientMinimize

        # . Local name.
        _name  = "book"

        # . The input data paths.
        dataPath = TestScript_InputDataPath ( _name )
        molPath  = os.path.join ( dataPath, "mol" )
        pdbPath  = os.path.join ( dataPath, "pdb" )
        pklPath  = os.path.join ( dataPath, "pkl" )
        xyzPath  = os.path.join ( dataPath, "xyz" )

        # . The output data path.
        scratchPath = TestScript_OutputDataPath ( _name )
        
        
        
        
        
        
        
        
        
        
        
        
        
        molecule = ImportSystem ( os.path.join ( xyzPath, "bala_c7eq.xyz" ) )
        molecule.DefineQCModel ( QCModelMNDO.WithOptions ( hamiltonian = "am1" ) )
        molecule.Summary ( )

        # . Save a copy of the starting coordinates.
        coordinates3 = Clone ( molecule.coordinates3 )

        # . Determine the starting energy.
        eStart = molecule.Energy ( )

        # . Optimization.
        ConjugateGradientMinimize_SystemGeometry ( molecule                    ,
                                                   logFrequency         =  1   ,
                                                   maximumIterations    =  5   ,
                                                   rmsGradientTolerance =  0.1 )

        # . Determine the final energy.
        eStop = molecule.Energy ( )

        # . Determine the RMS coordinate deviation between the optimized and unoptimized structures.
        masses = molecule.atoms.GetItemAttributes ( "Mass" )
        coordinates3.Superimpose ( molecule.coordinates3, weights = masses )
        rms = coordinates3.RootMeanSquareDeviation ( molecule.coordinates3, weights = masses )

        # . Print the results.
        table = logFile.GetTable ( columns = [ 30, 30 ] )
        table.Start ( )
        table.Title ( "Minimization Results" )
        table.Entry ( "Energy Change",            alignment = "l" )
        table.Entry ( "{:20.4f}".format ( eStop - eStart ) )
        table.Entry ( "RMS Coordinate Deviation", alignment = "l" )
        table.Entry ( "{:20.4f}".format ( rms ) )
        table.Stop ( )
        #XYZFile_FromSystem ( xyzPath, molecule, label = 'text.xyz', xyz = 'text_name.xyz' )
        
        #self.vismolSession.load (infile = os.path.join ( xyzPath, "bala_c7eq.xyz" ) )
        #self.main_treeview.refresh_gtk_main_treeview()
        #visObj = self.vismolSession.vismol_objects[-1]
        #self.vismolSession.glwidget.vm_widget.center_on_coordinates(visObj, visObj.mass_center)
        
        
        #self.vismolSession.glwidget.render()
        #self.vismolsession.refresh_gtk()
        #'''
    
    def on_file_open_activate (self, widget, click=None):
        """ Function doc """
        self.gtk_load_files()
        
    def on_terminal_button (self, widget, click=None):
        """ Function doc """
        #print ("terminal")
        if widget.get_active():
            self.vismolConsole.open_window()
            self.vismolConsole.actived =  True
        else:
            print ('desligado')
            self.vismolConsole.window.destroy()
            self.vismolConsole.actived =  False
    
    def on_main_toolbar_open_animate_trajectory (self, widget):
        """ Function doc """
        #animated_window = AnimatedWindow(self)
        if widget == self.builder.get_object('toolbutton_trajectory_tool'):
            if widget.get_active() == True:
                self.TrajectoryTool.open_window()
                self.TrajectoryTool.actived =  True
            else:
                print ('desligado')
                self.TrajectoryTool.window.destroy()
                self.TrajectoryTool.actived =  False

class GLMenu:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        pass

class GTKGUI (MainMenu,ToolBar,GLMenu):
    """ Class doc """
    
    def test_gl (self, widget):
        """ Function doc """
        self.vismolSession.glwidget.test_gl()
        
    def gtk_load_files (self):
        """ Function doc """
        filename = self.filechooser.open()
        if filename:
            self.vismolSession.load(filename)
            self.main_treeview.refresh_gtk_main_treeview()
            visObj = self.vismolSession.vismol_objects[-1]
            self.vismolSession.glwidget.vm_widget.center_on_coordinates(visObj, visObj.mass_center)
        else:
            pass
    
    def on_treemenu_item_selection (self, widget):
        """ Function doc """
        #print ( widget)
        if widget == self.builder.get_object('menuitem6_center'):
            tree = self.builder.get_object('treeview1')
            selection = tree.get_selection()
            model = tree.get_model()
            (model, iter) = selection.get_selected()
            obj_index = model.get_value(iter, 1)
            visObj = self.vismolSession.vismol_objects[(int(obj_index)-1)]
            self.vismolSession.glwidget.vm_widget.center_on_coordinates(visObj, visObj.mass_center)
        if widget == self.builder.get_object('menuitem5_rename'):
            tree = self.builder.get_object('treeview1')
            selection = tree.get_selection()
            model = tree.get_model()
            (model, iter) = selection.get_selected()
            obj_index = model.get_value(iter, 1)
            self.vismolSession.edit_by_index(int(obj_index)-1)
            self.vismolSession.glwidget.vm_widget.editing_mols = not self.vismolSession.glwidget.vm_widget.editing_mols
        
    def on_resize (self, widget):
        """ Function doc """
        print(widget)
        print(self.window.get_size ())
    
    def __init__ (self, vismolSession = None):
	    """ Class initialiser """
	    #glarea = gda.GLCanvas()

	    #self.glarea  = glarea
	    self.builder = Gtk.Builder()
	    self.builder.add_from_file('gtkGUI/MainWindow.glade')
	    self.builder.connect_signals(self)

	    self.window = self.builder.get_object('window1')

	    self.main_treeview =  GtkMainTreeView(vismolSession = vismolSession)
	    self.main_treeview.treeView

	    #self.main_treeview =  self.vismolSession.get_gtk_main_treeview ()
	    #get_gtk_main_treeview (self)


	    self.window.show_all()
	    self.TrajectoryTool = AnimatedWindow(self)
	    self.vismolConsole  = ConsoleWindow(self)
	    self.filechooser    = FileChooser()
	    self.textarea = Gtk.TextView()


	    self.notebook = Gtk.Notebook()
	    self.notebook.append_page(self.main_treeview.builder.get_object('scrolledwindow1'))
	    self.builder.get_object('paned_V').add(self.notebook)
	    #self.builder.get_object('notebook1').append_page(self.main_treeview.builder.get_object('scrolledwindow1'))
													     #'Objects')


	    #'''
	    self.vismolSession = vismolSession#( main_session = None)

	    #self.vismolSession.main_session = self




	    #self.vismolSession.build_gtkWidgets(self.builder.get_object("window1"))  
	    #self.main_treeview =  self.vismolSession.get_gtk_main_treeview ()
	    #scrolledwindow1 = Gtk.ScrolledWindow()
	    #scrolledwindow1.add(self.main_treeview) 
	    #self.builder.get_object('notebook1').append_page(scrolledwindow1)



	    #-----------------------------------------------------------------------------------
	    if self.vismolSession is not None:
		    
		    self.container = self.builder.get_object('paned2')

		    self.container.add(self.vismolSession.glwidget)
		    self.window.connect("key-press-event"  , self.vismolSession.glwidget.key_pressed)
		    self.window.connect("key-release-event", self.vismolSession.glwidget.key_released)

	    self.window.connect("delete-event",    Gtk.main_quit)
	    #self.window.set_size_request(800,800)



	    #  -------------- GTK Terminal GUI --------------
	    #self.gtkTerminalGui = GTKTerminalGUI(vismolSession)

	    #self.container2 = self.builder.get_object('paned_V')
	    #self.container2.add(self.textarea)
	    #print (a ,b, " <----------aqui oh")
	    #self.gtkTerminalGui.TerminalBox.hide()
	    #'''
	    #-----------------------------------------------------------------------------------



	    Gtk.main()



	    #window.set_size_request(800,600)
	    #self.handlers = {"on_btn_BallStick_clicked": self.glarea.switch_ball_stick,
	    #                 "on_file_quit_activate":    gtk.main_quit}
	    #self.builder.connect_signals(self.handlers)

	    #self.window.connect('key_press_event', self.EMSession.glarea.key_press)

	    #self.vbox = self.builder.get_object('vbox1')
	    #self.vbox.pack_start(self.EMSession.glarea, True, True)
	    #self.window.show_all()

	    #self.builder.get_object('toolbar_trajectory').hide()
	    #self.builder.get_object('notebook1').hide()


		      #------------------------------------------------#
		      #-                 WindowControl                 #
		      #------------------------------------------------#
	    ##------------------------------------------------------------#
	    #self.window_control = WindowControl(self.builder)            #
	    #
	    ##------------------------------------------------------------#
	    #
	    ##--------------------- Setup ComboBoxes ---------------------#
	    ##                                                            #
	    #combobox = 'combobox1'                                       #
	    #combolist = ["Atom", "Residue", "Chain", "Molecule"]         #
	    #self.window_control.SETUP_COMBOBOXES(combobox, combolist, 1) #
	    ##------------------------------------------------------------#
