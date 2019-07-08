"""
    This file is part of emol!.

    emol! is slideshow capable molecule viewing program.
    Copyright (C) 2008  Erik Thompson

    emol! is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    emol! is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with emol!.  If not, see <http://www.gnu.org/licenses/>.

    A copy of the license is found in the included file called: gpl-3.0.txt
    My contact information is available in the file called: contact.txt

---------------------------------------------------------------------------
    Portions of this program were copied from example code found on web pages
    or in the documentation of the programming libraries themselves.  I
    believe these examples are legal for me to use, but if someone owns the
    copyright and objects to my use of the code then please let me know
    which lines of code for which you own the copyright and I will either
    rewrite those lines of code or remove them from my program.  See the
    file contributors.txt to find the relevent links and/or author names.
---------------------------------------------------------------------------    
"""
import math


class Vector(object):
    """ class to load all the molecules in a .pdb file """
    def __init__(self):
        pass

    def add(self, a, b):
        """ vector a plus vector b = resulting vector """
        result = [a[0] + b[0], a[1] + b[1], a[2] + b[2]]
        return result

    def subtract(self, a, b):
        """ vector a minus vector b = resulting vector vector """
        result = [a[0] - b[0], a[1] - b[1], a[2] - b[2]]
        return result

    def multiply(self, scalar, vector):
        """ multiply a vector by a scalar """
        result = [scalar * vector[0], scalar * vector[1], scalar * vector[2]]
        return result

    def dotproduct(self, a, b):
        """ take the dot product of two vectors: a . b """
        result = a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
        return result

    def crossproduct(self, a, b):
        """ take the cross product of two vectors: a X b """
        cross = [0,0,0]
        cross[0] = a[1] * b[2] - a[2] * b[1]
        cross[1] = a[2] * b[0] - a[0] * b[2]
        cross[2] = a[0] * b[1] - a[1] * b[0]
        result = cross
        return result

    def mag(self, a):
        """ return the magnitude (length) of a vector """
        result = (a[0]**2 + a[1]**2 + a[2]**2)**(0.5)
        return result

    def normalize(self, a):
        """ convert a vector to a unit vector (length of 1) """
        magnitude = self.mag(a)
        result = [a[0]/magnitude, a[1]/magnitude, a[2]/magnitude]
        return result

    def angle(self, a, b):
        """ angle in degrees between two vectors """
        result = math.acos(self.dotproduct(a,b) / (self.mag(a)* self.mag(b))) # radians
        result = result * (180 / math.pi) # degrees
        return result
                        

if __name__ == '__main__':
    a = [1,2,3]
    b = [3,4,5]

    v = Vector()
    print ("Adding:"                                )
    print ("%s + %s = %s\n" % (a,b,v.add(a,b))      )
    print ("Subtracting"                            )
    print ("%s - %s = %s\n" % (a,b,v.subtract(a,b)) )
    print ("Multiplying a vector by a scalar"       )
    scalar = 2
    print ("%s * %s = %s\n" % (scalar,a,v.multiply(scalar,a))                            )
    print ("Taking the Dot Product of two vectors"                                       )
    print ("%s . %s = %s\n" % (a,b,v.dotproduct(a,a))                                    )
    print ("Taking the Cross Product of two vectors"                                     )
    print ("%s X %s = %s\n" % (a,v.scale(-1,a),v.crossproduct(a,v.scale(-1,a)))          )
    print ("Calculating the magnitude of a vector"                                       )
    print ("mag(%s) = %s\n" % (a,v.mag(a))                                               )
    print ("Normalizing a vector (i.e. converting it to a unit vector)"                  )
    print ("unit(%s) = %s\n" % (a,v.unit(a))                                             )
    print ("The angle between two vectors"                                               )
    print ("angle(%s,%s) = %.1f degrees\n" % (a,v.scale(-1,a),v.angle(a,v.scale(-1,a)))  )

    print ("-------------------------------------------\n")
    a = [1,0,0]
    b = [0,1,0]                                                                              
    print ("Starting from %s to get to %s:" % (a, b)                                         )
    print ("Rotate: %.1f degrees about the %s axis\n" % (v.angle(a, b), v.crossproduct(a, b)))
