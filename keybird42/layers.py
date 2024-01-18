from build123d import *

# dunno why it can't find `logging` via the previous import
import build123d
log = build123d.logging.getLogger("build123d")

log.info("hello!")

#MODE = "test"
MODE = "perspex"
#MODE = "plate"
#MODE = 1.001
#MODE = 5

SPREAD = 10

# plastic basics

PERSPEX_THICK = 3.0
PLATE_THICK = 1.5   # 0.06 in

# accent pieces are inserted at right-angles
# cast perspex tolerance is +/-10% plus 0.4mm
# https://www.theplasticshop.co.uk/perspex-faqs.html#21
ACCENT_CLEAR = PERSPEX_THICK * 0.1 + 0.4
log.info(f"{ACCENT_CLEAR=}")

# For most of the time we work with plates this thick, then re-adjust
# to the desired thickness right at the end. This avoids problems when
# the cad system refuses to work in pure 2d (for reasons that are
# unclear to me).
THICK = 1

# key switch basics

KEY_UNIT = 19.05

def ku(n):
    return KEY_UNIT * n

MX_PLATE_HOLE	= 14.0
MX_HOLE_RADIUS	= 0.5**0.5
MX_HOLE_RELIEF	= MX_HOLE_RADIUS * (2**0.5)
MX_RELIEF_POS	= MX_PLATE_HOLE - MX_HOLE_RELIEF

MX_PLATE_RIB	= KEY_UNIT - MX_PLATE_HOLE

MX_STAB_WIDTH	= 7
MX_STAB_DEPTH	= 16
MX_STAB_RADIUS	= 2

# key block layout

BLOCK_GAP	= ku( 0.25 )

KEYS_WIDE	= 15
KEYS_DEEP	= 5

MAIN_WIDTH	= KEY_UNIT * KEYS_WIDE
MAIN_DEPTH	= KEY_UNIT * KEYS_DEEP

FUN_WIDTH	= ku( 3.00 )
FUN_DEPTH	= ku( 2.00 )

# enclosure outline

CASE_SIDE	= ku( 1.00 ) - BLOCK_GAP
CASE_FRONT	= ku( 0.50 )
CASE_REAR	= ku( 7/6 )

WALL_THICK	= ku( 0.25 )
SIDE_THICK	= PERSPEX_THICK * 3

TOTAL_WIDTH	= MAIN_WIDTH + (BLOCK_GAP + FUN_WIDTH + CASE_SIDE) * 2
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

FUN_X		= MAIN_WIDTH / 2 + BLOCK_GAP + FUN_WIDTH / 2
FUN_Y1		= MAIN_Y + MAIN_DEPTH / 2 - BLOCK_GAP - FUN_DEPTH / 2
FUN_Y2		= FUN_Y1 - BLOCK_GAP - FUN_DEPTH
FUN_Y2a		= FUN_Y2 - ku(0.5) # lower arrows

# accent positions

SIDE_DEPTH	= 1 # placeholder

# this cutout rectangle sticks out by MX_PLATE_RIB/2
SIDE_INSET_W	= CASE_SIDE # wider than needed
SIDE_INSET_X	= TOTAL_WIDTH/2 + MX_PLATE_RIB/2 - SIDE_INSET_W/2

# holder for side accents
NOTCH_DEPTH	= 1
NOTCH_RADIUS	= NOTCH_DEPTH/2
NOTCH_WIDTH	= PERSPEX_THICK + ACCENT_CLEAR
NOTCH_X		= TOTAL_WIDTH/2 - SIDE_THICK/2

# side accents
CHEEK_DEPTH	= SIDE_DEPTH + NOTCH_DEPTH # placeholder
CHEEK_WIDTH	= PERSPEX_THICK
CHEEK_HEIGHT	= PERSPEX_THICK * 3 + PLATE_THICK * 3

# holder for penrest accent
SLOT_WIDTH	= MAIN_WIDTH
SLOT_DEPTH	= PERSPEX_THICK + ACCENT_CLEAR
SLOT_RADIUS	= ACCENT_CLEAR/2
SLOT_Y		= MAIN_Y + MAIN_DEPTH/2 + BLOCK_GAP + SLOT_DEPTH/2

# penrest accent
BROW_WIDTH	= SLOT_WIDTH - ACCENT_CLEAR
BROW_HEIGHT	= PERSPEX_THICK * 3 + PLATE_THICK
LOBROW_WIDTH	= BROW_WIDTH + PERSPEX_THICK * 2
LOBROW_HEIGHT	= BROW_HEIGHT - PERSPEX_THICK * 2 - ACCENT_CLEAR

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

# connector holes

USB_INSET	= 1.0
USB_WIDTH	= 9.0 # spec says 8.34
USB_CLEAR	= 0.5
USBDB_WIDTH	= 18
USBDB_DEPTH	= 18
USBDB_R		= 1.0
USBDB_Y		= TOTAL_DEPTH/2 - USBDB_DEPTH/2 - USB_CLEAR - USB_INSET

# for debugging
def multiocular_vertices(vertices):
    cs = [ Location(v.center()) for v in vertices ]
    iris = [ c * Circle(2) for c in cs ]
    pupil = [ c * Circle(1) for c in cs ]
    return Sketch() + iris - pupil

def perspex(shape):
    return extrude(shape, amount=PERSPEX_THICK)

def plate(shape):
    return extrude(shape, amount=PLATE_THICK)

def thick(shape):
    return extrude(shape, amount=THICK)

HALF_BOX = Box(CLIP_WIDTH, CLIP_DEPTH/2, THICK*3)

def rear_half(shape):
    return shape & Location((0, +CLIP_DEPTH/2)) * HALF_BOX

def front_half(shape):
    return shape & Location((0, -CLIP_DEPTH/2)) * HALF_BOX

def side_length(shape):
    return shape.edges().sort_by(Axis.X)[0].length

def top_faces(shape):
    faces = Sketch() + shape.faces().group_by(Axis.Z)[-1]
    return Location((0,0,-faces.center().Z)) * faces

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
    square = Rectangle(MX_PLATE_HOLE, MX_PLATE_HOLE)
    relief = [ loc * Circle(MX_HOLE_RADIUS) for loc in
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
        key = Location((x, y)) * hole[100]
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

    return Part() + (
        key_grid(-FUN_X, FUN_Y1, 3, 2) +
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
    return roundoff(holes, KEYBLOCK_RADIUS)

def case_outline_2d():
    middle = Rectangle(MIDDLE_WIDTH, TOTAL_DEPTH)
    edges = middle.edges()

    ellipse = Ellipse(ELLIPSE_AXIS, TOTAL_DEPTH / 2)
    left = Location(edges[0] @ 0.5) * ellipse
    right = Location(edges[2] @ 0.5) * ellipse

    oval = left + middle + right
    clip = Rectangle(TOTAL_WIDTH, CLIP_DEPTH)
    outline = oval & clip

    global SIDE_DEPTH
    global CHEEK_DEPTH
    SIDE_DEPTH = side_length(outline) - WALL_THICK*2
    CHEEK_DEPTH = SIDE_DEPTH + NOTCH_DEPTH

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
    hole = Circle(diameter / 2)
    return thick(Sketch() + [ pos * hole for pos in HOLE_POSITIONS ])

def notch_cutout():
    depth = SIDE_DEPTH + NOTCH_DEPTH*2
    notch = RectangleRounded(NOTCH_WIDTH, depth, NOTCH_RADIUS)
    return thick(Location((-NOTCH_X, 0)) * notch +
                 Location((+NOTCH_X, 0)) * notch)

def socket_cutout():
    usbdb = RectangleRounded(USBDB_WIDTH, USBDB_DEPTH, USBDB_R)
    inset = Rectangle(USB_WIDTH, USB_INSET*2)
    return thick(Location((0, USBDB_Y)) * offset(usbdb, USB_CLEAR) +
                 Location((0, TOTAL_DEPTH/2)) * inset)

def daughterboard_holes():
    holes = Sketch() + [ loc * Circle(HOLE_TINY/2) for loc in
                         GridLocations(14, 14, 2, 2) ]
    return thick(Location((0, USBDB_Y)) * holes)


FLAT_OUTLINE = case_outline_2d()
FLAT_INTERIOR = case_interior_2d(FLAT_OUTLINE)
CASE_OUTLINE = roundoff(FLAT_OUTLINE, SIDE_RADIUS)

SIDE_INSET = side_inset_2d()
NOTCH_CUTOUT = notch_cutout()
SOCKET_CUTOUT = socket_cutout()

HOLES_SCREW = holes(HOLE_SCREW)
HOLES_RIVNUT = holes(HOLE_RIVNUT)

TOP_LAYER = CASE_OUTLINE - top_cutouts() - HOLES_SCREW

SWITCH_PLATE = (roundoff(FLAT_OUTLINE - SIDE_INSET, SIDE_RADIUS)
                - NOTCH_CUTOUT - HOLES_SCREW) # - plate_cutouts())

HOLES_SCREW_RIVNUT = rear_half(HOLES_SCREW) + front_half(HOLES_RIVNUT)
BASE_LAYER = CASE_OUTLINE - daughterboard_holes() - HOLES_SCREW_RIVNUT

FLAT_WALLS = FLAT_OUTLINE - FLAT_INTERIOR - SIDE_INSET + hole_support_2d()
WALLS = roundoff(FLAT_WALLS, HOLE_MENISCUS, SIDE_RADIUS) - NOTCH_CUTOUT

WALLS_SCREW = WALLS - HOLES_SCREW
WALLS_RIVNUT = WALLS - HOLES_RIVNUT
FRONT_WALL_SCREW = front_half(WALLS_SCREW)
FRONT_WALL_RIVNUT = front_half(WALLS_RIVNUT)
REAR_WALL_SCREW = rear_half(WALLS_SCREW)
REAR_WALL_SOCKET = REAR_WALL_SCREW - SOCKET_CUTOUT

layers = [
    (TOP_LAYER,), # 0
    (FRONT_WALL_SCREW, REAR_WALL_SCREW), # 1
    (FRONT_WALL_SCREW, REAR_WALL_SCREW), # 2
    (SWITCH_PLATE,), # 3
    (FRONT_WALL_RIVNUT, REAR_WALL_SCREW), # 4
    (FRONT_WALL_RIVNUT, REAR_WALL_SOCKET), # 5
    (FRONT_WALL_RIVNUT, REAR_WALL_SOCKET), # 6
    (BASE_LAYER,), # 7
]

spread = []

if MODE == "test":
    pass

elif MODE == "perspex":
    for i in range(len(layers)):
        if i % 2 == 1:
            pass
        elif len(layers[i]) == 2:
            (front, rear) = layers[i]
            move = SPREAD * (i / 2)
            spread += [ Location((0, +move)) * rear,
                       Location((0, -move)) * front ]
        elif i == 0:
            spread += [ layers[i][0] ]

elif MODE == "plate":
    for i in range(len(layers)):
        if i % 2 == 0:
            pass
        elif len(layers[i]) == 2:
            (front, rear) = layers[i]
            move = SPREAD * (i / 4 + 0.75) + CLIP_DEPTH/2
            spread += [ Location((0, +move)) * rear,
                        Location((0, -move)) * front ]
        elif i == 3:
            spread += [ Location((0, -CLIP_DEPTH/2)) * layers[i][0] ]
        elif i == 7:
            spread += [ Location((0, +CLIP_DEPTH/2)) * layers[i][0] ]

show_object(spread)
