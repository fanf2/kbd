import math
import time
from build123d import *

def typing_angle(foot_height, foot_depth):
    return math.atan2(foot_height, foot_depth) * 360 / math.tau

# dunno why it can't find `logging` via the previous import
import build123d
log = build123d.logging.getLogger("build123d")

log.info("hello!")

EXPLODE = 0

# simplified plate cutouts? (0/1/2/3)
SPEED = 1

# For most of the time we work with plates this thick, then re-adjust
# to the desired thickness right at the end. This avoids problems when
# the cad system refuses to work in pure 2d (for reasons that are
# unclear to me).
THICK = 1
def thick(shape, amount=THICK):
    return extrude(shape, amount=amount)

# plastic basics

PERSPEX_THICK = 3.0
PLATE_THICK = 1.5   # 0.06 in

# accent pieces are inserted at right-angles
# cast perspex tolerance is +/-10% plus 0.4mm
# https://www.theplasticshop.co.uk/perspex-faqs.html#21
THICK_CLEAR = PERSPEX_THICK * 0.1 + 0.4
log.info(f"{THICK_CLEAR=}")

# space between laser cut pieces
SPREAD_CLEAR = 1

SVG_MARGIN = 10

# key switch basics

KEY_UNIT = 19.05

def ku(n):
    return KEY_UNIT * n

MX_PLATE_HOLE	= 14.0
MX_PLATE_RIB	= KEY_UNIT - MX_PLATE_HOLE
MX_HOLE_RADIUS	= 0.25 # max 0.012 in

MX_STAB_WIDTH	= 7
MX_STAB_DEPTH	= 16
MX_STAB_RADIUS	= 2

# over-complicated cutouts
MX_RELIEF_RADIUS= 0.5**0.5
MX_RELIEF_FILLET= MX_RELIEF_RADIUS * (2**0.5)
MX_RELIEF_POS	= MX_PLATE_HOLE - MX_RELIEF_FILLET

# key block layout

KEYBLOCK_GAP	= ku( 0.25 )

KEYS_WIDE	= 15
KEYS_DEEP	= 5

MAIN_WIDTH	= KEY_UNIT * KEYS_WIDE
MAIN_DEPTH	= KEY_UNIT * KEYS_DEEP

FUN_WIDTH	= ku( 3.00 )
FUN_DEPTH	= ku( 2.00 )

# enclosure outline

CASE_SIDE	= ku( 1.00 ) - KEYBLOCK_GAP
CASE_FRONT	= ku( 0.50 )
CASE_REAR	= ku( 7/6 ) # total depth 6.6666

WALL_THICK	= ku( 0.25 )
SIDE_THICK	= PERSPEX_THICK * 3

TOTAL_WIDTH	= MAIN_WIDTH + (KEYBLOCK_GAP + FUN_WIDTH + CASE_SIDE) * 2
TOTAL_DEPTH	= MAIN_DEPTH + CASE_FRONT + CASE_REAR

MIDDLE_WIDTH	= MAIN_WIDTH - ku(2.0)
ELLIPSE_AXIS	= ku(7.0)

# a little clearance
CLIP_WIDTH	= TOTAL_WIDTH + 1
CLIP_DEPTH	= TOTAL_DEPTH + 1

# round off sharp corners
SIDE_RADIUS	= 1.0
KEYBLOCK_RADIUS	= 0.5

# key block positions

MAIN_Y		= CASE_FRONT / 2 - CASE_REAR / 2

FUN_X		= MAIN_WIDTH / 2 + KEYBLOCK_GAP + FUN_WIDTH / 2
FUN_Y1		= MAIN_Y + MAIN_DEPTH / 2 - KEYBLOCK_GAP - FUN_DEPTH / 2
FUN_Y2		= FUN_Y1 - KEYBLOCK_GAP - FUN_DEPTH
FUN_Y2a		= FUN_Y2 - ku(0.5) # lower arrows

# accent positions

ACCENT_CLEAR	= 0.5
ACCENT_RADIUS	= SIDE_RADIUS

def side_length(shape):
    return shape.edges().sort_by(Axis.X)[0].length

SIDE_DEPTH	= 1 # placeholder
CHEEK_DEPTH	= 1 # placeholder
SLOT_WIDTH	= 1 # placeholder
BROW_WIDTH	= 1 # placeholder

def set_accent_sizes(side_length):
    global SIDE_DEPTH
    global CHEEK_DEPTH
    global NOTCHES_DEPTH
    global SLOT_WIDTH
    global BROW_WIDTH
    SIDE_DEPTH	= side_length - WALL_THICK*2
    NOTCHES_DEPTH = SIDE_DEPTH + NOTCH_DEPTH*2
    CHEEK_DEPTH	= NOTCHES_DEPTH - ACCENT_CLEAR
    BROW_WIDTH	= CHEEK_DEPTH*4 + BROW_SPACE*3
    SLOT_WIDTH	= BROW_WIDTH + ACCENT_CLEAR

# this cutout rectangle sticks out by MX_PLATE_RIB/2
SIDE_INSET_W	= CASE_SIDE # wider than needed
SIDE_INSET_X	= TOTAL_WIDTH/2 + MX_PLATE_RIB/2 - SIDE_INSET_W/2

# holder for side accents
NOTCH_DEPTH	= 1.5
NOTCH_WIDTH	= PERSPEX_THICK + THICK_CLEAR
NOTCH_RADIUS	= THICK_CLEAR
NOTCH_X		= TOTAL_WIDTH/2 - SIDE_THICK/2

# side accents
CHEEK_WIDTH	= PERSPEX_THICK
CHEEK_HEIGHT	= PERSPEX_THICK * 3 + PLATE_THICK * 3 - THICK_CLEAR

# holder for penrest accent
SLOT_DEPTH	= PERSPEX_THICK + THICK_CLEAR
SLOT_RADIUS	= THICK_CLEAR/2
SLOT_Y		= MAIN_Y + MAIN_DEPTH/2 + KEYBLOCK_GAP + SLOT_DEPTH/2

# penrest accent
BROW_SPACE	= 0.1
BROW_DEPTH	= PERSPEX_THICK
BROW_HEIGHT	= PERSPEX_THICK * 3 + PLATE_THICK
LOBROW_WIDER	= PERSPEX_THICK * 2
LOBROW_HEIGHT	= BROW_HEIGHT - PERSPEX_THICK * 2 - THICK_CLEAR

# fasteners

HOLE_TINY	= 2.2 # m2 screw diameter
HOLE_SCREW	= 3.2 # m3 screw diameter
HOLE_RIVNUT	= 5.2 # m3 rivnut barrel
HOLE_SUPPORT	= WALL_THICK*2
HOLE_MENISCUS	= WALL_THICK/2

HOLE_X1		= ku( 3.50 )
HOLE_X2		= ku( 9.25 )

HOLE_Y1		= TOTAL_DEPTH/2 - WALL_THICK
HOLE_Y2		= 0 # placeholder

HOLE_POSITIONS	= [] # placeholder

FOOT_DEPTH	= 1 # placeholder

# printed circuit board

COMPONENTS_THICK = 2.0
PCB_THICK	= 1.6
PCB_Z		= PLATE_THICK + PERSPEX_THICK - 5.0 + EXPLODE/2
PCB_INSET	= ku( 1/8 )
PCB_WING	= ku( 13/32 )
PCB_STAB	= ku( 7 - 1 )/2

# USB daughterboard

USB_INSET	= 1.0
USB_WIDTH	= 9.0 # spec says 8.34
USBDB_WIDTH	= 18
USBDB_DEPTH	= 18
USBDB_THICK	= 4.2
USBDB_CLEAR	= 0.5
USBDB_R		= 1.0
USBDB_Y		= TOTAL_DEPTH/2 - USBDB_DEPTH/2 - USBDB_CLEAR - USB_INSET

# for debugging
def multiocular_vertices(vertices):
    cs = [ Location(v.center()) for v in vertices ]
    iris = [ c * Circle(2) for c in cs ]
    pupil = [ c * Circle(1) for c in cs ]
    return Sketch() + iris - pupil

# from kicad

def pcba():
    rear = MAIN_Y + MAIN_DEPTH/2
    front = MAIN_Y - MAIN_DEPTH/2 + PCB_INSET
    right = MAIN_WIDTH/2 + PCB_INSET + FUN_WIDTH
    half = Polyline(
        (0, rear),
        (MAIN_WIDTH/2, rear),
        (MAIN_WIDTH/2 + KEYBLOCK_GAP, rear - KEYBLOCK_GAP),
        (right, rear - KEYBLOCK_GAP),
        (right + PCB_WING, rear - KEYBLOCK_GAP - PCB_WING),
        (right + PCB_WING, front + KEYBLOCK_GAP*2 + PCB_WING),
        (right, front + KEYBLOCK_GAP*2),
        (MAIN_WIDTH/2 + PCB_INSET + KEYBLOCK_GAP, front + KEYBLOCK_GAP*2),
        (MAIN_WIDTH/2 - PCB_INSET, front),
        (PCB_STAB + PCB_INSET*2, front),
        (PCB_STAB + PCB_INSET*1, front - PCB_INSET),
        (0, front - PCB_INSET),
    )
    outline = make_face(half + mirror(half, Plane.YZ))
    keepout = offset(outline, amount=-PCB_INSET)
    screws = (Location((+PCB_STAB, front)) * Circle(PCB_INSET) +
              Location((-PCB_STAB, front)) * Circle(PCB_INSET))
    components = Location((0,0,-PCB_THICK)) * (
        thick(keepout, COMPONENTS_THICK) +
        thick(screws, -COMPONENTS_THICK) )
    return thick(outline, PCB_THICK) + components

# the cad system kept refusing to fillet corners, so i'm doing it manually

def classify_vertex(shape2d, vertex):
    circle = Location(vertex.center()) * Circle(0.1)
    chomp = shape2d & circle
    return chomp.area / circle.area

def meniscus(shape2d, vertex, radius):
    vertex = vertex.center()
    circle = Location(vertex) * Circle(radius)
    chomp = shape2d & circle
    (edges, radii) = ([],[])
    for e in chomp.edges():
        # control point tangents are scaled and point towards vertex
        if e @ 1 == vertex:
            radii += [( (e @ 0), (e % 0) * (+radius*2/3) )]
        elif e @ 0 == vertex:
            radii += [( (e @ 1), (e % 1) * (-radius*2/3) )]
        else:
            edges += [e]
    if len(radii) != 2:
        log.info("meniscus requires 2 radial edges")
        return []
    if len(edges) == 0:
        log.info("meniscus could not make a closed curve")
        return []
    (p0, t0) = radii[0]
    (p1, t1) = radii[1]
    curve = Edge() + edges
    # ensure edges are in a consistent order
    # so that the resulting face points in the correct direction
    (start, end) = (curve.start_point(), curve.end_point())
    if start == p1 and end == p0:
        curve += Bezier(p0, p0 + t0, p1 + t1, p1)
    elif start == p0 and end == p1:
        curve += Bezier(p1, p1 + t1, p0 + t0, p0)
    else:
        log.info("mismatched endpoints in meniscus")
        return []
    curve = make_face(curve)
    if chomp.area / circle.area > 0.5:
        return [curve]
    else:
        return [circle - curve]

def roundoff(shape2d, mouth_r, ear_r=None):
    ear_r = ear_r or mouth_r
    mouths = []
    ears = []
    for v in shape2d.vertices():
        kind = classify_vertex(shape2d, v)
        if kind > 0.6:
            mouths += meniscus(shape2d, v, mouth_r)
        elif kind < 0.4:
            ears += meniscus(shape2d, v, ear_r)
        else:
            log.info(f"flat {mouth_r=} {ear_r=} {kind=}")
    shape3d = thick(shape2d)
    if mouths: shape3d += thick(Sketch() + mouths)
    if ears: shape3d -= thick(Sketch() + ears)
    return shape3d

def plate_cutouts():
    if SPEED > 1:
        switch = thick(Rectangle(MX_PLATE_HOLE, MX_PLATE_HOLE))
    elif SPEED > 0:
        switch = thick(RectangleRounded(
            MX_PLATE_HOLE, MX_PLATE_HOLE, MX_HOLE_RADIUS))
    else:
        square = Rectangle(MX_PLATE_HOLE, MX_PLATE_HOLE)
        relief = [ loc * Circle(MX_WIDE_RADIUS) for loc in
                   GridLocations(MX_RELIEF_POS, MX_RELIEF_POS, 2, 2) ]
        switch = roundoff(square + relief, MX_HOLE_RELIEF)

    stab = thick(RectangleRounded(
        MX_STAB_WIDTH, MX_STAB_DEPTH, MX_STAB_RADIUS))
    def stabs(width):
        return (Location((-ku(width - 1) / 2, 0)) * stab +
                Location((+ku(width - 1) / 2, 0)) * stab)

    hole = [None] * 1000
    hole[100] = switch
    hole[125] = switch
    hole[150] = switch
    hole[175] = switch
    hole[200] = switch + stabs(2.25) # sic
    hole[225] = switch + stabs(2.25)
    hole[275] = switch + stabs(2.75)
    hole[625] = switch + stabs(6.25)
    hole[700] = switch + stabs(7.00)

    def adjacent(y, keys, sign):
        row = []
        pos = -sign * MAIN_WIDTH / 2
        for k in keys:
            width = sign * ku(k/100)
            row.append(Location((pos + width/2, y)) * hole[k])
            pos += width
        return (row,pos)

    def key_grid(x, y, w, h):
        key = Location((x, y)) * switch
        return [] if w == 0 or h == 0 else [
            loc * key for loc in GridLocations(ku(1), ku(1), w, h) ]

    def key_row(y, left_keys, middle, right_keys):
        (left_row, left_pos) = adjacent(y, left_keys, +1)
        (right_row, right_pos) = adjacent(y, reversed(right_keys), -1)
        middle_row = key_grid((left_pos + right_pos)/2, y, middle, 1)
        return left_row + middle_row + right_row

    microsoft = [ 125, 125, 125, 625, 125, 125, 125, 125 ]
    tsangan = [ 150, 100, 150, 700, 150, 100, 150 ]
    keybird = [ 125, 125, 150, 700, 150, 125, 125 ]

    return (key_grid(-FUN_X, FUN_Y1, 3, 2) +
            key_grid(-FUN_X, FUN_Y2, 3, 2) +
            key_grid(+FUN_X, FUN_Y1, 3, 2) +
            key_grid(+FUN_X, FUN_Y2, 3, 2) +
            key_row(MAIN_Y + ku(+2), [], 15, []) +
            key_row(MAIN_Y + ku(+1), [150], 12, [150]) +
            key_row(MAIN_Y + ku(00), [175], 11, [225]) +
            key_row(MAIN_Y + ku(-1), [225], 10, [175, 100]) +
            key_row(MAIN_Y + ku(-2), [], 0, keybird))

def top_cutouts():
    main = (Location((0, MAIN_Y)) *
            Rectangle(MAIN_WIDTH, MAIN_DEPTH))
    fun = Rectangle(FUN_WIDTH, FUN_DEPTH)
    fun1 = Location((-FUN_X, FUN_Y1)) * fun
    fun2 = Location((-FUN_X, FUN_Y2)) * fun
    fun3 = Location((+FUN_X, FUN_Y1)) * fun
    fun4b = Location((FUN_X, FUN_Y2)) * Rectangle(ku(1), FUN_DEPTH)
    fun4a = Location((FUN_X, FUN_Y2a)) * Rectangle(FUN_WIDTH, ku(1))
    brow = (Location((0, SLOT_Y)) *
            RectangleRounded(SLOT_WIDTH, SLOT_DEPTH, SLOT_RADIUS))
    holes = Sketch() + [ main, fun1, fun2, fun3, fun4a, fun4b, brow ]
    return [ roundoff(holes, KEYBLOCK_RADIUS) ]

def case_outline_2d():
    middle = Rectangle(MIDDLE_WIDTH, TOTAL_DEPTH)
    edges = middle.edges()

    ellipse = Ellipse(ELLIPSE_AXIS, TOTAL_DEPTH / 2)
    left = Location(edges[0] @ 0.5) * ellipse
    right = Location(edges[2] @ 0.5) * ellipse

    oval = left + middle + right
    clip = Rectangle(TOTAL_WIDTH, CLIP_DEPTH)
    outline = oval & clip

    set_accent_sizes(side_length(outline))

    return outline

def case_interior_2d(outline):
    uniform = offset(outline, amount=-WALL_THICK)
    # re-clip so that the side walls are thicker
    sideclip = Rectangle(TOTAL_WIDTH - SIDE_THICK * 2, CLIP_DEPTH)
    interior = uniform & sideclip

    global HOLE_Y2
    holeclip = Rectangle(HOLE_X2 * 2, CLIP_DEPTH)
    HOLE_Y2 = side_length(interior & holeclip) / 2
    return interior

# A circle of diameter `HOLE_SUPPORT` does not touch the edge of the
# case at HOLE_X2, so it leaves a slight indentation in the foot; a
# circle of diameter `heel_width` sticks out slightly, so it doesn't
# meet the rear of the foot at a tangent, but it's close enough.
#
def feet(outline):
    global FOOT_DEPTH

    holeclip = Rectangle(HOLE_X2 * 2, CLIP_DEPTH)
    # baseline of foot
    foot_y0 = HOLE_Y2 - HOLE_SUPPORT/2
    # this is slightly more than foot_y0 + HOLE_SUPPORT
    foot_y1 = side_length(outline & holeclip) / 2

    foot_width = HOLE_X2 - HOLE_X1
    foot_depth = TOTAL_DEPTH/2 - foot_y0
    heel_depth = foot_y1 - foot_y0

    foot_x = HOLE_X1/2 + HOLE_X2/2
    foot_y = foot_y0 + foot_depth/2
    heel_y = foot_y0 + heel_depth/2

    arch = Location((foot_x, foot_y)) * Rectangle(foot_width, foot_depth)
    toes = Location((HOLE_X1, foot_y)) * Circle(foot_depth/2)
    heel = Location((HOLE_X2, heel_y)) * Circle(heel_depth/2)

    foot = heel + arch + toes
    feet = foot + mirror(foot, Plane.YZ)

    FOOT_DEPTH = foot_depth

    return thick(feet & outline)

def side_inset_2d():
    inset = Rectangle(SIDE_INSET_W, SIDE_DEPTH)
    return (Location((-SIDE_INSET_X, 0)) * inset +
            Location((+SIDE_INSET_X, 0)) * inset)

def hole_support_2d():
    support = Circle(HOLE_SUPPORT / 2)
    return Sketch() + [ pos * support for pos in HOLE_POSITIONS ]

def holes(diameter):
    global HOLE_POSITIONS
    if not HOLE_POSITIONS:
        log.info(f"{HOLE_X1=} {HOLE_Y1=} {HOLE_X2=} {HOLE_Y2=}")
        HOLE_POSITIONS = [ Location(p)
                           for i in [-1,+1] for j in [-1,+1]
                           for p in [(i*HOLE_X1, j*HOLE_Y1, 0),
                                     (i*HOLE_X2, j*HOLE_Y2, 0)] ]
    hole = thick(Circle(diameter / 2))
    return [ pos * hole for pos in HOLE_POSITIONS ]

def notch_cutouts():
    notch = thick(RectangleRounded(NOTCH_WIDTH, NOTCHES_DEPTH, NOTCH_RADIUS))
    return [ Location((-NOTCH_X, 0)) * notch,
             Location((+NOTCH_X, 0)) * notch ]

def socket_cutouts():
    usbdb = thick(RectangleRounded(USBDB_WIDTH, USBDB_DEPTH, USBDB_R))
    inset = thick(Rectangle(USB_WIDTH, USB_INSET*3))
    return [ Location((0, USBDB_Y)) * offset(usbdb, USBDB_CLEAR),
             Location((0, TOTAL_DEPTH/2)) * inset ]

def daughterboard_holes():
    hole = Location((0, USBDB_Y)) * thick(Circle(HOLE_TINY/2), USBDB_THICK)
    return [ loc * hole for loc in GridLocations(14, 14, 2, 2) ]

def daughterboard():
    return Location((0, USBDB_Y)) * thick(RectangleRounded(
        USBDB_WIDTH, USBDB_DEPTH, USBDB_R), USBDB_THICK) - daughterboard_holes()

def monobrow():
    lobrow_width = BROW_WIDTH + LOBROW_WIDER
    flat = (
        Location((0, BROW_HEIGHT/2)) * Rectangle(BROW_WIDTH, BROW_HEIGHT) +
        Location((0, LOBROW_HEIGHT/2)) * Rectangle(lobrow_width, LOBROW_HEIGHT))
    return roundoff(flat, ACCENT_RADIUS)

def polybrow(spacing):
    brow = RectangleRounded(CHEEK_DEPTH, CHEEK_HEIGHT, ACCENT_RADIUS)
    brow_x = CHEEK_DEPTH/2 + spacing/2
    brows = [ Location((+brow_x*3, CHEEK_HEIGHT/2)) * brow,
              Location((+brow_x*1, CHEEK_HEIGHT/2)) * brow,
              Location((-brow_x*1, CHEEK_HEIGHT/2)) * brow,
              Location((-brow_x*3, CHEEK_HEIGHT/2)) * brow ]
    return thick(Sketch() + brows)

def cheek():
    return thick(RectangleRounded(CHEEK_DEPTH, CHEEK_HEIGHT, ACCENT_RADIUS))

def cheek_perspex(cheek):
    rotated = cheek.rotate(Axis.Z, 90)
    cheek_x = MAIN_WIDTH/2 - CHEEK_HEIGHT/2 - KEYBLOCK_GAP
    cheek_y = FUN_Y1/2 + FUN_Y2/2
    return [ Location((+cheek_x, cheek_y)) * rotated,
             Location((-cheek_x, cheek_y)) * rotated ]

def thicken_accent(accent):
    thickened = scale(accent, (1,1, PERSPEX_THICK / THICK))
    return Location((0,0, -PERSPEX_THICK/2)) * thickened

def brow_vertical(brow, accent_z):
    rotated = thicken_accent(brow).rotate(Axis.X, 90)
    brow_z = accent_z + PLATE_THICK + THICK_CLEAR/2 + EXPLODE*3/2
    return [ Location((0, SLOT_Y, brow_z)) * rotated ]

def cheek_vertical(cheek, accent_z):
    rotated = thicken_accent(cheek).rotate(Axis.Z, 90).rotate(Axis.Y, 90)
    # off-centre due to difference between top layer and base plate
    cheek_z = accent_z - (PERSPEX_THICK - PLATE_THICK)/2
    return [ Location((-NOTCH_X, 0, cheek_z)) * rotated,
             Location((+NOTCH_X, 0, cheek_z)) * rotated ]

HALF_WALL = Box(CLIP_WIDTH, CLIP_DEPTH/2, THICK*3)
HALF_FOOT = Box(CLIP_WIDTH/2, CLIP_DEPTH, THICK*3)

def rear_wall(shape):
    return Location((0, +CLIP_DEPTH/4)) * HALF_WALL & shape

def front_wall(shape):
    return Location((0, -CLIP_DEPTH/4)) * HALF_WALL & shape

def left_foot(shape):
    return Location((-CLIP_WIDTH/4, 0)) * HALF_FOOT & shape

def right_foot(shape):
    return Location((+CLIP_WIDTH/4, 0)) * HALF_FOOT & shape

START = time.perf_counter()
def stamp(msg):
    print(f"{time.perf_counter() - START :6.3f} {msg}")

FLAT_OUTLINE = case_outline_2d()
FLAT_INTERIOR = case_interior_2d(FLAT_OUTLINE)
CASE_OUTLINE = roundoff(FLAT_OUTLINE, SIDE_RADIUS)

stamp("basic cutouts")

SIDE_INSET = side_inset_2d()
NOTCH_CUTOUTS = notch_cutouts()
SOCKET_CUTOUTS = socket_cutouts()

HOLES_SCREW = holes(HOLE_SCREW)
HOLES_RIVNUT = holes(HOLE_RIVNUT)

stamp("top layer")

TOP_CUTOUTS = top_cutouts() + HOLES_SCREW
TOP_LAYER = CASE_OUTLINE - TOP_CUTOUTS

stamp("switch plate")

PLATE_CUTOUTS = NOTCH_CUTOUTS + HOLES_SCREW + plate_cutouts()
SWITCH_PLATE = roundoff(FLAT_OUTLINE - SIDE_INSET, SIDE_RADIUS) - PLATE_CUTOUTS

stamp("base plate")

BASE_PLATE = CASE_OUTLINE - daughterboard_holes() - HOLES_RIVNUT

stamp("walls")

FLAT_WALLS = FLAT_OUTLINE - FLAT_INTERIOR - SIDE_INSET + hole_support_2d()
WALLS = roundoff(FLAT_WALLS, HOLE_MENISCUS, SIDE_RADIUS) - NOTCH_CUTOUTS

WALLS_SCREW = WALLS - HOLES_SCREW
WALLS_RIVNUT = WALLS - HOLES_RIVNUT
WALLS_SOCKET = WALLS_RIVNUT - SOCKET_CUTOUTS

stamp("feet")

FEET = feet(FLAT_OUTLINE)
# include some little donuts to use as shims
FEET_RIVNUT = FEET - HOLES_RIVNUT + rear_wall(HOLES_SCREW)

stamp("accents")

CHEEK = cheek()
MONOBROW = monobrow()
POLYBROW = polybrow(BROW_SPACE)

# for the stack view
BROW = MONOBROW

layers = [
    TOP_LAYER,
    WALLS_SCREW,
    WALLS_SCREW,
    SWITCH_PLATE,
    WALLS_RIVNUT,
    WALLS_SOCKET,
    WALLS_SOCKET,
    BASE_PLATE,
    FEET_RIVNUT,
    FEET_RIVNUT,
    FEET_RIVNUT,
    FEET_RIVNUT,
    FEET_RIVNUT,
    FEET_RIVNUT,
]

# 3d view of assembled or exploded board

stack = []

z = PLATE_THICK*4 + PERSPEX_THICK*4
for i in range(len(layers)):
    stamp(f"stack {i}")
    thickness = PLATE_THICK if i < 8 and i % 2 else PERSPEX_THICK
    z -= thickness + EXPLODE
    layer = scale(layers[i], (1, 1, thickness / THICK))
    stack += [ Location((0,0,z)) * layer ]
    if i == 3:
        accent_z = z
    if i == 4:
        stack += [ Location((0,0, z + PCB_Z)) * pcba() ]
    if i == 6:
        stack += [ Location((0,0, z + EXPLODE/2)) * daughterboard() ]

stack += brow_vertical(BROW, accent_z)
stack += cheek_vertical(CHEEK, accent_z)

stamp("show")
show_object(stack)

# export layouts for cutting

if SPEED < 3:

    perspex = []
    plates = []
    for i in range(len(layers)):
        stamp(f"spread {i}")
        if i == 0:
            perspex += [ layers[i] ]
        elif i == 3:
            plates += [ Location((0, +CLIP_DEPTH/2)) * layers[i] ]
        elif i == 7:
            plates += [ Location((0, -CLIP_DEPTH/2)) * layers[i] ]
        elif i >= 8:
            move_y = (8 - i) * (FOOT_DEPTH + SPREAD_CLEAR) - CASE_REAR - 1
            move_x = HOLE_X1 - FOOT_DEPTH/2 - 1
            perspex += [ Location((+move_x, move_y)) * left_foot(layers[i]),
                         Location((-move_x, move_y)) * right_foot(layers[i]) ]
        elif i % 2:
            move = (i / 4 + 0.75) * (HOLE_SUPPORT + SPREAD_CLEAR) + CLIP_DEPTH/2
            plates += [ Location((0, +move)) * rear_wall(layers[i]),
                        Location((0, -move)) * front_wall(layers[i]) ]
        else:
            move = (i / 2) * (HOLE_SUPPORT + SPREAD_CLEAR)
            perspex += [ Location((0, +move)) * rear_wall(layers[i]),
                         Location((0, -move)) * front_wall(layers[i]) ]

    brow_y = TOTAL_DEPTH/2 + HOLE_SUPPORT*3 + SPREAD_CLEAR*4
    perspex += [ Location((0, brow_y)) * MONOBROW ]
    perspex += cheek_perspex(CHEEK)

    accents = [ Location((0, -BROW_HEIGHT/2)) * MONOBROW,
                Location((0, CHEEK_HEIGHT/2)) * polybrow(SPREAD_CLEAR) ]

    def export(name, shape):
        stamp(f"flatten {name}")
        exporter = ExportSVG(margin=SVG_MARGIN)
        flat = section(Part() + shape, Plane.XY)
        stamp(f"export {name}")
        exporter.add_shape(flat)
        exporter.write(name + ".svg")

    export("accents", accents)
    export("perspex", perspex)
    export("plates", plates)

stamp("done")
