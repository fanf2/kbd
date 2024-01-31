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

KEYS_WIDTH = MAIN_WIDTH + KEYBLOCK_GAP*2 + FUN_WIDTH*2
KEYS_DEPTH = MAIN_DEPTH

FUN_X   = MAIN_WIDTH / 2 + KEYBLOCK_GAP + FUN_WIDTH / 2
FUN_Y1  = MAIN_DEPTH / 2 - KEYBLOCK_GAP - FUN_DEPTH / 2
FUN_Y2  = FUN_Y1 - KEYBLOCK_GAP - FUN_DEPTH
FUN_Y2a = FUN_Y2 - ku(0.5) # lower arrows

STAB_OFFSET = ku( 7 - 1 )/2

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

PCB_INSET = ku( 1/8 )

def kb42_pcb():
    wing = ku( 13/32 )
    rear = +MAIN_DEPTH/2
    front = -MAIN_DEPTH/2 + PCB_INSET
    right = MAIN_WIDTH/2 + PCB_INSET + FUN_WIDTH
    half = Polyline(
        (0, rear),
        (MAIN_WIDTH/2, rear),
        (MAIN_WIDTH/2 + KEYBLOCK_GAP, rear - KEYBLOCK_GAP),
        (right, rear - KEYBLOCK_GAP),
        (right + wing, rear - KEYBLOCK_GAP - wing),
        (right + wing, front + KEYBLOCK_GAP*2 + wing),
        (right, front + KEYBLOCK_GAP*2),
        (MAIN_WIDTH/2 + PCB_INSET + KEYBLOCK_GAP, front + KEYBLOCK_GAP*2),
        (MAIN_WIDTH/2 - PCB_INSET, front),
        (STAB_OFFSET + PCB_INSET*2, front),
        (STAB_OFFSET + PCB_INSET*1, front - PCB_INSET),
        (0, front - PCB_INSET),
    )
    return make_face(half + mirror(half, Plane.YZ))

def kb42_pcba():

    pcb_thick = 1.6
    pcba_thick = pcb_thick + 2.0

    outline = kb42_pcb()
    keepout = offset(outline, amount=-PCB_INSET)
    screw = Location((0, -MAIN_DEPTH/2 + PCB_INSET)) * Circle(PCB_INSET)
    screws = (Location((+STAB_OFFSET, 0)) * screw +
              Location((-STAB_OFFSET, 0)) * screw)
    components = extrude(keepout + screws, amount=-pcba_thick)
    cutouts = extrude(mx_pcb_cutouts(), amount=-pcba_thick)
    holes = key_positions([ cutouts ] * 1000)
    return extrude(outline, amount=-pcb_thick) + components - holes
