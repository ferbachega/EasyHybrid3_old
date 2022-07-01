#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright 2021 Carlos Eduardo Sequeiros Borja <carseq@amu.edu.pl>
#  

import numpy as np
import vModel.Vectors as LA

p = 0.6;
q = 0.8071;
COIL_POINTS = np.array([[ -p, -p, 0], [p, -p, 0], [p, p, 0], [-p, p, 0]], dtype=np.float32)

HELIX_POINTS = np.array([[-6.0 * p, -0.9 * q, 0], [-5.8 * p, -1.0 * q, 0],
                         [ 5.8 * p, -1.0 * q, 0], [ 6.0 * p, -0.9 * q, 0],
                         [ 6.0 * p,  0.9 * q, 0], [ 5.8 * p,  1.0 * q, 0],
                         [-5.8 * p,  1.0 * q, 0], [-6.0 * p,  0.9 * q, 0]], dtype=np.float32)

ARROW_POINTS = np.array([[-10.0 * p, -0.9 * q, 0], [ -9.8 * p, -1.0 * q, 0],
                         [  9.8 * p, -1.0 * q, 0], [ 10.0 * p, -0.9 * q, 0],
                         [ 10.0 * p,  0.9 * q, 0], [  9.8 * p,  1.0 * q, 0],
                         [ -9.8 * p,  1.0 * q, 0], [-10.0 * p,  0.9 * q, 0]], dtype=np.float32)

arcDetail = 2.0
splineDetail = 5

def cubic_hermite_interpolate(p_k1, tan_k1, p_k2, tan_k2, t):
    p = np.zeros(3, dtype=np.float32)
    tt = t * t
    tmt_t = 3.0 - 2.0 * t
    h01 = tt * tmt_t
    h00 = 1.0 - h01
    h10 = tt * (t - 2.0) + t
    h11 = tt * (t - 1.0)
    p[:] = p_k1[:]
    p*= h00
    p += tan_k1 * h10
    p += p_k2 * h01
    p += tan_k2 * h11
    return p

def catmull_rom_spline(points, num_points, subdivs, strength=0.6, circular=False):
    if circular:
        out_len = num_points * subdivs
    else:
        out_len = (num_points - 1) * subdivs + 1
    out = np.zeros([out_len, 3], dtype=np.float32)
    index = 0
    dt = 1.0 / subdivs
    tan_k1 = np.zeros(3, dtype=np.float32)
    tan_k2 = np.zeros(3, dtype=np.float32)
    p_k1 = np.zeros(3, dtype=np.float32)
    p_k2 = np.zeros(3, dtype=np.float32)
    p_k3 = np.zeros(3, dtype=np.float32)
    p_k4 = np.zeros(3, dtype=np.float32)
    p_k2[:] = points[0,:]
    p_k3[:] = points[1,:]
    if circular:
        p_k1[:] = points[-1,:]
        tan_k1[:] = p_k3 - p_k1
        tan_k1 *= strength
    else:
        p_k1[:] = points[0,:]
    i = 1
    e = num_points - 1
    while i < e:
        p_k4[:] = points[i+1,:]
        tan_k2[:] = p_k4 - p_k2
        tan_k2 *= strength
        for j in range(subdivs):
            out[index,:] = cubic_hermite_interpolate(p_k2, tan_k1, p_k3, tan_k2, dt*j)
            index += 1
        p_k1[:] = p_k2[:]
        p_k2[:] = p_k3[:]
        p_k3[:] = p_k4[:]
        tan_k1[:] = tan_k2[:]
        i += 1
    if circular:
        p_k4[0] = points[0,0]
        p_k4[1] = points[0,1]
        p_k4[2] = points[1,0]
        tan_k1 = p_k4 - p_k2
        tan_k1 *= strength
    else:
        tan_k1 = np.zeros(3, dtype=np.float32)
    for j in range(subdivs):
        out[index] = cubic_hermite_interpolate(p_k2, tan_k1, p_k3, tan_k2, dt*j)
        index += 1
    if not circular:
        out[index] = points[num_points-1:num_points]
        return out
    p_k1[:] = p_k2[:]
    p_k2[:] = p_k3[:]
    p_k3[:] = p_k4[:]
    tan_k1[:] = tan_k2[:]
    p_k4[:] = points[1,:]
    tan_k1 = p_k4 - p_k2
    tan_k1 *= strength
    for j in range(subdivs):
        out[index] = cubic_hermite_interpolate(p_k2, tan_k1, p_k3, tan_k2, dt*j)
        index += 1
    return out


# calphas = np.loadtxt("cas.txt")
# print(calphas)
# calphas = calphas.flatten()
# spline = catmull_rom_spline(np.copy(calphas), calphas.shape[0], 1)
# print(spline)

def get_rotmat3f(angle, dir_vec):
    # vector = np.array(dir_vec, dtype=np.float32)
    assert(np.linalg.norm(dir_vec)>0.0)
    # angle = angle*np.pi/180.0
    # x, y, z = vector/np.linalg.norm(vector)
    x, y, z = dir_vec
    c = np.cos(angle)
    s = np.sin(angle)
    rot_matrix = np.identity(3, dtype=np.float32)
    rot_matrix[0,0] = x*x*(1-c)+c
    rot_matrix[1,0] = y*x*(1-c)+z*s
    rot_matrix[2,0] = x*z*(1-c)-y*s
    rot_matrix[0,1] = x*y*(1-c)-z*s
    rot_matrix[1,1] = y*y*(1-c)+c
    rot_matrix[2,1] = y*z*(1-c)+x*s
    rot_matrix[0,2] = x*z*(1-c)+y*s
    rot_matrix[1,2] = y*z*(1-c)-x*s
    rot_matrix[2,2] = z*z*(1-c)+c
    return rot_matrix

def get_beta_vectors(p1, p2, p3):
    com123 = (p1 + p2 + p3) / 3.0
    com12 = (p1 - p2) / 2.0
    com23 = (p2 - p3) / 2.0
    vec1 = com123 - com12
    vec1 /= np.linalg.norm(vec1)
    vec2 = com123 - com23
    vec2 /= np.linalg.norm(vec2)
    up_vec = vec1 + vec2
    up_vec /= np.linalg.norm(up_vec)
    vec3 = p3 - p1
    side_vec = np.cross(up_vec, vec3)
    side_vec /= np.linalg.norm(side_vec)
    return up_vec, side_vec

def get_helix_vector(p1, p2, p3, p4):
    com1234 = (p1 + p2 + p3 + p4) / 4.0
    com12 = (p1 + p2) / 2.0
    com23 = (p2 + p3) / 2.0
    com34 = (p3 + p4) / 2.0
    # com14 = (p1 + p4) / 2.0
    vec1 = com23 - com1234
    vec2 = com34 - com1234
    vec3 = np.cross(vec1, vec2)
    vec3 /= np.linalg.norm(vec3)
    pointA = com1234 + vec3 * np.linalg.norm(com34-com1234)
    pointB = com1234 - vec3 * np.linalg.norm(com34-com1234)
    com12B = (com12 + pointB) / 2.0
    com34A = (com34 + pointA) / 2.0
    dir_vec = com34A - com12B
    return dir_vec / np.linalg.norm(dir_vec)

def get_coil(spline, coil_rad=0.2, color=None):
    if color is None:
        color = [1.0, 1.0, 1.0]
    coil_points = np.array([[ 0.5, 0.866, 0.0], [ 1.0, 0.0, 0.0],
                            [ 0.5,-0.866, 0.0], [-0.5,-0.866, 0.0],
                            [-1.0, 0.0, 0.0], [-0.5, 0.866, 0.0]], dtype=np.float32)
    coil_points *= coil_rad
    coords = np.zeros([spline.shape[0]*6, 3], dtype=np.float32)
    normals = np.zeros([spline.shape[0]*6, 3], dtype=np.float32)
    colors = np.array([color]*spline.shape[0]*6, dtype=np.float32)
    for i in range(spline.shape[0] - 1):
        dir_vec = spline[i+1] - spline[i]
        dir_vec /= np.linalg.norm(dir_vec)
        align_vec = np.cross([0.0, 0.0, 1.0], dir_vec)
        align_vec /= np.linalg.norm(align_vec)
        angle = np.arccos(np.dot([0.0, 0.0, 1.0], dir_vec))
        rotmat = get_rotmat3f(angle, align_vec)
        for j, point in enumerate(coil_points):
            coords[i*6+j,:] = np.matmul(rotmat, point) + spline[i]
            normals[i*6+j,:] = coords[i*6+j,:] - spline[i]
    for i, point in enumerate(coil_points):
        coords[-6+i,:] = np.matmul(rotmat, point) + spline[-1]
        normals[-6+i,:] = coords[-6+i,:] - spline[-1]
    return coords, normals, colors

def get_helix(spline, spline_detail, helix_rad=0.2, color=None):
    if color is None:
        color = [1.0, 0.0, 0.0]
    coords = np.zeros([spline.shape[0]*6, 3], dtype=np.float32)
    normals = np.zeros([spline.shape[0]*6, 3], dtype=np.float32)
    colors = np.array([color]*coords.shape[0], dtype=np.float32)
    helix_vec = np.zeros(3, dtype=np.float32)
    for i in range(spline.shape[0] - spline_detail*3):
        helix_vec += get_helix_vector(spline[i], spline[i+spline_detail],
                 spline[i+spline_detail*2], spline[i+spline_detail*3])
        helix_vec /= np.linalg.norm(helix_vec)
        dir_vec = spline[i+1] - spline[i]
        side_vec = np.cross(dir_vec, helix_vec)
        side_vec /= np.linalg.norm(side_vec)
        coords[i*6] = spline[i] + helix_vec + side_vec * helix_rad / 2.0
        coords[i*6+1] = spline[i] + side_vec * helix_rad
        coords[i*6+2] = spline[i] - helix_vec + side_vec * helix_rad / 2.0
        coords[i*6+3] = spline[i] - helix_vec - side_vec * helix_rad / 2.0
        coords[i*6+4] = spline[i] - side_vec * helix_rad
        coords[i*6+5] = spline[i] + helix_vec - side_vec * helix_rad / 2.0
        for j in range(6):
            normals[i*6+j] = coords[i*6+j] - spline[i]
    for i in range(spline.shape[0] - spline_detail*3, spline.shape[0]):
        if i < spline.shape[0] - 1:
            dir_vec = spline[i+1] - spline[i]
            side_vec = np.cross(dir_vec, helix_vec)
            side_vec /= np.linalg.norm(side_vec)
        coords[i*6] = spline[i] + helix_vec + side_vec * helix_rad / 2.0
        coords[i*6+1] = spline[i] + side_vec * helix_rad
        coords[i*6+2] = spline[i] - helix_vec + side_vec * helix_rad / 2.0
        coords[i*6+3] = spline[i] - helix_vec - side_vec * helix_rad / 2.0
        coords[i*6+4] = spline[i] - side_vec * helix_rad
        coords[i*6+5] = spline[i] + helix_vec - side_vec * helix_rad / 2.0
        for j in range(6):
            normals[i*6+j] = coords[i*6+j] - spline[i]
    return coords, normals, colors

def get_beta(orig_spline, spline_detail, beta_rad=0.5, color=None):
    if color is None:
        color = [1.0, 1.0, 0.0]
    p1 = orig_spline[0]
    p2 = np.zeros(3, dtype=np.float32)
    for i in range(0, orig_spline.shape[0], spline_detail):
        p2 += orig_spline[i]
    p2 /= (orig_spline.shape[0]/spline_detail)
    p3 = orig_spline[-1]
    spline = bezier_curve(p1, p2, p3, orig_spline.shape[0])
    coords = np.zeros([spline.shape[0]*4, 3], dtype=np.float32)
    normals = np.zeros([spline.shape[0]*4, 3], dtype=np.float32)
    colors = np.array([color]*coords.shape[0], dtype=np.float32)
    beta_up = np.zeros(3, dtype=np.float32)
    beta_side = np.zeros(3, dtype=np.float32)
    beta_dir = 1
    for i in range(spline.shape[0] - spline_detail):
        if i < spline.shape[0] - spline_detail * 2 and i % spline_detail == 0:
            _vecs = get_beta_vectors(spline[i], spline[i+spline_detail], spline[i+spline_detail*2])
            beta_up += _vecs[0] * beta_dir
            # beta_side += _vecs[1] * beta_dir
            beta_up /= np.linalg.norm(beta_up)
            beta_side = np.cross(spline[i+1]-spline[i], beta_up)
            beta_side /= np.linalg.norm(beta_side)
            # beta_dir *= -1
        coords[i*4] = spline[i] + beta_up * beta_rad / 1.5 + beta_side * beta_rad
        coords[i*4+1] = spline[i] - beta_up * beta_rad / 1.5 + beta_side * beta_rad
        coords[i*4+2] = spline[i] - beta_up * beta_rad / 1.5 - beta_side * beta_rad
        coords[i*4+3] = spline[i] + beta_up * beta_rad / 1.5 - beta_side * beta_rad
        for j in range(4):
            normals[i*4+j] = coords[i*4+j] - spline[i]
    arrow_rads = np.linspace(beta_rad*2.5, 0.1, spline_detail)
    arros_inds = np.arange(spline.shape[0] - spline_detail, spline.shape[0], dtype=np.uint32)
    for i, r in zip(arros_inds, arrow_rads):
        # _vecs = get_beta_vectors(spline[i], spline[i+spline_detail], spline[i+spline_detail*2])
        # beta_up += _vecs[0] * beta_dir
        # beta_side += _vecs[1] * beta_dir
        # beta_up /= np.linalg.norm(beta_up)
        # beta_side /= np.linalg.norm(beta_side)
        # beta_dir *= -1
        coords[i*4] = spline[i] + beta_up * beta_rad / 1.5 + beta_side * r
        coords[i*4+1] = spline[i] - beta_up * beta_rad / 1.5 + beta_side * r
        coords[i*4+2] = spline[i] - beta_up * beta_rad / 1.5 - beta_side * r
        coords[i*4+3] = spline[i] + beta_up * beta_rad / 1.5 - beta_side * r
        for j in range(4):
            normals[i*4+j] = coords[i*4+j] - spline[i]
    return coords, normals, colors

def get_indexes_BCK(rings, points_perring, offset=0):
    assert points_perring > 2
    indexes = np.zeros((rings-1)*points_perring*2*3, dtype=np.uint32)
    i = 0
    for r in range(rings-1):
        for p in range(points_perring-1):
            indexes[i] = r*points_perring+p
            indexes[i+1] = r*points_perring+p+1
            indexes[i+2] = (r+1)*points_perring+p
            i += 3
        indexes[i] = (r+1)*points_perring - 1
        indexes[i+1] = r*points_perring
        indexes[i+2] = (r+2)*points_perring - 1
        i += 3
        for p in range(points_perring-1):
            indexes[i] = (r+1)*points_perring+p
            indexes[i+1] = (r+1)*points_perring+p+1
            indexes[i+2] = r*points_perring+p+1
            i += 3
        indexes[i] = (r+2)*points_perring - 1
        indexes[i+1] = (r+1)*points_perring
        indexes[i+2] = r*points_perring
        i += 3
    indexes += offset
    return indexes

def get_indexes(num_points, points_perring, offset, is_beta=False):
    size_i = (num_points//points_perring)*2*6*3 + 2*4*3
    indexes = np.zeros(size_i, dtype=np.uint32)
    # Add indices for the initial cap
    if is_beta:
        indexes[:6] = [0,1,2, 2,3,0]
    else:
        indexes[:12] = [0,1,2, 2,3,4, 4,5,0, 0,2,4]
    i = 12
    for r in range(num_points//points_perring-1):
        for p in range(points_perring-1):
            indexes[i] = r*points_perring+p
            indexes[i+1] = r*points_perring+p+1
            indexes[i+2] = (r+1)*points_perring+p
            i += 3
        indexes[i] = (r+1)*points_perring - 1
        indexes[i+1] = r*points_perring
        indexes[i+2] = (r+2)*points_perring - 1
        i += 3
        for p in range(points_perring-1):
            indexes[i] = (r+1)*points_perring+p
            indexes[i+1] = (r+1)*points_perring+p+1
            indexes[i+2] = r*points_perring+p+1
            i += 3
        indexes[i] = (r+2)*points_perring - 1
        indexes[i+1] = (r+1)*points_perring
        indexes[i+2] = r*points_perring
        i += 3
    a = num_points - points_perring
    if is_beta:
        indexes[-6:] = [a,a+1,a+2, a+2,a+3,a]
    else:
        indexes[-12:] = [a,a+1,a+2, a+2,a+3,a+4, a+4,a+5,a, a,a+2,a+4]
    indexes += offset
    return indexes


def make_normals(coords, indexes):
    normals = np.zeros(coords.shape, dtype=np.float32)
    for i in range(0, indexes.shape[0], 3):
        vec1 = coords[indexes[i+1]] - coords[indexes[i]]
        vec2 = coords[indexes[i+2]] - coords[indexes[i]]
        normal = np.cross(vec1, vec2)
        normal /= np.linalg.norm(normal)
        normals[indexes[i]] = np.copy(normal)
        normals[indexes[i+1]] = np.copy(normal)
        normals[indexes[i+2]] = np.copy(normal)
    return normals

    
    
    
def cartoon(vobject, spline_detail=3, SSE_list = []):
    sd = spline_detail
    
    #calphas = np.loadtxt(calphas_file)
    vobject.get_backbone_indexes()
    
    calphas = []
    for atom in vobject.c_alpha_atoms:
        #print(atom.index, atom.name, atom.resn, atom.resi, atom.coords())
        calphas.append(atom.coords())
    calphas = np.array(calphas, dtype = np.float32)
    #print(calphas, type(calphas), len(calphas))
    spline = catmull_rom_spline(np.copy(calphas), calphas.shape[0], sd, strength = 0.9)
    
    # TODO: function to calculate the boundaries for secondary structures.
    # This list contains the indices of the residues that are alpha helices in
    # zero-based indexing.
    # secstruc = [(0, 0, 2), (1, 2, 13), (0, 13, 19), (1, 19, 33)]
    #secstruc = [[0, 0, 4], [1, 4, 5], [0, 5, 10], [1, 10, 19], [0, 19, 26], [1, 26, 30], [0, 30, 31], [1, 31, 33], [0, 33, 37], [1, 37, 47]]
    #secstruc = [[0, 1, 4], [1, 4, 5], [0, 5, 10], [1, 10, 19], [0, 19, 26], [1, 26, 30], [0, 30, 31], [1, 31, 33], [0, 33, 37], [1, 37, 47]]
    #secstruc = [(0, 0, 1), (2,1,6), (0,6,11), (2,11,16), (0,16,21), (1,21,35),
    #            (0,35,40), (2,40,45), (0,45,55), (1,55,60), (0,60,65),
    #            (2,65,71), (0,71,74)]
    #'''
    
    #secstruc = [[0, 0, 4], [1, 5, 10]]#, [0, 5, 10]]
    
    #secstruc = [[0, 0, 40],[1, 40, 50] ]#, [2,1,6], [0,6,11], [2,11,16], [0,16,21], [1,21,35], [0,35,40], [2,40,45], [0,45,55], [1,55,60], [0,60,65],[2,65,71], [0,71,74]]
    #secstruc = [[0, 0, 1], [0, 1, 10], [1, 10, 19], [0, 19, 26], [1, 26, 33], [0, 33, 37], [1, 37, 47] ]          
    secstruc = calculate_secondary_structure(vobject)
    #secstruc.pop(0)
    #secstruc[0][1] = 0
    
    #secstruc = secstruc[1]
    #secstruc(0) 
    print (secstruc)        
    #'''
    coords  = np.zeros([1,3], dtype=np.float32)
    normals = np.zeros([1,3], dtype=np.float32)
    colors  = np.zeros([1,3], dtype=np.float32)
    indexes = np.array([], dtype=np.uint32)
    
    for ss in secstruc:
        if ss[0] == 0:
            # _inds = get_indexes((ss[2] - ss[1])*sd + 1, 6, coords.shape[0]-1)
            # indexes = np.hstack((indexes, _inds))
            if ss[1] == 0:
                if ss[2] == calphas.shape[0]:
                    data = get_coil(spline[ss[1]*sd:ss[2]*sd])
                else:
                    data = get_coil(spline[ss[1]*sd:ss[2]*sd+1])
            else:
                if ss[2] == calphas.shape[0]:
                    data = get_coil(spline[ss[1]*sd-1:ss[2]*sd])
                else:
                    data = get_coil(spline[ss[1]*sd-1:ss[2]*sd+1])
            # data = get_coil(spline[ss[1]*sd:ss[2]*sd+1], sd)
            _inds = get_indexes(data[0].shape[0], 6, coords.shape[0]-1)
            indexes = np.hstack((indexes, _inds))
            coords = np.vstack((coords, data[0]))
            normals = np.vstack((normals, data[1]))
            colors = np.vstack((colors, data[2]))
        elif ss[0] == 1:
            # _inds = get_indexes((ss[2] - ss[1])*sd, 6, coords.shape[0]-1)
            # indexes = np.hstack((indexes, _inds))
            data = get_helix(spline[ss[1]*sd:ss[2]*sd], sd)
            _inds = get_indexes(data[0].shape[0], 6, coords.shape[0]-1)
            indexes = np.hstack((indexes, _inds))
            coords = np.vstack((coords, data[0]))
            normals = np.vstack((normals, data[1]))
            colors = np.vstack((colors, data[2]))
        elif ss[0] == 2:
            # _inds = get_indexes((ss[2] - ss[1])*sd, 6, coords.shape[0]-1)
            # indexes = np.hstack((indexes, _inds))
            data = get_beta(spline[ss[1]*sd:ss[2]*sd], sd)
            _inds = get_indexes(data[0].shape[0], 4, coords.shape[0]-1, is_beta=True)
            indexes = np.hstack((indexes, _inds))
            coords = np.vstack((coords, data[0]))
            normals = np.vstack((normals, data[1]))
            colors = np.vstack((colors, data[2]))
    coords = coords[1:]
    normals = normals[1:]
    colors = colors[1:]
    normals = make_normals(coords, indexes)
    print('len:')
    print(spline.shape, coords.shape, normals.shape, colors.shape, indexes.shape)
    return coords, normals, indexes, colors

def bezier_curve(p1, p2, p3, bezier_detail):
    points_mat = np.array([p1, p2, p3], dtype=np.float32)
    points = np.zeros([bezier_detail, 3], dtype=np.float32)
    for i, t in enumerate(np.linspace(0, 1, bezier_detail)):
        vec_t = np.array([(1-t)*(1-t), 2*t-2*t*t, t*t], dtype=np.float32)
        points[i,:] = np.matmul(vec_t, points_mat)
    return points



def calculate_secondary_structure(vobject):
    '''
        First, the distances d2i, d3i and d4i between the (i - 1)th
        residue and the (i + 1)th, the (i + 2)th and the (i + 3)th,
        respectively, are computed from the cartesian coordinates
        of the Ca carbons, as well as the angle ti and dihedral angle
        ai defined by the Ca carbon triplet (i - 1, i , i + 1) and
        quadruplet (i - 1, i, i + 1, i + 2), respectively.
        
        
        Assignment parameters
                                   Secondary structure
                                   
                                   Helix        Strand
                                   
        Angle T (°)               89 ± 12       124 ± 14
        Dihedral angle a (°)      50 ± 20      -170 ± 4 5
                                               
        Distance d2 (A)           5.5 ± 0.5    6.7 ± 0.6
        Distance d3 (A)           5.3 ± 0.5    9.9 ± 0.9
        Distance d4 (A)           6.4 ± 0.6    12.4 ± 1.1


    '''
    if vobject.c_alpha_bonds == [] or vobject.c_alpha_atoms == []:
        vobject.get_backbone_indexes()
    
    for atom in vobject.c_alpha_atoms:
        print(atom.index, atom.name, atom.bonds_indexes, atom.bonds)
    

    size = len(vobject.c_alpha_bonds)
    SSE_list  = "C"
    SSE_list2 = []
    
    
    block     = [0,0,1]
    SS_before = 1
    for i in range(1,size -2):
        
        CA0 = vobject.c_alpha_bonds[i-1].atom_i # i - 1
        CA1 = vobject.c_alpha_bonds[i-1].atom_j # i
        
        CA2 = vobject.c_alpha_bonds[i].atom_i   # i
        CA3 = vobject.c_alpha_bonds[i].atom_j   # i + 1
                                               
        CA4 = vobject.c_alpha_bonds[i+1].atom_i # i + 1
        CA5 = vobject.c_alpha_bonds[i+1].atom_j # i + 2
                                               
        CA6 = vobject.c_alpha_bonds[i+2].atom_i # i + 2
        CA7 = vobject.c_alpha_bonds[i+2].atom_j # i + 3
                                               
        #CA8 = vobject.c_alpha_bonds[i+3].atom_i # i + 3 
        #CA9 = vobject.c_alpha_bonds[i+3].atom_j #


        if CA1 == CA2 and CA3 == CA4 and CA5 == CA6:
            #print ('CA1 = CA2')
            
            # distances
            d2i  = LA.subtract(CA0.coords(), CA3.coords()) 
            d2i  = LA.length(d2i)
            
            d3i  = LA.subtract(CA0.coords(), CA5.coords()) 
            d3i  = LA.length(d3i)
            
            d4i  = LA.subtract(CA0.coords(), CA7.coords()) 
            d4i  = LA.length(d4i)
            
            # angle
            v0   = LA.subtract(CA1.coords(),CA0.coords())
            v1   = LA.subtract(CA1.coords(), CA3.coords())
            
            ti   = 57.295779513*(LA.angle(v0, v1))
            
            # dihedral 
            ai   = 57.295779513*(LA.dihedral(CA0.coords(), CA1.coords(), CA3.coords(), CA5.coords()))
            
            
            
            SS = None
            SS_char = None
            
            if 77.0 <= ti <= 101 and 30 <= ai <= 70:
                #print(CA1.resi, CA1.name, CA1.resn, CA1.name, 'H', d2i, d3i, d4i, ti,  ai)
                SS = 1
                SS_char = 'H'

            elif 5.0 <= d2i <= 6.0 and 4.8 <= d3i <= 5.8 and 5.8 <= d4i <= 7.0:
                SS = 1
                SS_char = 'H'
            
            elif 110.0 <= ti <= 138 and -215 <= ai <= -125:
                SS = 2
                SS_char = 'S'
            
            elif 6.1 <= d2i <= 7.3 and 9.0 <= d3i <= 10.8 and 11.3 <= d4i <= 13.5:
                SS = 1
                SS_char = 'S'
            
            '''
            if 5.0 <= d2i <= 6.0:
                #print('d2i', d2i)
                
                if 4.8 <= d3i <= 5.8:
                    #print('d3i', d3i)

                    if 5.8 <= d4i <= 7.0:
                        #print('d4i', d4i)

                        if 77.0 <= ti <= 101:
                            
                            if 30 <= ai <= 70:
                                print(CA1.resi, CA1.name, CA1.resn, CA1.name, 'H', d2i, d3i, d4i, ti,  ai)
                                SS = 'H'
      
                     
            if 6.1 <= d2i <= 7.3:
                #print('d2i', d2i)
                
                if 9.0 <= d3i <= 10.8:
                    #print('d3i', d3i)

                    if 11.3 <= d4i <= 13.5:
                        #print('d4i', d4i)

                        if 110.0 <= ti <= 138:
                            if -215 <= ai <= -125:
                                print(CA1.resi, CA1.name, CA1.resn, CA1.name, 'S', d2i, d3i, d4i, ti,  ai)
                                SS = 'S'
            '''
            
            if SS:
                pass
            else:
                SS = 0 
                SS_char = 'C'
            print(CA1.resi, CA1.name, CA1.resn, CA1.name, SS, d2i, d3i, d4i, ti,  ai)
            
            SSE_list += SS_char

            
    SSE_list += 'CCC'
    print(SSE_list, len(SSE_list))
    SSE_list = SSE_list.replace('CHCHC',  'CCCC')
    SSE_list = SSE_list.replace('CHC',  'CCC')
    SSE_list = SSE_list.replace('HCH',  'HHH')
    SSE_list = SSE_list.replace('CHS',  'CCS')

    SSE_list = SSE_list.replace('CHHC', 'CCCC')
    SSE_list = SSE_list.replace('CSSC', 'CCCC')
    SSE_list = SSE_list.replace('CSC',  'CCC')
    SSE_list = SSE_list.replace('HSH',  'HHH')
    SSE_list = SSE_list.replace('SHS',  'SSS')
    SSE_list = SSE_list.replace('CHSC',  'CCCC')
    print(SSE_list, len(SSE_list))
    
    
    SSE_list2     = []
    block         = [0,0,0]
    SS_before     = 'C'
    
    counter = 1
    for SS in SSE_list:
        
        if SS == SS_before:
            block[2] += 1
        else:
            SSE_list2.append(block)
            SS_before = SS
            print (block)
            
            if SS == "C":
                SS_code = 0
            
            elif SS == 'H':
                SS_code = 1
            
            else:
                SS_code = 2    
            
            block = [SS_code, counter-1, counter]
            
        counter += 1
    SSE_list2.append(block)
    print(SSE_list2)
    return SSE_list2 

















