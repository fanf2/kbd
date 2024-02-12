"""superellipses and superellipsoids

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

This code uses the parametric form to draw hyperellipses with
exponents less than 1.

In the same way that ellipses are scaled circles, superellipses are
scaled squircles. Therefore this code only constructs squircles; the
result must be scaled to get a superellipse. Similarly in three
dimensions for superellipsoids.

We approximate a superellipse by dividing it into sectors. The
superellipse's parameter `theta` ranges from 0 to `tau`; each sector
is an equal subdivision of this range. (But not an equal subdivision
of the resulting superellipse owing to its exponent.)

We can calculate the tangents at the points between each sector of
the superellipse. These determine a quadratic Bézier for each
segment. We don't have to use too many segments to get a good enough
approximation to the superellipse.

"""

from build123d import *
from collections import namedtuple
from cq_hacks import *
from functools import cache
from math import cos, sin, tau

# Default number of sectors per quadrant is DETAIL+2
DETAIL=3

# The clamp here is helpful for testing
def power(u, e):
    return max(2**-256, abs(u)) ** e

def sgn(a):
    return (-1 if a < 0 else
            +1 if a > 0 else 0)

def mul(a, b):
    return a.X * b.Y - a.Y * b.X


# The Bézier curves are too flat near the axes where there's a
# relatively large gap between points. The approximation is a lot
# closer to a superellipse if we add intermediate points in these
# gaps; empirically, 0.25 either side of each axis produces a more
# even spacing of points and good results as low as `DETAIL=3`
#
# Note this list excludes both endpoints, which are handled as special
# cases to ensure that superellipses are properly closed.
@cache
def quadrant_angles(n):
    return [ (tau / 4) * (i / n)
             for i in [0.25] + list(range(1, n)) + [n-0.25] ]

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

def superpoint(e, 𝜃):
    (c, s) = (cos(𝜃), sin(𝜃))
    return Vector(sgn(c) * power(c, e),
                  sgn(s) * power(s, e))

def supertangent(e, 𝜃):
    (c, s) = (cos(𝜃), sin(𝜃))
    return Vector(-s * power(c, e - 1),
                  +c * power(s, e - 1))

# points on X and Y axes are special cases
def superquadrant(e, detail=DETAIL):
    pt = [ (Vector(1,0), Vector(0,1)) ] + [
        (superpoint(e, 𝜃), supertangent(e, 𝜃))
        for 𝜃 in quadrant_angles(detail)
    ] +  [ (Vector(0,1), Vector(-1,0)) ]
    return [ Bezier(p0, bezier_ctrl(p0, t0, p1, t1), p1)
             for ((p0,t0),(p1,t1)) in zip(pt[:-1], pt[1:]) ]

def superellipse(e, detail=DETAIL):
    quarter = superquadrant(e, detail)
    half = mirror(quarter, Plane.YZ) + quarter
    whole = mirror(half, Plane.ZX) + half
    result = make_face(whole)
    return result

# for testing and experimentation
if __name__ != 'superellipse':

    for e in range(10):
        E = (e + 1) / 10
        stamp(f"{E=}")
        R = 20 - e

        # piecewise linear version to compare accuracy of curves
        HIRES=256
        show_object(Pos((0,0,e*3+1)) * extrude(make_face(Polyline(*[
            R * superpoint(E, tau*i/HIRES) for i in range(HIRES)
        ], close=True)), 1), **rgba("aaa"))

        show_object(Pos((0,0,e*3))
                    * extrude(scale(superellipse(E), R), 1),
                    **rgba("666"))

        # go round the whole way instead of just one quarter
        quarter = [0] + quadrant_angles(DETAIL)
        theta = [ a + q * tau/4 for q in range(4) for a in quarter ]

        # break out the construction
        show = []
        for a0, a1 in zip(theta, theta[1:] + theta[:1]):
            p0 = R * superpoint(E, a0)
            p1 = R * superpoint(E, a1)
            t0 = supertangent(E, a0)
            t1 = supertangent(E, a1)
            cp = bezier_ctrl(p0, t0, p1, t1)
            show += [ Pos(cp) * Box(.1,.1,.1), Bezier(p0, cp, p1),
                      Line(p0, cp), Line(cp, p1), Line(p1, p0),
                      arrow(Line(p0, p0+t0.normalized())),
                      arrow(Line(p1, p1-t1.normalized())) ]
        show_object([ Pos((0,0,e*3+2)) * thing for thing in show ])

"""

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
    return revolve(superellipse_half(a, b, e, resolution), Axis.X, 180)

"""
