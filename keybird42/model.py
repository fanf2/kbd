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
MX_PLATE_HOLE = 14.0

PCB_PLATE_GAP = MX_PLATE_HEIGHT - PLATE_THICK


# key block layout

BLOCK_GAP	= ku( 0.25 )

CASE_SIDE	= ku( 1.00 ) - BLOCK_GAP
CASE_FRONT	= ku( 0.50 )
CASE_REAR	= ku( 1.00 )

KEYS_WIDE	= 15
KEYS_DEEP	= 5

MAIN_WIDTH	= KEY_UNIT * KEYS_WIDE
MAIN_DEPTH	= KEY_UNIT * KEYS_DEEP
MAIN_Y		= CASE_FRONT / 2 - CASE_REAR / 2

FUN_WIDTH	= ku( 3.00 )
FUN_DEPTH	= ku( 2.00 )
FUN_X		= MAIN_WIDTH / 2 + BLOCK_GAP + FUN_WIDTH / 2
FUN_Y1		= MAIN_Y + MAIN_DEPTH / 2 - BLOCK_GAP - FUN_DEPTH / 2
FUN_Y2		= FUN_Y1 - BLOCK_GAP - FUN_DEPTH

TOTAL_WIDTH	= MAIN_WIDTH + (BLOCK_GAP + FUN_WIDTH + CASE_SIDE) * 2
TOTAL_DEPTH	= MAIN_DEPTH + CASE_FRONT + CASE_REAR

MIDDLE_WIDTH	= MAIN_WIDTH - ku(3)
ELLIPSE_AXIS	= ku( 7.50 )

class plate_cutout:
    k100 = Rectangle(MX_PLATE_HOLE, MX_PLATE_HOLE)
    k125 = k100
    k150 = k100
    k175 = k100
    k225 = k100
    k700 = k100

def key_row(width):
    return GridLocations(ku(1), ku(1), width, 1)

def key_matrix(keys):

    stagger = -ku(0.25)

    space = Location((0, MAIN_Y - ku(2))) * keys.k700

    key1 = Location((0, MAIN_Y + ku(2))) * keys.k100
    row1 = [ loc * key1 for loc in key_row(KEYS_WIDE) ]

    key2 = Location((0, MAIN_Y + ku(1))) * keys.k100
    row2 = [ loc * key2 for loc in key_row(KEYS_WIDE - 3) ]

    key3 = Location((stagger, MAIN_Y)) * keys.k100
    row3 = [ loc * key3 for loc in key_row(KEYS_WIDE - 4) ]

    key4 = Location((stagger, MAIN_Y - ku(1))) * keys.k100
    row4 = [ loc * key4 for loc in key_row(KEYS_WIDE - 5) ]

    rows = row1 + row2 + row3 + row4

    fun_block = GridLocations(ku(1), ku(1), 3, 2)

    key5 = Location((-FUN_X, FUN_Y1)) * keys.k100
    fun1 = [ loc * key5 for loc in fun_block ]

    key6 = Location((-FUN_X, FUN_Y2)) * keys.k100
    fun2 = [ loc * key6 for loc in fun_block ]

    key7 = Location((+FUN_X, FUN_Y1)) * keys.k100
    fun3 = [ loc * key7 for loc in fun_block ]

    key_hi = Location((+FUN_X, FUN_Y2 + ku(0.5))) * keys.k100
    key_lo = Location((+FUN_X, FUN_Y2 - ku(0.5))) * keys.k100
    arrows = [key_hi] + [ loc * key_lo for loc in key_row(3) ]

    funs = fun1 + fun2 + fun3 + arrows

    l = -MAIN_WIDTH / 2
    r = +MAIN_WIDTH / 2

    modifiers = [
        Location((l + ku(1.50/2), MAIN_Y + ku(1))) * keys.k150,
        Location((l + ku(1.75/2), MAIN_Y + ku(0))) * keys.k175,
        Location((l + ku(2.25/2), MAIN_Y - ku(1))) * keys.k225,
        Location((l + ku(1.25/2), MAIN_Y - ku(2))) * keys.k125,
        Location((l + ku(1.25/2 + 1.25), MAIN_Y - ku(2))) * keys.k125,
        Location((l + ku(1.50/2 + 2.50), MAIN_Y - ku(2))) * keys.k150,
        Location((r - ku(1.50/2), MAIN_Y + ku(1))) * keys.k150,
        Location((r - ku(2.25/2), MAIN_Y + ku(0))) * keys.k225,
        Location((r - ku(1.00/2), MAIN_Y - ku(1))) * keys.k100,
        Location((r - ku(1.25/2), MAIN_Y - ku(2))) * keys.k125,
        Location((r - ku(1.75/2 + 1.00), MAIN_Y - ku(1))) * keys.k175,
        Location((r - ku(1.25/2 + 1.25), MAIN_Y - ku(2))) * keys.k125,
        Location((r - ku(1.50/2 + 2.50), MAIN_Y - ku(2))) * keys.k150,
    ]

    matrix = space + modifiers + rows + funs

    return matrix

def ellipse_outline():
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
        Location((0, MAIN_Y))
        * Rectangle(MAIN_WIDTH, MAIN_DEPTH)
    )

    fun_block = Rectangle(FUN_WIDTH, FUN_DEPTH)
    fun_n1 = Location((-FUN_X, FUN_Y1)) * fun_block
    fun_n2 = Location((-FUN_X, FUN_Y2)) * fun_block
    fun_p1 = Location((+FUN_X, FUN_Y1)) * fun_block
    fun_p2 = Location((+FUN_X, FUN_Y2)) * fun_block
    fun_blocks = fun_n1 + fun_n2 + fun_p1 + fun_p2

    one_key = Rectangle(ku(1), ku(1))
    blocker1 = Location((FUN_X - ku(1), FUN_Y2 + ku(0.5))) * one_key
    blocker2 = Location((FUN_X + ku(1), FUN_Y2 + ku(0.5))) * one_key
    arrow_blockers = blocker1 + blocker2

    outline = outline - main_block - fun_blocks + arrow_blockers

    return outline

sketch = ellipse_outline()

matrix = key_matrix(plate_cutout)

sketch = sketch + matrix

show_object(sketch)
