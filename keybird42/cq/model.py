import cadquery as cq
import OPK.opk as opk

TRANSPARENT = cq.Color(0, 0, 0, 0)
CHARCOAL = cq.Color(0.1, 0.1, 0.1, 1.0)
SMOKE = cq.Color(0.25, 0.25, 0.25, 0.25)

KEY_UNIT = 19.05

PLATE_THICK = 1.5   # 0.06 in
PCB_THICK = 1.2     # minimum allowed by kailh socket knobs

# relative to top of the pcb
MX_BODY_HEIGHT = 11.0
MX_PLATE_HEIGHT = 5.0
MX_PIN_LENGTH = 3.3

PCB_PLATE_GAP = MX_PLATE_HEIGHT - PLATE_THICK

# this model is not very accurate
# the mx switch pins are 0.3mm too short
# the space from the base of to the plate is 0.25mm too little
# the clips above the plate are 0.25mm too thin
mx = cq.importers.importStep("mx.step")
# z vertical
mx = mx.rotate((-1,0,0),(+1,0,0), 90)

r1u1 = opk.keycap()

model = (
    cq
    .Assembly()
    .add(mx, name="mx", color=CHARCOAL)
    .add(r1u1, name="cap", color=SMOKE)
    .constrain("mx", "FixedRotation", (0,0,0))
    .constrain("cap", "FixedRotation", (0,0,0))
    .constrain("mx@faces@<Z[1]", "cap@faces@>Z[1]", "Point")
    .solve()
)

show_object(model)
