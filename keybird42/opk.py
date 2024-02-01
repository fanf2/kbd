"""
This is adapted from OPK, Open Programmatic Keycap
https://github.com/cubiq/OPK
Copyright (c) 2022 Matteo "Matt3o" Spinelli
https://matt3o.com
released under the Apache License 2.0

Changed by Tony Finch <dot@dotat.at>
to use build123d instead of CadQuery
"""

import build123d as bd
from mx import *

KEY_UNIT = 19.05

def keycaps(progress, simple=False):
    gen = simplified if simple else keycap
    row = [None] * 6
    for i in range(len(row)):
        row[i] = [None] * 1000
    for w in MX_KEY_WIDTHS:
        progress(w)
        if w < 300:
            row[0][w] = gen(unitX=w/100, height=11, angle=+0 )
            row[1][w] = gen(unitX=w/100, height=10, angle=+9 )
            row[2][w] = gen(unitX=w/100, height=8,  angle=+6 )
            row[3][w] = gen(unitX=w/100, height=8,  angle=-6 )
            row[4][w] = gen(unitX=w/100, height=9,  angle=-12 )
            row[5][w] = gen(unitX=w/100, height=9,  angle=+0 )
        else:
            row[5][w] = gen(unitX=w/100, height=9,  angle=+0, convex=True )
    return row

def simplified(
    unitX: float = 1,
    unitY: float = 1,
    base: float = 18.2,
    top: float = 13.2,
    curv: float = 1.7,
    bFillet: float = 0.5,
    tFillet: float = 5,
    height: float = 13,
    angle: float = 7,
    depth: float = 2.8,
    thickness: float = 1.5,
    convex: bool = False,
    legend: str = "",
    legendDepth: float = -1.0,
    font: str = "sans-serif",
    fontsize: float = 10,
    pos: bool = False
):
    top_diff = base - top
    bx = KEY_UNIT * unitX - (KEY_UNIT - base)
    by = KEY_UNIT * unitY - (KEY_UNIT - base)
    tx = bx - top_diff
    ty = by - top_diff
    base = bd.RectangleRounded(bx, by, bFillet)
    top = (bd.Location((0, 0, height - depth), (1,0,0), angle)
           * bd.RectangleRounded(tx, ty, tFillet))
    return bd.loft([base, top]);


def keycap(
    unitX: float = 1,           # keycap size in unit. Standard sizes: 1, 1.25, 1.5, ...
    unitY: float = 1,
    base: float = 18.2,         # 1-unit size in mm at the base
    top: float = 13.2,          # 1-unit size in mm at the top, actual hitting area will be slightly bigger
    curv: float = 1.7,          # Top side curvature. Higher value makes the top rounder (use small increments)
    bFillet: float = 0.5,       # Fillet at the base
    tFillet: float = 5,         # Fillet at the top
    height: float = 13,         # Height of the keycap before cutting the scoop (final height is lower)
    angle: float = 7,           # Angle of the top surface
    depth: float = 2.8,         # Scoop depth
    thickness: float = 1.5,     # Keycap sides thickness
    convex: bool = False,       # Is this a spacebar?
    legend: str = "",           # Legend
    legendDepth: float = -1.0,  # How deep to carve the legend, positive value makes the legend embossed
    font: str = "sans-serif",   # font name, use a font name including extension to use a local file
    fontsize: float = 10,       # the font size is in units
    pos: bool = False           # use POS style stabilizers
):

    # if spacebar make the top less round-y
    tension = .4 if convex else 1

    curv = min(curv, 1.9)
    curvy = curv * tension

    top_diff = base - top

    mFillet = (tFillet - bFillet) / 3

    bx = KEY_UNIT * unitX - (KEY_UNIT - base)
    by = KEY_UNIT * unitY - (KEY_UNIT - base)

    tx = bx - top_diff
    ty = by - top_diff

    # Three-section loft of rounded rectangles.
    # Can't find a better way to do variable fillet
    base = bd.RectangleRounded(bx, by, bFillet)

    mid = bd.RectangleRounded(bx, by, mFillet) \
        .moved(bd.Location((0, 0, height/4), (1,0,0), angle/4))

    top_corners = [(+curv-tx/2, +curvy-ty/2), (-curv+tx/2, +curvy-ty/2),
                   (-curv+tx/2, -curvy+ty/2), (+curv-tx/2, -curvy+ty/2)]
    top_sides = [(0,-ty/2), (+tx/2, 0), (0,+ty/2), (-tx/2,0)]
    top_points = [ [top_corners[i-1], top_sides[i-1], top_corners[i]]
                   for i in range(4) ]
    top_arcs = [ bd.ThreePointArc(*points) for points in top_points ]
    top = bd.fillet(bd.make_face(top_arcs).vertices(), tFillet) \
        .moved(bd.Location((0, 0, height), (1,0,0), angle))

    # Main shape
    keycap = bd.loft([base, mid, top]);

    # sketch the profile of a body that will be carved
    # from the main shape to create the top scoop

    def squared_arc(c0, c1, c2, s3, s4):
        return bd.make_face(bd.ThreePointArc(c0, c1, c2)
                            + bd.Polyline(c2, s3, s4, c0))

    if convex:
        scoop = [ bd.Location((0, -2.1)) *
                  squared_arc((-by/2, -1), (0, 2), (+by/2, -1),
                              (+by/2, 10), (-by/2, 10)) ]
    else:
        scoop = [
            squared_arc((-by/2+2, 0), (0, min(-0.1, -depth+1.5)), (+by/2-2, 0),
                        (+by/2, height), (-by/2, height)),
            squared_arc((-by/2-2, -0.5), (0, -depth), (+by/2+2, -0.5),
                        (+by/2, height), (-by/2, height))
        ]

    # spread out the faces above the keycap to form the scoop body

    keycap -= bd.loft([
        bd.Plane.YZ *
        bd.Location((0, height, (bx * i/len(scoop)) - bx/2), angle) *
        face for i, face in enumerate(scoop + [scoop[0]])
    ])

    # Top edge fillet
    keycap = bd.fillet(keycap.edges() >> bd.Axis.Z, 0.6)

    return keycap
