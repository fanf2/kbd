import cadquery as cq

TRANSPARENT = cq.Color(0, 0, 0, 0)
CHARCOAL = cq.Color(0.1, 0.1, 0.1, 1.0)
SMOKE = cq.Color(0.25, 0.25, 0.25, 0.25)

KEY_UNIT = 19       # metricated

PLATE_THICK = 1.5   # 0.06 in
PCB_THICK = 1.2     # minimum allowed by kailh socket knobs

# relative to top of the pcb
MX_BODY_HEIGHT = 11.0
MX_PLATE_HEIGHT = 5.0
MX_PIN_LENGTH = 3.3

PCB_PLATE_GAP = MX_PLATE_HEIGHT - PLATE_THICK

# neither of these models are very accurate

# the mx switch pins are 0.3mm too short
# the space from the base of to the plate is 0.25mm too little
# the clips above the plate are 0.25mm too thin
mx = cq.importers.importStep("mx.step")

# the top of the keycap is much too thick
dsa = cq.importers.importStep("dsa.step")

pcba = (
    cq.Workplane("XZ")
    .box(KEY_UNIT, KEY_UNIT, PCB_THICK)
)

plate = (
    cq.Workplane("XZ")
    .box(KEY_UNIT, KEY_UNIT, PLATE_THICK)
)

spacer = (
    cq.Workplane("XZ")
    .box(KEY_UNIT, KEY_UNIT, PCB_PLATE_GAP)
)

measure = (
    cq.Workplane("XZ")
    .box(KEY_UNIT, KEY_UNIT, MX_BODY_HEIGHT)
)

model = (
    cq
    .Assembly()
    .add(mx, name="mx", color=CHARCOAL)
    .add(dsa, name="dsa", color=SMOKE)
    .add(pcba, name="pcba", color=SMOKE)
    .add(plate, name="plate", color=SMOKE)
    .add(spacer, name="spacer", color=TRANSPARENT)
    .add(measure, name="measure", color=TRANSPARENT)
    .constrain("mx", "FixedRotation", (0,0,0))
    .constrain("dsa", "FixedRotation", (0,0,0))
    .constrain("pcba", "FixedRotation", (0,0,0))
    .constrain("plate", "FixedRotation", (0,0,0))
    .constrain("spacer", "FixedRotation", (0,0,0))
    .constrain("measure", "FixedRotation", (0,0,0))
    .constrain("mx@faces@>Y", "dsa@faces@<Y[0]", "Point")
    .constrain("mx@faces@>Y[1]", "pcba@faces@>Y", "Point")
    .constrain("pcba@faces@>Y", "spacer@faces@<Y", "Point")
    .constrain("pcba@faces@>Y", "measure@faces@<Y", "Point")
    .constrain("spacer@faces@>Y", "plate@faces@<Y", "Point")
    .solve()
)
show_object(model)
