import gi, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from GTKGUI.gtkWidgets.main_treeview import GtkMainTreeView
from GTKGUI.gtkWidgets.main_treeview import FileChooser

class GTKGUI ( ):
    """ Class doc """

    def gtk_load_files (self, button):
        filename = self.filechooser.open()
        if filename:
            self.vismolSession.load(filename)
            #self.main_treeview.refresh_gtk_main_treeview()
            #visObj = self.vismolSession.vismol_objects[-1]
            #self.vismolSession.glwidget.vm_widget.center_on_coordinates(visObj, visObj.mass_center)
        else:
            pass


    def __init__ (self, vismolSession = None):
        """ Class initialiser """
        self.builder = Gtk.Builder()
        self.builder.add_from_file('GTK3VisMol/MainWindow.glade')
        self.builder.connect_signals(self)
        self.window = self.builder.get_object('window1')
        self.window.set_default_size(600, 600)                          

        self.paned_V = self.builder.get_object('paned_V')
        #self.nootbook  =  self.builder.get_object('notebook2')
        #self.window = Gtk.Window(title="VisMol window")
        #self.main_box = Gtk.Box()
        
        
        
        #                         notebook_V1
        #-------------------------------------------------------------------
        self.notebook_V1 = Gtk.Notebook()
        print (self.notebook_V1.set_tab_pos(Gtk.PositionType.LEFT))
        self.page1 = Gtk.Box()
        #self.page1.set_border_width(5)
        
        self.text_view = Gtk.TextView()
        self.text_view.set_editable(True)
        self.page1.add( self.text_view)
        
        #self.page1.add(Gtk.Label('Here is the content of the first section.'))
        self.notebook_V1.append_page(self.page1, Gtk.Label('Logs'))
        #-------------------------------------------------------------------

        
        #                         notebook_H1
        #-------------------------------------------------------------------
        self.notebook_H1 = Gtk.Notebook()
        self.ScrolledWindow_notebook_H1 = Gtk.ScrolledWindow()
        #self.Tree_notebook_H1           = Gtk.TreeView()



        columns = ["First Name" ,
                   "Last Name"  ,
                   "Phone Number"]

        phonebook = [["Jurg", "Billeter", "555-0123"],
                     ["Johannes", "Schmid", "555-1234"],
                     ["Julita", "Inca", "555-2345"],
                     ["Javier", "Jardon", "555-3456"],
                     ["Jason", "Clinton", "555-4567"],
                     ["Random J.", "Hacker", "555-5678"]]





        listmodel = Gtk.ListStore(str, str, str)
        # append the values in the model
        for i in range(len(phonebook)):
            listmodel.append(phonebook[i])

        # a treeview to see the data stored in the model
        view = Gtk.TreeView(model=listmodel)
        # for each column
        for i, column in enumerate(columns):
            # cellrenderer to render the text
            cell = Gtk.CellRendererText()
            # the text in the first column should be in boldface
            if i == 0:
                cell.props.weight_set = True
                #cell.props.weight = Pango.Weight.BOLD
            # the column is created
            col = Gtk.TreeViewColumn(column, cell, text=i)
            # and it is appended to the treeview
            view.append_column(col)

        # when a row is selected, it emits a signal
        view.get_selection().connect("changed", self.on_changed)

        # the label we use to show the selection
        self.label = Gtk.Label()
        self.label.set_text("")

        # a grid to attach the widgets
        #grid = Gtk.Grid()
        #grid.attach(view, 0, 0, 1, 1)
        #grid.attach(self.label, 0, 1, 1, 1)

        # attach the grid to the window
        #self.add(grid)





        #self.ScrolledWindow_notebook_H1.add(self.Tree_notebook_H1)
        self.ScrolledWindow_notebook_H1.add(view)
        #self.page_1_notebook_H1.set_border_width(5)
        # textView

        self.notebook_H1.append_page(self.ScrolledWindow_notebook_H1, Gtk.Label('Vertical Tab'))
        #-------------------------------------------------------------------


        #                         notebook_H2
        #-------------------------------------------------------------------
        self.notebook_H2 = Gtk.Notebook()
        #-------------------------------------------------------------------
        
        
        self.paned_H = Gtk.Paned(orientation = Gtk.Orientation.HORIZONTAL)
        self.button = Gtk.Button(label="Click Here")
        #-------------------------------------------------------------------
        self.vismolSession = vismolSession#( main_session = None)
        self.filechooser   = FileChooser()
        #-------------------------------------------------------------------
        
        
        self.container = Gtk.Box (orientation = Gtk.Orientation.VERTICAL)
        
        self.vismolSession = vismolSession#( main_session = None)
        self.vismolSession.main_session = self
        
        if self.vismolSession is not None:
            self.container.pack_start(self.vismolSession.glwidget, True, True, 0)
            self.paned_H.add(self.notebook_H1)
            self.paned_H.add(self.notebook_H2)
            self.notebook_H2.append_page(self.container, Gtk.Label('view'))
            self.notebook_H2.append_page(Gtk.TextView(), Gtk.Label('view2'))

            self.paned_H.add(self.notebook_H2)

            self.paned_V.add(self.paned_H)
            #


        
        self.window.connect("delete-event",    Gtk.main_quit)
        self.window.show_all()


        Gtk.main()

    def on_changed(self, selection):
        # get the model and the iterator that points at the data in the model
        (model, iter) = selection.get_selected()
        # set the label to a new value depending on the selection
        self.label.set_text("\n %s %s %s" %
                            (model[iter][0],  model[iter][1], model[iter][2]))
        return True

    def test (self, widget):
        """ Function doc """
        self.paned_V.add(self.notebook_V1)
        self.paned_V.show()
        self.window.show_all()
