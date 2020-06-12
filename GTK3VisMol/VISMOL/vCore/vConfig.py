#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  vConfig.py
#  
#  Copyright 2020 Fernando <fernando@winter>
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

class VisMolConfig:
    """ Class doc """

    def __init__ (self, vSession):
        """ Class initialiser """


        self.vSession = vSession 
        self.gl_parameters      =     {
                                  'background_color'           : [0.0,0.0,0.0,1.0]    , 
                                  'color_type'                 : 0                    ,  # 0 - pymol style   1 - Gabedit    
                                                                                         
                                                                                         
                                  'dot_size'                   : 5                    ,  
                                  'dot_type'                   : 0                    ,  # 0 - square    1 - rounded
                                                                                         
                                  'line_width'                 : 1                    ,  
                                  'line_width_selection'       : 40                   ,  

                                  'line_type'                  : 0                    ,  # 0 - no detail       1 - Charlitos'style
                                  'line_color'                 : 0                    ,  # 0 - atom types      1 - black (for white bg)     2 - white (for black bg)
                                                                                                               
                                                                                                               
                                  'sphere_type'                : 0                    ,  # 0 - real spheres    1 - impostors 
                                  'sphere_scale'               : 0.85                 ,  # Scale size for real spheres
                                  'sphere_quality'             : 1                    ,  # Quality for real spheres - 1 if default
                                                                                         
                                                                                         
                                  'Stick_radius'               : 1.5                  ,  
                                  'stick_color'                : 0                    ,  
                                  'stick_type'                 : 0                    ,  # 0 - atom types      1 - black (for white bg)     2 - white (for black bg)
                                                                                
                                                                                    
                                  'antialias'                  : True                 ,
                                  'scroll_step'                : 0.9                  ,
                                  'field_of_view'              : 15                   ,
                                    

                                  'light_position'             : [-2.5, 2.5, 3.0    ] ,
                                  'light_color'                : [ 1.0, 1.0, 1.0,1.0] ,
                                  'light_ambient_coef'         : 0.4                  ,
                                  'light_shininess'            : 5.5                  ,
                                  'light_intensity'            : [0.6,0.6,0.6]        ,
                                  'light_specular_color'       : [1.0,1.0,1.0]        ,


                                   'center_on_coord_sleep_time' : 0.001                ,
                                 }
                                 
                                 
                                     
                                     
                                     
                                     
                                     
                                     
                                     
                                     
                                     
                                     
                                     
                                     
                                     
                                     
                                     
                                     
                                     
                                     
                                     
