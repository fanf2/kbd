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

middle_width = ku(8)

keys_y0 = main_y - keys_depth/2

front_x = middle_width/2
front_y = keys_y0 - ku(0.5)
front_r = ku(0.5)

side_w = ku(0.4)
side_x = ku(11)
side_y = 0

corner_x = side_x - side_w
corner_y = keys_y0 + ku(0.25)

side_stretch = 2

show_marker((corner_x, corner_y))
show_marker((front_x, front_y))
show_marker((side_x, side_y))

show_object(Location((0, main_y)) * keycap_cutouts(), **rgba("3331"))

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

def side_ellipse():
    height = side_y - corner_y
    width = side_w
    (radius_y, radius_x) = ellipse_radii_for_diagonal(height, width)
    centre_x = side_x - radius_x
    centre_y = side_y
    return EllipticalCenterArc(
        (centre_x, centre_y), radius_x, radius_y, -90, 0
    ) & RectangleAt(corner_x, corner_y, width, height)

front_path = (Line((0, front_y), (front_x, front_y))
              + front_ellipse()
              + side_ellipse())

def front_curve():
    section = make_face(ThreePointArc(
        (0, front_y, +front_r),
        (0, front_y - front_r, 0),
        (0, front_y, -front_r)
    ) + Line(
        (0, front_y, -front_r),
        (0, front_y, +front_r)
    ))

    path = scale(front_path, (1/side_stretch, 1, 1))
    squashed = sweep(section, path.edges())

    return scale(squashed, (side_stretch, 1, 1))

def rear_curve():
    show_object(        EllipticalCenterArc(
            (0,0), ku(1.0), ku(1.0), 0, 180)
        + Line((-ku(1), 0), (+ku(1), 0)))


    start_section = Location((0, -front_y, -front_r/2)) * (Plane.ZY * make_face(
        EllipticalCenterArc(
            (0,0), ku(1.0), ku(1.0), 0, 180)
        + Line((-ku(1), 0), (+ku(1), 0))))
    show_object(start_section, **rgba("00c"))
    
    end_section = Plane.XZ * Location((side_x, side_y)) * make_face(
        EllipticalCenterArc(
            (0,0), ku(1.0), ku(0.5), -90, +90)
        + Line((0,-ku(0.5)), (0,+ku(0.5))))
    show_object(end_section, **rgba("0c0"))

    return sweep([start_section, end_section],
                 mirror(front_path, Plane.ZX).edges(),
                 multisection=True)

show_object(front_curve())

show_object(rear_curve())
