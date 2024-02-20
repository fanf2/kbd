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

case_thick = inch(1/8)

ungula_rx = body_rx - ku(3/2)
ungula_ry = body_ry - ku(2/3)
ungula_e = 4/5

keys_y = ku(-0.125)
keys_z = body_rz - inch(1/16)

plate_rx = body_rx - case_thick
plate_ry = body_ry - case_thick
plate_e = body_xye
plate_z = keys_z - MX_UPPER_THICK

pcba_z = plate_z - MX_LOWER_THICK

desk_rx = ku(16)
desk_ry = ku(8)
desk_z = inch(-2/3)
desk_e = 4/5
desk_location = Pos((0, 0, desk_z)) * Rot(X=-typing_angle)

rgb_case = "113"
rgb_pcba = "070"
rgb_keys = "213"
rgb_plate = "222"

def loft_by(shape, movement):
    return loft([movement * shape, shape])

desk = desk_location * superellipse(desk_rx, desk_ry, desk_e, -1)
show_object(desk, **rgba("ccc"))

stamp("ungula")
def make_ungula():
    clip_surface = Rectangle(total_width, total_depth)
    clip_volume = loft([desk_location * clip_surface, clip_surface])
    superegg = superellipsoid(ungula_ry, ungula_ry, ungula_rx, 1, ungula_e)
    return (Rot(Y=90) * superegg) & clip_volume
ungula = make_ungula()

stamp("body")
body = supercube(body_xye, body_ze)
stamp("outside")
outside = scale(body, (body_rx, body_ry, body_rz))
stamp("inside")
inside = scale(body, tuple([r - case_thick for r in [body_rx, body_ry, body_rz]]))

stamp("cutouts")
top_sharpcut = extrude(offset(
    keycap_cutouts(), amount=keycap_clear, kind=Kind.INTERSECTION
), -7.5)
top_cutouts = (Location((0, keys_y, body_rz)) *
               fillet(top_sharpcut.edges() | Axis.Z, keycap_clear))

stamp("plate")
plate = superellipse(plate_rx, plate_ry, plate_e, -MX_PLATE_THICK)
plate -= extrude(keyswitch_cutouts(), -MX_PLATE_THICK)

# plate -= loft_by(keyswitch_cutouts(),
#                 Pos((0, 0, -MX_PLATE_THICK)))

shown = []
def show(obj, colour):
    global shown
    shown += [ (obj, colour) ]
    show_object(obj, **rgba(colour))

def show_sections(y, xs):
    pos = Pos((0,0,ku(y)))
    for x in xs:
        stamp(f"section {x}")
        for (obj, colour) in shown:
            sect = pos * section(obj, Plane.YZ.offset(ku(x)))
            show_object(sect, **rgba(colour))

stamp("show ungula")
show(ungula - outside, rgb_case)
stamp("show body")
show(outside - inside - top_cutouts, rgb_case)

stamp("show plate")
show(plate, rgb_plate)

stamp("show pcba")
show(Pos((0,keys_y,pcba_z)) * kb42_pcba(False), rgb_pcba)

show_sections(5, [1, 3, 5, 7.325, 7.625, 7.875, 9.25, 10.5, 11, 11.5])

# stamp("making keycaps")
# keycaps = []
# def show_keycap(keycap, legend, name):
#     global keycaps
#     keycaps += [ Location((0,keys_y,keys_z)) * keycap ]
# layout_keycaps(stamp, show_keycap, "simple", False)
# stamp("showing keycaps")
# show_object(keycaps, **rgb_keys)
