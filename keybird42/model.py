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

MX_PLATE_RIB	= KEY_UNIT - MX_PLATE_HOLE

# (0.484+0.004 - 0.26+0.004) * 25.4 == 5.9 mm
MX_STAB_BELOW	= 6
# (0.53+0.006) * 25.4 == 13.6 mm; 13.6 - 5.9 == 7.7 mm
MX_STAB_ABOVE	= 8

MX_STAB_WIDTH	= 7
MX_STAB_DEPTH	= MX_STAB_BELOW + MX_STAB_ABOVE
MX_STAB_Y	= MX_STAB_BELOW / 2 - MX_STAB_ABOVE / 2

INNER_FILLET	= 1.0
OUTER_FILLET	= 1.0

BLOCK_GAP	= ku( 0.25 )

CASE_SIDE	= ku( 1.00 ) - BLOCK_GAP
CASE_FRONT	= ku( 0.50 )
CASE_REAR	= ku( 7/6 )

SIDE_THICK	= ku( 0.25 )

ACCENT_CLEAR	= 2 * 0.2

CHEEK_WIDTH	= ku( 0.50 )
CHEEK_DEPTH	= ku( 33/8 )
CHEEK_HEIGHT	= PERSPEX_THICK * 3 + PLATE_THICK * 3
CHEEK_NOTCH	= 2

BROW_Y		= CASE_REAR - BLOCK_GAP
BROW_T		= PERSPEX_THICK + PLATE_THICK - ACCENT_CLEAR
BROW_HEIGHT	= PERSPEX_THICK * 3 + PLATE_THICK * 1

# key block layout

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

PCB_INSET	= ku( 1/8 )
PCB_WING	= ku( 13/32 )
# space bar stab hole distance from centre
PCB_STAB	= ku( 6.00 )/2

MIDDLE_WIDTH	= MAIN_WIDTH - ku(2.0)
ELLIPSE_AXIS	= ku(7.0)

HOLE_SMALL	= 3.2
HOLE_BIG	= 5.2
HOLE_SUPPORT	= ku(0.5)

HOLE_X1		= ku( 3.50 )
HOLE_Y1		= (TOTAL_DEPTH - HOLE_SUPPORT) / 2
HOLE_X2		= ku( 9.25 )
HOLE_Y2		= HOLE_Y1 - ku(0.3)

USB_INSET	= 1.0
USB_WIDTH	= 8.5 # spec says 8.34
USB_THICK	= 1 + 3.2
USB_THIN	= 1 + 1
USB_CLEAR	= 0.5
USBDB_WIDTH	= 18
USBDB_DEPTH	= 18
USBDB_R		= 1.0
USBDB_Y		= TOTAL_DEPTH/2 - USBDB_DEPTH/2 - USB_CLEAR/2 - USB_INSET

class plate_cutout:

    stab = Rectangle(MX_STAB_WIDTH, MX_STAB_DEPTH)
    def stabs(stab, width):
        sign = -1 if width < 0 else +1
        return (Location((-ku(sign*width - 1) / 2, sign*MX_STAB_Y)) * stab +
                Location((+ku(sign*width - 1) / 2, sign*MX_STAB_Y)) * stab)

    k100 = Rectangle(MX_PLATE_HOLE, MX_PLATE_HOLE)
    k125 = k100
    k150 = k100
    k175 = k100
    k225 = k100 + stabs(stab, +2.25)
    k700 = k100 + stabs(stab, -7.00)

class keycaps:

    def keycap(width):
        return Rectangle(ku(width) + 0.1, ku(1) + 0.1)

    k100 = keycap(1.00)
    k125 = keycap(1.25)
    k150 = keycap(1.50)
    k175 = keycap(1.75)
    k225 = keycap(2.25)
    k700 = keycap(7.00)

def key_matrix(keys, top=False):

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

    key8 = Location((+FUN_X, FUN_Y2)) * keys.k100
    fun4 = [ loc * key8 for loc in fun_block ]

    key_hi = Location((+FUN_X, FUN_Y2 + ku(0.5))) * keys.k100
    key_lo = Location((+FUN_X, FUN_Y2 - ku(0.5))) * keys.k100
    arrows = [key_hi] + [ loc * key_lo for loc in key_row(3) ]

    funs = fun1 + fun2 + fun3 + (arrows if top else fun4)

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

def pcb_outline():
    pcb_front = MAIN_Y - MAIN_DEPTH/2 + PCB_INSET
    half = Polyline(*[
        (0,
         MAIN_Y + MAIN_DEPTH/2),
        (MAIN_WIDTH/2,
         MAIN_Y + MAIN_DEPTH/2),
        (MAIN_WIDTH/2 + BLOCK_GAP,
         MAIN_Y + MAIN_DEPTH/2 - BLOCK_GAP),
        (MAIN_WIDTH/2 + PCB_INSET + FUN_WIDTH,
         MAIN_Y + MAIN_DEPTH/2 - BLOCK_GAP),
        (MAIN_WIDTH/2 + PCB_INSET + FUN_WIDTH + PCB_WING,
         MAIN_Y + MAIN_DEPTH/2 - BLOCK_GAP - PCB_WING),
        (MAIN_WIDTH/2 + PCB_INSET + FUN_WIDTH + PCB_WING,
         MAIN_Y - MAIN_DEPTH/2 + PCB_INSET + BLOCK_GAP*2 + PCB_WING),
        (MAIN_WIDTH/2 + PCB_INSET + FUN_WIDTH,
         MAIN_Y - MAIN_DEPTH/2 + PCB_INSET + BLOCK_GAP*2),
        (MAIN_WIDTH/2 + PCB_INSET + BLOCK_GAP,
         MAIN_Y - MAIN_DEPTH/2 + PCB_INSET + BLOCK_GAP*2),
        (MAIN_WIDTH/2 - PCB_INSET, pcb_front),
        (PCB_STAB + PCB_INSET*2,   pcb_front),
        (PCB_STAB + PCB_INSET,     pcb_front - PCB_INSET),
        (0,                        pcb_front - PCB_INSET),
    ])
    outline = make_face(half + mirror(half, Plane.YZ))
    # dunno why this comes out upside-down
    outline = mirror(outline, Plane.XY)
    keepout = offset(outline, amount=-PCB_INSET)
    screws = (Location((+PCB_STAB, pcb_front)) * Circle(PCB_INSET) +
            Location((-PCB_STAB, pcb_front)) * Circle(PCB_INSET))
    board = extrude(outline, amount=PCB_THICK)
    components = extrude(keepout + screws, amount=-COMPONENTS_THICK)
    return board + components

def elliptangle(width, depth, axis):
    middle = Rectangle(width, depth)

    # dunno why i need to explicitly convert these to locations
    edges = middle.edges()
    left = Location(edges[0].center())
    right = Location(edges[2].center())

    ellipse = Ellipse(axis, depth / 2)
    left = left * ellipse
    right = right * ellipse

    return left + middle + right

def ellipse_outline():
    oval = elliptangle(MIDDLE_WIDTH, TOTAL_DEPTH, ELLIPSE_AXIS)
    clip = Rectangle(TOTAL_WIDTH, TOTAL_DEPTH)
    return oval & clip

def foot_outline(thin=1.0):
    foot_width = abs(HOLE_X2 - HOLE_X1)
    foot_depth = abs(HOLE_Y2 - HOLE_Y1) + HOLE_SUPPORT
    oval = elliptangle(foot_width, foot_depth, foot_depth/2)
    foot_y = TOTAL_DEPTH / 2 - foot_depth / 2
    left = Location((HOLE_X1 + foot_width/2, foot_y)) * oval

    trim_box = Rectangle(foot_depth, foot_depth)
    trim = trim_box - Circle(HOLE_SUPPORT*1.15/2)
    trim -= Location((-foot_depth/2, 0)) * trim_box
    left -= Location((HOLE_X2, HOLE_Y2)) * trim

    right = mirror(left, Plane.YZ)
    return left + right

def screw_holes(diameter, smaller=None):
    smaller = smaller or diameter
    return [ Location((x*i, y*j)) * Circle(diameter/2 if j < 0 else smaller/2)
             for (x,y) in [(HOLE_X1, HOLE_Y1), (HOLE_X2, HOLE_Y2)]
             for i in [-1, +1]
             for j in [-1, +1]]

def side_walls():
    thicker = (Location((TOTAL_WIDTH/2 - CHEEK_WIDTH/2, 0))
               * Rectangle(CHEEK_WIDTH, CHEEK_DEPTH + ku(0.5)))
    return thicker + mirror(thicker, Plane.YZ)

def side_cutout():
    width = CASE_SIDE - MX_PLATE_RIB/2
    cutout = (Location((TOTAL_WIDTH/2 - width/2, 0))
              * Rectangle(width, CHEEK_DEPTH))
    notch_thick = PERSPEX_THICK + ACCENT_CLEAR
    notch_depth = CHEEK_NOTCH + ACCENT_CLEAR
    notch = RectangleRounded(notch_thick, notch_depth, CHEEK_NOTCH/2)
    notch_x = TOTAL_WIDTH/2 - CHEEK_WIDTH/2
    top_notch = Location((notch_x, +CHEEK_DEPTH / 2)) * notch
    bot_notch = Location((notch_x, -CHEEK_DEPTH / 2)) * notch
    cutout += top_notch + bot_notch
    cutout += mirror(cutout, Plane.YZ)
    return cutout

def side_accents():
    one = (Location((TOTAL_WIDTH/2 - CHEEK_WIDTH/2, 0))
           * Rectangle(PERSPEX_THICK, CHEEK_DEPTH + CHEEK_NOTCH/2))
    both = one + mirror(one, Plane.YZ)
    return extrude(both, amount=CHEEK_HEIGHT)

def rear_accent():
    brow = extrude(Location((0, TOTAL_DEPTH / 2 - BROW_Y))
                   * Rectangle(MAIN_WIDTH, PERSPEX_THICK),
                   amount=BROW_HEIGHT)
    keep = extrude(Location((0, TOTAL_DEPTH / 2 - BROW_Y))
                   * Rectangle(MAIN_WIDTH + BLOCK_GAP, PERSPEX_THICK),
                   amount=BROW_T)
    return brow + keep

def usb_cutout():
    usbdb = RectangleRounded(USBDB_WIDTH, USBDB_DEPTH, USBDB_R)
    inset = RectangleRounded(USB_WIDTH, 2 * USB_INSET + USB_CLEAR, USB_CLEAR)
    return (Location((0, USBDB_Y)) * offset(usbdb, USB_CLEAR)
            + Location((0, TOTAL_DEPTH/2)) * inset)

def daughterboard_holes():
    holes = Sketch() + [ loc * Circle(1.1) for loc in
                         GridLocations(14, 14, 2, 2) ]
    return Location((0, USBDB_Y)) * holes

def usb_daughterboard():
    holes = daughterboard_holes()
    board = (Location((0, USBDB_Y)) *
            RectangleRounded(USBDB_WIDTH, USBDB_DEPTH, USBDB_R))
    socket = (Location((0, USBDB_Y + USBDB_DEPTH/4)) *
            RectangleRounded(USBDB_WIDTH, USBDB_DEPTH/2, USBDB_R))
    return (extrude(board - holes, amount=USB_THIN) +
            extrude(socket - holes, amount=USB_THICK))

outline = ellipse_outline()

small_holes = screw_holes(HOLE_SMALL)
large_holes = screw_holes(HOLE_BIG)
mixed_holes = screw_holes(HOLE_BIG, HOLE_SMALL)
hole_support = screw_holes(HOLE_SUPPORT)

cheeks = side_cutout()

# TODO: fillet inner corners of top_perspex

brow = (Location((0, TOTAL_DEPTH / 2 - BROW_Y)) *
        Rectangle(MAIN_WIDTH + ACCENT_CLEAR, PERSPEX_THICK + ACCENT_CLEAR))

top_perspex	= outline - small_holes - key_matrix(keycaps, True) - brow
top_perspex	= extrude(top_perspex, amount=PERSPEX_THICK)

switch_plate	= outline - small_holes - key_matrix(plate_cutout) - cheeks
switch_plate	= extrude(switch_plate, amount=PLATE_THICK)

base_plate	= outline - mixed_holes - daughterboard_holes()
base_plate	= extrude(base_plate, amount=PLATE_THICK)

# TODO: fillet inner corners of side_walls()

inset = offset(outline, amount=-SIDE_THICK)
wall = outline - inset + hole_support + side_walls() - cheeks

upper_wall = wall - small_holes
lower_wall = wall - mixed_holes
bottom_wall = lower_wall - usb_cutout()

upper_perspex	= extrude(upper_wall, amount=PERSPEX_THICK)
upper_plate	= extrude(upper_wall, amount=PLATE_THICK)

lower_perspex	= extrude(lower_wall, amount=PERSPEX_THICK)
lower_plate	= extrude(bottom_wall, amount=PLATE_THICK)
bottom_perspex	= extrude(bottom_wall, amount=PERSPEX_THICK)

foot = foot_outline() & outline

small_foot_perspex = extrude(foot - small_holes, amount=PERSPEX_THICK)
small_foot_plate = extrude(foot - small_holes, amount=PLATE_THICK)
big_foot_perspex = extrude(foot - large_holes, amount=PERSPEX_THICK)
big_foot_plate = extrude(foot - large_holes, amount=PLATE_THICK)

model = Part() + [
    Location((0,0, EXPLODE * y)) * part
    for (y, part) in [
            ((-13.5), big_foot_plate),
            ((-12), big_foot_perspex),
            ((-9.0), big_foot_plate),
            ((-7.5), big_foot_perspex),
            ((-4.5), small_foot_plate),
            ((-3.0), small_foot_perspex),
            (( 0.0), base_plate),
            (( 1.5), bottom_perspex),
            (( 1.5), side_accents()),
            (( 1.5), usb_daughterboard()),
            (( 4.0), pcb_outline()), # 5mm below switch plate
            (( 4.5), lower_plate),
            (( 6.0), lower_perspex),
            (( 9.0), switch_plate),
            ((10.5), rear_accent()),
            ((10.5), upper_perspex),
            ((13.5), upper_plate),
            ((15.0), top_perspex),
    ] ]


# fillet outer corners
edges = model.edges().filter_by(Axis.Z).group_by(Axis.X)
model = fillet(edges[-1] + edges[+0], radius=OUTER_FILLET)

show_object(model)
