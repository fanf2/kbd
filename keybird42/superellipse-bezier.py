from build123d import *
from math import cos, sin, tau, pow
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
    return e * pow(abs(u), e-1)

def supertangent(a, b, e, theta):
    ( ct, st ) = ( cos(theta), sin(theta) )
    return (Vector( 0, 1 ) if theta == 0 else
            Vector( a * -st * dpow(ct, 2/e),
                    b * +ct * dpow(st, 2/e) ).normalized())

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

def triangle_apex(p0, t0, p1, t1):
    target_line = Line(p1, p1 - t1 * (p1-p0).length)
    return IntersectingLine(p0, t0, target_line) @ 1

def superellipse_bezier(a, b, e, n):
    pt = [ (Vector(superpoint(a, b, e, d * tau)),
            supertangent(a, b, e, d * tau)) for d in distances(n) ]
    curves = [ Bezier(p0, triangle_apex(p0, t0, p1, t1), p1)
               for ((p0,t0),(p1,t1)) in zip(pt, pt[1:] + pt[:1]) ]
    return make_face(curves)

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

show_superellipse(superellipse_lines, 3, 32)

show_superellipse(superellipse_bezier, 2, 32)

splined = show_superellipse(superellipse_spline, 1, 32)
show_object([ normal_ray(splined.wire(), d, ray)
               for d in distances(128) ])

def super_arrow(a, b, e, theta):
    p = superpoint(a, b, e, theta)
    t = supertangent(a, b, e, theta)
    n = t.rotate(Axis.Z, -90)
    return arrow(Line(p, p+n*ray))

show_object([ super_arrow(width, height, expo, d*tau)
               for d in distances(32) ])
