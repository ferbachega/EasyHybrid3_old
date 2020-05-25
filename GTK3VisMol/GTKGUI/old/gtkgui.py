import gi, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from VISMOL.gtkWidgets.main_treeview import GtkMainTreeView
from GTKGUI.gtkWidgets import FileChooser

class GTKGUI ( ):
    """ Class doc """

    def gtk_load_files (self, button):
        filename = self.filechooser.open()
        if filename:
            self.vismolSession.load(filename)
            self.main_treeview.refresh_gtk_main_treeview()
            visObj = self.vismolSession.vismol_objects[-1]
            self.vismolSession.glwidget.vm_widget.center_on_coordinates(visObj, visObj.mass_center)
        else:
            pass


    def __init__ (self, vismolSession = None):
        """ Class initialiser """
        #self.builder = Gtk.Builder()
        #self.builder.add_from_file('GTK3VisMol/GTKGUI/MainWindow.glade')
        #self.builder.connect_signals(self)
        #self.window = self.builder.get_object('window1')

        self.window = Gtk.Window(title="VisMol window")
        #self.button = Gtk.Button(label="Click Here")
        #self.button.connect("clicked", self.on_button_clicked)
        #self.add(self.button)
        self.vismolSession = vismolSession#( main_session = None)
        self.filechooser   = FileChooser()
        #self.button        = Gtk.Button('open')
        
        #self.button.set_hexpand(False)
        
        #self.button.connect('clicked', self.gtk_load_files)
        self.container = Gtk.Box (orientation = Gtk.Orientation.VERTICAL)
        #self.container.pack_start(self.button, True, True, 0)
        
        self.vismolSession = vismolSession#( main_session = None)
        self.vismolSession.main_session = self
        
        if self.vismolSession is not None:
            self.container.pack_start(self.vismolSession.glwidget, True, True, 0)
            self.window.connect("key-press-event"  , self.vismolSession.glwidget.key_pressed)
            self.window.connect("key-release-event", self.vismolSession.glwidget.key_released)
            self.window.add(self.container)

        
        self.window.connect("delete-event",    Gtk.main_quit)
        self.window.show_all()

        #self.vismolSession.load('/home/fernando/programs/EasyHybrid3/Coords/pdbs/step5_assembly.pdb')
        #visObj = self.vismolSession.vismol_objects[-1]
        #self.vismolSession.glwidget.vm_widget.center_on_coordinates(visObj, visObj.mass_center)
        Gtk.main()
