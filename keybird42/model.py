from build123d import *

# dunno why it can't find `logging` via the previous import
import build123d
log = build123d.logging.getLogger("build123d")

log.info("hello!")

EXPLODE = 10

# vertical measurements in mm

PERSPEX_THICK = 3.0
PLATE_THICK = 1.5   # 0.06 in
PCB_THICK = 1.6     # 1.2 is minimum allowed by kailh socket knobs

# relative to top of the pcb
MX_BODY_HEIGHT = 11.6
MX_PLATE_HEIGHT = 5.0
MX_PIN_LENGTH = 3.3

PCB_PLATE_GAP = MX_PLATE_HEIGHT - PLATE_THICK

# horizontal measurements in mm

KEY_UNIT = 19.05

def ku(n):
    return KEY_UNIT * n

MX_PLATE_HOLE	= 14.0

# (0.484+0.004 - 0.26+0.004) * 25.4 == 5.9 mm
MX_STAB_ABOVE	= 6
# (0.53+0.006) * 25.4 == 13.6 mm; 13.6 - 5.9 == 7.7 mm
MX_STAB_BELOW	= 8

MX_STAB_WIDTH	= 7
MX_STAB_DEPTH	= MX_STAB_BELOW + MX_STAB_ABOVE
MX_STAB_Y	= MX_STAB_BELOW / 2 - MX_STAB_ABOVE / 2

INNER_FILLET	= 1.0
OUTER_FILLET	= 1.0

# key block layout

BLOCK_GAP	= ku( 0.25 )

CASE_SIDE	= ku( 1.00 ) - BLOCK_GAP
CASE_FRONT	= ku( 0.50 )
CASE_REAR	= ku( 1.00 )

SIDE_THICK	= ku( 0.25 )

CHEEK_WIDTH	= ku( 0.50 )
CHEEK_DEPTH	= ku( 4.00 )
CHEEK_THICK	= 3
CHEEK_NOTCH	= 4
CHEEK_CLEAR	= 0.2

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

MIDDLE_WIDTH	= MAIN_WIDTH - ku(2.0)
ELLIPSE_AXIS	= ku( 7.0 )

class plate_cutout:
    k100 = Rectangle(MX_PLATE_HOLE, MX_PLATE_HOLE)

    stab = Rectangle(MX_STAB_WIDTH, MX_STAB_DEPTH)
    def balance(stab, width):
        return (Location((-ku(width - 1) / 2, MX_STAB_Y)) * stab +
                Location((+ku(width - 1) / 2, MX_STAB_Y)) * stab)

    k125 = k100
    k150 = k100
    k175 = k100
    k225 = k100 + balance(stab, 2.25)
    k700 = k100 + balance(stab, 7.00)

class keycaps:

    def keycap(width):
        return Rectangle(ku(width) + 0.1, ku(1) + 0.1)

    k100 = keycap(1.00)
    k125 = keycap(1.25)
    k150 = keycap(1.50)
    k175 = keycap(1.75)
    k225 = keycap(2.25)
    k700 = keycap(7.00)

def key_matrix(keys):

    def key_row(width):
        return GridLocations(ku(1), ku(1), width, 1)

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

    oval = left + middle + right

    clip = Rectangle(TOTAL_WIDTH, TOTAL_DEPTH)

    return oval & clip

def screw_holes(diameter):
    return [ Location((ku(x*i), ku(y*j))) * Circle(diameter/2)
             for (x,y) in [(3.5,3.0), (9.25, 2.75)]
             for i in [-1, +1]
             for j in [-1, +1]]

def side_walls():
    thicker = (Location((TOTAL_WIDTH/2 - CHEEK_WIDTH/2, 0))
               * Rectangle(CHEEK_WIDTH, CHEEK_DEPTH + ku(0.5)))
    return thicker + mirror(thicker, Plane.YZ)

def side_cutout():
    cutout = (Location((TOTAL_WIDTH/2 - CHEEK_WIDTH/2, 0))
              * Rectangle(CHEEK_WIDTH + CHEEK_CLEAR, CHEEK_DEPTH))
    notch_thick = CHEEK_THICK + CHEEK_CLEAR
    notch_x = TOTAL_WIDTH/2 - CHEEK_THICK - notch_thick / 2
    notch = Ellipse(notch_thick/2, CHEEK_NOTCH/2)
    top_notch = Location((notch_x, +CHEEK_DEPTH / 2)) * notch
    bot_notch = Location((notch_x, -CHEEK_DEPTH / 2)) * notch
    cutout += top_notch + bot_notch
    cutout += mirror(cutout, Plane.YZ)
    return cutout

outline = ellipse_outline()

small_holes = screw_holes(3.2)
large_holes = screw_holes(5.2)
hole_support = screw_holes(7.7)

cheeks = side_cutout()

# TODO: fillet inner corners of top_perspex

top_perspex	= outline - small_holes - key_matrix(keycaps)
top_perspex	= extrude(top_perspex, amount=PERSPEX_THICK)

switch_plate	= outline - small_holes - key_matrix(plate_cutout) - cheeks
switch_plate	= extrude(switch_plate, amount=PLATE_THICK)

base_plate	= outline - large_holes
base_plate	= extrude(base_plate, amount=PLATE_THICK)

# TODO: fillet inner corners of side_walls()

inset = offset(outline, amount=-SIDE_THICK)
wall = outline - inset + hole_support + side_walls() - cheeks

lower_wall = wall - large_holes
upper_wall = wall - small_holes

lower_perspex	= extrude(lower_wall, amount=PERSPEX_THICK)
lower_plate	= extrude(lower_wall, amount=PLATE_THICK)

upper_perspex	= extrude(upper_wall, amount=PERSPEX_THICK)
upper_plate	= extrude(upper_wall, amount=PLATE_THICK)

layers = (Location((0,0, EXPLODE * 0.0)) * base_plate +
          Location((0,0, EXPLODE * 1.5)) * lower_perspex +
          Location((0,0, EXPLODE * 4.5)) * lower_plate +
          Location((0,0, EXPLODE * 6.0)) * lower_perspex +
          Location((0,0, EXPLODE * 9.0)) * switch_plate +
          Location((0,0, EXPLODE* 10.5)) * upper_perspex +
          Location((0,0, EXPLODE* 13.5)) * upper_plate +
          Location((0,0, EXPLODE* 15.0)) * top_perspex)

# fillet outer corners
edges = layers.edges().filter_by(Axis.Z).group_by(Axis.X)
layers = fillet(edges[-1] + edges[+0], radius=OUTER_FILLET)

show_object(layers)
