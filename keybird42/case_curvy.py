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

main_x = 0
main_y = ku(-0.25)

main_width = ku(15)
keys_width = main_width + 2 * (ku(0.25) + ku(3))
keys_depth = ku(5)

middle_width = ku(8)

keys_y0 = main_y - keys_depth/2

corner_x = keys_width/2
corner_y = keys_y0 + ku(0.5)

front_x = middle_width/2
front_y = keys_y0 - ku(0.5)

side_w = ku(0.25)
side_x = corner_x + side_w
side_y = 0

assert side_x == ku(11)

show_marker((corner_x, corner_y))
show_marker((front_x, front_y))
show_marker((side_x, side_y))

show_object(Location((main_x, main_y)) * keycap_cutouts(), **rgba("3331"))

# find ellipse radii given displacement
# from point on axis to point on diagonal
def ellipse_radii_for_diagonal(a, b):
    v = b*b / (a - 2*b)
    return (a*a + a*v) ** 0.5, (a*v + v*v) ** 0.5

(e1_xr, e1_yr) = ellipse_radii_for_diagonal(
    corner_x - front_x, corner_y - front_y)

e1_xc = front_x
e1_yc = front_y + e1_yr

show_marker((e1_xc, e1_yc))

e1 = (EllipticalCenterArc((e1_xc, e1_yc), e1_xr, e1_yr, -90, 0)
      & Rectangle(corner_x * 2, ku(8)))

show_object(e1)
show_normal_tangent(e1, 1)

(e2_yr, e2_xr) = ellipse_radii_for_diagonal(
    side_y - corner_y, side_w)

e2_xc = side_x - e2_xr
e2_yc = side_y

show_marker((e2_xc, e2_yc))

e2 = (EllipticalCenterArc((e2_xc, e2_yc), e2_xr, e2_yr, -90, 90)
      & Location((corner_x + ku(1), 0)) * Rectangle(ku(2), ku(8)))
show_object(e2)
show_normal_tangent(e2, 0)
show_normal_tangent(e2, 1)

leftline = Line((0,0), (0,front_y)) + Line((0,front_y), (front_x,front_y))
outline = make_face(leftline + e1 + e2 + mirror(leftline + e1, Plane.XZ))
show_object(outline, **rgba("0c08"))


"""
e2cx = ku(10.5)
e2cy = ku(0)
e2xr = ku(0.5)

box((e2cx, e2cy))
box((e2cx+e2xr, e2cy))

e2 = EllipticalCenterArc(
    (e2cx, e2cy), e2xr,
    ellipse_x_radius(corner_y, corner_x, e2cy, e2cx, e2cx+e2xr),
    -90, +90)

e2 = e2 & (Location((ku(11.25),0)) * Rectangle(ku(1), ku(8)))

show_object(e2)

show_object(Line(e2 @ 0, e2 @ 0 + (e2 % 0).rotate(Axis.Z, 90) * 10))



total_width = ku(24)
middle_depth = ku(6)
middle_width = ku(10)
side_depth = ku(3)

front_diameter = ku(1)
rear_diameter = ku(2)

front_radius = front_diameter/2
rear_radius = rear_diameter/2
side_radius = front_radius * 2

side_stretch = side_radius / front_radius
stamp(f"{front_radius=}")
stamp(f"{side_radius=}")
stamp(f"{side_stretch=}")

front_y = -middle_depth/2
rear_y = +middle_depth/2
front_side_y = -side_depth/2
rear_side_y = -side_depth/2

rear_z = front_radius - rear_radius

side_x = total_width/2 - side_radius
side_y = side_depth/2

ellipse_xr = (side_x - middle_width/2) / side_stretch
ellipse_yr = (middle_depth - side_depth) / 2

typing_angle = atan2(rear_diameter - front_diameter, middle_depth)
stamp(f"{typing_angle=}")

front_section = make_face(ThreePointArc
                          ((0,front_y,+front_radius),
                           (0,front_y-front_radius,0),
                           (0,front_y,-front_radius))
                          + Line
                          ((0,front_y,-front_radius),
                           (0,front_y,+front_radius)))

rear_section = make_face(ThreePointArc
                         ((0, rear_y, rear_z + rear_radius),
                          (0, rear_y + rear_radius, rear_z),
                          (0, rear_y, rear_z - rear_radius))
                         + Line
                         ((0, rear_y, rear_z - rear_radius),
                          (0, rear_y, rear_z + rear_radius)))

side_section = Plane.XZ * make_face(
    EllipticalCenterArc(
        (side_x, 0),
        side_radius, front_radius,
        -90, +90)
    + Line(
        (side_x, -front_radius),
        (side_x, +front_radius)))


front_curve = sweep(front_section,
                    Line((-middle_width/2, front_y),
                         (+middle_width/2, front_y)))
rear_curve = sweep(rear_section,
                    Line((-middle_width/2, rear_y, rear_z),
                         (+middle_width/2, rear_y, rear_z)))
side_curve = sweep(side_section,
                    Line((side_x, -side_y),
                         (side_x, +side_y)))

show_object(front_curve)
show_object(rear_curve)
show_object(side_curve)

front_side_path = EllipticalCenterArc(
    (0, -side_y),
    ellipse_xr, ellipse_yr,
    -90, 0)

front_side_curve = Location((middle_width/2,0)) * scale(sweep(
    front_section, front_side_path), (side_stretch, 1, 1))

show_object(front_side_curve)

for i in range(10):
    p = front_side_path @ (i/10)
    x = p.X * side_stretch + middle_width/2
    show_object(Location((x, -p.Y, front_radius)) * Box(1,1,1))
"""
