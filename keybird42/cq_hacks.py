from build123d import *
import inspect
import math
import OCP.Aspect
import time

# surely there's a better way?
show_object = None
for f in inspect.stack():
    if "show_object" in f.frame.f_locals:
        show_object = f.frame.f_locals["show_object"]

START = time.perf_counter()
def stamp(msg):
    t = time.strftime('%F.%T')
    z = time.strftime('%z')
    f = (time.time_ns() // 100000) % 10000
    print(f"{t}.{f:03}{z} {time.perf_counter() - START :6.3f} {msg}")

def topo(obj):
    try: return obj.show_topology()
    except: return f"{obj}"

def show_normal_tangent(edge, pos):
    point = edge @ pos
    tangent = edge % pos * 10
    for angle in [0, 90, 180]:
        show_object(Line(point, point + tangent.rotate(Axis.Z, angle)))

def show_marker(p):
    show_object(Location(p) * Box(1,1,1), **rgba("f00"))

# for use with show_object()
def rgba(rgba):
    color = ()
    if len(rgba) < 5:
        for i in range(3):
            color += (int(rgba[i:i+1], 16) * 17,)
    else:
        for i in range(3):
            color += (int(rgba[i*2:i*2+2], 16),)
    alpha = None
    if len(rgba) == 4:
        alpha = int(rgba[-1:], 16) / 15.0
    if len(rgba) == 8:
        alpha = int(rgba[-2:], 16) / 255.0
    options = { "color": color }
    if alpha != None:
        options["alpha"] = alpha
    return { "options": options }

# surely there's a better way?
def find_main_window():
    for f in inspect.stack():
        if f.function == "main":
            return f.frame.f_locals["win"]

def set_view_preferences(line_width=1):
    viewer = find_main_window().viewer
    prefs = viewer.preferences
    prefs['Projection Type'] = 'Perspective'
    prefs['Use gradient'] = True
    prefs['Background color'] = (102,153,255)
    prefs['Background color (aux)'] = (153,204,255)
    viewer.updatePreferences()
    viewer.canvas.view.SetBgGradientStyle(
        OCP.Aspect.Aspect_GradientFillMethod_Vertical)
    drawer = viewer.canvas.context.DefaultDrawer()
    if line_width > 0:
        drawer.SetFaceBoundaryDraw(True)
        drawer.FaceBoundaryAspect().SetWidth(line_width)
    else:
        drawer.SetFaceBoundaryDraw(False)

def explode(spread):
    # when we are called from the console, the imports above are
    # not available - dunno why they lack proper lexical scoping
    import build123d
    main = find_main_window()
    ctx = main.viewer.canvas.context
    cq = main.components["object_tree"].CQ
    for i in range(cq.childCount()):
        obj = cq.child(i)
        if spread == 0:
            ctx.ResetLocation(obj.ais)
        else:
            min_z = math.inf
            if type(obj.shape) == list:
                for o in obj.shape:
                    z = o.bounding_box().min.Z
                    if min_z > z: min_z = z
            else:
                min_z = obj.shape.bounding_box().min.Z
            loc = build123d.Location((0,0, min_z * spread)).wrapped
            ctx.SetLocation(obj.ais, loc)
        ctx.Redisplay(obj.ais, True)
