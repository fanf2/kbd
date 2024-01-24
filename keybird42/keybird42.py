# non-enclosure parts of keybird42

from build123d import *
from mx import *

KEYS_WIDE	= 15
KEYS_DEEP	= 5

MAIN_WIDTH	= ku( KEYS_WIDE )
MAIN_DEPTH	= ku( KEYS_DEEP )

FUN_WIDTH	= ku( 3.00 )
FUN_DEPTH	= ku( 2.00 )

KEYBLOCK_GAP	= ku( 0.25 )

FUN_X   = MAIN_WIDTH / 2 + KEYBLOCK_GAP + FUN_WIDTH / 2
FUN_Y1  = MAIN_DEPTH / 2 - KEYBLOCK_GAP - FUN_DEPTH / 2
FUN_Y2  = FUN_Y1 - KEYBLOCK_GAP - FUN_DEPTH
FUN_Y2a = FUN_Y2 - ku(0.5) # lower arrows

def key_positions(k):
    row5 = [ 125, 125, 150, 700, 150, 125, 125 ]
    return (mx_key_grid(k, -FUN_X, FUN_Y1, 3, 2) +
            mx_key_grid(k, -FUN_X, FUN_Y2, 3, 2) +
            mx_key_grid(k, +FUN_X, FUN_Y1, 3, 2) +
            mx_key_grid(k, +FUN_X, FUN_Y2, 3, 2) +
            mx_key_row(k, MAIN_WIDTH, ku(+2), [], 15, []) +
            mx_key_row(k, MAIN_WIDTH, ku(+1), [150], 12, [150]) +
            mx_key_row(k, MAIN_WIDTH, ku(00), [175], 11, [225]) +
            mx_key_row(k, MAIN_WIDTH, ku(-1), [225], 10, [175, 100]) +
            mx_key_row(k, MAIN_WIDTH, ku(-2), [], 0, row5))

def keyswitch_cutouts():
    return Sketch() + key_positions(mx_plate_cutouts())

def keycap_cutouts():
    main = Rectangle(MAIN_WIDTH, MAIN_DEPTH)
    fun = Rectangle(FUN_WIDTH, FUN_DEPTH)
    fun1 = Location((-FUN_X, FUN_Y1)) * fun
    fun2 = Location((-FUN_X, FUN_Y2)) * fun
    fun3 = Location((+FUN_X, FUN_Y1)) * fun
    fun4b = Location((FUN_X, FUN_Y2)) * Rectangle(ku(1), FUN_DEPTH)
    fun4a = Location((FUN_X, FUN_Y2a)) * Rectangle(FUN_WIDTH, ku(1))
    return Sketch() + [ main, fun1, fun2, fun3, fun4a, fun4b ]

# from kicad

def pcba():

    pcb_thick = 1.6
    pcba_thick = pcb_thick + 2.0

    inset = ku( 1/8 )
    wing = ku( 13/32 )
    stab = ku( 7 - 1 )/2

    rear = +MAIN_DEPTH/2
    front = -MAIN_DEPTH/2 + inset
    right = MAIN_WIDTH/2 + inset + FUN_WIDTH

    half = Polyline(
        (0, rear),
        (MAIN_WIDTH/2, rear),
        (MAIN_WIDTH/2 + KEYBLOCK_GAP, rear - KEYBLOCK_GAP),
        (right, rear - KEYBLOCK_GAP),
        (right + wing, rear - KEYBLOCK_GAP - wing),
        (right + wing, front + KEYBLOCK_GAP*2 + wing),
        (right, front + KEYBLOCK_GAP*2),
        (MAIN_WIDTH/2 + inset + KEYBLOCK_GAP, front + KEYBLOCK_GAP*2),
        (MAIN_WIDTH/2 - inset, front),
        (stab + inset*2, front),
        (stab + inset*1, front - inset),
        (0, front - inset),
    )
    outline = make_face(half + mirror(half, Plane.YZ))
    keepout = offset(outline, amount=-inset)
    screws = (Location((+stab, front)) * Circle(inset) +
              Location((-stab, front)) * Circle(inset))
    components = ( extrude(keepout, amount=pcba_thick) +
                   extrude(screws, amount=-pcba_thick) )
    return extrude(outline, amount=pcb_thick) + components
