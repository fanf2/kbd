#![allow(dead_code)]

use anyhow::*;

const WIDTH: i8 = 4;
const DEPTH: i8 = 4;

// we are mostly working in inches, except for the holes
const MM_IN: f64 = 25.4;

const KERF: f64 = 0.01; // inch

const SWU: f64 = 0.75; // inch

// standrad corner radii, based on layer thicknesses
const SMOOTH: f64 = 1.0 / 8.0; // like 3mm acrylic
const BLUNT: f64 = SMOOTH / 2.0; // like PCB or plate
const SHARP: f64 = BLUNT / 2.0;

const KEYS_X: f64 = 0.0;
const KEYS_Y: f64 = 0.0;
const KEYS_W: f64 = WIDTH as f64 * SWU;
const KEYS_D: f64 = DEPTH as f64 * SWU;

const BLACK: f64 = 0.5 * SWU;
const BLACK_X: f64 = -BLACK;
const BLACK_Y: f64 = -BLACK;
const BLACK_W: f64 = KEYS_W + BLACK * 2.0;
const BLACK_D: f64 = KEYS_D + BLACK * 2.0;

const BEIGE_NEAR: f64 = 0.75 * SWU;
const BEIGE_SIDE: f64 = 1.0 * SWU;
const BEIGE_FAR: f64 = 1.25 * SWU;
const BEIGE_X: f64 = BLACK_X - BEIGE_SIDE;
const BEIGE_Y: f64 = BLACK_Y - BEIGE_FAR;
const BEIGE_W: f64 = BLACK_W + BEIGE_SIDE * 2.0;
const BEIGE_D: f64 = BLACK_D + BEIGE_FAR + BEIGE_NEAR;

const BOX_GAP: f64 = BLUNT;
const BOX_X: f64 = -BOX_GAP;
const BOX_Y: f64 = -BOX_GAP;
const BOX_W: f64 = KEYS_W + BOX_GAP * 2.0;
const BOX_D: f64 = KEYS_D + BOX_GAP * 2.0;

const PCB_SIDE: f64 = 0.5 * SWU;
const BOX_SIDE: f64 = PCB_SIDE + BOX_GAP;
const RECESS_SIDE: f64 = PCB_SIDE + BLACK + BEIGE_SIDE;
const RECESS_MID: f64 = BEIGE_W - RECESS_SIDE * 2.0;
const RECESS_PCB: f64 = BEIGE_FAR + BLACK;
const RECESS_BOX: f64 = RECESS_PCB - BOX_GAP;

// use the kerf to provide the right fit
const SCREW_HOLE: f64 = 3.0 / MM_IN;
const RIVET_HOLE: f64 = 5.0 / MM_IN;

const AROUND_HOLE: f64 = 4.0 / MM_IN; // radius

const DRILL_LEFT: f64 = BLACK_X + AROUND_HOLE;
const DRILL_RIGHT: f64 = BLACK_X + BLACK_W - AROUND_HOLE;
const DRILL_FAR: f64 = BLACK_Y + AROUND_HOLE;
const DRILL_NEAR: f64 = BLACK_Y + BLACK_D - AROUND_HOLE;

// for switches the kerf is larger than the tolerance
const SWITCH_HOLE: f64 = 14.0 / MM_IN - KERF;

const STAB_DEPTH: f64 = (0.26 - 0.484 + 0.53) * 2.0;
const STAB_WIDTH: f64 = 1.0 / 3.0;
const STAB_OFFSET_2U: f64 = 1.0 / 2.0;
const STAB_OFFSET_7U: f64 = 4.5 / 2.0;

fn main() -> Result<()> {
    let path =
    // outer surround
        Path::begin(BEIGE_X, BEIGE_Y)
        .rect(BEIGE_W, BEIGE_D, SMOOTH)
        .goto(BLACK_X, BLACK_Y)
        .rect(BLACK_W, BLACK_D, SHARP)
    // inner surround
        .goto(BLACK_X, BLACK_Y)
        .rect(BLACK_W, BLACK_D, BLUNT)
        .goto(KEYS_X, KEYS_Y)
        .rect(KEYS_W, KEYS_D, SHARP)
        .drill(SCREW_HOLE, SCREW_HOLE)
    // shim
        .goto(BEIGE_X, BEIGE_Y)
        .rect(BEIGE_W, BEIGE_D, SMOOTH)
        .goto(KEYS_X, KEYS_Y)
        .rect(KEYS_W, KEYS_D, SHARP)
        .drill(SCREW_HOLE, SCREW_HOLE)
    // plate
        .goto(BEIGE_X, BEIGE_Y)
        .rect(BEIGE_W, BEIGE_D, SMOOTH)
        .drill(SCREW_HOLE, SCREW_HOLE)
        .ortho_keys()
    // closed box
        .goto(BEIGE_X, BEIGE_Y)
        .rect(BEIGE_W, BEIGE_D, SMOOTH)
        .goto(BOX_X, BOX_Y)
        .rect(BOX_W, BOX_D, BLUNT)
        .drill(SCREW_HOLE, RIVET_HOLE)
    // open box
        .goto(BEIGE_X, BEIGE_Y)
        .frame(BEIGE_W, BEIGE_D, SMOOTH)
        .portal(RECESS_SIDE, BOX_SIDE, RECESS_BOX, BLUNT)
        .frame(BOX_W, BOX_D, BLUNT)
        .portal(RECESS_SIDE, BOX_SIDE, RECESS_BOX, BLUNT)
        .close()
        .drill(RIVET_HOLE, RIVET_HOLE)
        .ortho_feet()
    // base
        .goto(BEIGE_X, BEIGE_Y)
        .frame(BEIGE_W, BEIGE_D, SMOOTH)
        .recess((RECESS_SIDE, RECESS_MID, RECESS_SIDE),
                 RECESS_PCB, BLUNT)
        .close()
        .drill(RIVET_HOLE, RIVET_HOLE)
        ;

    save_svg("keybow/test.svg", &path, SWU)?;
    Ok(())
}

impl Path {
    fn drill(self, d_far: f64, d_near: f64) -> Path {
        self.goto(DRILL_LEFT, DRILL_FAR)
            .hole(d_far)
            .goto(DRILL_RIGHT, DRILL_FAR)
            .hole(d_far)
            .goto(DRILL_LEFT, DRILL_NEAR)
            .hole(d_near)
            .goto(DRILL_RIGHT, DRILL_NEAR)
            .hole(d_near)
    }

    fn ortho_keys(mut self) -> Path {
        for x in 0..WIDTH {
            for y in 0..DEPTH {
                self = self.switch(1.0, x as f64, y as f64);
            }
        }
        self
    }

    fn ortho_feet(mut self) -> Path {
        for y in 1..DEPTH {
            self = self.ortho_foot(1.0, y as f64);
            self = self.ortho_foot(3.0, y as f64);
        }
        self
    }

    fn ortho_foot(self, x: f64, y: f64) -> Path {
        self.goto(x * SWU, y * SWU)
            .hole(RIVET_HOLE)
            .goto(x * SWU, y * SWU)
            .hole((AROUND_HOLE + y / MM_IN) * 2.0)
    }

    fn hhkb_keys(mut self) -> Path {
        for x in 0..WIDTH {
            self = self.switch(1.0, x as f64, 0.0);
            if x < WIDTH - 3 {
                self = self.switch(1.0, x as f64 + 1.5, 1.0);
            }
            if x < WIDTH - 4 {
                self = self.switch(1.0, x as f64 + 1.75, 2.0);
            }
            if x < WIDTH - 5 {
                self = self.switch(1.0, x as f64 + 2.25, 3.0);
            }
        }
        self.switch(1.5, 0.0, 1.0)
            .switch(1.5, -1.5, 1.0)
            .switch(1.75, 0.0, 2.0)
            .switch(2.25, -2.25, 2.0)
            .switch(2.25, 0.0, 3.0)
            .switch(1.75, -2.75, 3.0)
            .switch(1.0, -1.0, 3.0)
            .switch(1.5, 0.0, 4.0)
            .switch(1.0, 1.5, 4.0)
            .switch(1.5, 2.5, 4.0)
            .switch(7.0, 4.0, 4.0)
            .switch(1.5, -4.0, 4.0)
            .switch(1.0, -2.5, 4.0)
            .switch(1.5, -1.5, 4.0)
    }

    fn switch(mut self, w: f64, mut x: f64, mut y: f64) -> Path {
        let width = w * SWU;
        let depth = 1.0 * SWU;
        if x < 0.0 {
            x += WIDTH as f64;
        }
        x = x * SWU + width / 2.0;
        y = y * SWU + depth / 2.0;
        if 2.0 - KERF < w && w < 3.0 - KERF {
            self = self.stab(STAB_OFFSET_2U, x, y);
        }
        if 7.0 - KERF < w && w < 7.0 + KERF {
            self = self.stab(STAB_OFFSET_7U, x, y);
        }
        self.goto(x, y).cutout(SWITCH_HOLE, SWITCH_HOLE, KERF)
    }

    fn stab(self, w: f64, x: f64, y: f64) -> Path {
        self.goto(x - w, y)
            .cutout(STAB_WIDTH, STAB_DEPTH, KERF)
            .goto(x + w, y)
            .cutout(STAB_WIDTH, STAB_DEPTH, KERF)
    }
}

#[derive(Clone, Copy, Debug, PartialEq)]
struct Pos {
    x: f64,
    y: f64,
}

const NO_PLACE: Pos = Pos { x: f64::NAN, y: f64::NAN };

#[derive(Clone, Copy, Debug, PartialEq)]
struct Bounds {
    min: Pos,
    max: Pos,
}

fn bounds(bbox: Bounds, pos: Pos) -> Bounds {
    let min = |a, b| if a <= b { a } else { b };
    let max = |a, b| if a >= b { a } else { b };
    Bounds {
        min: Pos { x: min(bbox.min.x, pos.x), y: min(bbox.min.y, pos.y) },
        max: Pos { x: max(bbox.max.x, pos.x), y: max(bbox.max.y, pos.y) },
    }
}

#[derive(Clone, Copy, Debug, PartialEq)]
enum Cut {
    Goto(Pos),
    Back(f64),
    Forth(f64),
    Left(f64),
    Right(f64),
    Corner(f64, u8, f64, f64), // radius, sweep, dx, dy
    Close(),
    Circle(f64), // diameter
}
use Cut::*;

fn save_svg(name: &str, path: &Path, margin: f64) -> Result<()> {
    let bbox = ensure_closed(&path.cuts);
    let width = bbox.max.x - bbox.min.x + margin * 2.0;
    let depth = bbox.max.y - bbox.min.y + margin * 2.0;
    let size = (bbox.min.x - margin, bbox.min.y - margin, width, depth);
    let document = svg::Document::new()
        .set("width", format!("{}in", width))
        .set("height", format!("{}in", depth))
        .set("viewBox", size)
        .add(to_svg(&path.cuts));
    svg::save(name, &document)?;
    Ok(())
}

type SvgCircle = svg::node::element::Circle;
type SvgGroup = svg::node::element::Group;
type SvgPath = svg::node::element::Path;
type PathData = svg::node::element::path::Data;

type SvgStyle<'a> = &'a [(&'a str, svg::node::Value)];

fn to_svg(cuts: &[Cut]) -> SvgGroup {
    let style: SvgStyle = &[
        ("fill", "none".into()),
        ("stroke", "goldenrod".into()),
        ("stroke-width", KERF.into()),
    ];

    let mut g = SvgGroup::new();
    let mut p = PathData::new();
    let mut pr = 0.0;

    let mut it = cuts.iter().peekable();
    while let Some(&this) = it.next() {
        let next = match it.peek() {
            Some(&thing) => *thing,
            None => return g,
        };

        match (this, next) {
            (Goto(Pos { x, y }), Circle(d)) => {
                let mut c = SvgCircle::new()
                    .set("cx", x)
                    .set("cy", y)
                    .set("r", d / 2.0);
                for attr in style {
                    c = c.set(attr.0, attr.1.clone());
                }
                g = g.add(c);
            }
            (Circle(_), _) => (),

            (_, Close()) => {
                let mut path = SvgPath::new().set("d", p.close());
                for attr in style {
                    path = path.set(attr.0, attr.1.clone());
                }
                g = g.add(path);
                p = PathData::new();
            }
            (Close(), _) => (),

            (Goto(Pos { x, y }), Corner(nr, _, _, _)) => {
                p = p.move_to((x + nr, y))
            }

            (Back(depth), Corner(nr, _, _, _)) => {
                p = p.line_by((0, -(depth - pr - nr)))
            }

            (Forth(depth), Corner(nr, _, _, _)) => {
                p = p.line_by((0, depth - pr - nr))
            }

            (Left(depth), Corner(nr, _, _, _)) => {
                p = p.line_by((-(depth - pr - nr), 0))
            }

            (Right(depth), Corner(nr, _, _, _)) => {
                p = p.line_by((depth - pr - nr, 0))
            }

            (Corner(r, sw, dx, dy), _) => {
                p = p.elliptical_arc_by((r, r, 0, 0, sw, dx, dy));
                pr = r;
            }

            _ => unimplemented!(),
        }
    }
    unreachable!()
}

fn ensure_closed(cuts: &[Cut]) -> Bounds {
    let mut start: Option<Pos> = None;
    let mut cur = NO_PLACE;
    let mut bbox = Bounds { min: cur, max: cur };
    for cut in cuts {
        match *cut {
            Close() => {
                let dx = start.unwrap().x - cur.x;
                let dy = start.unwrap().y - cur.y;
                assert!(dx * dx + dy * dy < 0.0001 * 0.0001);
                start = None;
            }
            Goto(pos) => {
                cur = pos;
                start = Some(pos);
            }
            Back(depth) => cur.y -= depth,
            Forth(depth) => cur.y += depth,
            Left(width) => cur.x -= width,
            Right(width) => cur.x += width,
            Corner(_, _, _, _) => (),
            Circle(diameter) => {
                let r = diameter / 2.0;
                bbox = bounds(bbox, Pos { x: cur.x - r, y: cur.y - r });
                bbox = bounds(bbox, Pos { x: cur.x + r, y: cur.y + r });
            }
        }
        bbox = bounds(bbox, cur);
    }
    bbox
}

macro_rules! path_state {
    { $name:ident : $($item:item)* } => {
        #[derive(Clone, Debug, PartialEq)]
        struct $name {
            cuts: Vec<Cut>,
        }
        impl $name {
            $($item)*
        }
    };
}

macro_rules! path_funky {
    { $name:ident($arg:ident) -> $state:ident = $cons:ident $vals:tt } => {
        fn $name(mut self, $arg: f64) -> $state {
            self.cuts.push($cons $vals);
            $state { cuts: self.cuts }
        }
    }
}

macro_rules! path_fn {
    { $name:ident($arg:ident) -> $state:ident = $cons:ident } => {
        path_funky!{ $name($arg) -> $state = $cons($arg) }
    }
}

macro_rules! path_closed {
    () => {
        fn close(mut self) -> Path {
            self.cuts.push(Close());
            ensure_closed(&self.cuts);
            Path { cuts: self.cuts }
        }
    };
}

path_state! {
    Path:

    fn begin(x: f64, y: f64) -> Moved {
        Moved { cuts: vec![Goto(Pos{x, y})] }
    }

    fn goto(mut self, x: f64, y: f64) -> Moved {
        self.cuts.push(Goto(Pos{x,y}));
        Moved { cuts: self.cuts }
    }
}

path_state! {
    Moved:

    fn hole(mut self, diameter: f64) -> Path {
        self.cuts.push(Circle(diameter));
        self.cuts.push(Close());
        Path { cuts: self.cuts }
    }

    // first corner must be top left
    path_funky! { ws(radius) -> Forthing = Corner(radius, 0, -radius, radius) }

    // around the outside omitting the back
    fn frame(self, width: f64, depth: f64, radius: f64) -> Lefting {
        self.ws(radius).forth(depth)
            .ws(radius).right(width)
            .ws(radius).back(depth)
            .ws(radius)
    }

    fn rect(self, width: f64, depth: f64, radius: f64) -> Path {
        self.frame(width, depth, radius)
            .left(width)
            .close()
    }

    fn cutout(mut self, width: f64, depth: f64, radius: f64) -> Path {
        match self.cuts.pop() {
            Some(Goto(Pos{ x, y })) => {
                self.cuts.push(Goto(Pos{ x: x - width / 2.0,
                                         y: y - depth / 2.0 }));
                self.rect(width, depth, radius)
            }
            _ => unreachable!(),
        }
    }
}

path_state! { Backing:  path_fn! { back(depth)  -> Backed  = Back  } }
path_state! { Forthing: path_fn! { forth(depth) -> Forthed = Forth } }

path_state! {
    Lefting:
    path_fn! { left(width) -> Lefted = Left }

    fn recess(self, (a,b,c): (f64,f64,f64), d: f64, radius: f64) -> Lefted {
        self.left(a).ws(radius)
            .forth(d).cw(radius)
            .left(b).cw(radius)
            .back(d).ws(radius)
            .left(c)
    }

    // into the inside
    fn portal(self, long: f64, short: f64, depth: f64, radius: f64) -> Righted {
        self.left(long).ws(radius)
            .forth(depth).ws(radius)
            .right(short)
    }
}
path_state! {
    Righting:
    path_fn! { right(width) -> Righted = Right }

    // back to the outside
    fn portal(self, long: f64, short: f64, depth: f64, radius: f64) -> Lefted {
        self.right(short).ws(radius)
            .back(depth).ws(radius)
            .left(long)
    }
}

path_state! {
    Backed:
    path_funky! { cw(radius) -> Righting = Corner(radius, 1, radius, -radius) }
    path_funky! { ws(radius) -> Lefting = Corner(radius, 0, -radius, -radius) }
    path_closed!();
}

path_state! {
    Forthed:
    path_funky! { cw(radius) -> Lefting = Corner(radius, 1, -radius, radius) }
    path_funky! { ws(radius) -> Righting = Corner(radius, 0, radius, radius) }
    path_closed!();
}

path_state! {
    Lefted:
    path_funky! { cw(radius) -> Backing = Corner(radius, 1, -radius, -radius) }
    path_funky! { ws(radius) -> Forthing = Corner(radius, 0, -radius, radius) }
    path_closed!();
}

path_state! {
    Righted:
    path_funky! { cw(radius) -> Forthing = Corner(radius, 1, radius, radius) }
    path_funky! { ws(radius) -> Backing = Corner(radius, 0, radius, -radius) }
    path_closed!();

    // inner cut, in opposite direction
    fn frame(self, width: f64, depth: f64, radius: f64) -> Righting {
        self.cw(radius).forth(depth)
            .cw(radius).left(width)
            .cw(radius).back(depth)
            .cw(radius)
    }
}
