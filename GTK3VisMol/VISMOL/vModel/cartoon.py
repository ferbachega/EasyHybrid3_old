#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright 2021 Carlos Eduardo Sequeiros Borja <carseq@amu.edu.pl>
#  

import numpy as np

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

def cartoon(visObj, spline_detail=3):
    sd = spline_detail
    
    #calphas = np.loadtxt(calphas_file)
    visObj.get_backbone_indexes()
    calphas = []
    for atom in visObj.c_alpha_atoms:
        print(atom.index, atom.name, atom.resn, atom.resi, atom.coords())
        calphas.append(atom.coords())
    calphas = np.array(calphas, dtype = np.float32)
    print(calphas, type(calphas), len(calphas))
    spline = catmull_rom_spline(np.copy(calphas), calphas.shape[0], sd, strength = 0.9)
    # TODO: function to calculate the boundaries for secondary structures.
    # This list contains the indices of the residues that are alpha helices in
    # zero-based indexing.
    # secstruc = [(0, 0, 2), (1, 2, 13), (0, 13, 19), (1, 19, 33)]
    secstruc = [(0, 0, 1), (2,1,6), (0,6,11), (2,11,16), (0,16,21), (1,21,35),
                (0,35,40), (2,40,45), (0,45,55), (1,55,60), (0,60,65),
                (2,65,71), (0,71,74)]
    coords = np.zeros([1,3], dtype=np.float32)
    normals = np.zeros([1,3], dtype=np.float32)
    colors = np.zeros([1,3], dtype=np.float32)
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
