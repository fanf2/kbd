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

set_view_preferences(line_width=0)

curve_steps = 13

total_width = ku(25)
total_depth = ku(7.5)
total_thick = ku(2)

desk_width = total_width + ku(12)
desk_depth = total_depth + ku(8)
desk_radius = ku(1)

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
side_w = ku(2/3)

rear_r = 16.666
rear_x = ku(6)
rear_y = front_y - front_r + total_depth - rear_r

corner_x = side_x - side_w
corner_y = keys_y0 + ku(1/2)

# this also determines the top cutout radius
keycap_clear = 0.5

assert total_thick > rear_r * 2

# show_marker((corner_x, +corner_y))
# show_marker((corner_x, -corner_y))
# show_marker((front_x, front_y - front_r))
# show_marker((front_x, front_y))
# show_marker((rear_x, rear_y))
# show_marker((rear_x, rear_y+rear_r))
# show_marker((side_x, 0))

typing_angle = atan2(rear_r*2 - front_r*2,
                     rear_y - front_y)
stamp(f"{typing_angle=}")

desk = (Location((0, front_y, -2*front_r)) *
        Rotation(X=-typing_angle) *
        Location((0, total_depth/2-front_r)) *
        RectangleRounded(desk_width, desk_depth, desk_radius))


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

def build_path():
    path = front_ellipse() + side_ellipse() + rear_ellipse()
    p0 = path @ 0
    p1 = path @ 1
    line0 = Line(p0, (0, p0.Y))
    line1 = Line(p1, (0, p1.Y))
    return line0 + path + line1

def curve_section(path, t):
    pos = path @ t
    rot = -Vector(0,1,0).get_signed_angle(path % t)
    normal = (path % t).rotate(Axis.Z, -90)

    yt = (pos.Y - front_y) / (rear_y - front_y)
    z = front_r + yt * (rear_r - front_r)

    xt = (pos.X - front_x) / (side_x - front_x)
    if pos.Y >= 0: xt = 1
    xtt = max(0,xt)**6
    r = min(front_r + xtt * (rear_r - front_r),
            pos.Y - min_y)

    # show_object(Location(pos) * Box(t+1,t+1,t+1))
    # show_object(Line(pos, pos + normal * r))
    # show_object(Line(pos, pos - (0, 0, 2*z)))

    semi = Plane.XZ * make_face(EllipticalCenterArc(
        (0,0), r, z, -90, +90
    ) + Line((0,-z), (0,+z)))
    return Location(pos - (0,0,z)) * Rotation(Z=rot) * semi

def build_curve(path, steps):
    sections = [ curve_section(path, i/steps)
                 for i in range(steps+1) ]
    #show_object(sections)

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
        curve += [segment, mirror(segment, Plane.YZ)]
    return curve

clip = extrude(desk, total_thick)

curve_path = build_path()

top_face = make_face(curve_path + mirror(curve_path, Plane.ZY))

top_sharpcut = extrude(offset(
    keycap_cutouts(), amount=keycap_clear, kind=Kind.INTERSECTION
), -7.5)

top_cutouts = (Location((0,main_y)) *
               fillet(top_sharpcut.edges() | Axis.Z, keycap_clear))

infill = extrude(top_face, -total_thick) - top_cutouts

# we need to clip the curve because it doesn't meet the desk at a
# perfect tangent: there's a discrepancy due to the typing angle

enclosure = clip & [infill] + build_curve(curve_path, curve_steps)

show_object(enclosure, **rgba("030303"))

keycaps = []
def show_keycap(keycap, legend, name):
    global keycaps
    keycaps += [ Location((0,main_y,-1)) * keycap ]

layout_keycaps(stamp, show_keycap, "simple", False)
show_object(keycaps, **rgba("111"))
