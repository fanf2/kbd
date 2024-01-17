from build123d import *

# dunno why it can't find `logging` via the previous import
import build123d
log = build123d.logging.getLogger("build123d")

log.info("hello!")

EXPLODE = 5

SPREAD = 10

# vertical measurements in mm

PERSPEX_THICK = 3.0
PLATE_THICK = 1.5   # 0.06 in
PCB_THICK = 1.6     # 1.2 is minimum allowed by kailh socket knobs
COMPONENTS_THICK = 2.0

# horizontal measurements in mm

KEY_UNIT = 19.05

def ku(n):
    return KEY_UNIT * n

MX_PLATE_HOLE	= 14.0

MX_PLATE_RIB	= KEY_UNIT - MX_PLATE_HOLE

MX_STAB_WIDTH	= 7
MX_STAB_DEPTH	= 16

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

ACCENT_CLEAR	= 0.2

TOTAL_WIDTH	= MAIN_WIDTH + (BLOCK_GAP + FUN_WIDTH + CASE_SIDE) * 2
TOTAL_DEPTH	= MAIN_DEPTH + CASE_FRONT + CASE_REAR

MIDDLE_WIDTH	= MAIN_WIDTH - ku(2.0)
ELLIPSE_AXIS	= ku(7.0)

# a little clearance
CLIP_WIDTH	= TOTAL_WIDTH + 1
CLIP_DEPTH	= TOTAL_DEPTH + 1

# round off sharp corners
SIDE_RADIUS	= 0.5

# visible extent of side accent
SIDE_DEPTH	= 1 # placeholder
# depth of cutout for side accent
SIDE_NOTCH_D	= 1 # placeholder
# side accent sized to fit notches
SIDE_ACCENT_D	= 1 # placeholder

# this cutout rectangle sticks out by MX_PLATE_RIB/2
SIDE_INSET_W	= CASE_SIDE
SIDE_INSET_X	= TOTAL_WIDTH/2 + MX_PLATE_RIB/2 - SIDE_INSET_W/2

SIDE_ACCENT_X	= TOTAL_WIDTH/2 - SIDE_THICK/2

# key block positions

MAIN_Y		= CASE_FRONT / 2 - CASE_REAR / 2

FUN_X		= MAIN_WIDTH / 2 + BLOCK_GAP + FUN_WIDTH / 2
FUN_Y1		= MAIN_Y + MAIN_DEPTH / 2 - BLOCK_GAP - FUN_DEPTH / 2
FUN_Y2		= FUN_Y1 - BLOCK_GAP - FUN_DEPTH

# fasteners

HOLE_SMALL	= 3.2 # m3 screw diameter
HOLE_LARGE	= 5.2 # m3 rivnut barrel
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

def multiocular_vertices(vertices):
    cs = [ Location(v.center()) for v in vertices ]
    iris = [ c * Circle(2) for c in cs ]
    pupil = [ c * Circle(1) for c in cs ]
    return Sketch() + iris - pupil

def side_length(shape):
    return shape.edges().sort_by(Axis.X)[0].length

def classify_vertex(shape, vertex):
    circle = Location(vertex.center()) * Circle(0.25)
    chomp = shape & circle
    return chomp.area / circle.area

def meniscus(shape, vertex, radius):
    vertex = vertex.center()
    circle = Location(vertex) * Circle(radius)
    chomp = shape & circle
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
        return
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
        return
    curve = make_face(curve)
    if chomp.area / circle.area > 0.5:
        return curve
    else:
        return circle - curve

def case_outline():
    middle = Rectangle(MIDDLE_WIDTH, TOTAL_DEPTH)

    # dunno why i need to explicitly convert these to locations
    edges = middle.edges()
    left = Location(edges[0].center())
    right = Location(edges[2].center())

    ellipse = Ellipse(ELLIPSE_AXIS, TOTAL_DEPTH / 2)
    left = left * ellipse
    right = right * ellipse
    oval = left + middle + right

    clip = Rectangle(TOTAL_WIDTH, CLIP_DEPTH)

    return oval & clip

def rear_half():
    return Location((0, CLIP_DEPTH/2)) * Rectangle(CLIP_WIDTH, CLIP_DEPTH/2)

def case_interior(outline):
    interior = offset(outline, amount=-WALL_THICK)
    # re-clip so that the side walls are thicker
    return interior & Rectangle(TOTAL_WIDTH - SIDE_THICK * 2, CLIP_DEPTH)

def set_side_depth(outline):
    global SIDE_DEPTH
    global SIDE_NOTCH_D
    global SIDE_ACCENT_D
    SIDE_DEPTH = side_length(outline) - WALL_THICK*2
    # notch depth comes from corner s-bend
    SIDE_ACCENT_D = SIDE_DEPTH + SIDE_RADIUS*2
    SIDE_NOTCH_D = SIDE_ACCENT_D + SIDE_RADIUS*2

def set_hole_positions(interior):
    global HOLE_Y2
    global HOLE_POSITIONS
    clip = Rectangle(HOLE_X2 * 2, CLIP_DEPTH)
    HOLE_Y2 = side_length(interior & clip) / 2
    HOLE_POSITIONS = [ Location(p)
                       for i in [-1,+1]
                       for j in [-1,+1]
                       for p in [(i*HOLE_X1, j*HOLE_Y1),
                                 (i*HOLE_X2, j*HOLE_Y2)] ]

def holes(diameter):
    hole = Circle(diameter / 2)
    return [ pos * hole for pos in HOLE_POSITIONS ]

def side_inset():
    inset = Rectangle(SIDE_INSET_W, SIDE_DEPTH)
    insets = (Location((-SIDE_INSET_X, 0)) * inset +
              Location((+SIDE_INSET_X, 0)) * inset)
    accent = RectangleRounded(
        PERSPEX_THICK + ACCENT_CLEAR, SIDE_NOTCH_D, SIDE_RADIUS)
    accents = (Location((-SIDE_ACCENT_X, 0)) * accent +
               Location((+SIDE_ACCENT_X, 0)) * accent)
    return insets + accents

def perspex(shape):
    return extrude(shape, amount=PERSPEX_THICK)

def plate(shape):
    return extrude(shape, amount=PLATE_THICK)

# round off vertices
def wall_rounded(wall):
    mouths = []
    ears = []
    for v in wall.vertices():
        kind = classify_vertex(wall, v)
        if kind < 0.33:
            m = meniscus(wall, v, SIDE_RADIUS)
            if m: ears.append(m)
            else: log.info("wat")
        elif kind > 0.66:
            m = meniscus(wall, v, HOLE_MENISCUS)
            if m: mouths.append(m)
            else: log.info("wat")
    # still puzzled why it doesn't work in 2D
    w = (extrude(wall, amount=1)
         + extrude(Sketch() + mouths, amount=1)
         - extrude(Sketch() + ears, amount=1))
    # extract the 2d face we wanted
    return w.faces().sort_by(Axis.Z)[0]

# round off vertices
def wall_socket(wall):
    usbdb = RectangleRounded(USBDB_WIDTH, USBDB_DEPTH, USBDB_R)
    inset = Rectangle(USB_WIDTH, USB_INSET*2)
    cutout = (Location((0, USBDB_Y)) * offset(usbdb, USB_CLEAR)
              + Location((0, TOTAL_DEPTH/2)) * inset)
    # yet again it doesn't work in 2D
    thick = extrude(wall, amount=1) - extrude(cutout, amount=2, both=True)
    bottom = thick.faces().group_by(Axis.Z)[0]
    return bottom[0] + bottom[1]

CASE_OUTLINE = case_outline()
CASE_INTERIOR = case_interior(CASE_OUTLINE)

set_hole_positions(CASE_INTERIOR)
set_side_depth(CASE_OUTLINE)

SIDE_INSET = side_inset()

WALLS = CASE_OUTLINE - CASE_INTERIOR - SIDE_INSET + holes(HOLE_SUPPORT)

WALL = wall_rounded(WALLS & rear_half())

# perspex walls: 1 above switch plate, 2 below
# plate walls: 1 above switch plate, 1 below
# front walls below plate use large holes, rest are small
# one perspex wall and one plate wall have USB cutouts

WALL_UPPER = WALL - holes(HOLE_SMALL)
WALL_LOWER = WALL - holes(HOLE_LARGE)

# all rear walls have small holes
WALL_BOTTOM = wall_socket(WALL_UPPER)

if True:
    walls = [
        WALL_UPPER, # front above
        WALL_LOWER, # front below
        WALL_LOWER, # front below
        WALL_UPPER, # rear above
        WALL_UPPER, # rear below
        WALL_BOTTOM, # rear below
    ]
    spread = [ Location((0, SPREAD * i)) * extrude(walls[i], amount=1)
               for i in range(len(walls)) ]
    show_object(Part() + spread)
