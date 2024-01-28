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

# factors of 24
TOTAL_WIDTH = ku(24)
TOTAL_DEPTH = ku(8)
TOTAL_HEIGHT = ku(2)

# linear stretches
MIDDLE_WIDTH = ku(12)
MIDDLE_DEPTH = ku(4)

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

rear_curves = quarter + mirror(quarter, Plane.YZ)
front_curves = mirror(rear_curves, Plane.ZX)

unit_case = rear_curves + front_curves + Box(middle_x*2, middle_y*2, 2)


surface = scale(unit_case, ELLIPSOID_RADII)

show_object(surface)

print(f"{ELLIPSOID_RADII}")
