from build123d import *
from cq_hacks import stamp
from functools import cache
from itertools import pairwise
from math import cos, sin, tau

RESOLUTION = 16

def triangle_apex(p0, t0, p1, t1):
    target_line = Line(p1, p1 - t1 * (p1-p0).length)
    return IntersectingLine(p0, t0, target_line) @ 1

def vertex_ray(e1, e0, length):
    assert e1 @ 1 == e0 @ 0
    point = (e1 @ 1 + e0 @ 0) / 2
    tangent = (e1 % 1 + e0 % 0) / 2
    normal = tangent.rotate(Axis.Z, -90)
    return Line(point, point + normal * length)

def angles(n):
    return [ tau * i / n for i in range(n) ]

def sgn(a):
    return (-1 if a < 0 else
            +1 if a > 0 else 0)

def power(u, e):
    return max(2**-256, abs(u)) ** e

def superpoint(a, b, e, r):
    (c, s) = (cos(r), sin(r))
    return Vector(a * sgn(c) * power(c, 2/e),
                  b * sgn(s) * power(s, 2/e))

def supertangent(a, b, e, r):
    (c, s) = (cos(r), sin(r))
    return Vector(a * -s * power(c, 2/e - 1),
                  b * +c * power(s, 2/e - 1)).normalized()

def superellipse(a, b, e, resolution=RESOLUTION):
    pt = [ (superpoint(a, b, e, r),
            supertangent(a, b, e, r))
           for r in angles(resolution) ]
    return make_face([
        Bezier(p0, triangle_apex(p0, t0, p1, t1), p1)
        for ((p0, t0), (p1, t1))
        in zip(pt, pt[1:] + pt[:1]) ])

def superellipse_half(a, b, e, resolution=RESOLUTION):
    clip = Location((0, b/2)) * Rectangle(a*2, b)
    return superellipse(a, b, e, resolution) & clip

def superhalf_on_line(line, b, e, resolution=RESOLUTION):
    half = Plane.ZX * superellipse_half(b, line.length, e, resolution)
    return Location(line @ 0) * Rotation(Z=line.tangent_angle_at(0)) * half

def superellipsoid(inner, outer, h, e, resolution=RESOLUTION):
    [outer] = outer.faces() # extract the one face for its size
    length = max(outer.length, outer.width)
    sectors = inner.edges()
    rays = [ vertex_ray(sectors[i-1], sectors[i-0], length)
             for i in range(len(sectors)) ]
    normals = Wire() + rays & outer
    stamp("superellipse sections")
    # sections have to be faces; multisection does not work with paths
    sections = [ superhalf_on_line(normal, h, e, resolution)
                 for normal in normals ]
    # append the section at the end of the last edge
    sections += [sections[0]]
    stamp("superellipse sweep")
    # When we pass many sections into a single `sweep()`, it can end up using
    # near-infinite CPU. So instead we `sweep()` a pair of sections at a time.
    return [ extrude(inner, amount=h, both=True) ] + [
        sweep([sections[i+0], sections[i+1]], e, multisection=True)
        for i,e in enumerate(sectors) ]

def superegg_half(a, b, e, resolution=RESOLUTION):
    """Half a superellipse revolved halfway around the X axis"""
    return revolve(superellipse_half(a, b, e, resolution), Axis.X, 180)
