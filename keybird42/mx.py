# cherry mx key switch dimensions

from build123d import *

KEY_UNIT = 19.05

def ku(n):
    return KEY_UNIT * n

MX_KEYCAP_THICK	= 8.0
MX_UPPER_THICK	= 6.5 # switch body above plate
MX_PLATE_THICK	= 1.5
MX_LOWER_THICK	= 5.0 # plate top to pcb top
MX_PINS_THICK	= 3.5

MX_PLATE_HOLE	= 14.0
MX_PLATE_RIB	= KEY_UNIT - MX_PLATE_HOLE
MX_HOLE_RADIUS	= 0.25 # max 0.012 in

MX_STAB_WIDTH	= 7
MX_STAB_DEPTH	= 16
MX_STAB_RADIUS	= 2

def mx_plate_cutouts():
    switch = RectangleRounded(
        MX_PLATE_HOLE, MX_PLATE_HOLE, MX_HOLE_RADIUS)
    stab = RectangleRounded(
        MX_STAB_WIDTH, MX_STAB_DEPTH, MX_STAB_RADIUS)

    def stabs(width):
        return (Location((-ku(width - 1) / 2, 0)) * stab +
                Location((+ku(width - 1) / 2, 0)) * stab)

    k = [None] * 1000
    k[100] = switch
    k[125] = switch
    k[150] = switch
    k[175] = switch
    k[200] = switch + stabs(2.25) # sic
    k[225] = switch + stabs(2.25)
    k[275] = switch + stabs(2.75)
    k[625] = switch + stabs(6.25)
    k[700] = switch + stabs(7.00)
    return k

def mx_key_grid(k, x, y, w, h):
    key = Location((x, y)) * k[100]
    return [] if w == 0 or h == 0 else [
        loc * key for loc in GridLocations(ku(1), ku(1), w, h) ]

def mx_key_row(k, width, y, left_keys, middle, right_keys):

    def adjacent(y, keys, sign):
        row = []
        pos = -sign * width / 2
        for kw in keys:
            mm = sign * ku(kw/100)
            row.append(Location((pos + mm/2, y)) * k[kw])
            pos += mm
        return (row,pos)

    (left_row, left_pos) = adjacent(y, left_keys, +1)
    (right_row, right_pos) = adjacent(y, reversed(right_keys), -1)
    middle_row = mx_key_grid(k, (left_pos + right_pos)/2, y, middle, 1)
    return left_row + middle_row + right_row
