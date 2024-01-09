from build123d import *

# dunno why it can't find `logging` via the previous import
import build123d
log = build123d.logging.getLogger("build123d")

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

BLOCK_GAP	= ku(  0.25 )

CASE_SIDE	= ku(  1.00 ) - BLOCK_GAP
CASE_FRONT	= ku(  0.50 )
CASE_REAR	= ku(  1.00 )

MAIN_WIDTH	= ku( 15.00 )
MAIN_DEPTH	= ku(  5.00 )
MAIN_Y		= CASE_FRONT / 2 - CASE_REAR / 2

FUNC_WIDTH	= ku(  3.00 )
FUNC_DEPTH	= ku(  2.00 )
FUNC_X		= MAIN_WIDTH / 2 + BLOCK_GAP + FUNC_WIDTH / 2
FUNC_Y1		= MAIN_Y + MAIN_DEPTH / 2 - BLOCK_GAP - FUNC_DEPTH / 2
FUNC_Y2		= FUNC_Y1 - BLOCK_GAP - FUNC_DEPTH

TOTAL_WIDTH	= MAIN_WIDTH + (BLOCK_GAP + FUNC_WIDTH + CASE_SIDE) * 2
TOTAL_DEPTH	= MAIN_DEPTH + CASE_FRONT + CASE_REAR

MIDDLE_WIDTH	= MAIN_WIDTH - ku(3)
ELLIPSE_AXIS	= ku( 7.50 )

def EllipseOutline():
    middle = Rectangle(MIDDLE_WIDTH, TOTAL_DEPTH)

    # dunno why i need to explicitly convert these to locations
    edges = middle.edges()
    left = Location(edges[0].center())
    right = Location(edges[2].center())

    ellipse = Ellipse(ELLIPSE_AXIS, TOTAL_DEPTH / 2)
    left = left * ellipse
    right = right * ellipse

    outline = left + middle + right

    clip = Rectangle(TOTAL_WIDTH, TOTAL_DEPTH)
    outline = outline & clip

    main_block = (
        Location((0, MAIN_Y, 0))
        * Rectangle(MAIN_WIDTH, MAIN_DEPTH)
    )

    func_block = Rectangle(FUNC_WIDTH, FUNC_DEPTH)
    func_n1 = Location((-FUNC_X, FUNC_Y1, 0)) * func_block
    func_n2 = Location((-FUNC_X, FUNC_Y2, 0)) * func_block
    func_p1 = Location((+FUNC_X, FUNC_Y1, 0)) * func_block
    func_p2 = Location((+FUNC_X, FUNC_Y2, 0)) * func_block
    func_blocks = func_n1 + func_n2 + func_p1 + func_p2

    one_key = Rectangle(ku(1), ku(1))
    blocker1 = Location((FUNC_X - ku(1), FUNC_Y2 + ku(0.5), 0)) * one_key
    blocker2 = Location((FUNC_X + ku(1), FUNC_Y2 + ku(0.5), 0)) * one_key
    arrow_blockers = blocker1 + blocker2

    outline = outline - main_block - func_blocks + arrow_blockers

    return outline

outline = EllipseOutline()
show_object(outline)
