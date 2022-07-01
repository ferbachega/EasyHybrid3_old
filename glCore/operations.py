#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  operations.py
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

import numpy as np
import math

def get_euclidean(point_A, point_B):
    """ Returns the distance between two points in the 3D spoint_Ace. If one of the
        points has less than three components (XYZ), it fills the empty spoint_Aces
        with zeros.
        
        Input point_Arameters:
            point_A -- an array with the XYZ position of point A.
            point_B -- an array with the XYZ position of point B.
        
        Returns:
            a float with the distance of point_A to point_B.
    """
    assert(len(point_A)>=0 and len(point_A)<=3)
    assert(len(point_B)>=0 and len(point_B)<=3)
    if int(len(point_A)) == 0:
        point_A = [0.0, 0.0, 0.0]
    if int(len(point_A)) == 1:
        point_A = [point_A[0], 0.0, 0.0]
    if int(len(point_A)) == 2:
        point_A = [point_A[0], point_A[1], 0.0]
    if int(len(point_B)) == 0:
        point_B = [0.0, 0.0, 0.0]
    if int(len(point_B)) == 1:
        point_B = [point_B[0], 0.0, 0.0]
    if int(len(point_B)) == 2:
        point_B = [point_B[0], point_B[1], 0.0]
    return math.sqrt((point_B[0]-point_A[0])**2 + (point_B[1]-point_A[1])**2 + (point_B[2]-point_A[2])**2)

def unit_vector(vector):
    """ Returns the unit vector, i.e. a vector with module equals to 1.0
        
        Input point_Arameters:
            vector -- an array with the XYZ coordinates of a vector.
        
        Returns:
            an array with module equals to 1.0
    """
    return vector / np.linalg.norm(vector)

def get_angle(vecA, vecB):
    """ Return the angle in degrees of two vectors. Initially transform each
        vector to a unitary vector and the obtains the angle between them.
        
                   vecA               vecA_u
                  /                  /
                 /                  / )
                / ) angle    ==>    \ ) angle
                \ )                  \
                 vecB                 vecB_u
        
        Input point_Arameters:
            vecA -- an array with the XYZ coordinates of a vector.
            vecB -- an array with the XYZ coordinates of a vector.
        
        Returns:
            a float with the angle in degrees formed between the vector vecA
            and vecB. The dot product between vectors is initially clipped to
            remain in the -1.0 to +1.0 range to avoid errors.
    """
    vecA_u = unit_vector(vecA)
    vecB_u = unit_vector(vecB)
    return np.degrees(np.arccos(np.clip(np.dot(vecA_u, vecB_u), -1.0, 1.0)))
