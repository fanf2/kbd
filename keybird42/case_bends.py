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

thick = MX_PLATE_THICK

inner_radius = thick # required by laserboost
outer_radius = inner_radius + thick
radius = (inner_radius + outer_radius) / 2

plate_to_top = 7
pcb_to_plate = 5

pcba_thick = 4 # MX pin length plus clearance

# plate, side-to-side

plate_side_height = plate_to_top - inner_radius - thick

plate_x_axis = Line((-KEYS_WIDTH/2, 0),
                    (+KEYS_WIDTH/2, 0))

right_arc = ArcFrom(plate_x_axis, 1, radius, 90)
right_side = LineFrom(right_arc, 1, plate_side_height)

left_arc = ArcFrom(plate_x_axis, 0, radius, 90)
left_side = LineFrom(left_arc, 1, plate_side_height)

plate_sides = (
    Location((0, KEYS_DEPTH/2, thick/2)) * Rotation(X=90) *
    extrude(trace(
        left_side + left_arc + plate_x_axis + right_arc + right_side,
        thick), amount=KEYS_DEPTH))

# plate, front-to-rear

plate_lip_height = pcba_thick + pcb_to_plate - inner_radius

plate_y_axis = Line((0, -KEYS_DEPTH/2),
                    (0, +KEYS_DEPTH/2))

rear_arc = ArcFrom(plate_y_axis, 1, radius, 90)
rear_lip = LineFrom(rear_arc, 1, plate_lip_height)

front_arc = ArcFrom(plate_y_axis, 0, radius, 90)
front_lip = LineFrom(front_arc, 1, plate_lip_height)

plate_lips = (
    Location((KEYS_WIDTH/2, 0, thick/2)) * Rotation(Y=-90) *
    extrude(trace(
        rear_lip + rear_arc + plate_y_axis + front_arc + front_lip,
        thick), amount=KEYS_WIDTH))


# combined plate

plate_cutouts = extrude(keyswitch_cutouts(), amount=thick)

plate = plate_sides + plate_lips - plate_cutouts

show_object(plate)

show_object(Location((0,0, -pcb_to_plate)) * pcba())
