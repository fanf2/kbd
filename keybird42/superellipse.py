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

"""Superellipses and squircles

The shape is approximated using a spline. We draw just the positive
quadrant, and mirror it to make the complete notation. This avoids a
couple of problems:

  * The spline approximation tends to go wrong if we try to draw the
    whole superellipse as a single spline; a quarter is more reliable.

  * There's no need to use `abs()` and `sgn()` to cope with powers of
    negative numbers.

notation
--------

We use `a` and `b` for the `x` and `y` semi-axes

The exponent `e` controls the squareness: `e == 2` is circular, larger
is squarer; the Piet Hein superellipse has `e = 5/2`.

When generating a superellipse, the `resolution` is the number of
points used to generate the spline. By default the resolution is 60.

A "superhalf" is half a superellipse.

"""

from build123d import *
from math import cos, sin, tau

RESOLUTION = 32

def distances(resolution=RESOLUTION):
    return [ i / resolution for i in range(resolution + 1) ]

def superpoint(a, b, e, theta):
    """A point on the positive quadrant of a superellipse"""
    return ( a * cos(theta)**(2/e), b * sin(theta)**(2/e) )

def superpoints(a, b, e, resolution=RESOLUTION):
    """Points dividing the positive quadrant of a superellipse
    into `n` segments"""
    points = [ superpoint(a, b, e, d * (tau/4))
               for d in distances(resolution)[:-1] ]
    # ensure that the curve meets the y axis, because
    # the last distance is not accurate enough
    return points + [(0,b)]

def superquadrant_path(a, b, e, resolution=RESOLUTION):
    """A spline approximating the positive quadrant of a superellipse"""
    points = superpoints(a, b, e, resolution)
    return Spline(*points, tangents=[(0,1),(-1,0)])

def superhalf_path(a, b, e, resolution=RESOLUTION):
    """Half a superellipse above the X axis"""
    quadrant = superquadrant_path(a, b, e, resolution)
    return quadrant + mirror(quadrant, Plane.YZ)

def superellipse(a, b, e, resolution=RESOLUTION):
    """A face in the shape of a superellipse"""
    half = superhalf_path(a, b, e, resolution)
    return make_face(half + mirror(half, Plane.XZ))

def superhalf(a, b, e, resolution=RESOLUTION):
    """A face in the shape of half a superellipse above the X axis"""
    half = superhalf_path(a, b, e, resolution)
    return make_face(half + Line((-a,0), (+a,0)))

def superhalf_on_line(line, b, e, resolution=RESOLUTION):
    """Half a superellipse with a semi-axis described by a line
    in the XY plane; the b axis is vertical."""
    half = Plane.ZX * superhalf(b, line.length, e, resolution)
    return Location(line @ 0) * Rotation(Z=line.tangent_angle_at(0)) * half

def superegg_half(a, b, e, resolution=RESOLUTION):
    """Half a superellipse revolved halfway around the X axis"""
    return revolve(superhalf(a, b, e, resolution), Axis.X, 180)

def normal_ray(curve, distance, length):
    """A line extending from `curve @ distance`, perpendicular
    to the tangent according to the right hand rule"""
    point = curve @ distance
    normal = (curve % distance).rotate(Axis.Z, -90)
    return Line(point, point + normal * length)

def normal_rays(curve, length, resolution=RESOLUTION):
    return [ normal_ray(curve, d, length) for d in distances(resolution) ]

# When we pass many sections into a single `sweep()`, it can end up
# using near-infinite CPU. So instead we `sweep()` a pair of sections
# at a time.

def segments(curve, resolution=RESOLUTION):
    ds = distances(resolution)
    return [ curve.trim(*dz) for dz in zip(ds, ds[1:]) ]


#show_object(superegg_half(15, 10, 2.5))

inner = superellipse(40, 20, 2.5)
outer = superellipse(50, 25, 3.0)

inner_quadrant = inner.edges()[0]

normals = (Wire() + normal_rays(inner_quadrant, 1000)) & outer

show_object([ superhalf_on_line(normal, 5, 4)
              for normal in normals ])

show_object([ Arrow(arrow_size=seg.length/4, head_at_start=False,
                    shaft_width=seg.length/16, shaft_path=seg)
              for seg in segments(inner_quadrant) ])
