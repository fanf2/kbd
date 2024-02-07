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

front_x = ku(4)
front_y = keys_y0 - ku(0.5)
front_r = ku(0.5)

centre_y = front_y - front_r + total_depth/2

side_r = ku(1)
side_x = total_width/2 - side_r
side_w = ku(1/3)

rear_r = ku(1.0)
rear_x = ku(6)
rear_y = front_y - front_r + ku(8) - rear_r
rear_z = front_r - rear_r

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

show_object(Location((0, centre_y, front_r))
            * Rectangle(total_width, total_depth),
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
    height = -corner_y
    width = side_w
    (radius_y, radius_x) = ellipse_radii_for_diagonal(height, width)
    centre_x = side_x - radius_x
    centre_y = 0
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

def smoothstep(t):
    return 3 * t**2 - 2 * t**3

def rear_section(path, t):
    eps = 0.2
    # the cad kernel gets into trouble if we try to specify the curve too precisely
    #s = 0 if t < eps else smoothstep((t - eps) / (1 - eps))
    s = smoothstep(t)
    z = (0, 0, s * rear_z)
    r = front_r - s * rear_z
    pos = path @ t + z
    rot = Vector(0,1,0).get_angle(path % t)
    show_object(Location(pos) * Box(t+1,t+1,t+1))
    semi = Plane.XZ * make_face(EllipticalCenterArc(
        (0,0), ku(1.0), r, -90, +90
    ) + Line((0,-r), (0,+r)))
    return Location(pos) * Rotation(Z=rot) * semi

def rear_curve():
    side_path = mirror(side_ellipse(), Plane.ZX).edges()
    corner_path = rear_ellipse()

    # the cad kernel goes AWOL if this is cranked up too much
    steps = 4
    sections = [ rear_section(corner_path, i/steps)
                 for i in range(steps+1) ]
    show_object(sections)
    stamp("sections")

    start_pos = (0, rear_y, rear_z)
    mid_pos = (rear_x, rear_y, rear_z)
    rear_curve = sweep(sections[-1], Line(start_pos, mid_pos))
    show_object(rear_curve, **rgba("4444"))
    stamp("rear")

    side_curve = sweep(sections[0], side_path)
    show_object(side_curve, **rgba("4444"))
    stamp("side")

    corner_curve = sweep(sections, corner_path, multisection=True)
    show_object(corner_curve, **rgba("4444"))
    stamp("corner")

    return

show_object(front_curve(), **rgba("4444"))
stamp("front")

rear_curve()
