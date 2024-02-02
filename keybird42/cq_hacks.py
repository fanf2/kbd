import inspect
import math
import OCP.Aspect

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
