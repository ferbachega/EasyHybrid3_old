import gi, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from GTKGUI.gtkWidgets.main_treeview import GtkMainTreeView
from GTKGUI.gtkWidgets.main_treeview import FileChooser

class VismolMainWindow ( ):
    """ Class doc """

    def gtk_load_files (self, button):
        filename = self.filechooser.open()
        if filename:
            self.vismolSession.load(filename)
            
            #self.treeview.append()
            #self.treeview.refresh_gtk_main_treeview()
            visObj = self.vismolSession.vismol_objects[-1]
            self.treeview.append(visObj)

            #self.vismolSession.glwidget.vm_widget.center_on_coordinates(visObj, visObj.mass_center)
        else:
            pass


    def __init__ (self, vismolSession = None):
        """ Class initialiser """
        self.builder = Gtk.Builder()
        self.builder.add_from_file('GTK3VisMol/GTKGUI/MainWindow.glade')
        self.builder.connect_signals(self)
        self.window = self.builder.get_object('window1')
        self.window.set_default_size(600, 600)                          

        self.paned_V = self.builder.get_object('paned_V')
        #self.nootbook  =  self.builder.get_object('notebook2')
        #self.window = Gtk.Window(title="VisMol window")
        #self.main_box = Gtk.Box()
        self.vismolSession = vismolSession#( main_session = None)
        self.vismolSession.main_session = self
        
        
        #                         notebook_V1
        #-------------------------------------------------------------------
        self.notebook_V1 = Gtk.Notebook()
        #print (self.notebook_V1.set_tab_pos(Gtk.PositionType.LEFT))
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
        self.treeview = GtkMainTreeView(vismolSession)
        #self.treeview  = self.gtkTreeViewObj.treeview
        self.ScrolledWindow_notebook_H1.add(self.treeview)
        self.notebook_H1.append_page(self.ScrolledWindow_notebook_H1, Gtk.Label('Vertical Tab'))

        
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
        self.vismolSession = vismolSession#( main_session = None)
        self.filechooser   = FileChooser()
        #-------------------------------------------------------------------
        
        
        self.container = Gtk.Box (orientation = Gtk.Orientation.VERTICAL)
        self.command_line_entry = Gtk.Entry()

        
        if self.vismolSession is not None:
            self.container.pack_start(self.vismolSession.glwidget, True, True, 0)
            
            self.container.pack_start(self.command_line_entry, False, False, 0)
            self.paned_H.add(self.notebook_H1)
            self.paned_H.add(self.notebook_H2)
            
            self.notebook_H2.append_page(self.container, Gtk.Label('view'))
            self.notebook_H2.append_page(Gtk.TextView(), Gtk.Label('logs'))


            self.paned_V.add(self.paned_H)


        
        self.window.connect("delete-event",    Gtk.main_quit)
        self.window.show_all()


        Gtk.main()



    def test (self, widget):
        """ Function doc """
        container = Gtk.Box (orientation = Gtk.Orientation.VERTICAL)
        container.pack_start(self.notebook_V1, True, True, 0)
        container.pack_start(self.command_line_entry, False, False, 0)
        self.paned_V.add(container)
        self.paned_V.show()
        self.window.show_all()



class GtkMainTreeView(Gtk.TreeView):
    """ Class doc """
    
    def __init__ (self, vismolSession):
        """ Class initialiser """
        
        Gtk.TreeView.__init__(self)
        self.vismolSession = vismolSession
        self.treeview_menu = TreeViewMenu(self)
        self.store         = Gtk.ListStore(bool,str , str ,str, str)

        self.set_model(self.store)



        #----------------------------------------------------------------------
        # the cellrenderer for the second column - boolean rendered as a toggle
        renderer_toggle = Gtk.CellRendererToggle()
        # the second column is created
        column_in_out = Gtk.TreeViewColumn("", renderer_toggle, active=0)
        # and it is appended to the treeview
        self.append_column(column_in_out)
        # connect the cellrenderertoggle with a callback function
        renderer_toggle.connect("toggled", self.on_toggled)


        # the cellrenderer for text columns
        renderer_text = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("id",     renderer_text, text=1)
        self.append_column(column)

        renderer_text = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Object", renderer_text, text=2)
        self.append_column(column)
    
        renderer_text = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Atoms",  renderer_text, text=3)
        self.append_column(column)
    
        renderer_text = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Frames", renderer_text, text=4)
        self.append_column(column)

        self.connect('button-release-event', self.on_treeview_Objects_button_release_event )
        #----------------------------------------------------------------------

    
    
    def on_toggled(self, widget, path):
        # the boolean value of the selected row
        current_value = self.store[path][0]

        # change the boolean value of the selected row in the model
        self.store[path][0] = not current_value       
        if self.store[path][0]:
            obj_index = self.store[path][1]
            self.vismolSession.enable_by_index(int(obj_index))
            self.vismolSession.glwidget.queue_draw()
        else:
            obj_index = self.store[path][1]
            self.vismolSession.disable_by_index(int(obj_index))
            self.vismolSession.glwidget.queue_draw()
 
    
    def append(self, visObj):
        i = self.vismolSession.vismol_objects.index(visObj)
        
        data = [visObj.active         , 
               str(i)                 ,
               visObj.name            , 
               str(len(visObj.atoms)) , 
               str(len(visObj.frames)),
               ]
        print (data)
        self.store.append(data)
        #self.set_model(self.liststore)
    
    def remove (self):
        """ Function doc """
        
    def on_treeview_Objects_button_release_event(self, tree, event):
        if event.button == 3:
            selection     = self.get_selection()
            model         = self.get_model()
            (model, iter) = selection.get_selected()
            if iter != None:
                self.selectedID  = str(model.get_value(iter, 1))  # @+
                self.selectedObj = str(model.get_value(iter, 2))
    
                self.treeview_menu.open_menu(self.selectedObj)
                
                #self.builder.get_object('TreeViewObjLabel').set_label('- ' +self.selectedObj+' -' )

                #widget = self.builder.get_object('treeview_menu')
                #widget.popup(None, None, None, None, event.button, event.time)
                #print ('button == 3')


        if event.button == 2:
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            #pymol_object = model.get_value(iter, 0)
            #self.refresh_gtk_main_self.treeView()
            print ('button == 2')
            
            self.selectedID  = int(model.get_value(iter, 1))  # @+
            visObj = self.vismolSession.vismol_objects[self.selectedID]
            self.vismolSession.center(visObj)

        if event.button == 1:
            print ('event.button == 1:')
    

class TreeViewMenu:
    """ Class doc """
    
    def __init__ (self, treeview):
        """ Class initialiser """
        pass
        self.treeview = treeview
        
        functions = {
                'test':self.f1 ,
                'f1': self.f1,
                'f2': self.f2,
                'delete': self.f3,
        }
        self.build_glmenu(functions)



    def f1 (self):
        """ Function doc """
        print('f1')
        
    def f2 (self):
        """ Function doc """
        print('f2')
        self._show_lines(visObj = self.vismol_objects[0], indices = [0,1,2,3,4] )
    
    def f3 (self, visObj = None):
        """ Function doc """
        
        selection     = self.treeview.get_selection()
        (model, iter) = selection.get_selected()


        self.selectedID  = int(model.get_value(iter, 1))  # @+
        
        
        
        #visObj = self.treeview.vismolSession.vismol_objects[self.selectedID]
        visObj = self.treeview.vismolSession.vismol_objects.pop(self.selectedID)
        
        self.treeview.store .clear()
        #n = 0
        #i = 1
        for vis_object in self.treeview.vismolSession.vismol_objects:
            print ('\n\n',vis_object.name,'\n\n')

            data = [vis_object.active          , 
                    str(self.treeview.vismolSession.vismol_objects.index(vis_object)),
                    vis_object.name            , 
                    str(len(vis_object.atoms)) , 
                    str(len(vis_object.frames)),
                   ]
            model.append(data)
        self.treeview.vismolSession.glwidget.queue_draw()
            #i +=1
            #n = n + 1
        
        
        #self.treeview.vismolSession.center(visObj)

        
        print('f3')

    def build_glmenu (self, menu_items = None):
        """ Function doc """
        self.glMenu = Gtk.Menu()
        for label in menu_items:
            mitem = Gtk.MenuItem(label)
            mitem.connect('activate', menu_items[label])
            self.glMenu.append(mitem)
            mitem = Gtk.SeparatorMenuItem()
            self.glMenu.append(mitem)

        self.glMenu.show_all()

    def open_menu (self, visObj = None):
        """ Function doc """
        print (visObj)
        
        
        self.glMenu.popup(None, None, None, None, 0, 0)




























    
    


class GtkMainTreeView_old(Gtk.TreeView):

    def __init__(self, vismolSession):
        Gtk.TreeView.__init__(self)
        self.connect('button-release-event', self.on_treeview_Objects_button_release_event )
        self.vismolSession = vismolSession


        columns = [" " ,
                   'id',
                   "Object",
                   "Atoms" ,
                   "Frames"]
  
        self.liststore  = Gtk.ListStore(bool,str ,str, str, str)
        # append the values in the model

        # a treeview to see the data stored in the model
        #self = Gtk.TreeView(model=self.liststore )
        # for each column
        for i, column in enumerate(columns):

            # the text in the first column should be in boldface
            if i == 0:
                cell = Gtk.CellRendererToggle()
                cell.set_property('activatable', True)
                cell.connect('toggled', self.on_chk_renderer_toggled, self.liststore)
                col = Gtk.TreeViewColumn(None, cell )
                col.add_attribute(cell, 'active', 0)

            
            else:
                cell = Gtk.CellRendererText()
                col = Gtk.TreeViewColumn(column, cell, text=i)
            # and it is appended to the treeview
            self.append_column(col)

        self.treeview_menu = TreeViewMenu()


    def on_chk_renderer_toggled(self, cell, path, model):
        model[path][0] = not model[path][0]
        print (model[path][0], model, )
        for item in model:
            print (item)
        #if self.items[model[path][0]] not in self.active_list:
        #    self.active_list.append(self.items[model[path][0]])
        #else:
        #    self.active_list.remove(self.items[model[path][0]])
        
        #""" Function doc """
        #print ('on_chk_renderer_toggled')
        #self.liststore[path][0] = not self.liststore[path][0]
        #print (path, self.liststore[path][0], self.liststore[path][1],self.liststore[path][2] )
        #
        #true_or_false =self.liststore[path][0] 
        #obj_index     =self.liststore[path][1]
        #pymol_object  =self.liststore[path][2]
        ##pymol_object  = self.liststore.get_value(iter, 2)
        ##true_or_false = self.liststore.get_value(iter, 0)
        ##obj_index     = self.liststore.get_value(iter, 1)
        #
        #if cell.get_active():
        #    self.vismolSession.disable_by_index(int(obj_index)-1)
        #    self.vismolSession.glwidget.queue_draw()
        #    #cell.set_active(False)
        #
        #else:
        #    self.vismolSession.enable_by_index(int(obj_index)-1)
        #    self.vismolSession.glwidget.queue_draw()
        #    #cell.set_active(True)
        #self.refresh_gtk_main_treeview()
        #print ('end')

    
    

     


    def append(self, visObj):
        i = self.vismolSession.vismol_objects.index(visObj)
        
        data = [visObj.active, 
               str(i)        ,
               visObj.name      , 
               str(len(visObj.atoms)) , 
               str(len(visObj.frames)),
               ]
        self.liststore.append(data)
        self.set_model(self.liststore)


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
    
            data = [vis_object.active, 
                   str(i)        ,
                   vis_object.name      , 
                   str(len(vis_object.atoms)) , 
                   str(len(vis_object.frames)),
                   ]
            print (data)
            model.append(data)
            i +=1
            n = n + 1
        self.set_model(model)
        #print ('load fuction finished')


    def on_treeview_Objects_button_release_event(self, tree, event):
        if event.button == 3:
            selection     = self.get_selection()
            model         = self.get_model()
            (model, iter) = selection.get_selected()
            if iter != None:
                self.selectedID  = str(model.get_value(iter, 1))  # @+
                self.selectedObj = str(model.get_value(iter, 2))
    
                #
                self.treeview_menu.glMenu.popup(None, None, None, None, 0, 0)
                #self.builder.get_object('TreeViewObjLabel').set_label('- ' +self.selectedObj+' -' )

                #widget = self.builder.get_object('treeview_menu')
                #widget.popup(None, None, None, None, event.button, event.time)
                #print ('button == 3')


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
            print ('event.button == 1:')
           
            #selection     = tree.get_selection()
            #model         = tree.get_model()
            #
            #(model, iter) = selection.get_selected()
            #print ('button == 1')
            #
            #if iter != None:
            #    #print model, iter
            #    pymol_object  = model.get_value(iter, 2)  # @+
            #    true_or_false = model.get_value(iter, 0)
            #    obj_index     = model.get_value(iter, 1)
            #    #print pymol_object
            #    if true_or_false == False:
            #        self.vismolSession.enable_by_index(int(obj_index)-1)
            #        true_or_false = True
            #        model.set(iter, 0, true_or_false)
            #        print (true_or_false)
            #        self.vismolSession.glwidget.queue_draw()
            #    
            #    else:
            #        self.vismolSession.disable_by_index(int(obj_index)-1)
            #        true_or_false = False
            #        model.set(iter, 0, true_or_false)
            #        self.vismolSession.glwidget.queue_draw()
            #    self.treeview.set_model(model)


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
        



