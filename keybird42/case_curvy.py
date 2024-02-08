from build123d import *
import cq_hacks
from cq_hacks import *
from keybird42 import *
import math
from monkeypatch_JernArc import *
from mx import *

def sgn(a):
    return (-1 if a < 0 else
            +1 if a > 0 else 0)

def atan2(opposite, adjacent):
    return math.atan2(opposite, adjacent) * 360/math.tau

def subdiv(n):
    return [ i / n for i in range(n+1) ]

def fractions(n):
    return map(lambda i: i/n, range(n+1))

stamp("------------------------------------------")

set_view_preferences(line_width=1)

resolution = 60

main_y = ku(-0.125)
main_width = ku(15)
keys_width = main_width + 2 * (ku(0.25) + ku(3))
keys_depth = ku(5)

radius_x = ku(1.00)
radius_y = ku(0.75)
radius_z = ku(0.50)

top_a = ku(11)
top_b = ku(2.75)

# empirically enough to fit around the key blocks
top_e = 8

# empirically enough to ensure the side radius
# does not bulge downwards before curving upwards
radius_e = 10

# purely aesthetic
side_e = 3

# this also determines the top cutout radius
keycap_clear = 0.5

desk_a = ku(16)
desk_b = ku(8)
desk_e = 3

typing_angle = 6.6666

# positive quadrant only
def superpoint(a, b, e, theta):
    return ( a * cos(theta)**(2/e), b * sin(theta)**(2/e) )

def superpoints(a, b, e, n):
    points = [ superpoint(a, b, e, (i/n) * (math.tau/4))
               for i in range(n) ]
    # ensure that the curve meets the y axis, because iterating
    # an extra step `range(n + 1)` is not exact enough
    return points + [(0,b)]

def superquarter(a, b, e):
    points = superpoints(a, b, e, resolution)
    return Spline(*points, tangents=[(0,1),(-1,0)])

def superellipse(a, b, e):
    # splines get pouty or janky if we try to draw the whole
    # superellipse in one go, so make a quarter and mirror it
    quarter = superquarter(a, b, e)
    half = quarter + mirror(quarter, Plane.YZ)
    whole = half + mirror(half, Plane.XZ)
    return make_face(whole).faces()[0]

def side_section(path, t):
    pos = path @ t
    rot = -Vector(0,1).get_signed_angle(path % t)

    xt = (pos.X / top_a) ** radius_e
    r = radius_y + (radius_x - radius_y) * xt

    section = Plane.XZ * (superellipse(r, radius_z, side_e)
                          & Location((r,0)) * Rectangle(r*2, radius_z*2))

    return Location(pos) * Rotation(Z=rot) * section

def build_sides(path, steps):
    sections = [ side_section(path, i/steps)
                 for i in range(steps+1) ]

    curve = []
    for i in range(steps):
        t0 = ((i + 0) / steps)
        t1 = ((i + 1) / steps)
        p0 = path @ t0
        p1 = path @ t1
        n0 = (path % t0).rotate(Axis.Z, -90)
        n1 = (path % t1).rotate(Axis.Z, -90)
        clip = make_face(Polyline(p0-n0*ku(0.22), p0+n0*ku(2),
                                  p1+n1*ku(2), p1-n1*ku(0.22)))
        segment = sweep([sections[i], sections[i+1]],
                        path & clip, multisection=True)
        flipped = mirror(segment, Plane.ZX)
        flopped = mirror(flipped, Plane.YZ)
        flapped = mirror(flopped, Plane.ZX)
        curve += [segment, flipped, flopped, flapped]
    return curve

infill = extrude(superellipse(top_a, top_b, top_e), radius_z, both=True)

top_sharpcut = extrude(offset(
    keycap_cutouts(), amount=keycap_clear, kind=Kind.INTERSECTION
), -7.5)

top_cutouts = (Location((0, main_y, radius_z)) *
               fillet(top_sharpcut.edges() | Axis.Z, keycap_clear))
show_object(infill - top_cutouts, **rgba("111"))

desk = (Location((0, 0, -ku(0.85))) *
        Rotation(X=-typing_angle) *
        superellipse(desk_a, desk_b, desk_e))

foot = []
for i in range(-2, 3):
    a = top_a - i * ku(0.25)
    b = top_b - i * ku(0.125)
    z = ku(0.875) + i * ku(0.125)
    foot += [extrude(superellipse(a, b, top_e), -z)]

foot = extrude(desk, ku(2)) & foot
show_object(foot, **rgba("111"))

show_object(desk, **rgba("ccc"))

show_object(build_sides(superquarter(top_a, top_b, top_e), 20), **rgba("111"))

keycaps = []
def show_keycap(keycap, legend, name):
    global keycaps
    keycaps += [ Location((0,main_y,radius_z-1)) * keycap ]
layout_keycaps(stamp, show_keycap, "simple", False)
show_object(keycaps, **rgba("222"))
