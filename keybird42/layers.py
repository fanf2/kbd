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

TOTAL_WIDTH	= MAIN_WIDTH + (BLOCK_GAP + FUN_WIDTH + CASE_SIDE) * 2
TOTAL_DEPTH	= MAIN_DEPTH + CASE_FRONT + CASE_REAR

MIDDLE_WIDTH	= MAIN_WIDTH - ku(2.0)
ELLIPSE_AXIS	= ku(7.0)

CLIP_DEPTH	= TOTAL_DEPTH + 1 # a little clearance

SIDE_DEPTH	= ku(1) # placeholder

# the cutout rectangle sticks out by MX_PLATE_RIB/2
SIDE_INSET_W	= CASE_SIDE
SIDE_INSET_X	= TOTAL_WIDTH/2 + MX_PLATE_RIB/2 - SIDE_INSET_W/2

# key block positions

MAIN_Y		= CASE_FRONT / 2 - CASE_REAR / 2

FUN_X		= MAIN_WIDTH / 2 + BLOCK_GAP + FUN_WIDTH / 2
FUN_Y1		= MAIN_Y + MAIN_DEPTH / 2 - BLOCK_GAP - FUN_DEPTH / 2
FUN_Y2		= FUN_Y1 - BLOCK_GAP - FUN_DEPTH

# fasteners

HOLE_SMALL	= 3.2
HOLE_BIG	= 5.2
HOLE_SUPPORT	= 2 * WALL_THICK

HOLE_X1		= ku( 3.50 )
HOLE_X2		= ku( 9.25 )

HOLE_Y1		= 0 # placeholder
HOLE_Y2		= 0 # placeholder

# connector holes

USB_INSET	= 1.0
USB_WIDTH	= 8.5 # spec says 8.34
USB_CLEAR	= 0.5
USBDB_WIDTH	= 18
USBDB_DEPTH	= 18
USBDB_R		= 1.0
USBDB_Y		= TOTAL_DEPTH/2 - USBDB_DEPTH/2 - USB_CLEAR/2 - USB_INSET

def multiocular_vertices(shape):
    cs = [ Location(v.center()) for v in shape.vertices() ]
    iris = [ c * Circle(2) for c in cs ]
    pupil = [ c * Circle(1) for c in cs ]
    return Sketch() + iris - pupil

def meniscus(shape, vertex, radius):
    vertex = vertex.center()
    chomp = shape & Location(vertex) * Circle(radius)
    log.info(chomp.show_topology())
    r0 = [ (e, e @ 0, e % 0)
           for e in chomp.edges() if e @ 1 == vertex ]
    r1 = [ (e, e @ 1, -(e % 1))
           for e in chomp.edges() if e @ 0 == vertex ]
    radii = r0 + r1
    log.info(radii)
    if len(radii) != 2:
        log.info("meniscus requires 2 radial edges")
        return
    (e0, p0, t0) = radii[0]
    (e1, p1, t1) = radii[1]
    c0 = p0 + t0
    c1 = p1 + t1
    e2 = Bezier(p0, p0 + t0, p1 + t1, p1)
    meniscus = Curve() + e0 + e1 + e2
    log.info(meniscus)
    show_object(meniscus)
    log.info(meniscus.show_topology())
    show_object(shape + make_face(meniscus))

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

def side_depth(outline):
    side = outline.edges().sort_by(Axis.X)[0]
    return side.length - WALL_THICK * 2

def case_walls(outline):
    inset = offset(outline, amount=-WALL_THICK)
    # side walls are thicker
    inset = inset & Rectangle(TOTAL_WIDTH - SIDE_THICK * 2, CLIP_DEPTH)

    side = Rectangle(SIDE_INSET_W, SIDE_DEPTH)
    sides = (Location((-SIDE_INSET_X, 0)) * side +
             Location((+SIDE_INSET_X, 0)) * side)

    return outline - inset - sides

CASE_OUTLINE = case_outline()

SIDE_DEPTH = side_depth(CASE_OUTLINE)

WALLS = case_walls(CASE_OUTLINE)

v = WALLS.vertices().group_by(Axis.X)[-2].sort_by(Axis.Y)[-1]
meniscus(WALLS, v, 2)

#show_object(WALLS)
