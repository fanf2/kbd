import build123d as bd
import OPK.opk as opk

KEY_UNIT = 19.05

PLATE_THICK = 1.5   # 0.06 in
PCB_THICK = 1.2     # minimum allowed by kailh socket knobs

# relative to top of the pcb
MX_BODY_HEIGHT = 11.0
MX_PLATE_HEIGHT = 5.0
MX_PIN_LENGTH = 3.3

PCB_PLATE_GAP = MX_PLATE_HEIGHT - PLATE_THICK

show_object(opk.keycap())
