#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  __main__.py
#  
#  Copyright 2016 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
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

import gi, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
#import os
#import threading

from GTK3VisMol.VISMOL.vCore.VismolSession  import VisMolSession
#from GTKGUI  import gtkgui
#/home/fernando/programs/EasyHybrid3/GTK3VisMol/EasyHybrid/simpleWindow.py
class VismolGTK3Session():
    """ Class doc """
        
    def __init__ (self, filein ):
        """ Class initialiser """
        #----------------------------------------------------------------------------#
        # - - - - - - - - -  GTK STUFFS  - - - - - - - - -               
        self.window = Gtk.Window(title="VisMol window")                  
        #filechooser = FileChooser()                                     
        self.window.set_default_size(600, 600)                          
        self.container = Gtk.Box (orientation = Gtk.Orientation.VERTICAL)
        # - - - - - - - - - - - -  - - - - - - - - - - - -               
                                         
                                         
        #---------------------------------------------------------------------------  
        self.vismolSession  =  VisMolSession(glwidget = True, toolkit = 'gtk3')       
        self.vismolSession.insert_glmenu()
        self.container.pack_start(self.vismolSession.glwidget, True, True, 0)         
                                         
        self.window.connect("key-press-event"  , self.vismolSession.glwidget.key_pressed)  
        self.window.connect("key-release-event", self.vismolSession.glwidget.key_released) 
        self.window.add(self.container)                                                    
        #------------------------------------------------------------------------
        self.entry = Gtk.Entry()
        
        self.container.pack_start(self.entry, False, False, 0)
        #--------------------------------------------------------------------------- #
        self.window.connect("delete-event",    Gtk.main_quit)                             #
        self.window.show_all()                                                            #
        #----------------------------------------------------------------------------#



        #args =  sys.argv
        #print  (args)
        #filein = args[-1]
        
        #---------------------------------------------------------------------------
        self.vismolSession.load(filein)
        #self.vismolSession._picking_selection_mode = False
        #self.vismolSession.load('/home/fernando/programs/EasyHybrid3/Coords/pdbs/1gab.pdb')

        #vobject = vismolSession.vobjects[-1]
        #vismolSession.glwidget.vm_widget.center_on_coordinates(vobject, vobject.mass_center)
        #---------------------------------------------------------------------------

        #def run(self):
        Gtk.main()
        return None

	    
#Gdk.threads_init()
#EasyHybrid = EasyHybrid_main()
#EasyHybrid.run()

