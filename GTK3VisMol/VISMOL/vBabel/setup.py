from distutils.core import setup
from Cython.Build import cythonize

setup(
    #ext_modules = cythonize("cfunctions.pyx")
    ext_modules = cythonize("PDBFiles.pyx")
)

'''
setup(
    #ext_modules = cythonize("cfunctions.pyx")
    ext_modules = cythonize("PDBFiles2.pyx")
)
'''

'''
setup(
    #ext_modules = cythonize("cfunctions.pyx")
    ext_modules = cythonize("cfunctions.pyx")
)
'''
