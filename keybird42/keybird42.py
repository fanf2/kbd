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
    ["F4", 4], ["F1", 4], ["F5", 4], ["F2", 4], ["F6", 4], ["F3", 4],
    ["F10", 4], ["F7", 4], ["F11", 4], ["F8", 4], ["F12", 4], ["F9", 4],
    ["F16", 4], ["F13", 4], ["F17", 4], ["F14", 4], ["F18", 4], ["F15", 4],
    ["↑", 9], ["←", 9], ["↓", 9], ["→", 9],

    ["ESC", 4],
    ["1", 7], ["2", 7], ["3", 7], ["4", 7], ["5", 7],
    ["6", 7], ["7", 7], ["8", 7], ["9", 7], ["Ø", 7],
    ["−", 9], ["+", 9], ["¦", 7], ["~", 7],

    ["TAB", 4],
    ["Q", 7], ["W", 7], ["E", 7], ["R", 7], ["T", 7], ["Y", 7],
    ["U", 7], ["I", 7], ["O", 7], ["P", 7], ["{", 7], ["}", 7],
    ["DELETE", 4],

    ["CTRL", 4],
    ["A", 7], ["S", 7], ["D", 7], ["F", 7], ["G", 7], ["H", 7],
    ["J", 7], ["K", 7], ["L", 7], [";", 9], ['"', 9],
    ["RETURN", 4],

    ["SHIFT", 4],
    ["Z", 7], ["X", 7], ["C", 7], ["V", 7], ["B", 7],
    ["N", 7], ["M", 7], ["<", 9], [">", 9], ["?", 7],
    ["CTRL", 4],
    ["SHIFT", 4],

    ["HYPER", 4],
    ["ALT", 4],
    ["META", 4],
    None,
    ["META", 4],
    ["ALT", 4],
    ["HYPER", 4],
]

def layout_keycaps(stamp, style, legends):
    keycaps = key_positions(opk.keycaps(stamp, style == "simple"))
    if not legends:
        return keycaps
    itop = 9 if style == "simple" else 8
    for i, keycap in enumerate(keycaps):
        if KEY_LEGENDS[i] is None:
            continue
        print(KEY_LEGENDS[i][0], end=" ", flush=True)
        keytop = keycap.faces()[itop]
        normal = keytop.normal_at()
        legend = (Location(keytop.center() + normal) *
                  Text(*KEY_LEGENDS[i], font_path=FONT))
        projected = []
        for letter in legend.faces():
            projected += letter.project_to_shape(keycap, -normal)
        keycaps[i] += [ Solid.extrude(f, direction=0.1*normal)
                        for p in projected for f in p.faces() ]
    print("done")
    return keycaps

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
