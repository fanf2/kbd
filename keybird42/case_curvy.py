from build123d import *
from keybird42 import *
import math
from monkeypatch_JernArc import *
from mx import *

def atan2(opposite, adjacent):
    return math.atan2(opposite, adjacent) * 360/math.tau

def string_object(obj):
    try: return obj.show_topology()
    except: return f"{obj}"

#

THICK = 1.5
KEYCAP_CLEAR = 0.5

# defining features
FRONT_RADIUS = ku(1)/2
REAR_RADIUS = ku(2)/2

TOTAL_WIDTH = ku(24)
TOTAL_DEPTH = TOTAL_WIDTH/3

# rectangular section
MIDDLE_WIDTH = TOTAL_WIDTH/2
MIDDLE_DEPTH = TOTAL_DEPTH -FRONT_RADIUS - REAR_RADIUS
ELLIPSE_X_RADIUS = TOTAL_WIDTH/3
ELLIPSE_Y_RADIUS = MIDDLE_DEPTH/2

# position of keys relative to case top
MAIN_Y = MAIN_DEPTH/2 - MIDDLE_DEPTH/2 + ku(0.5)

half_angle = atan2((REAR_RADIUS - FRONT_RADIUS), MIDDLE_DEPTH)

print(f"{MIDDLE_DEPTH=}")
print(f"{half_angle=}")

top = Rotation(X=+half_angle) * Line(
    (0, 0, +FRONT_RADIUS),
    (0, MIDDLE_DEPTH, +FRONT_RADIUS))

base = Rotation(X=-half_angle) * Line(
    (0, 0, -FRONT_RADIUS),
    (0, MIDDLE_DEPTH, -FRONT_RADIUS))

# find centre of rear circle
rear_y = IntersectingLine(top.location_at(1).position,
                          top.tangent_at(1).rotate(Axis.X, -90),
                          Line((0,0,0),(0,1000,0))
                          ).location_at(1).position.Y + REAR_RADIUS
print(f"{rear_y=}")

front = ThreePointArc(top.vertices().sort_by(Axis.Y)[+0],
                  (0, -FRONT_RADIUS, 0),
                  base.vertices().sort_by(Axis.Y)[+0])

rear = ThreePointArc(top.vertices().sort_by(Axis.Y)[-1],
                     (0, rear_y, 0),
                     base.vertices().sort_by(Axis.Y)[-1])

# ensure we found the correct centre
assert top % 1 == rear % 0
assert base % 1 == -(rear % 1)

section = make_face([top,base,front,rear])

middle = extrude(section, amount=MIDDLE_WIDTH/2, both=True)

top_face = middle.faces().sort_by(Axis.Z)[-1]

# for some reason the top face's XY plane is a YX plane
keyholes = (top_face.center_location *
            (Rotation(Z=-90) *
             Location((0,MAIN_Y,0)) *
             extrude(keyswitch_cutouts(),
                     amount=-REAR_RADIUS*2)))

show_object(middle - keyholes)
