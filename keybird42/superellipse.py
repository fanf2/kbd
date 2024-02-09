# Written by Tony Finch <<dot@dotat.at>> in Cambridge
#
# Permission is hereby granted to use, copy, modify, and/or
# distribute this software for any purpose with or without fee.
#
# This software is provided 'as is', without warranty of any kind.
# In no event shall the authors be liable for any damages arising
# from the use of this software.
#
# SPDX-License-Identifier: 0BSD OR MIT-0

from build123d import *
from cq_hacks import stamp
from functools import cache
from itertools import pairwise
from math import cos, sin, tau

RESOLUTION = 256

def sgn(a):
    return (-1 if a < 0 else
            +1 if a > 0 else 0)

def arrow(shaft):
    return Arrow(arrow_size = shaft.length/4, head_at_start = False,
                 shaft_width = shaft.length/16, shaft_path = shaft)

def vertex_ray(e1, e0, length):
    assert e1 @ 1 == e0 @ 0
    point = (e1 @ 1 + e0 @ 0) / 2
    tangent = (e1 % 1 + e0 % 0) / 2
    normal = tangent.rotate(Axis.Z, -90)
    return Line(point, point + normal * length)

@cache
def superpoint(a, b, e, theta):
    ( x, y ) = ( cos(theta), sin(theta) )
    return ( a * sgn(x) * abs(x)**(2/e), b * sgn(y) * abs(y)**(2/e) )

@cache
def superellipse(a, b, e, resolution=RESOLUTION):
    return make_face(Polyline(*[
        superpoint(a, b, e, tau * i / resolution)
        for i in range(resolution)
    ], close=True))

@cache
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
    stamp(f"superellipse sections")
    # sections have to be faces; multisection does not work with paths
    sections = [ superhalf_on_line(normal, h, e, resolution)
                 for normal in normals ]
    # append the section at the end of the last edge
    sections += [sections[0]]
    # When we pass many sections into a single `sweep()`, it can end up using
    # near-infinite CPU. So instead we `sweep()` a pair of sections at a time.
    segments = [ extrude(inner, amount=h, both=True) ]
    for i,e in enumerate(sectors):
        if i % 50 == 0: stamp(f"superellipse sweep {i}")
        segments += [ sweep([sections[i+0], sections[i+1]], e, multisection=True) ]
    return segments

def superegg_half(a, b, e, resolution=RESOLUTION):
    """Half a superellipse revolved halfway around the X axis"""
    return revolve(superellipse_half(a, b, e, resolution), Axis.X, 180)
