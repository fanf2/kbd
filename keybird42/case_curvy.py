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

TYPING_ANGLE = 7.5
CASE_ANGLE = 10

# factors of 24
TOTAL_WIDTH = ku(24)
TOTAL_DEPTH = ku(8)
TOTAL_HEIGHT = ku(2)

# linear stretches
MIDDLE_WIDTH = ku(12)
MIDDLE_DEPTH = ku(4)

PENREST_RADIUS = ku(0.25)
PENREST_WIDTH = ku(12)

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

unit_case = left_curves + Box(middle_x*2, middle_y*2, 2) + right_curves

surface = scale(unit_case, ELLIPSOID_RADII)

print(f"{ELLIPSOID_RADII=}")

# form a wedge

clip_width = TOTAL_WIDTH + ku(1)
clip_depth = TOTAL_DEPTH + ku(2)
clip_height = ku(3/8)

clip_top = (Location((0, -clip_depth/2, clip_height))
            * Rotation(X=CASE_ANGLE/2)
            * Location((0, +clip_depth/2, 0))
            * Rectangle(clip_width, clip_depth))

clip_base = mirror(clip_top, Plane.XY)
clip = loft([clip_base, clip_top])

print(f"{topo(clip_top.location)}")

# z positions relative to top of case

main_y = -ku(3/8)
main_z = ku(1)

pcba_clear = 1.0
cavity_clear = ku(1/8)
cavity_height = MX_LOWER_THICK - MX_PLATE_THICK + MX_PINS_THICK + pcba_clear
cavity_outline = offset(kb42_pcb(), cavity_clear)

upper_height = MX_UPPER_THICK + MX_KEYCAP_THICK # more than enough

holes = (Location((0, main_y, main_z))
         * Rotation(X=TYPING_ANGLE - CASE_ANGLE/2)
         * (Location((0,main_y,0))
            * extrude(keycap_cutouts(), -upper_height) +
            Location((0,main_y,-upper_height))
            * extrude(keyswitch_cutouts(), -MX_PLATE_THICK) +
            Location((0,main_y,-upper_height-MX_PLATE_THICK))
            * extrude(cavity_outline, -cavity_height)))

penrest_y = MIDDLE_DEPTH/2 + PENREST_RADIUS
penrest_z = TOTAL_HEIGHT/2 + PENREST_RADIUS/2
penrest = (
    Location((0, penrest_y, penrest_z)) *
    (Plane.YZ * Cylinder(PENREST_RADIUS, PENREST_WIDTH)))

penrest += (Location((+PENREST_WIDTH/2, penrest_y, penrest_z))
            * Sphere(PENREST_RADIUS) +
            Location((-PENREST_WIDTH/2, penrest_y, penrest_z))
            * Sphere(PENREST_RADIUS, rotation=(0,0,180)))

show_object((surface & clip) - (penrest + holes))
