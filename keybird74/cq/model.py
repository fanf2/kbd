import cadquery as cq

CHARCOAL = cq.Color(0.1, 0.1, 0.1)
SMOKE = cq.Color(0.25, 0.25, 0.25, 0.25)

mx = cq.importers.importStep("mx.step")
dsa = cq.importers.importStep("dsa.step")

model = (
    cq
    .Assembly()
    .add(mx, name="mx", color=CHARCOAL)
    .add(dsa, name="dsa", color=SMOKE)
    .constrain("mx@faces@>Y", "dsa@faces@<Y[0]", "Plane")
    .solve()
)
show_object(model)
