#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  edtsurf.py
#
#  Python interface to EDTSurf via ctypes
#
#  Copyright 2020 Samuel Reghim Silva <samuelrsilva@gmail.com>
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

from ctypes import *
from os.path import abspath, dirname, join


class Point(Structure):
    _fields_ = [("x", c_double),
                ("y", c_double),
                ("z", c_double)]

class Triangle(Structure):
	_fields_ = [("a", c_int),
                ("b", c_int),
                ("c", c_int)]


# Call EDTSurf to calculate molecular surface.
# triangulation type, 1-MC 2-VCMC (default is 2)
# surface type, 1-VWS 2-SAS 3-MS 0-DEPTH (default is 3)
# color mode, 1-pure 2-atom 3-chain (default is 2)
# probe radius, float point in [0,2.0] (default is 1.4)
# inner or outer surface for output, 1-inner and outer 2-outer 3-inner (default is 2)
# scale factor, float point in (0,20.0] (default is 4.0)
#
# Return [list_of_vertices, list_of_triangles] similar to the OFF (Object File
# Format) description, where
#     list_of_vertices is [[x0, y0, z0], [x1, y1, z1], ...]
# and list_of_triangles is [[a0, b0, c0], [a1, b1, c1], ...]
#
# Indexing in list_of_triangles is 0-based as usual
#
# If an error occurs, an Exception is raised


def calc_surface(pdbfname, triangulation_type=2, surface_type=3, color_mode=2, probe_radius=1.4, scale_factor=4.0):

	me = abspath(dirname(__file__))
	lib = cdll.LoadLibrary(join(me, "libEDTSurf.so"))

	c_point_p = POINTER(Point)
	c_tri_p   = POINTER(Triangle)

	lib.calc_surface.argtypes = [c_char_p, c_int, c_int, c_int, c_double, c_double, c_int, POINTER(c_point_p), POINTER(c_int), POINTER(c_tri_p), POINTER(c_int)]
	lib.calc_surface.restype = c_int

	inname = pdbfname.encode('utf-8')

	nvertices  = c_int()
	ntriangles = c_int()

	vertices  = c_point_p()
	triangles = c_tri_p()
	inner_surface = c_int(2) # outer surface only

	# Use byref to pass the address of the pointer
	res = lib.calc_surface(c_char_p(inname), triangulation_type, surface_type, color_mode, probe_radius, scale_factor, inner_surface, byref(vertices), byref(nvertices), byref(triangles), byref(ntriangles))

	print('res =', res)
	if res == -1:
		raise Exception('Input file could not be opened')
	if res == 0:
		raise Exception('Memory error')

	# cast the result to array
	array_vert_t   = Point * nvertices.value
	array_vert_t_p = POINTER(array_vert_t)

	array_tri_t   = Triangle * ntriangles.value
	array_tri_t_p = POINTER(array_tri_t)

	# pointer cast
	p_vert_array = cast(vertices, array_vert_t_p)
	p_tri_array  = cast(triangles, array_tri_t_p)

	# pointer dereference
	vert_array = p_vert_array.contents
	tri_array  = p_tri_array.contents

	assert(len(vert_array) == nvertices.value)
	assert(len(tri_array)  == ntriangles.value)

	# copy the data to Python lists
	pyverts = [[0.0] * 3 for i in range(nvertices.value)]
	pytris  = [[0]   * 3 for i in range(ntriangles.value)]

	for i in range(len(pyverts)): # use i and range to avoid append()
		pyverts[i][0] = vert_array[i].x
		pyverts[i][1] = vert_array[i].y
		pyverts[i][2] = vert_array[i].z

	for i in range(len(pytris)):
		pytris[i][0] = tri_array[i].a
		pytris[i][1] = tri_array[i].b
		pytris[i][2] = tri_array[i].c

	print('free EDTSurf arrays')
	lib.freelists.argtypes = [c_point_p, c_tri_p]
	lib.freelists.restype = None

	lib.freelists(vertices, triangles)

	return [pyverts, pytris]



if __name__ == '__main__':

	pdbfname = '2k5x_a.pdb'

	verts = []
	tris = []

	try:
		# todos os argumentos após pdbfname possuem valores padrão
		[verts, tris] = calc_surface(pdbfname)

		# talvez scale_factor seja um argumento a se ajustar
		#[verts, tris] = calc_surface(pdbfname, scale_factor=1.0)
	except Exception as err:
		print('Failed to calculate surface:', err)
	else:
		print('len(verts) =', len(verts), ', [0] =', verts[0])
		print('len(tris) =', len(tris), ', [0] =', tris[0])

		print('Done')
