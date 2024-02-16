from build123d import *
from cq_hacks import *
from keybird42 import *
import math
from mx import *
from superellipse import *

stamp("------------------------------------------")

set_view_preferences(line_width=1)

def inch(n):
    return 25.4 * n

# this also determines the top cutout radius
keycap_clear = 0.5

typing_angle = 6.6666

total_width = ku(24)
total_depth = total_width/3

body_rx = total_width/2
body_ry = total_depth/2
body_rz = ku(0.50)
body_xye = 1/2
body_ze = 1/3

ungula_rx = body_rx - ku(1.5)
ungula_ry = body_ry - ku(0.75)
ungula_e = 4/5

main_width = ku(15)
keys_width = main_width + 2 * (ku(0.25) + ku(3))
keys_depth = ku(5)
keys_y = ku(-0.25)
keys_z = body_rz - inch(1/16)

desk_rx = ku(16)
desk_ry = ku(8)
desk_z = inch(-2/3)
desk_e = 4/5
desk_location = Pos((0, 0, desk_z)) * Rot(X=-typing_angle)

rgb_case = rgba("113")
rgb_keys = rgba("213")

def thicken(shape, movement):
    return loft([movement * shape, shape])

#desk = desk_location * superellipse(desk_rx, desk_ry, desk_e)
desk = desk_location * thicken(superellipse(desk_rx, desk_ry, desk_e),
                               Pos((0,0,-1)))
show_object(desk, **rgba("ccc"))

stamp("making ungula")
ungula = Rot(Y=90) * superellipsoid(
    ungula_ry, ungula_ry, ungula_rx, 1, ungula_e
) & thicken(Rectangle(total_width, total_depth), desk_location)

show_object(ungula, **rgb_case)

body = superellipsoid(body_rx, body_ry, body_rz, body_xye, body_ze)

stamp("making cutouts")
top_sharpcut = extrude(offset(
    keycap_cutouts(), amount=keycap_clear, kind=Kind.INTERSECTION
), -7.5)
top_cutouts = (Location((0, keys_y, body_rz)) *
               fillet(top_sharpcut.edges() | Axis.Z, keycap_clear))

show_object(body - top_cutouts, **rgb_case)

stamp("making keycaps")
keycaps = []
def show_keycap(keycap, legend, name):
    global keycaps
    keycaps += [ Location((0,keys_y,keys_z)) * keycap ]
layout_keycaps(stamp, show_keycap, "simple", False)
stamp("showing keycaps")
show_object(keycaps, **rgb_keys)
