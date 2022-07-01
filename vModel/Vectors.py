#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Vectors.py
#  
#  Copyright 2015 farminf <farminf@farminf-3>
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
import math

# Support Cartesian points, vectors and operators (dot products,
# cross products, etc).

def Point(x, y, z):
	return (x, y, z)

def Vector(x, y, z):
	return (x, y, z)

def length(v):
	"Return length of a vector."
	sum = 0.0
	for c in v:
		sum += c * c
	return math.sqrt(sum)

def subtract(u, v): # u[x,y,z]
	"Return difference between two vectors."
	x = u[0] - v[0]
	y = u[1] - v[1]
	z = u[2] - v[2]
	return Vector(x, y, z)

def dot(u, v):
	"Return dot product of two vectors."
	sum = 0.0
	for cu, cv in zip(u, v):
		sum += cu * cv
	return sum

def cross(u, v):
	"Return the cross product of two vectors."
	x = u[1] * v[2] - u[2] * v[1]
	y = u[2] * v[0] - u[0] * v[2]
	z = u[0] * v[1] - u[1] * v[0]
	return Vector(x, y, z)

def angle(v0, v1):
    "Return angle [0..pi] between two vectors."
    #print v0, v1
    try:
        cosa = dot(v0, v1) / length(v0) / length(v1)
        return math.acos(cosa)
    except:
        return False
        
def dihedral(p0, p1, p2, p3):
    "Return angle [0..2*pi] formed by vertices p0-p1-p2-p3."
    v01 = subtract(p0, p1)
    v32 = subtract(p3, p2)
    v12 = subtract(p1, p2)
    v0 = cross(v12, v01)
    v3 = cross(v12, v32)
    # The cross product vectors are both normal to the axis
    # vector v12, so the angle between them is the dihedral
    # angle that we are looking for.  However, since "angle"
    # only returns values between 0 and pi, we need to make
    # sure we get the right sign relative to the rotation axis
    a = angle(v0, v3)
    if dot(cross(v0, v3), v12) > 0:
        a = -a
    #print a
    return a

