from build123d import *
from keybird42 import *
import math
from mx import *

from monkeypatch_JernArc import *

def print_object(message, object):
    print(message)
    try: print(object.show_topology())
    except: print(f"{object}")

def LineBy(start, direction, length):
    return Line(start, start + (length / direction.length) * direction)

def sweep_arc(face, radius, angle, plane):
    return sweep(face, JernArc(
        face.center(), face.normal_at(), radius, angle, plane=plane))

def sweep_line(face, length):
    return sweep(face, LineBy(face.center(), face.normal_at(), length))

THICK = MX_PLATE_THICK

# thicken downwards from top surface
def thick(shape, amount=THICK):
    return extrude(shape, amount=-amount)

inner_radius = THICK # required by laserboost
outer_radius = inner_radius + THICK
bend_radius = (inner_radius + outer_radius) / 2

# minimum metal needed eash side of a bend
bend_grip = 7.1

washer_thick = 1.5

magnet_thick = 4

pcba_thick = 3.3 # MX pin length
pcba_clear = 1.2

plate_to_top = magnet_thick + washer_thick + THICK
pcb_to_plate = 5

base_inset = THICK / 3 # for appearance
base_clear = THICK / 3

# this also determines the top cutout radius
keycap_clearance = 0.5

TYPING_ANGLE_DIVISOR = 48
TYPING_ANGLE_DEGREES = 360 / TYPING_ANGLE_DIVISOR
TYPING_ANGLE_RADIANS = math.tau / TYPING_ANGLE_DIVISOR

# unscientific adjustment to make the height of the front and
# rear walls roughly match the depth of the chin and brow
fudge = 6
CHIN_DEPTH = ku(1) - fudge
BROW_DEPTH = ku(2) - fudge

TOTAL_WIDTH = ku(24)
TOP_DEPTH = CHIN_DEPTH + KEYS_DEPTH + BROW_DEPTH
TOP_Y = BROW_DEPTH/2 - CHIN_DEPTH/2

plate_surround = ku(0.25)

assert plate_surround + MX_PLATE_RIB/2 + outer_radius > bend_grip

# at the spacebar stabilizer screws where clearance is tightest

datum_y = KEYS_DEPTH / 2
datum_z = pcba_clear + pcba_thick + pcb_to_plate
datum_loc = (Rotation(X=TYPING_ANGLE_DEGREES) *
             Location((0, datum_y, datum_z)))

# pcb and plate are centred on the middle of the key blocks

pcb = datum_loc * Location((0,0,-pcb_to_plate)) * kb42_pcba()
show_object(pcb)

plate_width = KEYS_WIDTH + plate_surround*2
plate_depth = KEYS_DEPTH + plate_surround*2

plate_cutouts = thick(keyswitch_cutouts())
plate = datum_loc * (thick(Rectangle(plate_width, plate_depth)) - plate_cutouts)

# plate supports

plate_faces = plate.faces().sort_by(Axis.Y)

plate_chin = sweep_arc(plate_faces[0], bend_radius,
                       +90-TYPING_ANGLE_DEGREES, Plane.YZ)
plate_brow = sweep_arc(plate_faces[-1], bend_radius, -90, Plane.YZ)

front_hip = plate_chin.faces().sort_by(Axis.Z)[0]
front_leg = sweep_line(front_hip,
                       front_hip.center().Z - outer_radius - washer_thick)
front_ankle = front_leg.faces().sort_by(Axis.Z)[0]
front_heel = sweep_arc(front_ankle, bend_radius, -90, Plane.YZ)

hip_top = plate_chin.edges().filter_by(Axis.X).sort_by(Axis.Z)[-1].center().Z
foot_base = front_heel.edges().filter_by(Axis.X).sort_by(Axis.Z)[0].center().Z
print(f"{hip_top=}")
print(f"{foot_base=}")
print(f"{hip_top - foot_base=}")
print(f"{bend_grip=}")
assert hip_top - foot_base > bend_grip

plate += [ plate_brow, plate_chin, front_leg, front_heel ]

show_object(plate)

# the top has more of a brow so it needs an extra translation

top_sharpcut = thick(offset(
    keycap_cutouts(), amount=keycap_clearance, kind=Kind.INTERSECTION))
top_cutouts = fillet(top_sharpcut.edges() | Axis.Z, keycap_clearance)
top = datum_loc * Location((0,0,plate_to_top)) * (
    thick(Location((0,TOP_Y)) * Rectangle(TOTAL_WIDTH, TOP_DEPTH))
    - top_cutouts)

# add front and rear walls

top_faces = top.faces().sort_by(Axis.Y)
top_chin_arc = sweep_arc(top_faces[0], bend_radius,
                         +90-TYPING_ANGLE_DEGREES, Plane.YZ)
front_wall_top = top_chin_arc.faces().sort_by(Axis.Z)[0]
front_wall_height = front_wall_top.center().Z + THICK
front_wall = sweep_line(front_wall_top, front_wall_height)
print(f"{CHIN_DEPTH=}")
print(f"{front_wall_height=}")

top_brow_arc = sweep_arc(top_faces[-1], bend_radius,
                         -90-TYPING_ANGLE_DEGREES, Plane.YZ)
rear_wall_top = top_brow_arc.faces().sort_by(Axis.Z)[0]
rear_wall_height = rear_wall_top.center().Z + THICK
rear_wall = sweep_line(rear_wall_top, rear_wall_height)
print(f"{BROW_DEPTH=}")
print(f"{rear_wall_height=}")

top += [ top_chin_arc, front_wall, top_brow_arc, rear_wall ]

top = fillet(top.edges() << Axis.Z | Axis.Y, outer_radius)

show_object(top)

# base, without sides for now

[base_front, base_rear] = [
    face.center() for face in top.faces() << Axis.Z > Axis.Y ]

base_front = base_front.Y + THICK/2 + base_clear
base_rear = base_rear.Y - THICK/2 - base_clear
base_depth = base_rear - base_front
base_width = TOTAL_WIDTH - base_inset*2 - outer_radius*2
base_y = base_rear/2 + base_front/2

base = Location((0,base_y)) * thick(Rectangle(base_width, base_depth))

show_object(base)
