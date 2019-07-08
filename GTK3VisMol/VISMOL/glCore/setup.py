from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules = cythonize("matrix_operations.pyx"))
setup(ext_modules = cythonize("sphere_representation.pyx"))

