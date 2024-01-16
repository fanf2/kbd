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
        log.info(chomp.show_topology())
        log.info(radius)
        log.info(radii)
        return
    (p0, t0) = radii[0]
    (p1, t1) = radii[1]
    e = Bezier(p0, p0 + t0, p1 + t1, p1)
    edges = Curve() + e + edges
    meniscus = make_face(edges)
    if chomp.area * 2 < circle.area:
        meniscus = circle - meniscus
    return meniscus

def quadrants(shape):
    shape += mirror(shape, Plane.XZ)
    shape += mirror(shape, Plane.YZ)
    return shape

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

    ring = outline - inset

    v = ring.vertices().group_by(Axis.X)[-2].sort_by(Axis.Y)[-1]
    inner = quadrants(meniscus(ring, v, WALL_THICK / 2))

    side = Rectangle(SIDE_INSET_W, SIDE_DEPTH)
    sides = (Location((-SIDE_INSET_X, 0)) * side +
             Location((+SIDE_INSET_X, 0)) * side)

    walls = ring + inner

    vs = walls.vertices().group_by(Axis.X)[0]
    outer = quadrants(meniscus(ring, vs[0], WALL_THICK / 4) +
                      meniscus(ring, vs[1], WALL_THICK / 4))

    return walls - outer - sides

CASE_OUTLINE = case_outline()

SIDE_DEPTH = side_depth(CASE_OUTLINE)

WALLS = case_walls(CASE_OUTLINE)

log.info(WALLS.show_topology())

show_object(WALLS)
