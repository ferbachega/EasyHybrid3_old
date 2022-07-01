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

from vCore.VismolSession  import VisMolSession
#from GTKGUI  import gtkgui

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
        self.vm_session  =  VisMolSession(glwidget = True, toolkit = 'gtk3')       
        self.vm_session.insert_glmenu()
        self.container.pack_start(self.vm_session.glwidget, True, True, 0)         
                                         
        self.window.connect("key-press-event"  , self.vm_session.glwidget.key_pressed)  
        self.window.connect("key-release-event", self.vm_session.glwidget.key_released) 
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
        self.vm_session.load(filein)
        #self.vm_session._picking_selection_mode = False
        #self.vm_session.load('/home/fernando/programs/EasyHybrid3/Coords/pdbs/1gab.pdb')

        #visObj = vm_session.vismol_objects[-1]
        #vm_session.glwidget.vm_widget.center_on_coordinates(visObj, visObj.mass_center)
        #---------------------------------------------------------------------------

        #def run(self):
        Gtk.main()
        return None

	    
#Gdk.threads_init()
#EasyHybrid = EasyHybrid_main()
#EasyHybrid.run()

