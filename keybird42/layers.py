from build123d import *

# dunno why it can't find `logging` via the previous import
import build123d
log = build123d.logging.getLogger("build123d")

log.info("hello!")

EXPLODE = 5

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
HOLE_BIG	= 5.2 # m3 rivnut barrel
HOLE_SUPPORT	= WALL_THICK*2
HOLE_MENISCUS	= WALL_THICK/2

HOLE_X1		= ku( 3.50 )
HOLE_X2		= ku( 9.25 )

HOLE_Y1		= TOTAL_DEPTH/2 - WALL_THICK
HOLE_Y2		= 0 # placeholder

# connector holes

USB_INSET	= 1.0
USB_WIDTH	= 8.5 # spec says 8.34
USB_CLEAR	= 0.5
USBDB_WIDTH	= 18
USBDB_DEPTH	= 18
USBDB_R		= 1.0
USBDB_Y		= TOTAL_DEPTH/2 - USBDB_DEPTH/2 - USB_CLEAR/2 - USB_INSET

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
    edges = []
    radii = []
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
        log.info(vertex)
        log.info(radius)
        log.info(radii)
        return
    (p0, t0) = radii[0]
    (p1, t1) = radii[1]
    e = Bezier(p0, p0 + t0, p1 + t1, p1)
    edges = Curve() + e + edges
    meniscus = make_face(edges)
    if chomp.area * 2 < circle.area:
        meniscus = make_face(circle - meniscus)
    return meniscus

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

def hole_positions(interior):
    global HOLE_Y2
    clip = Rectangle(HOLE_X2 * 2, CLIP_DEPTH)
    HOLE_Y2 = side_length(interior & clip) / 2
    return [ Location(p) for p in [
        (-HOLE_X2, HOLE_Y2),
        (-HOLE_X1, HOLE_Y1),
        (+HOLE_X1, HOLE_Y1),
        (+HOLE_X2, HOLE_Y2) ]]

def side_inset():
    inset = Rectangle(SIDE_INSET_W, SIDE_DEPTH)
    insets = (Location((-SIDE_INSET_X, 0)) * inset +
              Location((+SIDE_INSET_X, 0)) * inset)
    accent = RectangleRounded(
        PERSPEX_THICK + ACCENT_CLEAR, SIDE_NOTCH_D, SIDE_RADIUS)
    accents = (Location((-SIDE_ACCENT_X, 0)) * accent +
               Location((+SIDE_ACCENT_X, 0)) * accent)
    return insets + accents

def basic_wall(outline, interior, holepos, side_inset):
    walls = outline - interior - side_inset

    choose = Location((0, CLIP_DEPTH/2)) * Rectangle(CLIP_WIDTH, CLIP_DEPTH/2)
    wall = ShapeList(walls.get_type(Face)).sort_by(Axis.Y)[-1]

    hole = Circle(HOLE_SUPPORT / 2)
    holes = [ pos * hole for pos in holepos ]

    return wall + holes

# round off vertices
def wall_rounded(wall):
    mouths = []
    ears = []
    for v in wall.vertices():
        kind = classify_vertex(wall, v)
        if kind < 0.33:
            m = meniscus(wall, v, SIDE_RADIUS)
            if m: ears.append(m)
        elif kind > 0.66:
            m = meniscus(wall, v, HOLE_MENISCUS)
            if m: mouths.append(m)
    show_object(Sketch() + ears)
    show_object(Sketch() + mouths)

CASE_OUTLINE = case_outline()
CASE_INTERIOR = case_interior(CASE_OUTLINE)
HOLE_POSITIONS = hole_positions(CASE_INTERIOR)

set_side_depth(CASE_OUTLINE)
SIDE_INSET = side_inset()

WALL = basic_wall(CASE_OUTLINE, CASE_INTERIOR, HOLE_POSITIONS, SIDE_INSET)

log.info(WALL.show_topology())

show_object(WALL)

wall_rounded(WALL)
