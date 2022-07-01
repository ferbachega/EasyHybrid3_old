#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  easyhybrid_pDynamo_selection.py
#  
#  Copyright 2022 Fernando <fernando@winter>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
#from GTKGUI.gtkWidgets.filechooser import FileChooser
#from easyhybrid.pDynamoMethods.pDynamo2Vismol import *
import gc
import os

VISMOL_HOME = os.environ.get('VISMOL_HOME')
HOME        = os.environ.get('HOME')


class SelectionListWindow(Gtk.Window):
    """ Class doc """
    
    def OpenWindow (self):
        """ Function doc /home/fernando/programs/VisMol/easyhybrid/gui/selection_list.glade"""
        if self.visible  ==  False:
            self.builder = Gtk.Builder()
            self.builder.add_from_file(os.path.join(VISMOL_HOME,'easyhybrid/gui/selection_list.glade'))
            self.builder.connect_signals(self)
            
            self.window = self.builder.get_object('window')
            #self.window.set_border_width(10)
            self.window.set_default_size(200, 600)  
            self.window.set_title('Selections')  
            
            self.window.set_keep_above(True)

            self.coordinates_liststore.clear()
            self.system_liststore     .clear()
            #self.selection_liststore  .clear()
            
            
            
            '''--------------------------------------------------------------------------------------------'''
            self.system_names_combo =self.builder.get_object('systems_combobox')
            self.system_names_combo.set_model(self.system_liststore)
            self.system_names_combo.connect("changed", self.on_system_names_combobox_changed)

            renderer_text = Gtk.CellRendererText()
            self.system_names_combo.pack_start(renderer_text, True)
            self.system_names_combo.add_attribute(renderer_text, "text", 0)
            self.refresh_system_liststore()
            '''--------------------------------------------------------------------------------------------'''


            '''--------------------------------------------------------------------------------------------'''
            self.coordinates_combobox =self.builder.get_object('coordinates_combobox')
            self.coordinates_combobox.set_model(self.coordinates_liststore)
            renderer_text2 = Gtk.CellRendererText()
            self.coordinates_combobox.pack_start(renderer_text2, True)
            self.coordinates_combobox.add_attribute(renderer_text2, "text", 0)
            '''--------------------------------------------------------------------------------------------'''
            #
            #
            
            '''--------------------------------------------------------------------------------------------'''
            self.treeview = self.builder.get_object('selection_terreview')
            for i, column_title in enumerate(['Selection',"number of atoms"]):
                renderer = Gtk.CellRendererText()
                #renderer.set_property("editable", True)
                column = Gtk.TreeViewColumn(column_title, renderer, text=i)
                self.treeview.append_column(column)
            self.treeview.set_model(self.selection_liststore)

            self.treeview.connect('row_activated', self.on_treeview_Objects_row_activated )
            self.treeview.connect('button-release-event', self.on_treeview_Objects_button_release_event )

            self.treeview_menu         = TreeViewMenu(self)
            self.window.show_all()                                               
            self.system_names_combo.set_active(0)
            self.visible    =  True
            '''--------------------------------------------------------------------------------------------'''


    def CloseWindow (self, button, data  = None):
        """ Function doc """
        #self.BackUpWindowData()
        self.window.destroy()
        self.visible    =  False
        #print('self.visible',self.visible)
    
    def __init__(self, main = None, system_liststore = None):
        """ Class initialiser """
        self.easyhybrid_main       = main
        self.visible               =  False        
        self.p_session             = main.p_session
        self.vm_session            = main.vm_session
        self.coordinates_liststore = Gtk.ListStore(str, int)
        #self.system_liststore      = Gtk.ListStore(str, int)
        self.system_liststore      = system_liststore
        
        self.selection_liststore   = Gtk.ListStore(str, int)
        

    
    def update_window (self, system_names = True, coordinates = False,  selections = True ):
        """ Function doc """

        if self.visible:
            
            _id = self.system_names_combo.get_active()
            if _id == -1:
                '''_id = -1 means no item inside the combobox'''
                return None
            else:    
                _, system_id = self.system_liststore[_id]
            
            if system_names:
                self.refresh_system_liststore ()
                self.system_names_combo.set_active(_id)
            
            if coordinates:
                self.refresh_coordinates_liststore ()
            
            
            if selections:
                _, system_id = self.system_liststore[_id]
                self.refresh_selection_liststore(system_id)
        else:
            pass

    def refresh_system_liststore (self):
        """ Function doc """
        self.easyhybrid_main.refresh_system_liststore()
        #self.system_liststore     .clear()
        ##self.selection_liststore  .clear()
        #'''--------------------------------------------------------------------------------------------'''
        #self.system_names_combo =self.builder.get_object('systems_combobox')
        #for key, system  in self.p_session.systems.items():
        #    try:
        #        self.system_liststore.append([system['name'], key])
        #    except:
        #        print(system)
    
    def refresh_selection_liststore (self, system_id = None ):
        """ Function doc """
        self.selection_liststore.clear()
        if 'selections' in self.p_session.systems[system_id].keys():
            pass
        else:
            self.p_session.systems[system_id]['selections'] = {}

        
        
        ''' QC atoms'''
        if self.p_session.systems[system_id]['system'].qcModel:
            self.p_session.systems[system_id]['selections']["QC atoms"] = list(self.p_session.systems[system_id]['system'].qcState.pureQCAtoms)

        
        
        '''Fixed atoms'''
        if self.p_session.systems[system_id]['system'].freeAtoms is None:
            pass
        
        else:
            self.p_session.systems[system_id]['selections']["fixed atoms"]   = self.p_session.get_fixed_atoms_from_system(self.p_session.systems[system_id]['system'])
  
        
        for selection , indexes in self.p_session.systems[system_id]['selections'].items():
            #if vobject.easyhybrid_system_id == self.p_session.active_id]:
            #print([selection, str(len(indexes))])
            self.selection_liststore.append([selection, len(indexes)])
    
    def refresh_coordinates_liststore(self, system_id = None):
        """ Function doc """
        cb_id = self.coordinates_combobox.get_active()
        
        if system_id:
            pass
        else:
            _id = self.system_names_combo.get_active()
            if _id == -1:
                return False
            else:
                #print('_id', _id)
                _, system_id = self.system_liststore[_id]
        
        self.coordinates_liststore.clear()
        for key , vobject in self.vm_session.vobjects_dic.items():
            if vobject.easyhybrid_system_id == system_id:
                self.coordinates_liststore.append([vobject.name, key])
        
        self.coordinates_combobox.set_active(cb_id)
        
        
    def on_system_names_combobox_changed(self, widget):
        """ Function doc """
        
        _id = self.system_names_combo.get_active()
        #print('_id', _id)
        
        if _id == -1:
            '''_id = -1 means no item inside the combobox'''
            return None
        
        else:    
            _, system_id = self.system_liststore[_id]
            

            self.refresh_coordinates_liststore(system_id)
            self.refresh_selection_liststore (system_id)
            
            size  =  len(list(self.coordinates_liststore))
            self.coordinates_combobox.set_active(size-1)

        
        
    def on_treeview_Objects_row_activated(self, tree, event, data):
        #print ('row activated')  
        _id = self.system_names_combo.get_active()
        _, system_id = self.system_liststore[_id]
        
        selection     = self.treeview.get_selection()
        (model, iter) = selection.get_selected()
        #print(model.get_value(iter, 0),model.get_value(iter, 1))
        key = model.get_value(iter, 0)
        
        indexes = self.p_session.systems[system_id]['selections'][key] 
    
        
        _id = self.coordinates_combobox.get_active()
        _, _key = self.coordinates_liststore[_id]
        
        
        vobject = self.vm_session.vobjects_dic[_key]
        self.vm_session.selections[self.vm_session.current_selection].selecting_by_indexes (vobject = vobject, indexes = indexes, clear = True)
        self.vm_session.selections[self.vm_session.current_selection].active = True
        
        
        self.vm_session.center_by_atomlist(atoms = self.vm_session.selections[self.vm_session.current_selection].selected_atoms) 
        
        self.vm_session.glwidget.queue_draw()
        
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
        
        
        _id = self.system_names_combo.get_active()
        if _id == -1:
            '''_id = -1 means no item inside the combobox'''
            return None
        else:    
            _, system_id = self.system_liststore[_id]
            
            
            
        if event.button == 3:
            selection     = self.treeview.get_selection()
            (model, iter) = selection.get_selected()
            for item in model:
                pass
                #print (item[0], model[iter][0])
            if iter != None:
                self.treeview_menu.open_menu(iter, system_id)

        if event.button == 1:
            print ('event.button == 1:')



class TreeViewMenu:
    """ Class doc """
    
    def __init__ (self, sele_window):
        """ Class initialiser """
        pass
        self.treeview = sele_window.treeview
        self.p_session = sele_window.p_session
        self.sele_window = sele_window 
        functions = {
                    'Rename'                : self.print_test ,
                    'Delete'                : self.delete_system ,
                    }
        self.build_tree_view_menu(functions)


    def print_test (self, menu_item = None ):
        """  
        menu_item = Gtk.MenuItem object at 0x7fbdcc035700 (GtkMenuItem at 0x37cf6c0)
        
        """
        print(menu_item)

    def rename (self, menu_item):
        """ Function doc """
        pass
        
        
        

    def delete_system (self, menu_item = None ):
        """ Function doc """
        selection = self.treeview.get_selection()
        (model, iter) = selection.get_selected()
        #print(model[iter][0])


        sele = self.p_session.systems[self.system_id]['selections'].pop(model[iter][0])
        #print ('deleting',sele)
        #print ('selections', self.p_session.systems[self.system_id]['selections'])
        self.sele_window.update_window (system_names = False, coordinates = False,  selections = True )


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

    def open_menu (self, vobject = None, system_id = None):
        """ Function doc """
        self.system_id = system_id
        #print (vobject)
        self.tree_view_menu.popup(None, None, None, None, 0, 0)


