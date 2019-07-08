#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  vaos.py
#  
#  Copyright 2017 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
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

import ctypes
import numpy as np
import shapes

from OpenGL import GL

def _get_normal(vec1, vec2):
    """ Function doc """
    return (vec1 + vec2) / np.linalg.norm(vec1 + vec2)

def make_spheres(program, points):
    """ Function doc """
    amount = int(len(points))
    coords = np.array([], dtype=np.float32)
    colors = np.array([], dtype=np.float32)
    centers = np.array([], dtype=np.float32)
    indexes = np.array([], dtype=np.uint32)
    for i in range(0, amount, 3):
        center = [points[i], points[i+1], points[i+2]]
        verts, inds, cols = shapes.get_sphere(center, 1.1, [0, 1, 0], level='level_2')
        center *= int(verts.size/3)
        to_add = int(verts.size/3) * int(i/3)
        inds += to_add
        coords = np.concatenate((coords,verts))
        colors = np.concatenate((colors,cols))
        centers = np.concatenate((centers,center))
        indexes = np.concatenate((indexes,inds))
    
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)
    
    coords = np.array(coords,dtype=np.float32)
    colors = np.array(colors,dtype=np.float32)
    centers = np.array(centers,dtype=np.float32)
    indexes = np.array(indexes, dtype=np.uint32)
    
    ind_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ind_vbo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indexes.itemsize*int(len(indexes)), indexes, GL.GL_DYNAMIC_DRAW)
    
    coord_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_STATIC_DRAW)
    gl_coord = GL.glGetAttribLocation(program, 'vert_coord')
    GL.glEnableVertexAttribArray(gl_coord)
    GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
    
    centr_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, centr_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, centers.itemsize*len(centers), centers, GL.GL_STATIC_DRAW)
    gl_center = GL.glGetAttribLocation(program, 'vert_centr')
    GL.glEnableVertexAttribArray(gl_center)
    GL.glVertexAttribPointer(gl_center, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*centers.itemsize, ctypes.c_void_p(0))
    
    col_vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, col_vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors.itemsize*len(colors), colors, GL.GL_STATIC_DRAW)
    gl_colors = GL.glGetAttribLocation(program, 'vert_color')
    GL.glEnableVertexAttribArray(gl_colors)
    GL.glVertexAttribPointer(gl_colors, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*colors.itemsize, ctypes.c_void_p(0))
    
    GL.glBindVertexArray(0)
    GL.glDisableVertexAttribArray(gl_coord)
    GL.glDisableVertexAttribArray(gl_center)
    GL.glDisableVertexAttribArray(gl_colors)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    return vertex_array_object, (coord_vbo, centr_vbo, col_vbo), int(len(indexes))

