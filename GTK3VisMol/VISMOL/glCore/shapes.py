#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  shapes.py
#  
#  Copyright 2016 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
#  
#  This program is free software, you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY, without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program, if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import numpy as np
import math
import ctypes
from OpenGL import GL

import VISMOL.glCore.sphere_data as sphd
import VISMOL.glCore.cylinder_data as cyd
import VISMOL.glCore.matrix_operations as mop



def build_gl_VAO_and_buffers (program   = None, 
                              VAO       = True,
                              indices   = None,
                              coords    = None, 
                              colors    = None, 
                              dot_sizes = None):
    
    """ This function is used in all the others presented below """
    
    if VAO:
        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)
    else:
        pass
	
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.itemsize*int(len(indices)), indices, GL.GL_DYNAMIC_DRAW)
    
    if coords is not None:
        coord_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.nbytes, coords, GL.GL_STATIC_DRAW)
        att_position = GL.glGetAttribLocation(program, 'vert_coord')
        GL.glEnableVertexAttribArray(att_position)
        GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
        
        #GL.glDisableVertexAttribArray(att_position)
    else:
        coord_vbo = None
    
    if colors is not None:
        col_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.nbytes, colors, GL.GL_STATIC_DRAW)
        att_colors = GL.glGetAttribLocation(program, 'vert_color')
        GL.glEnableVertexAttribArray(att_colors)
        GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
        
        #GL.glDisableVertexAttribArray(att_colors)
    else:
        col_vbo = None
    
    if dot_sizes is not None:
        dot_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, dot_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, dot_sizes.itemsize*len(dot_sizes), dot_sizes, GL.GL_STATIC_DRAW)
        att_size = GL.glGetAttribLocation(program, 'vert_dot_size')
        GL.glEnableVertexAttribArray(att_size)
        GL.glVertexAttribPointer(att_size, 1, GL.GL_FLOAT, GL.GL_FALSE, dot_sizes.itemsize, ctypes.c_void_p(0))
        
        #GL.glDisableVertexAttribArray(att_size)
    
    else:
        dot_sizes = None
    
    GL.glBindVertexArray(0)
    
    
    #GL.glDisableVertexAttribArray(att_size)
    #GL.glDisableVertexAttribArray(att_bck_color)

    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    return vao, (ind_vbo, coord_vbo, col_vbo)




def _make_gl_selection_dots(program, vismol_object = None):
    """ Function doc
    """

    dot_sizes = vismol_object.vdw_dot_sizes
    coords    = vismol_object.frames[0]
    colors    = [0.,1.,1.]*int(len(coords)/3)
    colors    = np.array(colors, dtype=np.float32)
   
    dot_qtty = int(len(coords)/3)
    
    #bckgrnd_color = [bckgrnd_color[0],bckgrnd_color[1],
    #                 bckgrnd_color[2],bckgrnd_color[3]]*dot_qtty
    bckgrnd_color = [0,0,0]
    bckgrnd_color = np.array(bckgrnd_color, dtype=np.float32)
    
    indices = []
    for i in range(dot_qtty):
        indices.append(i)
    indices = np.array(indices,dtype=np.uint32)
    
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.itemsize*int(len(indices)), indices, GL.GL_DYNAMIC_DRAW)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.itemsize*int(len(indices)), indices, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*int(len(coords)), coords, GL.GL_STATIC_DRAW)
    att_position = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(att_position)
    GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
    att_colors = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(att_colors)
    GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    #vao_list.append(vao)
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(att_position)
    GL.glDisableVertexAttribArray(att_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    vismol_object.selection_dots_vao      = vao
    vismol_object.selection_dot_buffers   = (ind_vbo, coord_vbo, col_vbo)
    return True


def _make_gl_dots(program, vismol_object = None, bckgrnd_color= [0.0,0.0,0.0,1.0]):
    """ Function doc
    """
    #colors    = vismol_object.color_indices
    colors    = vismol_object.colors
    coords    = vismol_object.frames[0]
    dot_sizes = vismol_object.vdw_dot_sizes
    dot_qtty  = int(len(coords)/3)

    indices = []
    for i in range(dot_qtty):
        indices.append(i)
    indices = np.array(indices,dtype=np.uint32)
    

    
    vao, buffers = build_gl_VAO_and_buffers (program   = program, 
                                             VAO       = True,
                                             indices   = indices,
                                             coords    = coords, 
                                             colors    = colors, 
                                             dot_sizes = None)
    
    vismol_object.dots_vao = vao
    vismol_object.dots_buffers = buffers
        
    #vao = GL.glGenVertexArrays(1)
    #GL.glBindVertexArray(vao)
    #
    #ind_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    #GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.itemsize*int(len(indices)), indices, GL.GL_DYNAMIC_DRAW)
    #
    #coord_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    #GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*int(len(coords)), coords, GL.GL_STATIC_DRAW)
    #att_position = GL.glGetAttribLocation(program, 'vert_coord')
    #GL.glEnableVertexAttribArray(att_position)
    #GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    #
    #col_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    #GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
    #att_colors = GL.glGetAttribLocation(program, 'vert_color')
    #GL.glEnableVertexAttribArray(att_colors)
    #GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    #dot_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, dot_vbo)
    #GL.glBufferData(GL.GL_ARRAY_BUFFER, dot_sizes.itemsize*len(dot_sizes), dot_sizes, GL.GL_STATIC_DRAW)
    #att_size = GL.glGetAttribLocation(program, 'vert_dot_size')
    #GL.glEnableVertexAttribArray(att_size)
    #GL.glVertexAttribPointer(att_size, 1, GL.GL_FLOAT, GL.GL_FALSE, dot_sizes.itemsize, ctypes.c_void_p(0))
    #
    #bckgrnd_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, bckgrnd_vbo)
    #GL.glBufferData(GL.GL_ARRAY_BUFFER, bckgrnd_color.itemsize*len(bckgrnd_color), bckgrnd_color, GL.GL_STATIC_DRAW)
    #att_bck_color = GL.glGetAttribLocation(program, 'bckgrnd_color')
    #GL.glEnableVertexAttribArray(att_bck_color)
    #GL.glVertexAttribPointer(att_bck_color, 4, GL.GL_FLOAT, GL.GL_FALSE, 4*bckgrnd_color.itemsize, ctypes.c_void_p(0))
    
    #vao_list.append(vao)
    #GL.glBindVertexArray(0)
    #GL.glDisableVertexAttribArray(att_position)
    #GL.glDisableVertexAttribArray(att_colors)
    #GL.glDisableVertexAttribArray(att_size)
    #GL.glDisableVertexAttribArray(att_bck_color)

    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    
    #vismol_object.dots_vao      = vao
    #vismol_object.dots_buffers   = (ind_vbo, coord_vbo, col_vbo)
    return True


def _make_gl_non_bonded(program, vismol_object = None):
    """ Function doc
    """
    indices = np.array(vismol_object.non_bonded_atoms, dtype=np.uint32)
    coords  = vismol_object.frames[0]
    colors  = vismol_object.colors
    
    vao, buffers  = build_gl_VAO_and_buffers (program   = program, 
                                              VAO       = True,
                                              indices   = indices,
                                              coords    = coords, 
                                              colors    = colors, 
                                              dot_sizes = None)
    vismol_object.non_bonded_vao = vao
    vismol_object.non_bonded_buffers = buffers
    
    #vao = GL.glGenVertexArrays(1)
    #GL.glBindVertexArray(vao)
    #
    #ind_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    #GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.itemsize*int(len(indices)), indices, GL.GL_DYNAMIC_DRAW)
    #
    #coord_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    #GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*int(len(coords)), coords, GL.GL_STATIC_DRAW)
    #att_position = GL.glGetAttribLocation(program, 'vert_coord')
    #GL.glEnableVertexAttribArray(att_position)
    #GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    #
    #col_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    #GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
    #att_colors = GL.glGetAttribLocation(program, 'vert_color')
    #GL.glEnableVertexAttribArray(att_colors)
    #GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    #
    #GL.glBindVertexArray(0)
    #GL.glDisableVertexAttribArray(att_position)
    #GL.glDisableVertexAttribArray(att_colors)
    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    #
    #vismol_object.non_bonded_vao = vao
    #vismol_object.non_bonded_buffers = (ind_vbo, coord_vbo, col_vbo)
    return True


def _make_gl_sticks(program, vismol_object = None):
    """ Function doc
    """
    indices = np.array(vismol_object.index_bonds,dtype=np.uint32)
    coords  = vismol_object.frames[0]
    colors  = vismol_object.colors
    
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.itemsize*int(len(indices)), indices, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*int(len(coords)), coords, GL.GL_STATIC_DRAW)
    att_position = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(att_position)
    GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
    att_colors = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(att_colors)
    GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(att_position)
    GL.glDisableVertexAttribArray(att_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    vismol_object.sticks_vao = vao
    vismol_object.sticks_buffers = (ind_vbo, coord_vbo, col_vbo)
    return True


def _make_gl_dots_surface(program, vismol_object = None):
    """ Function doc
    """
    
    colors = vismol_object.colors
    coords = vismol_object.frames[0]
    indices = np.array(vismol_object.dot_indices,dtype=np.uint32)
    
    vao , buffers =  build_gl_VAO_and_buffers (program   = program, 
                                               VAO       = True,
                                               indices   = indices,
                                               coords    = coords, 
                                               colors    = colors, 
                                               dot_sizes = None)
    
    vismol_object.dots_surface_vao      = vao
    vismol_object.dots_surface_buffers  = buffers
    
    #vao = GL.glGenVertexArrays(1)
    #GL.glBindVertexArray(vao)
    #
    #ind_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    #GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.itemsize*int(len(indices)), indices, GL.GL_DYNAMIC_DRAW)
    #
    #coord_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    #GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*int(len(coords)), coords, GL.GL_STATIC_DRAW)
    #att_position = GL.glGetAttribLocation(program, 'vert_coord')
    #GL.glEnableVertexAttribArray(att_position)
    #GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    #
    #col_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    #GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
    #att_colors = GL.glGetAttribLocation(program, 'vert_color')
    #GL.glEnableVertexAttribArray(att_colors)
    #GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    #
    #GL.glBindVertexArray(0)
    #GL.glDisableVertexAttribArray(att_position)
    #GL.glDisableVertexAttribArray(att_colors)
    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    #
    #vismol_object.dots_surface_vao     = vao
    #vismol_object.dots_surface_buffers = (ind_vbo, coord_vbo, col_vbo)
    return True


def _make_gl_lines(program, vismol_object = None):
    """ Function doc
    """ 
    indices = np.array(vismol_object.index_bonds,dtype=np.uint32)
    coords  = vismol_object.frames[0]
    colors  = vismol_object.colors
    '''
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.itemsize*int(len(indices)), indices, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*int(len(coords)), coords, GL.GL_STATIC_DRAW)
    att_position = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(att_position)
    GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
    att_colors = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(att_colors)
    GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    #vao_list.append(vao)
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(att_position)
    GL.glDisableVertexAttribArray(att_colors)
    '''

    print ('here@@')
    
    vao, buffers = build_gl_VAO_and_buffers (program   = program, 
                                             VAO       = True,
                                             indices   = indices,
                                             coords    = coords, 
                                             colors    = colors, 
                                             dot_sizes = None) 
    vismol_object.lines_vao     = vao
    vismol_object.line_buffers  = buffers
     
        
def _make_new_selection_gl_lines (program, vismol_object = None):
    """ Function doc """
    indices = np.array(vismol_object.index_bonds,dtype=np.uint32)
    coords  = vismol_object.frames[0]
    colors  = vismol_object.color_indices
    

    vao , buffers =  build_gl_VAO_and_buffers (program   = program, 
                                               VAO       = True,
                                               indices   = indices,
                                               coords    = coords, 
                                               colors    = colors, 
                                               dot_sizes = None)
    
    vismol_object.new_selection_lines_vao     = vao
    vismol_object.new_selection_lines_buffers = buffers

    '''
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.nbytes, coords, GL.GL_STATIC_DRAW)
    att_position = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(att_position)
    GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.nbytes, colors, GL.GL_STATIC_DRAW)
    att_colors = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(att_colors)
    GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    #vao_list.append(vao)
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(att_position)
    GL.glDisableVertexAttribArray(att_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)

    
    vismol_object.new_selection_lines_vao      = vao
    vismol_object.new_selection_lines_buffers  = (ind_vbo, coord_vbo, col_vbo)
    #return vao, (ind_vbo, coord_vbo, col_vbo)
    '''


def _make_gl_ribbon_lines(program, vismol_object = None):
    """ Function doc
    """  
    indices = np.array(vismol_object.ribbons_Calpha_indices_rep,dtype=np.uint32)
    coords  = vismol_object.frames[0]
    colors  = vismol_object.colors
    
    vao , buffers =  build_gl_VAO_and_buffers (program   = program, 
                                               VAO       = True,
                                               indices   = indices,
                                               coords    = coords, 
                                               colors    = colors, 
                                               dot_sizes = None)
    
    vismol_object.ribbons_vao     = vao
    vismol_object.ribbons_buffers = buffers
    

'''
              S E L E C T I O N S 
'''

def _make_sel_gl_dots (program, vismol_object = None):
    """ Function doc """
    colors    = vismol_object.color_indices
    coords    = vismol_object.frames[0]
    dot_sizes = vismol_object.vdw_dot_sizes
    dot_qtty  = int(len(coords)/3)

    indices = []
    for i in range(dot_qtty):
        indices.append(i)
    indices = np.array(indices,dtype=np.uint32)
    
    
    vao, buffers = build_gl_VAO_and_buffers (program   = program, 
                                             VAO       = True,
                                             indices   = indices,
                                             coords    = coords, 
                                             colors    = colors, 
                                             dot_sizes = None)
    
    vismol_object.sel_dots_vao     = vao
    vismol_object.sel_dots_buffers = buffers


def _make_sel_gl_dots_old(program, vismol_object = None, bckgrnd_color= [1.0,1.0,1.0,1.0]):
    """ Function doc
    """
    colors    = vismol_object.color_indices
    #dot_sizes = vismol_object.vdw_dot_sizes
    coords    = vismol_object.frames[0]
    
    dot_qtty = int(len(coords)/3)
    bckgrnd_color = [bckgrnd_color[0],bckgrnd_color[1],
                     bckgrnd_color[2],bckgrnd_color[3]]*dot_qtty
    bckgrnd_color = np.array(bckgrnd_color, dtype=np.float32)
    #indices = np.array(vismol_object.dot_indices, dtype=np.uint32)
    
    indices = []
    for i in range(dot_qtty):
        indices.append(i)
    indices = np.array(indices,dtype=np.uint32)
    
    
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.itemsize*int(len(indices)), indices, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*int(len(coords)), coords, GL.GL_STATIC_DRAW)
    att_position = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(att_position)
    GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
    att_colors = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(att_colors)
    GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    dot_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, dot_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, dot_sizes.itemsize*len(dot_sizes), dot_sizes, GL.GL_STATIC_DRAW)
    att_size = GL.glGetAttribLocation(program, 'vert_dot_size')
    GL.glEnableVertexAttribArray(att_size)
    GL.glVertexAttribPointer(att_size, 1, GL.GL_FLOAT, GL.GL_FALSE, dot_sizes.itemsize, ctypes.c_void_p(0))
    
    bckgrnd_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, bckgrnd_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, bckgrnd_color.itemsize*len(bckgrnd_color), bckgrnd_color, GL.GL_STATIC_DRAW)
    att_bck_color = GL.glGetAttribLocation(program, 'bckgrnd_color')
    GL.glEnableVertexAttribArray(att_bck_color)
    GL.glVertexAttribPointer(att_bck_color, 4, GL.GL_FLOAT, GL.GL_FALSE, 4*bckgrnd_color.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(att_position)
    GL.glDisableVertexAttribArray(att_colors)
    GL.glDisableVertexAttribArray(att_size)
    GL.glDisableVertexAttribArray(att_bck_color)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    vismol_object.sel_dots_vao = vao
    vismol_object.sel_dots_buffers = (ind_vbo, coord_vbo, col_vbo)
    return True


def _make_sel_gl_non_bonded(program, vismol_object = None):
    """ Function doc
    """
    indices = np.array(vismol_object.non_bonded_atoms, dtype=np.uint32)
    coords  = vismol_object.frames[0]
    colors  = vismol_object.color_indices
    
    vao , buffers =  build_gl_VAO_and_buffers (program   = program, 
                                               VAO       = True,
                                               indices   = indices,
                                               coords    = coords, 
                                               colors    = colors, 
                                               dot_sizes = None)
    
    vismol_object.sel_non_bonded_vao     = vao
    vismol_object.sel_non_bonded_buffers = buffers
    
    #vao = GL.glGenVertexArrays(1)
    #GL.glBindVertexArray(vao)
    #
    #ind_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    #GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.itemsize*int(len(indices)), indices, GL.GL_DYNAMIC_DRAW)
    #
    #coord_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    #GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*int(len(coords)), coords, GL.GL_STATIC_DRAW)
    #att_position = GL.glGetAttribLocation(program, 'vert_coord')
    #GL.glEnableVertexAttribArray(att_position)
    #GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    #
    #col_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    #GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
    #att_colors = GL.glGetAttribLocation(program, 'vert_color')
    #GL.glEnableVertexAttribArray(att_colors)
    #GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    #
    #GL.glBindVertexArray(0)
    #GL.glDisableVertexAttribArray(att_position)
    #GL.glDisableVertexAttribArray(att_colors)
    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    #
    #vismol_object.sel_non_bonded_vao = vao
    #vismol_object.sel_non_bonded_buffers = (ind_vbo, coord_vbo, col_vbo)
    return True


def _make_sel_gl_sticks(program, vismol_object = None):
    """ Function doc
    """
    indices = np.array(vismol_object.index_bonds,dtype=np.uint32)
    coords  = vismol_object.frames[0]
    colors  = vismol_object.color_indices
    vao , buffers =  build_gl_VAO_and_buffers (program   = program, 
                                               VAO       = True,
                                               indices   = indices,
                                               coords    = coords, 
                                               colors    = colors, 
                                               dot_sizes = None)
    
    vismol_object.sel_sticks_vao     = vao
    vismol_object.sel_sticks_buffers = buffers
    #
    #vao = GL.glGenVertexArrays(1)
    #GL.glBindVertexArray(vao)
    #
    #ind_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    #GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.itemsize*int(len(indices)), indices, GL.GL_DYNAMIC_DRAW)
    #
    #coord_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    #GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*int(len(coords)), coords, GL.GL_STATIC_DRAW)
    #att_position = GL.glGetAttribLocation(program, 'vert_coord')
    #GL.glEnableVertexAttribArray(att_position)
    #GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    #
    #col_vbo = GL.glGenBuffers(1)
    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    #GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
    #att_colors = GL.glGetAttribLocation(program, 'vert_color')
    #GL.glEnableVertexAttribArray(att_colors)
    #GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    #
    #GL.glBindVertexArray(0)
    #GL.glDisableVertexAttribArray(att_position)
    #GL.glDisableVertexAttribArray(att_colors)
    #GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    #GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    #
    #vismol_object.sel_sticks_vao    = vao
    #vismol_object.sel_sticks_buffers = (ind_vbo, coord_vbo, col_vbo)
    return True


def _make_sel_gl_dots_surface(program, vismol_object = None):
    """ Function doc
    """
    colors = vismol_object.color_indices
    coords = vismol_object.frames[0]
    indices = np.array(vismol_object.dot_indices,dtype=np.uint32)
    
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.itemsize*int(len(indices)), indices, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*int(len(coords)), coords, GL.GL_STATIC_DRAW)
    att_position = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(att_position)
    GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
    att_colors = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(att_colors)
    GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(att_position)
    GL.glDisableVertexAttribArray(att_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    vismol_object.sel_dots_surface_vao = vao
    vismol_object.sel_dots_surface_buffers = (ind_vbo, coord_vbo, col_vbo)
    return True


def change_vbo_indices (ind_vbo = None, indices = []):
    """ Function doc """
    indices = np.array(indices,dtype=np.uint32)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.itemsize*int(len(indices)), indices, GL.GL_DYNAMIC_DRAW)


def change_vbo_colors  (col_vbo = None, colors = [], program = None):
    """ Function doc """
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
    att_colors = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(att_colors)
    GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))


def _make_gl_spheres_ON_THE_FLY (program, vismol_object = None): # unused
    """ Function doc
    """
    colors  = vismol_object.colors
    coords  = vismol_object.frames[0]
    indices = np.array(vismol_object.dot_indices,dtype=np.uint32)
    
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.itemsize*int(len(indices)), indices, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*int(len(coords)), coords, GL.GL_STATIC_DRAW)
    att_position = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(att_position)
    GL.glVertexAttribPointer(att_position, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*int(len(colors)), colors, GL.GL_STATIC_DRAW)
    att_colors = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(att_colors)
    GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(att_position)
    GL.glDisableVertexAttribArray(att_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    vismol_object.spheres_vao_ON_THE_FLY      = vao
    vismol_object.spheres_buffers_ON_THE_FLY  = (ind_vbo, coord_vbo, col_vbo)
    return True


