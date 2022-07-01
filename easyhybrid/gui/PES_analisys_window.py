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



gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
from matplotlib.backends.backend_gtk3agg import FigureCanvas  # or gtk3cairo.
from matplotlib.figure import Figure
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import copy as cp
import gc
import os
from vModel import VismolObject




VISMOL_HOME = os.environ.get('VISMOL_HOME')
HOME        = os.environ.get('HOME')


class PotentialEnergyAnalysisWindow():
    
    def OpenWindow (self, vobject = None):
        """ Function doc """
        if self.Visible  ==  False:
            self.builder = Gtk.Builder()
            self.builder.add_from_file(os.path.join(VISMOL_HOME,'easyhybrid/gui/PES_analysis_window.glade'))
            self.builder.connect_signals(self)
            self.vobject = vobject
            self.window = self.builder.get_object('window')
            self.window.set_title('Analysis Window')
            self.window.set_keep_above(True)            
            self.window.set_default_size(700, 450)
            
            self.hbox           = self.builder.get_object('hbox_matplot_figures')
            self.scale_traj     = self.builder.get_object('scale_trajectory_from_PES')
            self.adjustment     = Gtk.Adjustment(value         = 0,
                                                 lower         = 0,
                                                 upper         = 100,
                                                 step_increment= 1,
                                                 page_increment= 1,
                                                 page_size     = 1)

            self.scale_traj.set_adjustment ( self.adjustment)
            self.scale_traj.set_digits(0)
            self.reaction_coord_label = self.builder.get_object('RC1_RC2_label')
            
            
            
            
            
            '''-------------------------------------------------------------'''
            self.fig = Figure(figsize=(6, 4))#,constrained_layout=True)
            self.canvas = FigureCanvas(self.fig)  # a Gtk.DrawingArea
            self.canvas.mpl_connect('button_press_event', self.on_pick)
            self.canvas.mpl_connect('motion_notify_event', self.on_motion_notify_event)

            self.hbox.pack_start(self.canvas, True, True, 0)
            self.ax = self.fig.add_subplot(1,1,1)
            '''-------------------------------------------------------------'''




            '''-------------------------------------------------------------'''
            self.fig2 = Figure(figsize=(6, 4), dpi=100)
            self.ax2 = self.fig2.add_subplot(1,1,1)
            self.ax3 = self.fig2.add_subplot(1,1,1)
            
            #self.line2, = self.ax2.plot([], [], '-o')
            #self.secax = self.ax2.secondary_xaxis('top', functions=(self.seconday_xaxis_function))

            self.canvas2 = FigureCanvas(self.fig2)  # a Gtk.DrawingArea
            self.hbox.pack_start(self.canvas2, True, True, 0)        
            '''-------------------------------------------------------------'''





            
            self.grid = self.builder.get_object('grid_setup')
            
            sys_selected = 0
            
            
            
            #'''------------------------------------------------------------------------------------
            self.vobject_liststore = Gtk.ListStore(str, int)
            names = [ ]
            for key , system in self.main.p_session.systems.items():
                #print ()
                try:
                    print("system data", system['logfile_data'])
                    if system['logfile_data']:
                        for vobject_id in  system['logfile_data'].keys():
                            print(['vobject_id:', vobject_id ,system['logfile_data'].keys()])
                            try:
                                _vobject = self.main.vm_session.vobjects_dic[vobject_id]
                                print(['_vobject:', _vobject.name,_vobject.index])
                                self.vobject_liststore.append([_vobject.name, _vobject.index])
                            except:
                                print('self.vobject_liststore.append([_vobject.name, _vobject.index])', 'failed!')
                except:
                    pass
            #self.vobject_liststore.append(['all', _vobject.index])

            self.coordinates_combobox = Gtk.ComboBox()
            renderer_text = Gtk.CellRendererText()
            self.coordinates_combobox.pack_start(renderer_text, True)
            self.coordinates_combobox.add_attribute(renderer_text, "text", 0)
            self.coordinates_combobox.set_model(self.vobject_liststore)
            self.coordinates_combobox.connect('changed', self.on_coordinates_combobox_change)
            self.grid.attach (self.coordinates_combobox, 1, 0, 1, 1)
            #------------------------------------------------------------------------------------
            
            
            
            
            
            #------------------------------------------------------------------------------------
            self.data_combobox = Gtk.ComboBox()
            renderer_text = Gtk.CellRendererText()
            self.data_combobox.pack_start(renderer_text, True)
            self.data_combobox.add_attribute(renderer_text, "text", 0)
            self.data_combobox.set_model(self.data_liststore)
            self.data_combobox.connect('changed', self.on_data_combobox_change)
            self.grid.attach (self.data_combobox, 3, 0, 1, 1)
            #------------------------------------------------------------------------------------
            
            
            
            #------------------------------------------------------------------------------------
            if sys_selected:
                self.coordinates_combobox.set_active(sys_selected)
            else:
                self.coordinates_combobox.set_active(0)
            #------------------------------------------------------------------------------------'''
 
            self.window.show_all()
            self.Visible  = True
    
        else:
            _id = self.coordinates_combobox.get_active()
            self.vobject_liststore = Gtk.ListStore(str, int)
            names = [ ]
            for key , system in self.main.p_session.systems.items():
                try:
                    for vobject_id in  system['logfile_data'].keys():
                        try:
                            _vobject = self.main.vm_session.vobjects_dic[vobject_id]
                            print(['_vobject:', _vobject.name,_vobject.index])
                            self.vobject_liststore.append([_vobject.name, _vobject.index])
                        except:
                            print('self.vobject_liststore.append([_vobject.name, _vobject.index])', 'failed!')
                except:
                    pass
            #self.vobject_liststore.append(['all', _vobject.index])
            self.coordinates_combobox.set_model(self.vobject_liststore)
            self.coordinates_combobox.set_active(_id)


    def seconday_xaxis_function (self):
        """ Function doc """
        pass

    def _draw_data (self, cla = True, refresh = True):
        """ Function doc """
        print('self.pcm.cla()')
        if cla:
            if self.ax:
                self.ax.cla()
                #if self.pcm:
                self.fig.gca().clear()
                self.fig.canvas.draw()
            else:
                pass

        self.pcm = self.ax.pcolormesh(range(len(self.data['Z'][0])), 
                                      range(len(self.data['Z'])), 
                                      self.data['Z'], 
                                      cmap='jet', 
                                      #vmin=0, #shading='auto'
                                      )
                                      
        
        am = self.ax.contour(range(len(self.data['Z'][0])), 
                             range(len(self.data['Z']))   , 
                             self.data['Z']               ,
                             colors='k')
        if self.color_bar:
            self.color_bar.remove() 
        self.color_bar = self.fig.colorbar(self.pcm,  ax=self.ax)#, extend='both')
        self.fig.canvas.draw()
    
    
    def on_coordinates_combobox_change (self, widget):
        """ Function doc """
        _id = self.coordinates_combobox.get_active()
        print(_id)
        vobject_index = None
        #-----------------------------------------------------------------------------
        _iter = self.coordinates_combobox.get_active_iter()
        if _iter is not None:
            '''selecting the vismol object from the content that is in the combobox '''
            model = self.coordinates_combobox.get_model()
            _name, vobject_index = model[_iter][:2]
            print ('\n\n\_name, vobject_index:', _name, vobject_index, '\n\n')
        #-----------------------------------------------------------------------------
        self.vobject = self.main.vm_session.vobjects_dic[vobject_index]

        self.data_liststore.clear()
        for index , data in enumerate(self.main.p_session.systems[self.vobject.easyhybrid_system_id]['logfile_data'][vobject_index]):
            #print(data)
            self.data_liststore.append([data['name'], index])
        
        
        #self.data_liststore.append(['all', 2])
        
        self.data_combobox.set_active(0)


    def on_data_combobox_change (self, widget):
        """ Function doc """

        _iter = self.data_combobox.get_active_iter()
        if _iter is not None:
            '''selecting the vismol object from the content that is in the combobox '''
            model = self.data_combobox.get_model()
            _name, index = model[_iter][:2]
            #print ('\n\n\_name, index:', _name,  index, '\n\n')
        
        #self.vobject = self.main.vm_session.vobjects_dic[vobject_index]
        self.data = self.main.p_session.systems[self.vobject.easyhybrid_system_id]['logfile_data'][self.vobject.index][index] 
        print(self.data)
        self._draw_data(cla = True)
        
        
    def on_motion_notify_event (self, event):
        """ Function doc """
        if event.xdata is None or event.ydata is None:
            pass
        else:
            x, y = int(event.xdata), int(event.ydata)
            try:
                rc1 = self.data['RC1'][y][x]
                rc2 = self.data['RC2'][y][x]
                
                label_text =  '({:3d}) RC1: {:.4f}     ({:3d}) RC2: {:.4f}  '.format(x, rc1, y, rc2) 
                
                self.reaction_coord_label.set_text(label_text)
                print(rc1, rc2, x,y)
            except:
                pass
            
    
    def on_pick(self, event):
        ''' Function doc '''
        
        #self.ax.pcolormesh(self.X, self.Y, self.Z, cmap='jet', vmin=0, shading='gouraud')
        #self.ax.pcolormesh(self.X, self.Y, self.Z, cmap='jet', vmin=0, shading='gouraud')
        
        #self.pcm = self.ax.pcolormesh(self.X, self.Y, self.Z, cmap='jet', vmin=0)#, shading='gouraud')
        #am = self.ax.contour(self.X, self.Y, self.Z,lspacing = 10, colors='k')
        button_number = int(event.button)
        
        if button_number == 1:
            self.ax.cla()
            self.pcm = self.ax.pcolormesh(range(len(self.data['Z'][0])), 
                                          range(len(self.data['Z'])), 
                                          self.data['Z'], 
                                          cmap='jet',# shading='auto', 
                                          )#vmin=0)
                                          
            
            am = self.ax.contour(range(len(self.data['Z'][0])), 
                                 range(len(self.data['Z']))   , 
                                 self.data['Z']               ,
                                 colors='k')
            
            
            
            if event.xdata is None or event.ydata is None:
                self.xdata  = []
                self.ydata  = []
                self.indexes = []
                self.zdata   = []
                self.ax2.cla()
                
                self.xy_traj = []
                self.scale_traj_new_definitions()

            else:
                
                #print('you pressed', event.button)
                #print('you pressed', event.xdata, event.ydata)
                x, y = int(event.xdata), int(event.ydata)
                #print (x, y)
                print('you pressed', x, y, self.data['Z'][y][x])
                #print('you pressed', event)
                
                if self.interpolate:
                    if len(self.xy_traj) > 0 :
                        print([self.xy_traj[-1],[x,y] ])
                        xy_list = build_chain_of_states( [self.xy_traj[-1],[x,y] ])
                    else:
                        xy_list = [[x,y]]
                else: xy_list = [[x,y]]
                
                for xy in xy_list:
                    x = xy[0]
                    y = xy[1]
                    
                    #self.xdata.append(event.xdata)
                    #self.ydata.append(event.ydata)
                    self.xdata.append(x+0.5)
                    self.ydata.append(y+0.5)
                    self.xy_traj.append([x,y])
                    
                    self.scale_traj_new_definitions()
                    
                    self.zdata.append(self.data['Z'][y][x])
                #self.line, = self.ax.plot(event.xdata, event.ydata, '-o')  # plot the first row
            
            self.line, = self.ax.plot(self.xdata, self.ydata, '-ok')  # plot the first row
            self.ax2.cla()
            self.line2, = self.ax2.plot(range(0, len(self.zdata)), self.zdata, '-ob')  # plot the first row
            
            self.canvas.draw()
            self.canvas2.draw()

    def __init__(self, main = None ):
        """ Class initialiser """
        self.main     = main
        #self.p_session           = self.easyhybrid_main.p_session
        #self.vm_session          = main.vm_session
        self.Visible             =  False        
        
        self.vobject_liststore   = Gtk.ListStore(str, int)
        self.data_liststore      = Gtk.ListStore(str, int)
        #self.residue_liststore   = Gtk.ListStore(str, str, str)
        
        #self.interpolate = False#True
        self.interpolate =  True
        self.opt_methods = { 0 : 'ConjugatedGradient',
                             1 : 'SteepestDescent'   ,
                             2 : 'LFBGS'             ,
                             3 : 'QuasiNewton'       ,
                             4 : 'FIRE'              }
        
        self.xdata = []
        self.ydata = []
        self.zdata = []
        self.xy_traj = []
        self.pcm = None
        self.color_bar = None
        self.vobject = None
        self.traj_export_index = 1
    
    def scale_traj_new_definitions(self):
        #self.scale_traj
        self.scale_traj.set_range(0, len(self.xy_traj))
        #self.scale_traj.set_value(self.vm_session.get_frame())

    def on_scaler_frame_value_changed (self, hscale, text= None,  data=None):
        """ Function doc """
        value = self.scale_traj.get_value()
        pos   = self.scale_traj.get_value_pos ()
        
        
        #print(self.xy_traj[int(value)])
        xy = self.xy_traj[int(value)]
        print(xy, self.zdata[int(value)])
        
        self.ax2.cla()
        self.ax3.cla()
        self.ax2.plot(range(0, len(self.zdata)), self.zdata, '-ob')
        self.ax3.plot( [int(value)], [self.zdata[int(value)]], '-or')
        
        if self.vobject:
            frame = self.vobject.trajectory2D_xy_indexes[(xy[0], xy[1])]
            self.main.vm_session.set_frame(int(frame)) 
        self.canvas2.draw()
        #self.scale_traj.set_value(int(value))

    def on_button_export_trajectory (self, widget):
        """ Function doc """
        print (
        self.xdata   ,
        self.ydata   ,
        self.zdata   ,
        self.xy_traj ,
        self.vobject ,
        )
        
        #print (self.main.p_session.systems.keys())
        #print (self.vobject.easyhybrid_system_id)
        active_id = self.main.p_session.active_id
        
        
        self.main.p_session.active_id = self.vobject.easyhybrid_system_id
        system_id = self.vobject.easyhybrid_system_id

        frames     = []
        frame      = []

        for xy in self.xy_traj:
            frame_number = self.vobject.trajectory2D_xy_indexes[(xy[0], xy[1])]
            #print(frame, len(vobject.frames))
            frames.append(self.vobject.frames[frame_number])
        self.traj_export_index += 1
        
        
        
        print(len(frames))
        vobject = self.main.p_session.build_vobject_from_pDynamo_system (
                                                           name                 = 'Trajectory from PES', #+str(self.traj_export_index)  ,
                                                           system_id            = system_id,
                                                           vobject_active = True        ,
                                                           autocenter           = True        ,
                                                           refresh_qc_and_fixed = False,
                                                           frames               = frames)
        
        
        
        
        
        
        self.main.p_session.refresh_qc_and_fixed_representations(      _all = False, 
                                                                  system_id = system_id , 
                                                                     vobject = vobject,    
                                                                 fixed_atoms = True , 
                                                                    QC_atoms = True , 
                                                                      static = True )

        self.main.p_session.active_id = active_id


    def change_check_button_reaction_coordinate (self, widget):
        """ Function doc """
        #radiobutton_bidimensional = self.builder.get_object('radiobutton_bidimensional')
        if self.builder.get_object('label_check_button_reaction_coordinate2').get_active():
            self.box_reaction_coordinate2.set_sensitive(True)
            self.builder.get_object('n_CPUs_spinbutton').set_sensitive(True)
            self.builder.get_object('n_CPUs_label').set_sensitive(True)
        else:
            self.box_reaction_coordinate2.set_sensitive(False)
            self.builder.get_object('n_CPUs_spinbutton').set_sensitive(False)
            self.builder.get_object('n_CPUs_label')     .set_sensitive(False)

    #======================================================================================
    def CloseWindow (self, button, data  = None):
        """ Function doc """
        self.window.destroy()
        self.Visible    =  False







def parse_1D_scan_logfile (logfile):
    """ Function doc """
    

def parse_2D_scan_logfile (logfile):
    """ Function doc """
    
    data  =  open(logfile, 'r')
    lines =  data.readlines()
    xlist = []
    ylist = []
    zlist = []
    
    lastline = lines[-1].split()
    x_size = int(lastline[0])
    y_size = int(lastline[1])

    
    rows = y_size+1
    cols = x_size+1
     
    Z       = [[0]*cols for _ in range(rows)]
    RC1     = [[0]*cols for _ in range(rows)]
    RC2     = [[0]*cols for _ in range(rows)]
    
    #print (zlist)
    
    for line in lines[1:]:
        line2 = line.split()
        x = int(line2[0])
        y = int(line2[1])
        #print(x,y, line2[-1])
        
        
    
        Z[y][x]       = float(line2[-1]) 
        RC1[y][x]     = float(line2[-3]) 
        RC2[y][x]     = float(line2[-2]) 
    data.close()

    data = {
           'RC1': RC1,
           'RC2': RC2,
           'Z': Z
           }
    return data

def find_the_midpoint (coord1 , coord2):
	""" Function doc """
	#print (coord1, coord2)
	
	x = float(coord2[0] - coord1[0])
	x = (x/2)
	#print ('x', x)
	x = coord1[0] + x


	y = float(coord2[1] - coord1[1])
	y = (y/2)
	#print ('y', y)

	y = coord1[1] + y

	#print (x, y)
	#return [int(x), int(round(y))]
	return [int(x), int( y )]

def build_chain_of_states( input_coord):
 
    #print (input_coord)
    inset_point = True


    while inset_point == True:
        a = 0
        counter = 0

        while a == 0:

            try:
                coord1 =  input_coord[ counter  ]
                coord2 =  input_coord[ counter+1]

                inset_point = check_distance (coord1 , coord2)
                
                if inset_point == False:
                    counter += 1
                    #print ('inset_point == False')
                else:
                    midpoint = find_the_midpoint (coord1 , coord2)
                    #print counter, counter+1, midpoint, input_coord
                    input_coord.insert(counter+1, 0 )
                    input_coord[counter+1] = midpoint
            except:
                a = True
                #print input_coord
    return input_coord[1:]


def check_distance (coord1 , coord2):
	""" Function doc """
	x = float(coord2[0] - coord1[0])
	y = float(coord2[1] - coord1[1])
	d =  (x**2 + y**2)**0.5
	if d < 1.42:
		return False
	else:
		#print 'not too close'
		return True





def main(args):
    
    win = PotentialEnergyAnalysisWindow()
    win.OpenWindow()
    Gtk.main()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
