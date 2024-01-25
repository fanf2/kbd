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

TYPING_ANGLE_DIVISOR = 48
TYPING_ANGLE_DEGREES = 360 / TYPING_ANGLE_DIVISOR
TYPING_ANGLE_RADIANS = math.tau / TYPING_ANGLE_DIVISOR

CHIN_DEPTH = ku(1)
BROW_DEPTH = ku(1)
FOREHEAD_DEPTH = ku(3)

TOTAL_WIDTH = ku(24)

# provisional
TOTAL_DEPTH = CHIN_DEPTH + KEYS_DEPTH + BROW_DEPTH + FOREHEAD_DEPTH

THICK = MX_PLATE_THICK

# thicken downwards from top surface
def thick(shape, amount=THICK):
    return extrude(shape, amount=-amount)

inner_radius = THICK # required by laserboost
outer_radius = inner_radius + THICK
BEND_RADIUS = (inner_radius + outer_radius) / 2

# minimum metal needed eash side of a bend
bend_grip = 7.1 - THICK - inner_radius

washer_thick = 1.5

magnet_thick = 4

pcba_thick = 4 # MX pin length plus clearance

plate_to_top = magnet_thick + washer_thick + THICK
pcb_to_plate = 5

side_inset = THICK / 3 # for appearance

# this also determines the top cutout radius
keycap_clearance = 0.5

plate_surround = ku(0.25)

assert plate_surround + MX_PLATE_RIB/2 > bend_grip

# at the spacebar stabilizer screws where clearance is tightest

datum_y = KEYS_DEPTH / 2
datum_z = pcba_thick + pcb_to_plate

datum_loc = (Location((0, 0, datum_z)) *
             Rotation(X=TYPING_ANGLE_DEGREES) *
             Location((0, datum_y, 0)))

# all of these are centred on the middle of the key blocks

plate_width = KEYS_WIDTH + plate_surround*2
plate_depth = KEYS_DEPTH + plate_surround*2

top_width = TOTAL_WIDTH
top_depth = CHIN_DEPTH + KEYS_DEPTH + BROW_DEPTH

plate_cutouts = thick(keyswitch_cutouts())
plate = datum_loc * (thick(Rectangle(plate_width, plate_depth)) - plate_cutouts)

top_sharpcut = thick(offset(
    keycap_cutouts(), amount=keycap_clearance, kind=Kind.INTERSECTION))
top_cutouts = fillet(top_sharpcut.edges() | Axis.Z, keycap_clearance)
top = datum_loc * Location((0,0,plate_to_top)) * (
    thick(Rectangle(top_width, top_depth)) - top_cutouts)

pcb = datum_loc * Location((0,0,-pcb_to_plate)) * kb42_pcba()

show_object(plate)
show_object(top)
show_object(pcb)

plate_front = plate.faces().sort_by(Axis.Y)[0]

arc = sweep(plate_front,
            JernArc(plate_front.center(), plate_front.normal_at(),
                    BEND_RADIUS, 90 - TYPING_ANGLE_DEGREES, plane=Plane.YZ))

arc_bottom = arc.faces().sort_by(Axis.Z)[0]

wall = sweep(arc_bottom, LineBy(arc_bottom.center(), arc_bottom.normal_at(), arc_bottom.center().Z))

show_object(arc + wall)
