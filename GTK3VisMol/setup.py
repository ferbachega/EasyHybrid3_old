#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright 2021 Carlos Eduardo Sequeiros Borja <carseq@amu.edu.pl>
#  

import numpy as np
from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension("VISMOL.glCore.matrix_operations",
              sources=["VISMOL/glCore/matrix_operations.pyx"],
              include_dirs=[np.get_include()]),
    Extension("VISMOL.glCore.sphere_representation",
              sources=["VISMOL/glCore/sphere_representation.pyx"],
              include_dirs=[np.get_include()]),
    Extension("VISMOL.vBabel.PDBFiles",
              sources=["VISMOL/vBabel/PDBFiles.pyx"],
              include_dirs=[np.get_include()]),
    Extension("VISMOL.vBabel.GROFiles",
              sources=["VISMOL/vBabel/GROFiles.pyx"],
              include_dirs=[np.get_include()]),
    Extension("VISMOL.vModel.cDistances",
              sources=["VISMOL/vModel/cDistances.pyx"],
              include_dirs=[np.get_include()]),
    Extension("VISMOL.vModel.VismolObject",
              sources=["VISMOL/vModel/VismolObject.pyx"],
              include_dirs=[np.get_include()])
]

setup(
    name="VisMol",
    ext_modules=cythonize(extensions),
)
