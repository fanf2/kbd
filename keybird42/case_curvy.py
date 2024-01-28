from build123d import *
from keybird42 import *
import math
from monkeypatch_JernArc import *
from mx import *

def atan2(opposite, adjacent):
    return math.atan2(opposite, adjacent) * 360/math.tau

def topo(obj):
    try: return obj.show_topology()
    except: return f"{obj}"

print("----------------------------------------------------------------")

THICK = 1.5
KEYCAP_CLEAR = 0.5

TYPING_ANGLE = 7
HALF_ANGLE = TYPING_ANGLE/2

# factors of 24
TOTAL_WIDTH = ku(24)
TOTAL_DEPTH = ku(8)
TOTAL_HEIGHT = ku(2)

# linear stretches
MIDDLE_WIDTH = ku(12)
MIDDLE_DEPTH = ku(2)

ELLIPSOID_X_RADIUS = (TOTAL_WIDTH - MIDDLE_WIDTH) / 2
ELLIPSOID_Y_RADIUS = (TOTAL_DEPTH - MIDDLE_DEPTH) / 2
ELLIPSOID_Z_RADIUS = TOTAL_HEIGHT/2
ELLIPSOID_RADII = (ELLIPSOID_X_RADIUS,
                   ELLIPSOID_Y_RADIUS,
                   ELLIPSOID_Z_RADIUS)

semi = (Circle(1) & Location((0.5, 0)) * Rectangle(1, 2))
semi_xz = Plane.XZ * semi
semi_yz = Plane.YZ * semi

middle_x = (MIDDLE_WIDTH/2) * (1/ELLIPSOID_X_RADIUS)
middle_y = (MIDDLE_DEPTH/2) * (1/ELLIPSOID_Y_RADIUS)

rear_curve = extrude(semi_yz, -middle_x)
right_curve = extrude(semi_xz, +middle_y)
corner_curve = revolve(semi_xz, Axis.Z, 90)

quarter = Location((middle_x, middle_y)) * (
    rear_curve + corner_curve + right_curve)

right_curves = quarter + mirror(quarter, Plane.XZ)
left_curves = mirror(right_curves, Plane.YZ)

unit_case = left_curves + Box(middle_x*2, middle_y*2, 2) # + right_curves

surface = scale(unit_case, ELLIPSOID_RADII)

print(f"{ELLIPSOID_RADII=}")

# z positions relative to top of plate

pcba_clear = 1.0
cavity_clear = ku(1/8)

upper_height = MX_UPPER_THICK #+ MX_KEYCAP_THICK
cavity_height = MX_LOWER_THICK - MX_PLATE_THICK + MX_PINS_THICK + pcba_clear

print(f"{upper_height=}")
print(f"{cavity_height=}")

cavity_outline = offset(kb42_pcb(), cavity_clear)

# xy position relative to front centre of space bar
holes = Location((0,MAIN_DEPTH/2)) * (
    extrude(keycap_cutouts(), upper_height) +
    extrude(keyswitch_cutouts(), -MX_PLATE_THICK) +
    Location((0,0,-MX_PLATE_THICK)) * extrude(cavity_outline, -cavity_height))

holes = Location((0,-ku(3.5), 0)) * Rotation(X=TYPING_ANGLE) * holes

show_object(surface - holes)
