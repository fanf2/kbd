from build123d import *
from keybird42 import *
import math
from mx import *

from monkeypatch_JernArc import *

def print_object(message, object):
    print(message)
    try: print(object.show_topology())
    except: print(f"{object}")

def edges_x_z(shape):
    return shape.edges().filter_by(Axis.X).sort_by(Axis.Z)

def upper_point(shape): return edges_x_z(shape)[-1].center()
def lower_point(shape): return edges_x_z(shape)[0].center()

def sort_faces(shape, axis):
    return shape.faces().sort_by(axis)

def upper_face(shape): return sort_faces(shape, Axis.Z)[-1]
def lower_face(shape): return sort_faces(shape, Axis.Z)[+0]
def rear_face(shape):  return sort_faces(shape, Axis.Y)[-1]
def front_face(shape): return sort_faces(shape, Axis.Y)[+0]
def right_face(shape): return sort_faces(shape, Axis.X)[-1]
def left_face(shape):  return sort_faces(shape, Axis.X)[+0]

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
washer_diameter = 8
washer_radius = washer_diameter/2

magnet_thick = 4

pcba_thick = 3.3 # MX pin length
pcba_clear = 1.2
pcba_width = 420

plate_to_top = magnet_thick + washer_thick + THICK
pcb_to_plate = 5

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

# the fudge makes TOP_WIDTH = TOP_DEPTH * 3 too narrow
TOP_DEPTH = CHIN_DEPTH + KEYS_DEPTH + BROW_DEPTH
TOP_WIDTH = ku(24)
TOP_Y = BROW_DEPTH/2 - CHIN_DEPTH/2

print(f"{TOP_WIDTH=}")
print(f"{pcba_width + outer_radius*2=}")

assert TOP_WIDTH > pcba_width + outer_radius*2

plate_surround = ku(0.25)

assert plate_surround + MX_PLATE_RIB/2 + outer_radius > bend_grip

# at the spacebar stabilizer screws where clearance is tightest

datum_y = KEYS_DEPTH / 2
datum_z = pcba_clear + pcba_thick + pcb_to_plate
datum_loc = (Rotation(X=TYPING_ANGLE_DEGREES) *
             Location((0, datum_y, datum_z)))

# the top case determines many of the other dimensions

top_sharpcut = thick(offset(
    keycap_cutouts(), amount=keycap_clearance, kind=Kind.INTERSECTION))
top_cutouts = fillet(top_sharpcut.edges() | Axis.Z, keycap_clearance)
top = datum_loc * Location((0,0,plate_to_top)) * (
    thick(Location((0,TOP_Y)) * Rectangle(TOP_WIDTH, TOP_DEPTH))
    - top_cutouts)

# add front and rear walls

top_chin = sweep_arc(front_face(top), bend_radius,
                         +90-TYPING_ANGLE_DEGREES, Plane.YZ)
front_wall_top = lower_face(top_chin)
front_wall_height = front_wall_top.center().Z + THICK
front_wall = sweep_line(front_wall_top, front_wall_height)
front_wall = fillet((front_wall.edges() | Plane.YZ) << Axis.Z, outer_radius)

# the fudge factor should make these about the same
print(f"{CHIN_DEPTH=}")
print(f"{front_wall_height=}")

top_brow = sweep_arc(rear_face(top), bend_radius, -90, Plane.YZ)
rear_wall_top = lower_face(top_brow)
rear_wall_height = rear_wall_top.center().Z + THICK
rear_wall = sweep_line(rear_wall_top, rear_wall_height)
rear_wall = fillet((rear_wall.edges() | Plane.YZ) << Axis.Z, outer_radius)

# the fudge factor should make these about the same
print(f"{BROW_DEPTH=}")
print(f"{rear_wall_height=}")

top += [ top_chin, front_wall, top_brow, rear_wall ]

show_object(top)
top.export_step("bends_top.step")

# base with sides

base_front = lower_face(top).center().Y + THICK/2 + base_clear
# the multiple of base_clear here is a fudge to cope with
# the angle between the rear wall and the base elbows
base_rear = sort_faces(top, Axis.Z)[1].center().Y - THICK/2 - base_clear*1.8
base_depth = base_rear - base_front
base_width = TOP_WIDTH - outer_radius*2
base_y = base_rear/2 + base_front/2

base = Location((0,base_y)) * thick(Rectangle(base_width, base_depth))

left_elbow = sweep_arc(left_face(base), bend_radius, -90, Plane.XZ)
right_elbow = sweep_arc(right_face(base), bend_radius, +90, Plane.XZ)

# offset() doesn't work with the top case, so extrude the sides up to
# a simplified top that is displaced by the clearance we want

base_limit = (thick(datum_loc
                   * Location((0,0,plate_to_top - base_clear))
                   * Rectangle(ku(32), ku(16)))
              + thick(Location(lower_point(rear_wall)) *
                      Rotation(X=90+TYPING_ANGLE_DEGREES) *
                      Location((0,0,base_clear)) * Rectangle(ku(32), ku(16))))

def extrude_side(elbow):
    return extrude(upper_face(elbow), target=base_limit, until=Until.NEXT)

left_side = extrude_side(left_elbow)
right_side = extrude_side(right_elbow)

base += [left_elbow, right_elbow, left_side, right_side]
base = fillet(edges_x_z(base)[-4:], inner_radius)

show_object(base)
top.export_step("bends_base.step")

# pcb and plate are centred on the middle of the key blocks

pcb = datum_loc * Location((0,0,-pcb_to_plate)) * kb42_pcba()
show_object(pcb)

plate_width = KEYS_WIDTH + plate_surround*2 + MX_PLATE_RIB
plate_depth = KEYS_DEPTH + plate_surround*2

plate_cutouts = thick(keyswitch_cutouts())
plate = datum_loc * (thick(Rectangle(plate_width, plate_depth)) - plate_cutouts)

# front plate support

plate_chin = sweep_arc(front_face(plate), bend_radius,
                       +90-TYPING_ANGLE_DEGREES, Plane.YZ)
front_legtop = lower_face(plate_chin)
front_leglen = front_legtop.center().Z - outer_radius - washer_thick
front_leg = sweep_line(front_legtop, front_leglen)

front_heel = sweep_arc(lower_face(front_leg), bend_radius, -90, Plane.YZ)

front_heel_base = lower_point(front_heel)
front_chin_top = upper_point(plate_chin)
print(f"{front_chin_top.Z=}")
print(f"{front_heel_base.Z=}")
print(f"{front_chin_top.Z - front_heel_base.Z=}")
print(f"{bend_grip=}")
assert front_chin_top.Z - front_heel_base.Z > bend_grip

front_foot_len = front_heel_base.Y - base_front
print(f"{front_foot_len + outer_radius=}")
assert front_foot_len + outer_radius > bend_grip

front_foot = sweep_line(front_face(front_heel), front_foot_len)

# the rear plate support is at an angle, on the vague principle that
# it will be in closer alignment to the typing forces, so less likely
# to loosen the fasteners over time. and it looks neat. because of
# this we need some cunning to work out exactly how long its leg is.

plate_brow = sweep_arc(rear_face(plate), bend_radius, -90, Plane.YZ)

# create the heel with no leg - it's too high
rear_legtop = lower_face(plate_brow)
rear_heel = sweep_arc(rear_legtop, bend_radius,
                      +90-TYPING_ANGLE_DEGREES, Plane.YZ)

# move to correct Z position - it's too far forward
rear_heel_z = lower_point(rear_heel).Z
rear_heel = Location((0,0, washer_thick-rear_heel_z)) * rear_heel

rear_heelplane = upper_face(rear_heel).center()

# intersection of line (normal of rear_legtop)
# and plane (xy plane passing through rear_heelplane)
rear_leglen = (
    (rear_heelplane - rear_legtop.center()).dot(Axis.Z.direction)
    / rear_legtop.normal_at().dot(Axis.Z.direction))

rear_leg = sweep_line(rear_legtop, rear_leglen)

# move to correct Y position
rear_legbot = lower_face(rear_leg).center()
rear_heel = Location((0, rear_legbot.Y - rear_heelplane.Y, 0)) * rear_heel

rear_foot = sweep_line(rear_face(rear_heel), washer_diameter)

plate += [ plate_chin, front_leg, front_heel, front_foot,
           plate_brow, rear_leg, rear_heel, rear_foot ]

show_object(plate)
top.export_step("bends_plate.step")
