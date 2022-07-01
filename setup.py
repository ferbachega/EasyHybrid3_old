#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright 2021 Carlos Eduardo Sequeiros Borja <carseq@amu.edu.pl>
#  

import numpy as np
from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension("glCore.matrix_operations",
              sources=["glCore/matrix_operations.pyx"],
              include_dirs=[np.get_include()]),
    Extension("vBabel.PDBFiles",
              sources=["vBabel/PDBFiles.pyx"],
              include_dirs=[np.get_include()]),
    Extension("vBabel.GROFiles",
              sources=["vBabel/GROFiles.pyx"],
              include_dirs=[np.get_include()]),
    Extension("vModel.cDistances",
              sources=["vModel/cDistances.pyx"],
              include_dirs=[np.get_include()]),
    Extension("vModel.VismolObject",
              sources=["vModel/VismolObject.pyx"],
              include_dirs=[np.get_include()]),
    Extension("vModel.Atom",
              sources=["vModel/Atom.pyx"],
              include_dirs=[np.get_include()])
]

setup(
    name="VisMol",
    ext_modules=cythonize(extensions),
)
