"""superellipses and superellipsoids

Superellipses are a more sophisticated alternative to rounded
rectangles, with smoothly changing curvature. They are flexible
shapes that can be adjusted by changing the "exponent" to get a
result that varies between rectangular and elliptical, or from
square, through squircle, to circle, and beyond...

Superellipses can be found:

  * in typefaces such as Melior, Eurostyle, and Computer Modern

  * as the shape of airliner windows, tables, plates

  * clipping the outline of iOS app icons

They were named and popularized in the 1950s-1960s by the Danish
mathematician and poet Piet Hein, who used them in the winning
design for the Sergels Torg roundabout in Stockholm.

There are two complementary definitions of a superellipse, depending
on whether the author prefers [the implicit equation][enwp] or [the
parametric equation][bourke] (scroll down past the sportsball
section). In the implicit version, superellipses are ellipses when
`e = 2` and get more rectangular (hyperelliptical) for larger `e`,
and more pointy (hypoelliptical) for smaller `e`. In the parametric
version, superellipses are rectangles at `e = 0`, ellipses at `e =
1`, and pointy for larger `e`.

[enwp]: https://en.wikipedia.org/wiki/Superellipse
[bourke]: https://paulbourke.net/geometry/spherical/

This code uses the parametric form to draw superellipses. Its
purpose is mostly for hyperellipses with exponents `0 <= e <= 1`,
though it can draw hypoellipses too.

In the same way that ellipses are scaled circles, superellipses are
scaled squircles. Therefore this code only constructs squircles; the
result must be scaled to get a superellipse. Similarly in three
dimensions for superellipsoids.

We approximate a superellipse by dividing it into sectors, each of
which is drawn using a quadratic Bézier curve. Five sectors per
quarter is enough to get a good approximation. A quadratic Bézier
curve can be defined by the tangents at its end points; the
intersection of the tangents determines its control point.

A 3D superellipsoid is made from two orthogonal 2D superellipses,
with independent exponents. Every horizontal section (line of
latitude) through the superellipsoid has the same shape as the
horizontal superellipse, scaled so that it intersects the vertical
superellipse. Every vertical section through the vertical axis of
the superellipsoid (line of longitude) has the same shape as the
vertical superellipse, scaled so that it intersects the horizontal
superellipse at the superellipsoid's equator.

Piet Hein's superegg is a superellipsoid with horizontal exponent
xye = 1 (circular) and vertical exponent ze = 4/5, stretched so its
height is 6/5 of its width.

"""

from build123d import *
from collections import namedtuple
from cq_hacks import *
from math import cos, sin, tau

from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCP.Geom import Geom_BezierSurface
from OCP.Precision import Precision
from OCP.TColgp import TColgp_Array2OfPnt

# Default number of sectors per quadrant is DETAIL+2
DETAIL=3

def bezier_surface(points) :
    array = TColgp_Array2OfPnt(1, len(points), 1, len(points[0]))

    for i, row in enumerate(points):
        for j, p in enumerate(row):
            array.SetValue(i + 1, j + 1, Vector(p).to_pnt())

    bezier = Geom_BezierSurface(array)
    wrapped = BRepBuilderAPI_MakeFace(bezier, Precision.Confusion_s())
    return Face(wrapped.Face())

def mul(a, b):
    return a.X * b.Y - a.Y * b.X

# We want to make a quadratic Bézier curve from p0 to p1,
# with tangents t0 at p0 and t1 at p1. Its control point
# is at the intersection of the tangent lines.
def bezier_ctrl(p0, t0, p1, t1):
    (pt0, pt1) = (p0 + t0, p1 + t1)
    div = mul(t0, t1)
    m0 = mul(p0, pt0) / div
    m1 = mul(p1, pt1) / div
    return Vector(m1 * t0.X - m0 * t1.X,
                  m1 * t0.Y - m0 * t1.Y)

# In a squarish superellipse, the Bézier curves are too flat near
# the axes where there's a relatively large gap between points. For
# roundish superellipses the Bézier curves are not flat enough. The
# approximation is a lot closer to the superellipse if we add
# intermediate points in these gaps; empirically, 0.25 (for
# squarish) or 0.5 (for roundish) either side of each axis produces
# a more even spacing of points and good results as low as
# `DETAIL=3`
#
# Note this list excludes both endpoints, which are handled as
# special cases to ensure that superellipses are properly closed.
#
def quadrant_angles(e, n=DETAIL):
    ni = list(range(1, n))
    if e < 1: ni = [0.25] + ni + [n - 0.25]
    elif e < 2: ni = [0.5] + ni + [n - 0.5]
    return [ (tau / 4) * (i / n) for i in ni ]

# Calculates a point on the positive quadrant of a superellipse
def superpoint(e, 𝜃):
    return Vector(cos(𝜃) ** e, sin(𝜃) ** e)

# Calculus! The derivative of the superpoint equation.
def supertangent(e, 𝜃):
    (c, s, eʹ) = (cos(𝜃), sin(𝜃), e - 1)
    return Vector(-s * c ** eʹ, +c * s ** eʹ)

# Points on X and Y axes are special cases to ensure quadrants join
# up correctly. For small exponents, the tangents are perpendicular
# to the axes; for larger exponents, when the superellipse gets
# diamond shaped or more pointy, the tangents are along the axis.
#
# Calculates (point, tangent) pairs for a quadrant of a superellipse.
def superquadrant2(e):
    pt0 = (Vector(1,0), Vector(0,+1)) if e < 2 else (Vector(1,0), Vector(1,0))
    pt1 = (Vector(0,1), Vector(-1,0)) if e < 2 else (Vector(0,1), Vector(0,1))
    return [ pt0 ] + [ (superpoint(e, 𝜃), supertangent(e, 𝜃))
                       for 𝜃 in quadrant_angles(e) ] + [ pt1 ]

# Calculates [start point, control point, end point] triples
# describing the Bézier curve for each sector of a superellipse.
def superquadrant3(e):
    pt = superquadrant2(e)
    return [ [p0, bezier_ctrl(p0, t0, p1, t1), p1]
             for ((p0,t0),(p1,t1)) in zip(pt[:-1], pt[1:]) ]

def superellipse(e):
    curves = [ Bezier(*pcp) for pcp in superquadrant3(e) ]
    curves += [ curve.mirror(Plane.ZX) for curve in curves ]
    curves += [ curve.mirror(Plane.YZ) for curve in curves ]
    return make_face(curves)

def superellipsoid(xye, ze):
    patches = [ bezier_surface([ [
      (xy.X * z.X, xy.Y * z.X, z.Y)
        for xy in xypcp ]
          for z in zpcp ])
            for xypcp in superquadrant3(xye)
              for zpcp in superquadrant3(ze) ]
    patches += [ patch.mirror(Plane.ZX) for patch in patches ]
    patches += [ patch.mirror(Plane.XY) for patch in patches ]
    patches += [ patch.mirror(Plane.YZ) for patch in patches ]
    return Shell.make_shell(patches)

# for testing and experimentation
if __name__ != 'superellipse':

    set_view_preferences(line_width=0)

    N = 13
    blobs = []
    for xy in range(N):
        for z in range(N):
            stamp(f"{xy=} {z=}")
            blobs += [ Pos((xy*3 - N*3/2 + 3/2,
                            z*3 - N*3/2 + 3/2,
                            N*3 + 5))
                       * superellipsoid(0.1 + xy / 5,
                                        0.1 + z / 5) ]
    show_object(blobs, **rgba("73c"))

    for e in range(N):
        E = 0.09 + e / 5
        R = 10 + N - e
        stamp(f"{E=} {R=}")

        # piecewise linear version to compare accuracy of curves
        HIRES=64
        points = [ R * superpoint(E, (tau/4)*(i/HIRES)) for i in range(HIRES) ]
        points += [ Vector(-p.Y,p.X) for p in points ]
        points += reversed([ Vector(p.X,-p.Y) for p in points ])

        show_object(Pos((0,0,e*3+1)) *
                    extrude(make_face(Polyline(*points)), 1),
                    **rgba("aaa"))

        show_object(Pos((0,0,e*3))
                    * extrude(scale(superellipse(E), R), 1),
                    **rgba("666"))

        # break out the construction
        show = []
        pt = superquadrant2(E)
        for ((p0,t0),(p1,t1)) in zip(pt[:-1], pt[1:]):
            p0 = R * p0
            p1 = R * p1
            cp = bezier_ctrl(p0, t0, p1, t1)
            show += [ Pos(cp) * Box(.1,.1,.1),
                      Bezier(p0, cp, p1),
                      Line(p0, cp), Line(cp, p1), Line(p1, p0),
                      arrow(Line(p0, p0-t0.normalized())),
                      arrow(Line(p1, p1+t1.normalized())) ]
        show += [ thing.mirror(Plane.YZ) for thing in show ]
        show += [ thing.mirror(Plane.ZX) for thing in show ]
        show_object([ Pos((0,0,e*3+2)) * thing for thing in show ])
