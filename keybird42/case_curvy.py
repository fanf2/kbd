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

main_y = ku(-0.125)

main_width = ku(15)
keys_width = main_width + 2 * (ku(0.25) + ku(3))
keys_depth = ku(5)

keys_y0 = main_y - keys_depth/2

front_x = ku(4)
front_y = keys_y0 - ku(0.5)
front_r = ku(0.5)

rear_x = ku(6)
rear_y = -front_y
rear_r = ku(1.0)
rear_z = front_r - rear_r

side_w = ku(0.4)
side_x = ku(11)
side_y = 0

corner_x = side_x - side_w
corner_y = keys_y0 + ku(0.25)

side_stretch = 2

show_marker((corner_x, corner_y))
show_marker((front_x, front_y))
show_marker((rear_x, rear_y))
show_marker((side_x, side_y))

show_object(Location((0, main_y)) * keycap_cutouts(), **rgba("3333"))

show_object(Location((0, 0, front_r))
            * Rectangle(ku(24), ku(8)),
            **rgba("cccc"))

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
    height = side_y - corner_y
    width = side_w
    (radius_y, radius_x) = ellipse_radii_for_diagonal(height, width)
    centre_x = side_x - radius_x
    centre_y = side_y
    return EllipticalCenterArc(
        (centre_x, centre_y), radius_x, radius_y, -90, 0
    ) & RectangleAt(corner_x, corner_y, width, height)


def front_curve():
    path = (Line((0, front_y), (front_x, front_y))
            + front_ellipse()
            + side_ellipse())

    section = make_face(ThreePointArc(
        (0, front_y, +front_r),
        (0, front_y - front_r, 0),
        (0, front_y, -front_r)
    ) + Line(
        (0, front_y, -front_r),
        (0, front_y, +front_r)
    ))

    squashed_path = scale(path, (1/side_stretch, 1, 1))
    squashed_curve = sweep(section, squashed_path.edges())

    return scale(squashed_curve, (side_stretch, 1, 1))

def rear_curve():
    rear_semi = Plane.ZY * make_face(EllipticalCenterArc(
        (0,0), ku(1.0), ku(1.0), 0, 180
    ) + Line((-ku(1), 0), (+ku(1), 0)))

    side_semi = Plane.XZ * make_face(EllipticalCenterArc(
        (0,0), ku(1.0), ku(0.5), -90, +90
    ) + Line((0,-ku(0.5)), (0,+ku(0.5))))

    start_pos = (0, rear_y, rear_z)
    start_section = Location(start_pos) * rear_semi

    mid_pos = (rear_x, rear_y, rear_z)
    mid_section = Location(mid_pos) * rear_semi

    rear_curve = sweep(start_section, Line(start_pos, mid_pos))
    show_object(rear_curve, **rgba("4444"))

    end_section = Location((corner_x, -corner_y)) * Rotation(Z=45) * side_semi
    side_curve = sweep(end_section, mirror(side_ellipse(), Plane.ZX).edges())
    show_object(side_curve, **rgba("4444"))

    corner_path = rear_ellipse()
    show_object(corner_path)

    corner_curve = sweep([mid_section, end_section],
                         corner_path, multisection=True)
    show_object(corner_curve, **rgba("4444"))

    return

show_object(front_curve(), **rgba("4444"))

rear_curve()
