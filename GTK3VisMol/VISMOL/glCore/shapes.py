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

import ctypes
import numpy as np
from OpenGL import GL


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
    else:
        coord_vbo = None
    
    if colors is not None:
        col_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.nbytes, colors, GL.GL_STATIC_DRAW)
        att_colors = GL.glGetAttribLocation(program, 'vert_color')
        GL.glEnableVertexAttribArray(att_colors)
        GL.glVertexAttribPointer(att_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    else:
        col_vbo = None
    
    if dot_sizes is not None:
        dot_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, dot_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, dot_sizes.itemsize*len(dot_sizes), dot_sizes, GL.GL_STATIC_DRAW)
        att_size = GL.glGetAttribLocation(program, 'vert_dot_size')
        GL.glEnableVertexAttribArray(att_size)
        GL.glVertexAttribPointer(att_size, 1, GL.GL_FLOAT, GL.GL_FALSE, dot_sizes.itemsize, ctypes.c_void_p(0))

    GL.glBindVertexArray(0)
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
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(att_position)
    GL.glDisableVertexAttribArray(att_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    vismol_object.selection_dots_vao      = vao
    vismol_object.selection_dot_buffers   = (ind_vbo, coord_vbo, col_vbo)
    return True
