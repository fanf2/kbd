from build123d import *
from cq_hacks import *
from keybird42 import *
import math
from monkeypatch_JernArc import *
from mx import *

def atan2(opposite, adjacent):
    return math.atan2(opposite, adjacent) * 360/math.tau

stamp("----------------------------------------------------------------")

set_view_preferences(line_width=1)

show_object(keycap_cutouts(), **rgba("3331"))

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

# make a bad guess at the path then move its starting point to the right place
x = (side_x - middle_width/2) / side_stretch
y = rear_y - side_y
rear_side_path = Rotation(X=-45) * CenterArc((0,0), y, 90,-90)

# the Z position ends up completely wrong if I stretch in one stage
rear_side_path = scale(rear_side_path, (x / (rear_side_path @ 1).X, 1, 1))
rear_side_path = scale(rear_side_path, (1, y / (rear_side_path @ 0).Y, 1))
rear_side_path = scale(rear_side_path, (1, 1, rear_z / (rear_side_path @ 0).Z))

# turn the path back into a simple edge
rear_side_path = rear_side_path.edges()[0]

rear_side_start_section = (Location(rear_side_path @ 0)
                           * Location((0,-rear_y,-rear_z))
                           * rear_section)

rear_side_end_section = (Location(rear_side_path @ 1)
                         * Rotation(Z=90)
                         * Location((0,-front_y))
                         * front_section)

rear_side_curve = Location((middle_width/2,+side_y)) * scale(sweep([
     rear_side_start_section, rear_side_end_section
], rear_side_path, multisection=True), (side_stretch, 1, 1))

show_object(rear_side_curve)
