import build123d as bd

log = bd.logging.getLogger("build123d")
log.addHandler(bd.logging.NullHandler())

log.info("hello!")

# measurements in mm

KEY_UNIT = 19.05

def ku(n):
    return KEY_UNIT * n

PLATE_THICK = 1.5   # 0.06 in
PCB_THICK = 1.5     # minimum allowed by kailh socket knobs

# relative to top of the pcb
MX_BODY_HEIGHT = 11.6
MX_PLATE_HEIGHT = 5.0
MX_PIN_LENGTH = 3.3

PCB_PLATE_GAP = MX_PLATE_HEIGHT - PLATE_THICK


# key block layout

MAIN_WIDTH	= ku( 15.00 )
MAIN_DEPTH	= ku(  5.00 )

BLOCK_GAP	= ku(  0.25 )

CASE_SIDE	= ku(  1.00 ) - BLOCK_GAP
CASE_FRONT	= ku(  0.50 )
CASE_REAR	= ku(  1.00 )

FUNC_WIDTH	= ku(  3.00 )
FUNC_DEPTH	= ku(  2.00 )

FUNC_REAR	= CASE_REAR + BLOCK_GAP
FUNC_FRONT	= CASE_FRONT + MAIN_DEPTH - (BLOCK_GAP + FUNC_DEPTH) * 2

TOTAL_WIDTH	= MAIN_WIDTH + (BLOCK_GAP + FUNC_WIDTH + CASE_SIDE) * 2
TOTAL_DEPTH	= MAIN_DEPTH + CASE_FRONT + CASE_REAR

MIDDLE_WIDTH	= MAIN_WIDTH - ku(3)
ELLIPSE_AXIS	= ku(  7.50 )


def EllipseOutline():
    middle = bd.Rectangle(MIDDLE_WIDTH, TOTAL_DEPTH)
    edges = middle.edges()
    left = bd.Location(edges[0].center())
    right = bd.Location(edges[2].center())
    ellipse = bd.Ellipse(ELLIPSE_AXIS, TOTAL_DEPTH / 2)
    wideboy = middle + left * ellipse + right * ellipse
    outline = bd.Rectangle(TOTAL_WIDTH, TOTAL_DEPTH)
    return wideboy.intersect(outline)

outline = EllipseOutline()
show_object(outline)
