from build123d import *
from math import cos, sin, tau
from itertools import pairwise

def sgn(a):
    return (-1 if a < 0 else
            +1 if a > 0 else 0)

def distances(n):
    return [ i / n for i in range(n) ]

def superpoint(a, b, e, theta):
    ( ct, st ) = ( cos(theta), sin(theta) )
    return ( a * sgn(ct) * abs(ct) ** (2/e),
             b * sgn(st) * abs(st) ** (2/e) )

def dpow(u, e):
    return 0 if u == 0 else e * abs(u) ** (e - 1)

def dsuperpoint(a, b, e, theta):
    ( ct, st ) = ( cos(theta), sin(theta) )
    return (( 0, 1 ) if theta == 0 else
            ( a * -st * dpow(ct, 2/e), b * +ct * dpow(st, 2/e) ))

def superellipse_spline(a, b, e, n):
    points = [ superpoint(a, b, e, d * (tau/4))
               for d in distances(n) ]
    # ensure that the quarter meets the y axis, because
    # the last distance is not accurate enough
    quarter = Spline(*points, (0,b), tangents=[(0,1),(-1,0)])
    half = quarter + mirror(quarter, Plane.YZ)
    return make_face(half + mirror(half, Plane.XZ))

def superellipse_lines(a, b, e, n):
    return make_face(Polyline(*[
        superpoint(a, b, e, d * tau)
        for d in distances(n)
    ], close=True))

def arrow(shaft):
    return Arrow(arrow_size = shaft.length/4, head_at_start = False,
                 shaft_width = shaft.length/16, shaft_path = shaft)

def normal_ray(curve, distance, length):
    point = curve @ distance
    normal = (curve % distance).rotate(Axis.Z, -90)
    return Line(point, point + normal * length)

width = 320
height = 256
thick = 8
inset = 16
ray = 64
expo = 5/2

def show_superellipse(fun, Q, n):
    squircle = fun(width - inset * Q, height - inset * Q, expo, n)
    show_object(extrude(squircle, thick * Q),
                options={"color": (255 - 51*Q,)*3})
    return squircle

show_superellipse(superellipse_lines, 2, 32)

splined = show_superellipse(superellipse_spline, 1, 32)
show_object([ normal_ray(splined.wire(), d, ray)
               for d in distances(128) ])

def super_arrow(a, b, e, theta):
    p = superpoint(a, b, e, theta)
    show_object(Location(p) * Box(1,1,1))
    t = Vector(dsuperpoint(a, b, e, theta)).normalized().rotate(Axis.Z, -90)
    show_object(arrow(Line(p, p+t*inset)))

[ super_arrow(width, height, expo, d*tau)
               for d in distances(128) ]
