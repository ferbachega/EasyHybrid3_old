from distutils.core import setup
from Cython.Build import cythonize

setup(
    #ext_modules = cythonize("cfunctions.pyx")
    ext_modules = cythonize("VismolObject.pyx")
)


setup(
    #ext_modules = cythonize("cfunctions.pyx")
    ext_modules = cythonize("cDistances.pyx")
)

