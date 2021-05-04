#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  VisMolFont.py
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

import numpy as np
import freetype as ft
import ctypes
from OpenGL import GL

class VisMolFont():
    """ VisMolFont stores the data created using the freetype python binding
        library, such as filename, character width, character height, character
        resolution, font color, etc.
    """
    
    def __init__ (self, font_file='GTK3VisMol/VISMOL/glCore/Fonts/VeraMono.ttf', char_res=64, c_w=0.25, c_h=0.3, color=[1,1,1,1]):
        """ Class initialiser
        """
        self.font_file = font_file
        self.char_res = char_res
        self.char_width = c_w
        self.char_height = c_h
        self.offset = np.array([c_w/2.0,c_h/2.0],dtype=np.float32)
        self.color = np.array(color,dtype=np.float32)
        self.font_buffer = None
        self.texture_id = None
        self.text_u = None
        self.text_v = None
        self.vao = None
        self.vbos = None
    
    def make_freetype_font(self):
        """ Function doc
        """
        face = ft.Face(self.font_file)
        face.set_char_size(self.char_res*64)
        # Determine largest glyph size
        width, height, ascender, descender = 0, 0, 0, 0
        for c in range(32,128):
            face.load_char(chr(c), ft.FT_LOAD_RENDER | ft.FT_LOAD_FORCE_AUTOHINT)
            bitmap = face.glyph.bitmap
            width = max(width, bitmap.width)
            ascender = max(ascender, face.glyph.bitmap_top)
            descender = max(descender, bitmap.rows-face.glyph.bitmap_top)
        height = ascender+descender
        # Generate texture data
        self.font_buffer = np.zeros((height*6, width*16), dtype=np.ubyte)
        for j in range(6):
            for i in range(16):
                face.load_char(chr(32+j*16+i), ft.FT_LOAD_RENDER | ft.FT_LOAD_FORCE_AUTOHINT )
                bitmap = face.glyph.bitmap
                x = i*width  + face.glyph.bitmap_left
                y = j*height + ascender - face.glyph.bitmap_top
                self.font_buffer[y:y+bitmap.rows,x:x+bitmap.width].flat = bitmap.buffer
        # Bound texture
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
        self.texture_id = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RED, self.font_buffer.shape[1], self.font_buffer.shape[0], 0, GL.GL_RED, GL.GL_UNSIGNED_BYTE, self.font_buffer)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        # Fill the font variables with data
        self.text_u = width/float(self.font_buffer.shape[1])
        self.text_v = height/float(self.font_buffer.shape[0])
        return True
    
    def make_freetype_texture(self, program):
        """ Function doc
        """
        coords = np.zeros(3,np.float32)
        uv_pos = np.zeros(4,np.float32)
        
        vertex_array_object = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vertex_array_object)
        
        coord_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, coord_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, coords.itemsize*len(coords), coords, GL.GL_DYNAMIC_DRAW)
        gl_coord = GL.glGetAttribLocation(program, 'vert_coord')
        GL.glEnableVertexAttribArray(gl_coord)
        GL.glVertexAttribPointer(gl_coord, 3, GL.GL_FLOAT, GL.GL_FALSE, 3*coords.itemsize, ctypes.c_void_p(0))
        
        tex_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, tex_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, uv_pos.itemsize*len(uv_pos), uv_pos, GL.GL_DYNAMIC_DRAW)
        gl_texture = GL.glGetAttribLocation(program, 'vert_uv')
        GL.glEnableVertexAttribArray(gl_texture)
        GL.glVertexAttribPointer(gl_texture, 4, GL.GL_FLOAT, GL.GL_FALSE, 4*uv_pos.itemsize, ctypes.c_void_p(0))
        
        GL.glBindVertexArray(0)
        GL.glDisableVertexAttribArray(gl_coord)
        GL.glDisableVertexAttribArray(gl_texture)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        
        self.vao = vertex_array_object
        self.vbos = (coord_vbo, tex_vbo)
        return True
    
    def load_matrices(self, program, view_mat, proj_mat):
        """ Function doc """
        view = GL.glGetUniformLocation(program, 'view_mat')
        GL.glUniformMatrix4fv(view, 1, GL.GL_FALSE, view_mat)
        proj = GL.glGetUniformLocation(program, 'proj_mat')
        GL.glUniformMatrix4fv(proj, 1, GL.GL_FALSE, proj_mat)
    
    def load_font_params(self, program):
        """ Loads the uniform parameters for the OpenGL program, such as the
            offset coordinates (X,Y) to calculate the quad and the color of
            the font.
        """
        offset = GL.glGetUniformLocation(program, 'offset')
        GL.glUniform2fv(offset, 1, self.offset)
        color = GL.glGetUniformLocation(program, 'text_color')
        GL.glUniform4fv(color, 1, self.color)
        return True
    
    def print_all(self):
        """ Function created only with debuging purposes.
        """
        print("#############################################")
        print(self.font_file, 'font_file')
        print(self.char_res, 'char_res')
        print(self.char_width, 'char_width')
        print(self.char_height, 'char_height')
        print(self.offset, 'offset')
        print(self.color, 'color')
        print(self.font_buffer, 'font_buffer')
        print(self.texture_id, 'texture_id')
        print(self.text_u, 'text_u')
        print(self.text_v, 'text_v')
        print(self.vao, 'vao')
        print(self.vbos, 'vbos')
    
