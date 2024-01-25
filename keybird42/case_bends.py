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

def sweep_arc(face, radius, angle, plane=Plane.XY):
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
BEND_RADIUS = (inner_radius + outer_radius) / 2

# minimum metal needed eash side of a bend
bend_grip = 7.1 - outer_radius

washer_thick = 1.5

magnet_thick = 4

pcba_thick = 4 # MX pin length plus clearance

plate_to_top = magnet_thick + washer_thick + THICK
pcb_to_plate = 5

base_inset = THICK / 3 # for appearance
base_clear = THICK / 3

# this also determines the top cutout radius
keycap_clearance = 0.5

TYPING_ANGLE_DIVISOR = 48
TYPING_ANGLE_DEGREES = 360 / TYPING_ANGLE_DIVISOR
TYPING_ANGLE_RADIANS = math.tau / TYPING_ANGLE_DIVISOR

CHIN_DEPTH = ku(1)
BROW_DEPTH = ku(2)

TOTAL_WIDTH = ku(24)
TOP_DEPTH = CHIN_DEPTH + KEYS_DEPTH + BROW_DEPTH
TOP_Y = BROW_DEPTH/2 - CHIN_DEPTH/2

plate_surround = ku(0.25)

assert plate_surround + MX_PLATE_RIB/2 > bend_grip

# at the spacebar stabilizer screws where clearance is tightest

datum_y = KEYS_DEPTH / 2
datum_z = pcba_thick + pcb_to_plate
datum_loc = (Rotation(X=TYPING_ANGLE_DEGREES) *
             Location((0, datum_y, datum_z)))

# all of these are centred on the middle of the key blocks

plate_width = KEYS_WIDTH + plate_surround*2
plate_depth = KEYS_DEPTH + plate_surround*2

plate_cutouts = thick(keyswitch_cutouts())
plate = datum_loc * (thick(Rectangle(plate_width, plate_depth)) - plate_cutouts)

top_sharpcut = thick(offset(
    keycap_cutouts(), amount=keycap_clearance, kind=Kind.INTERSECTION))
top_cutouts = fillet(top_sharpcut.edges() | Axis.Z, keycap_clearance)
top = datum_loc * Location((0,0,plate_to_top)) * (
    thick(Location((0,TOP_Y)) * Rectangle(TOTAL_WIDTH, TOP_DEPTH))
    - top_cutouts)

pcb = datum_loc * Location((0,0,-pcb_to_plate)) * kb42_pcba()

show_object(plate)
show_object(pcb)

top_front = top.faces().sort_by(Axis.Y)[0]
chin_arc = sweep_arc(
    top_front, BEND_RADIUS, +90 - TYPING_ANGLE_DEGREES, plane=Plane.YZ)
chin_top = chin_arc.faces().sort_by(Axis.Z)[0]
front_wall = sweep_line(chin_top, chin_top.center().Z + THICK)

top_rear = top.faces().sort_by(Axis.Y)[-1]
brow_arc = sweep_arc(
    top_rear, BEND_RADIUS, -90 - TYPING_ANGLE_DEGREES, plane=Plane.YZ)
brow_top = brow_arc.faces().sort_by(Axis.Z)[0]
rear_wall = sweep_line(brow_top, brow_top.center().Z + THICK)

top += [ chin_arc, front_wall, brow_arc, rear_wall ]

top = fillet(top.edges() << Axis.Z | Axis.Y, outer_radius)

show_object(top)

[base_front, base_rear] = [
    face.center() for face in top.faces() << Axis.Z > Axis.Y ]

base_front = base_front.Y + THICK/2 + base_clear
base_rear = base_rear.Y - THICK/2 - base_clear
base_depth = base_rear - base_front
base_width = TOTAL_WIDTH - base_inset*2 - outer_radius*2
base_y = base_rear/2 + base_front/2

base = Location((0,base_y)) * thick(Rectangle(base_width, base_depth))

show_object(base)
