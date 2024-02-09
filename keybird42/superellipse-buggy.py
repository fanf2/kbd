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

def spline_pouty(points):
    return Spline(*points)

def spline_janky(points):
    return Spline(*points, tangents=[(0,1), (0,1)])

def markers(points):
    return Part()+[ Location(p) * Box(1,1,1) for p in points ]

points = superpoints(400, 160, 6)

show_object(Location((0,+200)) * spline_pouty(points))
show_object(Location((0,-200)) * spline_janky(points))

show_object(Location((0,+200)) * markers(points))
show_object(Location((0,-200)) * markers(points))
