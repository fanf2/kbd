from build123d import *
import cq_hacks
from cq_hacks import *
from keybird42 import *
import math
from monkeypatch_JernArc import *
from mx import *

def atan2(opposite, adjacent):
    return math.atan2(opposite, adjacent) * 360/math.tau

def subdiv(n):
    return [ i / n for i in range(n+1) ]

stamp("----------------------------------------------------------------")

set_view_preferences(line_width=1)

total_width = ku(24)
total_depth = ku(8)

main_y = ku(-0.25)

main_width = ku(15)
keys_width = main_width + 2 * (ku(0.25) + ku(3))
keys_depth = ku(5)

keys_y0 = main_y - keys_depth/2

front_r = ku(0.5)
front_x = ku(4)
front_y = keys_y0 - ku(0.5)

min_y = front_y - front_r
centre_y = min_y + total_depth/2

side_r = ku(1)
side_x = total_width/2 - side_r
side_w = ku(1/3)

rear_r = ku(0.9)
rear_x = ku(6)
rear_y = front_y - front_r + ku(8) - rear_r

corner_x = side_x - side_w
corner_y = keys_y0 + ku(1/3)

side_stretch = side_r / front_r

show_marker((corner_x, +corner_y))
show_marker((corner_x, -corner_y))
show_marker((front_x, front_y - front_r))
show_marker((front_x, front_y))
show_marker((rear_x, rear_y))
show_marker((rear_x, rear_y+rear_r))
show_marker((side_x, 0))

show_object(Location((0, main_y)) * keycap_cutouts(), **rgba("3333"))

show_object(Location((0, centre_y))
            * Rectangle(total_width, total_depth),
            **rgba("000c"))

typing_angle = atan2(rear_r*2 - front_r*2,
                     rear_y - front_y)
stamp(f"{typing_angle=}")

# find ellipse radii given displacement
# from point on axis to point on diagonal
def ellipse_radii_for_diagonal(a, b):
    v = b*b / (a - 2*b)
    return (a*a + a*v) ** 0.5, (a*v + v*v) ** 0.5

def RectangleAt(x, y, w, h):
    return Location((x + w/2, y + h/2)) * Rectangle(w, h)

def front_ellipse():
    width = corner_x - front_x
    height = corner_y - front_y
    (radius_x, radius_y) = ellipse_radii_for_diagonal(width, height)
    centre_x = front_x
    centre_y = front_y + radius_y
    return EllipticalCenterArc(
        (centre_x, centre_y), radius_x, radius_y, -90, 0
    ) & RectangleAt(front_x, front_y, width, height)

def rear_ellipse():
    width = corner_x - rear_x
    height = corner_y + rear_y
    (radius_x, radius_y) = ellipse_radii_for_diagonal(width, height)
    centre_x = rear_x
    centre_y = rear_y - radius_y
    return EllipticalCenterArc(
        (centre_x, centre_y), radius_x, radius_y, 0, -90
    ) & RectangleAt(rear_x, rear_y, width, -height)

def side_ellipse():
    height = -corner_y
    width = side_w
    (radius_y, radius_x) = ellipse_radii_for_diagonal(height, width)
    centre_x = side_x - radius_x
    centre_y = 0
    return EllipticalCenterArc(
        (centre_x, centre_y), radius_x, radius_y, -90, +90
    ) & RectangleAt(corner_x, corner_y, width, height*2)

def curve_section(path, t):
    pos = path @ t
    rot = -Vector(0,1,0).get_signed_angle(path % t)
    normal = (path % t).rotate(Axis.Z, -90)

    yt = (pos.Y - front_y) / (rear_y - front_y)
    z = front_r + yt * (rear_r - front_r)

    xt = (pos.X - front_x) / (side_x - front_x)
    if pos.Y >= 0: xt = 1
    xtt = max(0,xt)**6
    stamp((xt, xtt))
    r = min(front_r + xtt * (rear_r - front_r),
            pos.Y - min_y)

    # show_object(Location(pos) * Box(t+1,t+1,t+1))
    # show_object(Line(pos, pos + normal * r))
    # show_object(Line(pos, pos - (0, 0, 2*z)))

    semi = Plane.XZ * make_face(EllipticalCenterArc(
        (0,0), r, z, -90, +90
    ) + Line((0,-z), (0,+z)))
    return Location(pos - (0,0,z)) * Rotation(Z=rot) * semi

def side_curve(steps):
    path = front_ellipse() + side_ellipse() + rear_ellipse()

    sections = [ curve_section(path, i/steps)
                 for i in range(steps+1) ]
    #show_object(sections)

    show_object(extrude(sections[0], (path @ 0).X), **rgba("444"))

    for i in range(steps):
        t0 = ((i + 0) / steps)
        t1 = ((i + 1) / steps)
        p0 = path @ t0
        p1 = path @ t1
        n0 = (path % t0).rotate(Axis.Z, -90)
        n1 = (path % t1).rotate(Axis.Z, -90)
        clip = make_face(Polyline(p0-n0*ku(0.22), p0+n0*ku(2),
                                  p1+n1*ku(2), p1-n1*ku(0.22)))
        show_object(sweep([sections[i], sections[i+1]],
                          path & clip, multisection=True),
                     **rgba("444"))

    show_object(extrude(sections[-1], -(path @ 1).X), **rgba("444"))
    return

side_curve(5)
