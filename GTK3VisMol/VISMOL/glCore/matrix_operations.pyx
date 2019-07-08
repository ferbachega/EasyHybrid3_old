#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  matrix_operations.pyx
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

import math
import numpy as np
cimport numpy as np

def my_glSideVectorAbs(in_matrix):
    """ Uses a numpy array as input to obtain the side vector untransformed,
        i.e. when you apply a modification to a vector using a matrix,
        its coordinates are changed, so this function returns the
        "original" vector or the vector in tha ABSOLUTE coordinates
        system. The entry numpy array has shape (4, 4), size of 16 and ndim=2.
        
        Keyword arguments:
        in_matrix -- a numpy array that can be the PROJECTION, VIEW or 
                     MODEL matrix.
        
        Returns:
            side -- Numpy array of 3 elements corresponding to the Side vector.
    """
    inv_mat = np.matrix(in_matrix, dtype=np.float32).I
    side = np.array([[1],[0],[0],[1]],dtype=np.float32)
    side = np.array(inv_mat*side).T
    return side[0,:3]

def my_glUpVectorAbs(in_matrix):
    """ Uses a 4x4 matrix as input to obtain the up vector untransformed,
        i.e. when you apply a modification to a vector using a matrix,
        its coordinates are changed, so this function returns the
        "original" vector or the vector in tha ABSOLUTE coordinates
        system.
        
        Keyword arguments:
        in_matrix -- a 4x4 matrix that can be the PROJECTION, VIEW or 
                     MODEL matrix.
        
        Returns:
            Numpy array of 3 elements corresponding to the Up vector.
    """
    inv_mat = np.matrix(in_matrix, dtype=np.float32).I
    side = np.array([[0],[1],[0],[1]],dtype=np.float32)
    side = np.array(inv_mat*side).T
    return side[0,:3]

def my_glForwardVectorAbs(in_matrix):
    """ Uses a 4x4 matrix as input to obtain the forward vector untransformed,
        i.e. when you apply a modification to a vector using a matrix,
        its coordinates are changed, so this function returns the
        "original" vector or the vector in tha ABSOLUTE coordinates
        system.
        
        Keyword arguments:
        in_matrix -- a 4x4 matrix that can be the PROJECTION, VIEW or 
                     MODEL matrix.
        
        Returns:
            Numpy array of 3 elements corresponding to the Forward vector.
    """
    inv_mat = np.matrix(in_matrix, dtype=np.float32).I
    side = np.array([[0],[0],[-1],[1]],dtype=np.float32)
    side = np.array(inv_mat*side).T
    return side[0,:3]

def my_glTranslatef(np.ndarray in_matrix, np.ndarray position):
    """ Creates a translation matrix using an identity matrix and the
        position's coordinates at the last row, but only the xyz components.
        As initial result, you get the following matrix:
        
                        |1 0 0 0|       |1 0 0 0|
                        |0 1 0 0|  ==>  |0 1 0 0|
                        |0 0 1 0|  ==>  |0 0 1 0|
                        |0 0 0 1|       |x y z 1|
        
        then, this translation matrix is multiplied to the input matrix to
        obtain the final result, a translated matrix to position.
        
        Keyword arguments:
            in_matrix -- a 4x4 matrix that you want to apply a translation.
            position -- a 3 elements numpy ndarray with the coordinates of
                        your desired translation.
        
        Returns:
            A multiplied 4x4 matrix of [in_matrix] x [trans_matrix].
    """
    cdef np.ndarray[np.float32_t, ndim=2] trans_matrix = np.identity(4, dtype=np.float32)
    trans_matrix[3,:3] = position
    return my_glMultiplyMatricesf(in_matrix, trans_matrix)

def my_glMultiplyMatricesf(np.ndarray mat1, np.ndarray mat2):
    """ Multiplication of matrices in the order [mat1] x [mat2].
        
        Keyword arguments:
            mat1 -- a 4x4 matrix.
            mat2 -- a 4x4 matrix.
        
        Returns:
            result -- a multiplied 4x4 matrix of [mat1] x [mat2].
    """
    cdef np.ndarray[np.float32_t, ndim=2] result = np.zeros((4,4), dtype=np.float32)
    result[0,0] = mat1[0,0]*mat2[0,0]+mat1[0,1]*mat2[1,0]+mat1[0,2]*mat2[2,0]+mat1[0,3]*mat2[3,0]
    result[1,0] = mat1[1,0]*mat2[0,0]+mat1[1,1]*mat2[1,0]+mat1[1,2]*mat2[2,0]+mat1[1,3]*mat2[3,0]
    result[2,0] = mat1[2,0]*mat2[0,0]+mat1[2,1]*mat2[1,0]+mat1[2,2]*mat2[2,0]+mat1[2,3]*mat2[3,0]
    result[3,0] = mat1[3,0]*mat2[0,0]+mat1[3,1]*mat2[1,0]+mat1[3,2]*mat2[2,0]+mat1[3,3]*mat2[3,0]
    
    result[0,1] = mat1[0,0]*mat2[0,1]+mat1[0,1]*mat2[1,1]+mat1[0,2]*mat2[2,1]+mat1[0,3]*mat2[3,1]
    result[1,1] = mat1[1,0]*mat2[0,1]+mat1[1,1]*mat2[1,1]+mat1[1,2]*mat2[2,1]+mat1[1,3]*mat2[3,1]
    result[2,1] = mat1[2,0]*mat2[0,1]+mat1[2,1]*mat2[1,1]+mat1[2,2]*mat2[2,1]+mat1[2,3]*mat2[3,1]
    result[3,1] = mat1[3,0]*mat2[0,1]+mat1[3,1]*mat2[1,1]+mat1[3,2]*mat2[2,1]+mat1[3,3]*mat2[3,1]
    
    result[0,2] = mat1[0,0]*mat2[0,2]+mat1[0,1]*mat2[1,2]+mat1[0,2]*mat2[2,2]+mat1[0,3]*mat2[3,2]
    result[1,2] = mat1[1,0]*mat2[0,2]+mat1[1,1]*mat2[1,2]+mat1[1,2]*mat2[2,2]+mat1[1,3]*mat2[3,2]
    result[2,2] = mat1[2,0]*mat2[0,2]+mat1[2,1]*mat2[1,2]+mat1[2,2]*mat2[2,2]+mat1[2,3]*mat2[3,2]
    result[3,2] = mat1[3,0]*mat2[0,2]+mat1[3,1]*mat2[1,2]+mat1[3,2]*mat2[2,2]+mat1[3,3]*mat2[3,2]
    
    result[0,3] = mat1[0,0]*mat2[0,3]+mat1[0,1]*mat2[1,3]+mat1[0,2]*mat2[2,3]+mat1[0,3]*mat2[3,3]
    result[1,3] = mat1[1,0]*mat2[0,3]+mat1[1,1]*mat2[1,3]+mat1[1,2]*mat2[2,3]+mat1[1,3]*mat2[3,3]
    result[2,3] = mat1[2,0]*mat2[0,3]+mat1[2,1]*mat2[1,3]+mat1[2,2]*mat2[2,3]+mat1[2,3]*mat2[3,3]
    result[3,3] = mat1[3,0]*mat2[0,3]+mat1[3,1]*mat2[1,3]+mat1[3,2]*mat2[2,3]+mat1[3,3]*mat2[3,3]
    return result

def my_glRotatef(np.ndarray in_matrix, np.float32_t angle, np.ndarray dir_vec):
    """ Produces a rotation matrix of "angle" degrees around the vector 
        "dir_vec", then multiply the input matrix "in_matrix" with this 
        rotation matrix "rot_matrix" in the order [in_matrix] x [trans_matrix].
        The rotation matrix takes the form of:
        
        | x*x*(1-c)+c   x*y*(1-c)-z*s   x*z*(1-c)+y*s   0|
        |y*x*(1-c)+z*s   y*y*(1-c)+c    y*z*(1-c)-x*s   0|
        |x*z*(1-c)-y*s  y*z*(1-c)+x*s    z*z*(1-c)+c    0|
        |      0              0               0         1|
        
        Keyword arguments:
            in_matrix -- a 4x4 matrix that you want to apply a rotation.
            angle -- the angle of rotation in radians.
            dir_vec -- a 3 elements vector with the xyz components to use as
                       axis of rotation.
        
        Returns:
            A multiplied 4x4 matrix of [in_matrix] x [rot_matrix].
    """
    cdef np.ndarray[np.float32_t, ndim=1] vector = np.array(dir_vec, dtype=np.float32)
    assert(np.linalg.norm(vector)>0.0)
    #assert(angle>=0.0)
    angle = angle*math.pi/180.0
    cdef np.float32_t x, y, z
    x, y, z = vector/np.linalg.norm(vector)
    cdef np.float32_t c = math.cos(angle)
    cdef np.float32_t s = math.sin(angle)
    cdef np.ndarray[np.float32_t, ndim=2] rot_matrix = np.identity(4, dtype=np.float32)
    rot_matrix[0,0] = x*x*(1-c)+c
    rot_matrix[1,0] = y*x*(1-c)+z*s
    rot_matrix[2,0] = x*z*(1-c)-y*s
    rot_matrix[0,1] = x*y*(1-c)-z*s
    rot_matrix[1,1] = y*y*(1-c)+c
    rot_matrix[2,1] = y*z*(1-c)+x*s
    rot_matrix[0,2] = x*z*(1-c)+y*s
    rot_matrix[1,2] = y*z*(1-c)-x*s
    rot_matrix[2,2] = z*z*(1-c)+c
    return my_glMultiplyMatricesf(in_matrix, rot_matrix)

def my_glPerspectivef(np.float32_t fovy, np.float32_t aspect, np.float32_t z_near, np.float32_t z_far):
    """ Creates a perspective matrix with "fovy" as field of view, "aspect" as
        viewport aspect ratio, "z_near" as the near clipping plane and "z_far"
        as far clipping plane. The perpective matrix is constructed in the form:
        
        |f/aspect  0                 0                   0|
        |   0      f                 0                   0|
        |   0      0    (z_near+z_far)/(z_near-z_far)   -1|
        |   0      0   2.0*z_near*z_far/(z_near-z_far)   0|
        
        With f = cotangent(fovy/2)
        
    """
    assert(aspect>0.0)
    assert(z_far>z_near)
    cdef np.float32_t f = np.float32(1.0/(math.tan(fovy*math.pi/180.0)))
    cdef np.ndarray[np.float32_t, ndim=2] pers_matrix = np.zeros((4,4), dtype=np.float32)
    pers_matrix[0,0] = f/aspect
    pers_matrix[1,1] = f
    pers_matrix[2,2] = (z_near+z_far)/(z_near-z_far)
    pers_matrix[3,2] = 2.0*z_near*z_far/(z_near-z_far)
    pers_matrix[2,3] = -1.0
    return pers_matrix

def my_glFrustumf(np.float32_t left, np.float32_t rigth, np.float32_t bottom, np.float32_t top, np.float32_t near, np.float32_t far):
    """ Creates a frustrum to use as perspective matrix. Uses the "left" and 
        "right" as leaft and rigth vertical clipping planes of the frustrum.
        The "top" and "bottom" as the top and bottom horizontal clipping planes.
        The "near" and "far" especify the near and far depth clipping planes.
        The resulting matrix is constructed in the form:
        
        |  2.0*near/(rigth-left)                0                         0               0|
        |            0                2.0*near/(top-bottom)               0               0|
        |(rigth+left)/(rigth-left)  (top+bottom)/(top-bottom)   (far+near)/(near-far)    -1|
        |            0                          0              -2.0*near*far/(far-near)   0|
        
    """
    cdef np.ndarray[np.float32_t, ndim=2] frust = np.zeros((4,4), dtype=np.float32)
    frust[0,0] = 2.0*near/(rigth-left)
    frust[1,1] = 2.0*near/(top-bottom)
    frust[2,0] = (rigth+left)/(rigth-left)
    frust[2,1] = (top+bottom)/(top-bottom)
    frust[2,2] = (far+near)/(near-far)
    frust[2,3] = -1.0
    frust[3,2] = -2.0*near*far/(far-near)
    return frust

def my_glOrthof(np.float32_t left, np.float32_t rigth, np.float32_t bottom, np.float32_t top, np.float32_t near, np.float32_t far):
    """ 
    """
    cdef np.ndarray[np.float32_t, ndim=2] ortho = np.zeros((4,4), dtype=np.float32)
    ortho[0,0] = 2.0/(rigth-left)
    ortho[1,1] = 2.0/(top-bottom)
    ortho[2,2] = -2.0/(far-near)
    ortho[3,0] = (rigth+left)/(left-rigth)
    ortho[3,1] = (top+bottom)/(bottom-top)
    ortho[3,2] = (far+near)/(near-far)
    ortho[3,3] = 1.0
    return ortho

def get_xyz_coords(np.ndarray xyz_mat):
    """ Returns the x, y, z position contained in the xyz_mat matrix. The
        input matrix needs to be a 4x4 matrix.
    """
    assert(xyz_mat.ndim==2)
    assert(xyz_mat.size==16)
    cdef np.ndarray[np.float32_t, ndim=2] rot_mat = xyz_mat[:3,:3]
    cdef np.ndarray[np.float32_t, ndim=1] pos = -xyz_mat[3,:3]
    cdef np.ndarray[np.float32_t, ndim=1] position = pos.dot(rot_mat)
    return position

def get_inverse_matrix(mat):
    """ Function doc
    """
    mat_o = np.matrix(np.copy(mat))
    assert(mat.shape == (4,4))
    return np.array(mat_o.I)

#def my_glScalef(np.ndarray in_matrix, np.ndarray scale_vec):
    #""" This method uses a vector of floats (scale_vec) )to create a scale
        #matrix
        
    #"""
    #x_scale = np.float32(scale_vec[0])
    #y_scale = np.float32(scale_vec[1])
    #z_scale = np.float32(scale_vec[2])
    #scale_matrix = np.identity(4, dtype=np.float32)
    #scale_matrix[0,0] = x_scale
    #scale_matrix[1,1] = y_scale
    #scale_matrix[2,2] = z_scale
    #return my_glMultiplyMatricesf(in_matrix, scale_matrix)

#def my_glScalef(scale):
    #scale_matrix = np.identity(4, dtype=np.float32)
    #scale_matrix[0,0] = scale
    #scale_matrix[1,1] = scale
    #scale_matrix[2,2] = scale
    #return scale_matrix

#def my_glPerspectived(fovy, aspect, z_near, z_far):
    #y_max = np.float64(z_near*math.tan(fovy*math.pi/360.0))
    #x_max = np.float64(y_max*aspect)
    #return my_gluFrustumd(-x_max, x_max, -y_max, y_max, z_near, z_far)

#def my_gluFrustumd(left, rigth, bottom, top, near, far):
    #frust = np.zeros((4,4), dtype=np.float64)
    #frust[0,0] = np.float64((2*near)/(rigth-left))
    #frust[1,1] = np.float64((2*near)/(top-bottom))
    #frust[2,0] = np.float64((rigth+left)/(rigth-left))
    #frust[2,1] = np.float64((top+bottom)/(top-bottom))
    #frust[2,2] = np.float64((-far-near)/(far-near))
    #frust[2,3] = np.float64(-1)
    #frust[3,2] = np.float64((-2*near*far)/(far-near))
    #return frust

#def my_gluFrustumf(left, rigth, bottom, top, near, far):
    #frust = np.zeros((4,4), dtype=np.float32)
    #frust[0,0] = np.float32((2*near)/(rigth-left))
    #frust[1,1] = np.float32((2*near)/(top-bottom))
    #frust[2,0] = np.float32((rigth+left)/(rigth-left))
    #frust[2,1] = np.float32((top+bottom)/(top-bottom))
    #frust[2,2] = np.float32((-far-near)/(far-near))
    #frust[2,3] = np.float32(-1)
    #frust[3,2] = np.float32((-2*near*far)/(far-near))
    #return frust

#def my_glRotateXf(in_matrix, angle):
    #angle = angle*math.pi/180.0
    #rot_matrix = np.identity(4, dtype=np.float32)
    #rot_matrix[1,1] = math.cos(angle)
    #rot_matrix[2,1] = math.sin(angle)
    #rot_matrix[1,2] = -math.sin(angle)
    #rot_matrix[2,2] =  math.cos(angle)
    #return my_glMultiplyMatricesf(in_matrix, rot_matrix)

#def my_glRotateYf(in_matrix, angle):
    #angle = angle*math.pi/180.0
    #rot_matrix = np.identity(4, dtype=np.float32)
    #rot_matrix[0,0] = math.cos(angle)
    #rot_matrix[0,2] = math.sin(angle)
    #rot_matrix[2,0] = -math.sin(angle)
    #rot_matrix[2,2] =  math.cos(angle)
    #return my_glMultiplyMatricesf(in_matrix, rot_matrix)

#def my_glRotateZf(in_matrix, angle):
    #angle = angle*math.pi/180.0
    #rot_matrix = np.identity(4, dtype=np.float32)
    #rot_matrix[0,0] = math.cos(angle)
    #rot_matrix[1,0] = math.sin(angle)
    #rot_matrix[0,1] = -math.sin(angle)
    #rot_matrix[1,1] =  math.cos(angle)
    #return my_glMultiplyMatricesf(in_matrix, rot_matrix)

#def my_gluLookAt(in_matrix, eye, target, up):
    #forward = target - eye
    #forward = forward/np.linalg.norm(forward)
    #side = np.cross(forward, up)
    #side = side/np.linalg.norm(side)
    #up = np.cross(side, forward)
    #temp_matrix = np.identity(4, dtype=np.float32)
    #temp_matrix[:3,0] = side
    #temp_matrix[:3,1] = up
    #temp_matrix[:3,2] = -forward
    #result_matrix = my_glMultiplyMatricesf(in_matrix, temp_matrix)
    #result_matrix = my_glTranslatef(result_matrix, -eye)
    #result_matrix = my_glTranslatef(temp_matrix, -eye)
    #return result_matrix
    #view_matrix = np.identity(4, dtype=np.float32)
    #forward = target - eye
    #forward = forward/np.linalg.norm(forward)
    #side = np.cross(up, forward)
    #side = side/np.linalg.norm(side)
    #up = np.cross(forward, side)
    #up = up/np.linalg.norm(up)
    #dot_x = -np.dot(side, eye)
    #dot_y = -np.dot(up, eye)
    #dot_z = -np.dot(forward, eye)
    #view_matrix[:3,0] = side
    #view_matrix[:3,1] = up
    #view_matrix[:3,2] = -forward
    #view_matrix[3,0] = dot_x
    #view_matrix[3,1] = dot_y
    #view_matrix[3,2] = dot_z
    #return view_matrix














