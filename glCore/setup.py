#from distutils.core import setup
#from Cython.Build import cythonize
#import numpy
#
#setup(ext_modules = cythonize("matrix_operations.pyx"), include_dirs=[numpy.get_include()])
#setup(ext_modules = cythonize("sphere_representation.pyx"), include_dirs=[numpy.get_include()])
#
from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(ext_modules = cythonize("matrix_operations.pyx"), include_dirs=[numpy.get_include()])
#setup(ext_modules = cythonize("sphere_representation.pyx"), include_dirs=[numpy.get_include()])
