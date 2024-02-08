from build123d import *
from math import sin, cos, tau

def sgn(a):
    return (-1 if a < 0 else
            +1 if a > 0 else 0)

def superpoint(a, b, e, theta):
    (x, y) = (cos(theta), sin(theta))
    return (a * sgn(x) * abs(x)**(2/e), b * sgn(y) * abs(y)**(2/e))

def superpoints(a, b, e):
    precision = 60
    return [ superpoint(a, b, e, i * tau/precision)
             for i in range(precision + 1) ]

def superellipse_pouty(a, b, e):
    return Spline(*superpoints(a, b, e))

def superellipse_janky(a, b, e):
    return Spline(*superpoints(a, b, e),
                  tangents=[(0,1), (0,1)])

def superellipse_markers(a, b, e):
    for p in superpoints(a, b, e):
        show_object(Location(p) * Box(1,1,1))

show_object(Location((0,+200))
            * superellipse_pouty(400, 160, 6))

show_object(Location((0,-200))
            * superellipse_janky(400, 160, 6))
