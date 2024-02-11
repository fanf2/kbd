from build123d import *
from math import cos, sin, tau
from itertools import pairwise

def distances(n):
    return [ i / n for i in range(n) ]

def sgn(a):
    return (-1 if a < 0 else
            +1 if a > 0 else 0)

def power(u, e):
    return max(2**-256, abs(u)) ** e

def superpoint(a, b, e, theta):
    ( ct, st ) = ( cos(theta), sin(theta) )
    return ( a * sgn(ct) * power(ct, 2/e),
             b * sgn(st) * power(st, 2/e) )

def supertangent(a, b, e, theta):
    ( ct, st ) = ( cos(theta), sin(theta) )
    return Vector( a * -st * power(ct, 2/e - 1),
                   b * +ct * power(st, 2/e - 1) ).normalized()

def superellipse_spline(a, b, e, n):
    points = [ superpoint(a, b, e, d * (tau/4))
               for d in distances(n//4) ]
    # ensure that the quarter meets the y axis, because
    # the last distance is not accurate enough
    quarter = Spline(*points, (0,b), tangents=[(0,1),(-1,0)])
    half = quarter + mirror(quarter, Plane.YZ)
    return make_face(half + mirror(half, Plane.XZ))

def superellipse_linear(a, b, e, n):
    return make_face(Polyline(*[
        superpoint(a, b, e, d * tau)
        for d in distances(n)
    ], close=True))

def triangle_apex(p0, t0, p1, t1):
    target_line = Line(p1, p1 - t1 * (p1-p0).length)
    return IntersectingLine(p0, t0, target_line) @ 1

def superellipse_bezier(a, b, e, n):
    pt = [ (Vector(superpoint(a, b, e, d * tau)),
            supertangent(a, b, e, d * tau)) for d in distances(n) ]
    curves = [ Bezier(p0, triangle_apex(p0, t0, p1, t1), p1)
               for ((p0,t0),(p1,t1)) in zip(pt, pt[1:] + pt[:1]) ]
    return make_face(curves)

detail = 16
expo = 5/2
width = 70
height = 60
thick = 1

def show_thing(Q, fun, n):
    thing = fun(width, height, expo, n)
    show_object(Location((0,0,thick*Q)) * extrude(thing, thick),
                options={"color": (255 - 51*Q,)*3})

show_thing(1, superellipse_spline, detail)
show_thing(2, superellipse_linear, 256)
show_thing(3, superellipse_bezier, detail)
show_thing(4, superellipse_linear, detail)
