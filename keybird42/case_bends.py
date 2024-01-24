from build123d import *
from keybird42 import *
from mx import *

def print_object(message, object):
    print(message)
    try: print(object.show_topology())
    except: print(f"{object}")

def LineBy(start, direction, length):
    return Line(start, start + (length / direction.length) * direction)

def interpolated(pos):
    return pos * 2 - 1

def tangent(curve, pos):
    return (curve % pos) * interpolated(pos)

def LineFrom(curve, pos, length):
    return LineBy(curve @ pos, tangent(curve, pos), length)

def ArcFrom(curve, pos, radius, angle):
    return JernArc(curve @ pos, tangent(curve, pos),
                   radius, interpolated(pos) * angle)

TYPING_ANGLE = 7

TOTAL_WIDTH = ku(24)

CHIN_DEPTH = ku(1)
BROW_DEPTH = ku(1)
FOREHEAD_DEPTH = ku(3)

THICK = MX_PLATE_THICK

inner_radius = THICK # required by laserboost
outer_radius = inner_radius + THICK
radius = (inner_radius + outer_radius) / 2

# minimum metal needed eash side of a bend
bend_grip = 7.1 - THICK - inner_radius

plate_to_top = 7
pcb_to_plate = 5

pcba_thick = 4 # MX pin length plus clearance

washer_thick = 1
side_inset = 1

plate_width = TOTAL_WIDTH - 2 * (
    inner_radius + THICK + washer_thick + THICK + side_inset)

# need to work out the proper details here...
plate_depth = KEYS_DEPTH + (CHIN_DEPTH + BROW_DEPTH) / 2

# plate, side-to-side

plate_side_height = plate_to_top - inner_radius - THICK


plate_x_axis = Line((-plate_width/2, 0),
                    (+plate_width/2, 0))

right_arc = ArcFrom(plate_x_axis, 1, radius, 90)
right_side = LineFrom(right_arc, 1, plate_side_height)

left_arc = ArcFrom(plate_x_axis, 0, radius, 90)
left_side = LineFrom(left_arc, 1, plate_side_height)

plate_sides = (
    Location((0, plate_depth/2, THICK/2)) * Rotation(X=90) *
    extrude(trace(
        left_side + left_arc + plate_x_axis + right_arc + right_side,
        THICK), amount=plate_depth))

# plate, front-to-rear

plate_lip_height = pcba_thick + pcb_to_plate - inner_radius

plate_y_axis = Line((0, -plate_depth/2),
                    (0, +plate_depth/2))

rear_arc = ArcFrom(plate_y_axis, 1, radius, 90 - TYPING_ANGLE)
rear_lip = LineFrom(rear_arc, 1, plate_lip_height)

front_arc = ArcFrom(plate_y_axis, 0, radius, 90 - TYPING_ANGLE)
front_lip = LineFrom(front_arc, 1, plate_lip_height)

plate_lips = (
    Location((plate_width/2, 0, THICK/2)) * Rotation(Y=-90) *
    extrude(trace(
        rear_lip + rear_arc + plate_y_axis + front_arc + front_lip,
        THICK), amount=plate_width))


# combined plate

plate_cutouts = extrude(keyswitch_cutouts(), amount=THICK)

plate = plate_sides + plate_lips - plate_cutouts

show_object(plate)

show_object(Location((0,0, -pcb_to_plate)) * pcba())
