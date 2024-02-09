from build123d import *
from cq_hacks import *
from keybird42 import *
import math
from monkeypatch_JernArc import *
from mx import *
from superellipse import *

stamp("------------------------------------------")

set_view_preferences(line_width=0)

RESOLUTION_XY = 64
RESOLUTION_Z = 16

# this also determines the top cutout radius
keycap_clear = 0.5

typing_angle = 6.6666

main_y = ku(-0.125)
main_width = ku(15)
keys_width = main_width + 2 * (ku(0.25) + ku(3))
keys_depth = ku(5)

total_width = ku(24)
total_depth = ku(7.25)

radius_x = ku(1.00)
radius_y = ku(0.75)
radius_z = ku(0.50)

outer_a = total_width/2
outer_b = total_depth/2
inner_a = outer_a - radius_x
inner_b = outer_b - radius_y

# empirically enough to fit around the key blocks
inner_e = 8

# softer than the inner curve but not
# getting squashed around the corner
outer_e = 6

# piet hein
side_e = 5/2

ungula_a = inner_a - ku(0.25)
ungula_b = inner_b + ku(0.25)
# any smaller and the spline fucks up
ungula_e = 4
ungula_z = ku(0.25)

desk_a = ku(16)
desk_b = ku(8)
desk_e = 3
desk_z = ku(0.85)

rgb_case = rgba("113")
rgb_keys = rgba("213")

desk = (Location((0, 0, -desk_z)) *
        Rotation(X=-typing_angle) *
        superellipse(desk_a, desk_b, desk_e))
show_object(extrude(desk, -1), **rgba("ccc"))

ungula = mirror(Location((0, 0, -ungula_z)) *
                superegg_half(ungula_a, ungula_b, ungula_e),
                Plane.XY) & extrude(desk, ku(2))
stamp("ungula")

inner = superellipse(inner_a, inner_b, inner_e, RESOLUTION_XY)
outer = superellipse(outer_a, outer_b, outer_e, RESOLUTION_XY)
stamp("body")
body = superellipsoid(inner, outer, radius_z, side_e, RESOLUTION_Z)
stamp("body")

top_sharpcut = extrude(offset(
    keycap_cutouts(), amount=keycap_clear, kind=Kind.INTERSECTION
), -7.5)
top_cutouts = (Location((0, main_y, radius_z)) *
               fillet(top_sharpcut.edges() | Axis.Z, keycap_clear))
stamp("cutouts")

case = ungula + body - top_cutouts
stamp("case")

show_object(case, **rgb_case)
stamp("show")

keycaps = []
def show_keycap(keycap, legend, name):
    global keycaps
    keycaps += [ Location((0,main_y,radius_z-1)) * keycap ]
layout_keycaps(stamp, show_keycap, "simple", False)
stamp("keycaps")
show_object(keycaps, **rgb_keys)
