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
FRONT_HEIGHT = 7+5+4+1
FRONT_RADIUS = FRONT_HEIGHT/2
REAR_RADIUS = FRONT_RADIUS*2

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
typing_angle = half_angle*2

print(f"{FRONT_HEIGHT=}")
print(f"{MIDDLE_DEPTH/KEY_UNIT=}")
print(f"{typing_angle=}")

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

top_center = middle.faces().sort_by(Axis.Z)[-1].center_location

def on_top(shape):
    # for some reason the top face's XY plane is a YX plane
    return top_center * (Rotation(Z=-90) * shape)

holes = on_top(Location((0,MAIN_Y,0)) * (
    extrude(keycap_cutouts(), amount=-7) +
    extrude(keyswitch_cutouts(), amount=-7-5)))

show_object(middle - holes)

whole_top = on_top(Rectangle(TOTAL_WIDTH, TOTAL_DEPTH))

right_ellipse = on_top(Location((MIDDLE_WIDTH/2, 0)) *
                       Ellipse(ELLIPSE_X_RADIUS, ELLIPSE_Y_RADIUS))

right_top_edge = (right_ellipse & whole_top).edges().sort_by(Axis.Z)[-1]
right_base_edge = (Location(top_center.to_axis().direction * -FRONT_HEIGHT)
                   * right_top_edge)

right_base_front = right_base_edge @ 0
right_base_rear = right_base_edge @ 1
right_top_front = right_top_edge @ 0
right_top_rear = right_top_edge @ 1

right_front_center = (right_top_front + right_base_front) / 2
right_rear_center = (right_top_rear + right_base_rear) / 2
right_center = (right_front_center + right_rear_center) / 2

right_front_circle = (Location(right_front_center)
                      * (Plane.YZ * Circle(FRONT_RADIUS)))
right_rear_circle = (Location(right_rear_center)
                     * (Plane.YZ * Circle(FRONT_RADIUS)))

right_rectangle = Polygon(right_top_front,
                          right_top_rear,
                          right_base_rear,
                          right_base_front)

right_face = (Location(right_center - right_rectangle.center())
              * right_rectangle) + right_front_circle + right_rear_circle

show_object(right_face)
