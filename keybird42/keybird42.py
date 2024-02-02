# non-enclosure parts of keybird42

from build123d import *
from mx import *
import opk

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

FONT="/Users/fanf/Code/kbd/Gorton_Perfected_1.02/Light.otf"
FONT="/Users/fanf/Code/kbd/SOD/SOD_Regular.otf"

def key_positions(row):
    if row[0]:
        arrows = (mx_key_grid(row[2], +FUN_X, FUN_Y2+ku(0.5), 1, 1) +
                  mx_key_grid(row[4], +FUN_X, FUN_Y2-ku(0.5), 3, 1))
    else:
        row = [row,row,row,row,row,row]
        arrows = mx_key_grid(row[0], +FUN_X, FUN_Y2, 3, 2)
    row5 = [ 125, 125, 150, 700, 150, 125, 125 ]
    return (mx_key_grid(row[0], -FUN_X, FUN_Y1, 3, 2) +
            mx_key_grid(row[0], -FUN_X, FUN_Y2, 3, 2) +
            mx_key_grid(row[0], +FUN_X, FUN_Y1, 3, 2) +
            arrows +
            mx_key_row(row[1], MAIN_WIDTH, ku(+2), [], 15, []) +
            mx_key_row(row[2], MAIN_WIDTH, ku(+1), [150], 12, [150]) +
            mx_key_row(row[3], MAIN_WIDTH, ku(00), [175], 11, [225]) +
            mx_key_row(row[4], MAIN_WIDTH, ku(-1), [225], 10, [175, 100]) +
            mx_key_row(row[5], MAIN_WIDTH, ku(-2), [], 0, row5))

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

KEY_LEGENDS = [
    ("F2", 5), ("F1", 5), ("F6", 5), ("F5", 5), ("F10", 5), ("F9", 5),
    ("F4", 5), ("F3", 5), ("F8", 5), ("F7", 5), ("F12", 5), ("F11", 5),
    ("F16", 5), ("F13", 5), ("F17", 5), ("F14", 5), ("F18", 5), ("F15", 5),
    ("↑", 9), ("←", 9), ("↓", 9), ("→", 9),

    ("ESC", 5),
    ("1", 8), ("2", 8), ("3", 8), ("4", 8), ("5", 8),
    ("6", 8), ("7", 8), ("8", 8), ("9", 8), ("0", 8),
    ("-", 9), ("+", 9), ("|", 8), ("~", 8),

    ("TAB", 5),
    ("Q", 8), ("W", 8), ("E", 8), ("R", 8), ("T", 8), ("Y", 8),
    ("U", 8), ("I", 8), ("O", 8), ("P", 8), ("{", 8), ("}", 8),
    ("DELETE", 5),

    ("CTRL", 5),
    ("A", 8), ("S", 8), ("D", 8), ("F", 8), ("G", 8), ("H", 8),
    ("J", 8), ("K", 8), ("L", 8), (";", 9), ('"', 9),
    ("RETURN", 5),

    ("SHIFT", 5),
    ("Z", 8), ("X", 8), ("C", 8), ("V", 8), ("B", 8),
    ("N", 8), ("M", 8), ("<", 9), (">", 9), ("?", 8),
    ("CTRL", 5),
    ("SHIFT", 5),

    ("HYPER", 5),
    ("ALT", 5),
    ("META", 5),
    ("SPACE", 0),
    ("META", 5),
    ("ALT", 5),
    ("HYPER", 5),
]

def layout_keycaps(stamp, show_it, style, legends):
    keycaps = key_positions(opk.keycaps(stamp, style == "simple"))
    itop = 9 if style == "simple" else 8
    for i, keycap in enumerate(keycaps):
        (name, font_size) = KEY_LEGENDS[i]
        if not legends or font_size == 0:
            show_it(keycap, None, name)
            continue
        keytop = keycap.faces()[itop]
        normal = keytop.normal_at()
        rendered = (Location(keytop.center() + normal) *
                    Text(name, font_size, font_path=FONT))
        projected = []
        for f in rendered.faces():
            projected += f.project_to_shape(keycap, -normal)
        legend = Part() + [ Solid.extrude(f, direction=0.1*normal)
                            for p in projected for f in p.faces() ]
        show_it(keycap, legend, name)

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

def kb42_pcba(holes):

    pcb_thick = 1.6
    pcba_thick = pcb_thick + 2.0

    outline = kb42_pcb()
    keepout = offset(outline, amount=-PCB_INSET)
    screw = Location((0, -MAIN_DEPTH/2 + PCB_INSET)) * Circle(PCB_INSET)
    screws = (Location((+STAB_OFFSET, 0)) * screw +
              Location((-STAB_OFFSET, 0)) * screw)
    components = extrude(keepout + screws, amount=-pcba_thick)
    cutouts = extrude(mx_pcb_cutouts(), amount=-pcba_thick)
    pcba = extrude(outline, amount=-pcb_thick) + components
    if holes: pcba -= key_positions([ cutouts ] * 1000)
    return pcba
