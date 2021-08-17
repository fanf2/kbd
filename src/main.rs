#![allow(dead_code)]

use anyhow::*;

const WIDTH: i8 = 15;
const DEPTH: i8 = 5;

const HHKB: bool = WIDTH > 10;

const fn hhkb_ortho(hhkb: f64, ortho: f64) -> f64 {
    if HHKB {
        hhkb
    } else {
        ortho
    }
}

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

const BLACK_LR: f64 = 1.0 * SWU;
const BLACK_NF: f64 = 0.5 * SWU;
const BLACK_X: f64 = -BLACK_LR;
const BLACK_Y: f64 = -BLACK_NF;
const BLACK_W: f64 = KEYS_W + BLACK_LR * 2.0;
const BLACK_D: f64 = KEYS_D + BLACK_NF * 2.0;

const CREAM_LR: f64 = 1.0 * SWU;
const CREAM_NEAR: f64 = 0.75 * SWU;
const CREAM_FAR: f64 = 1.25 * SWU;
const CREAM_X: f64 = BLACK_X - CREAM_LR;
const CREAM_Y: f64 = BLACK_Y - CREAM_FAR;
const CREAM_W: f64 = BLACK_W + CREAM_LR * 2.0;
const CREAM_D: f64 = BLACK_D + CREAM_FAR + CREAM_NEAR;

const BOX_GAP: f64 = BLUNT;
const BOX_X: f64 = -BOX_GAP;
const BOX_Y: f64 = -BOX_GAP;
const BOX_W: f64 = KEYS_W + BOX_GAP * 2.0;
const BOX_D: f64 = KEYS_D + BOX_GAP * 2.0;

const RECESS_LEFT: f64 = CREAM_LR + BLACK_LR + hhkb_ortho(SWU / 8.0, SWU / 2.0);
const RECESS_MID: f64 = hhkb_ortho(SWU * 14.0 / 8.0, SWU * 3.0);
const RECESS_RIGHT: f64 = CREAM_W - RECESS_LEFT - RECESS_MID;
const RECESS_INNER: f64 = CREAM_LR + BLACK_LR - BOX_GAP;
const RECESS_L_IN: f64 = RECESS_LEFT - RECESS_INNER;
const RECESS_R_IN: f64 = RECESS_RIGHT - RECESS_INNER;
const RECESS_PCB: f64 = CREAM_FAR + BLACK_NF;
const RECESS_BOX: f64 = RECESS_PCB - BOX_GAP;

// use the kerf to provide the right fit
const SCREW_HOLE: f64 = 3.0 / MM_IN;
const RIVET_HOLE: f64 = 5.0 / MM_IN;

const AROUND_HOLE: f64 = 4.0 / MM_IN; // radius

const DRILL_LEFT: f64 = BLACK_X + AROUND_HOLE;
const DRILL_RIGHT: f64 = BLACK_X + BLACK_W - AROUND_HOLE;
const DRILL_LEFTISH: f64 = KEYS_X + KEYS_W * 1.0 / 3.0;
const DRILL_RIGHTISH: f64 = KEYS_X + KEYS_W * 2.0 / 3.0;
const DRILL_FAR: f64 = BLACK_Y + AROUND_HOLE;
const DRILL_NEAR: f64 = BLACK_Y + BLACK_D - AROUND_HOLE;

// for switches the kerf is larger than the tolerance
const SWITCH_HOLE: f64 = 14.0 / MM_IN - KERF;

const STAB_DEPTH: f64 = (0.26 - 0.484 + 0.53) * 2.0;
const STAB_WIDTH: f64 = 1.0 / 3.0;
const STAB_OFFSET_2U: f64 = 1.0 / 2.0;
const STAB_OFFSET_7U: f64 = 4.5 / 2.0;

const STAB_GAP: f64 = STAB_OFFSET_2U - STAB_WIDTH / 2.0 - SWITCH_HOLE / 2.0;
const STAB_JOIN: f64 = SWITCH_HOLE * 0.75;

fn base() -> Path {
    Path::begin(CREAM_X, CREAM_Y)
        .frame(CREAM_W, CREAM_D, SMOOTH)
        .left(RECESS_RIGHT)
        .ws(BLUNT)
        .ucw(RECESS_PCB, RECESS_MID, RECESS_PCB, BLUNT)
        .ws(BLUNT)
        .left(RECESS_LEFT)
        .close()
        .drill(RIVET_HOLE, RIVET_HOLE)
}

fn socket() -> Path {
    Path::begin(CREAM_X, CREAM_Y)
        .frame(CREAM_W, CREAM_D, SMOOTH)
        .uws(RECESS_RIGHT, RECESS_BOX, RECESS_R_IN, BLUNT)
        .frame(BOX_W, BOX_D, BLUNT)
        .uws(RECESS_L_IN, RECESS_BOX, RECESS_LEFT, BLUNT)
        .close()
        .drill(RIVET_HOLE, RIVET_HOLE)
}

fn closed() -> Path {
    Path::begin(CREAM_X, CREAM_Y)
        .rect(CREAM_W, CREAM_D, SMOOTH)
        .goto(BOX_X, BOX_Y)
        .rect(BOX_W, BOX_D, BLUNT)
        .drill(SCREW_HOLE, RIVET_HOLE)
}

fn plate() -> Path {
    Path::begin(CREAM_X, CREAM_Y)
        .rect(CREAM_W, CREAM_D, SMOOTH)
        .drill(SCREW_HOLE, SCREW_HOLE)
        .keys()
}

fn shim() -> Path {
    Path::begin(CREAM_X, CREAM_Y)
        .rect(CREAM_W, CREAM_D, SMOOTH)
        .goto(KEYS_X, KEYS_Y)
        .rect(KEYS_W, KEYS_D, SHARP)
        .drill(SCREW_HOLE, SCREW_HOLE)
        .feet()
}

fn cream_top() -> Path {
    // inner radius should be sharper than outer radius of black top
    Path::begin(CREAM_X, CREAM_Y)
        .rect(CREAM_W, CREAM_D, SMOOTH)
        .goto(BLACK_X, BLACK_Y)
        .rect(BLACK_W, BLACK_D, SHARP)
}

fn black_top() -> Path {
    // base of keycaps is 18mm leaving a 0.5mm gap between keycaps and
    // the KEYS rectangle; the SHARP radius is 0.8mm; distance between
    // keycap corner and centre of SHARP curve is 0.3mm orthogonally,
    // or sqrt(2) * 0.3 == 0.4mm diagonally, so distance betweem
    // keycap corner and SHARP corner is 0.4mm.
    Path::begin(BLACK_X, BLACK_Y)
        .rect(BLACK_W, BLACK_D, BLUNT)
        .goto(KEYS_X, KEYS_Y)
        .rect(KEYS_W, KEYS_D, SHARP)
        .drill(SCREW_HOLE, SCREW_HOLE)
}

fn main() -> Result<()> {
    let mut all = Path { cuts: vec![] };
    std::env::set_current_dir(if HHKB { "hhkb" } else { "keybow" })?;
    all.concat(save_svg("L0_clear15.svg", base())?);
    all.concat(save_svg("L12_beige30.svg", socket())?);
    all.concat(save_svg("L3_beige30.svg", closed())?);
    all.concat(save_svg("L4_clear15.svg", plate())?);
    all.concat(save_svg("L5_clear15.svg", shim())?);
    all.concat(save_svg("L67_beige30.svg", beige_top())?);
    all.concat(save_svg("L8_black50.svg", black_top())?);
    save_svg("all.svg", all)?;
    Ok(())
}

impl Path {
    fn drill(mut self, d_far: f64, d_near: f64) -> Path {
        self = self
            .goto(DRILL_LEFT, DRILL_FAR)
            .hole(d_far)
            .goto(DRILL_RIGHT, DRILL_FAR)
            .hole(d_far)
            .goto(DRILL_LEFT, DRILL_NEAR)
            .hole(d_near)
            .goto(DRILL_RIGHT, DRILL_NEAR)
            .hole(d_near);
        if WIDTH > DEPTH * 2 {
            self = self
                .goto(DRILL_LEFTISH, DRILL_FAR)
                .hole(d_far)
                .goto(DRILL_RIGHTISH, DRILL_FAR)
                .hole(d_far)
                .goto(DRILL_LEFTISH, DRILL_NEAR)
                .hole(d_near)
                .goto(DRILL_RIGHTISH, DRILL_NEAR)
                .hole(d_near);
        }
        self
    }

    fn keys(self) -> Path {
        if HHKB {
            self.hhkb_keys()
        } else {
            self.ortho_keys()
        }
    }

    fn feet(self) -> Path {
        if HHKB {
            self.hhkb_feet()
        } else {
            self.ortho_feet()
        }
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

    fn hhkb_feet(mut self) -> Path {
        for y in 1..DEPTH {
            self = self.hhkb_foot(4.0 * SWU, y as f64);
            self = self.hhkb_foot(11.0 * SWU, y as f64);
        }
        self
    }

    fn hhkb_foot(self, mid: f64, y: f64) -> Path {
        let wid = (DRILL_LEFTISH - DRILL_LEFT) / 2.0;
        let rad = AROUND_HOLE + y / MM_IN;
        self.goto(mid - wid, y * SWU)
            .hole(RIVET_HOLE)
            .goto(mid + wid, y * SWU)
            .hole(RIVET_HOLE)
            .goto(mid - wid - rad, y * SWU - rad)
            .rect(wid * 2.0 + rad * 2.0, rad * 2.0, AROUND_HOLE)
    }

    fn switch(self, w: f64, mut x: f64, mut y: f64) -> Path {
        let width = w * SWU;
        let depth = 1.0 * SWU;
        if x < 0.0 {
            x += WIDTH as f64;
        }
        x = x * SWU + width / 2.0;
        y = y * SWU + depth / 2.0;
        if 1.0 - KERF < w && w < 2.0 - KERF {
            return self.goto(x, y).cutout(SWITCH_HOLE, SWITCH_HOLE, KERF);
        }
        if 2.0 - KERF < w && w < 3.0 - KERF {
            return self.switch_stab(x, y);
        }
        if 7.0 - KERF < w && w < 7.0 + KERF {
            return self
                .goto(x - STAB_OFFSET_7U, y)
                .cutout(STAB_WIDTH, STAB_DEPTH, KERF)
                .goto(x + STAB_OFFSET_7U, y)
                .cutout(STAB_WIDTH, STAB_DEPTH, KERF)
                .goto(x, y)
                .cutout(SWITCH_HOLE, SWITCH_HOLE, KERF);
        }
        unreachable!("unsupported key size {}", w)
    }

    fn switch_stab(self, x: f64, y: f64) -> Path {
        self.goto(x - SWITCH_HOLE / 2.0, y - SWITCH_HOLE / 2.0)
            .ws(KERF)
            .ucw(
                (SWITCH_HOLE - STAB_JOIN) / 2.0,
                STAB_GAP,
                (STAB_DEPTH - STAB_JOIN) / 2.0,
                KERF,
            )
            .frame(STAB_WIDTH, STAB_DEPTH, KERF)
            .ucw(
                (STAB_DEPTH - STAB_JOIN) / 2.0,
                STAB_GAP,
                (SWITCH_HOLE - STAB_JOIN) / 2.0,
                KERF,
            )
            .ws(KERF)
            .right(SWITCH_HOLE)
            .ws(KERF)
            .ucw(
                (SWITCH_HOLE - STAB_JOIN) / 2.0,
                STAB_GAP,
                (STAB_DEPTH - STAB_JOIN) / 2.0,
                KERF,
            )
            .frame(STAB_WIDTH, STAB_DEPTH, KERF)
            .ucw(
                (STAB_DEPTH - STAB_JOIN) / 2.0,
                STAB_GAP,
                (SWITCH_HOLE - STAB_JOIN) / 2.0,
                KERF,
            )
            .ws(KERF)
            .left(SWITCH_HOLE)
            .close()
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

fn save_svg(name: &str, path: Path) -> Result<Path> {
    let bbox = ensure_closed(&path.cuts);
    let margin = 0.25;
    let width = bbox.max.x - bbox.min.x + margin * 2.0;
    let depth = bbox.max.y - bbox.min.y + margin * 2.0;
    let size = (bbox.min.x - margin, bbox.min.y - margin, width, depth);
    let document = svg::Document::new()
        .set("width", format!("{}in", width))
        .set("height", format!("{}in", depth))
        .set("viewBox", size)
        .add(to_svg(&path.cuts));
    svg::save(name, &document)?;
    Ok(path)
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

path_state! {
    Path:

    fn begin(x: f64, y: f64) -> Moved {
        Moved { cuts: vec![Goto(Pos{x, y})] }
    }

    fn goto(mut self, x: f64, y: f64) -> Moved {
        self.cuts.push(Goto(Pos{x,y}));
        Moved { cuts: self.cuts }
    }

    fn concat(&mut self, other: Path) {
        self.cuts.extend_from_slice(&other.cuts);
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

path_state! {
    Backing:
    path_fn! { back(depth) -> Backed = Back }

    fn ucw(self, back: f64, right: f64, forth: f64, radius: f64) -> Forthed {
        self.back(back).cw(radius)
            .right(right).cw(radius)
            .forth(forth)
    }
}

path_state! {
    Forthing:
    path_fn! { forth(depth) -> Forthed = Forth }

    fn ucw(self, forth: f64, left: f64, back: f64, radius: f64) -> Backed {
        self.forth(forth).cw(radius)
            .left(left).cw(radius)
            .back(back)
    }
}

path_state! {
    Lefting:
    path_fn! { left(width) -> Lefted = Left }

    fn uws(self, left: f64, forth: f64, right: f64, radius: f64) -> Righted {
        self.left(left).ws(radius)
            .forth(forth).ws(radius)
            .right(right)
    }
}
path_state! {
    Righting:
    path_fn! { right(width) -> Righted = Right }

    fn uws(self, right: f64, back: f64, left: f64, radius: f64) -> Lefted {
        self.right(right).ws(radius)
            .back(back).ws(radius)
            .left(left)
    }
}

path_state! {
    Backed:
    path_funky! { cw(radius) -> Righting = Corner(radius, 1, radius, -radius) }
    path_funky! { ws(radius) -> Lefting = Corner(radius, 0, -radius, -radius) }

    fn frame(self, width: f64, depth: f64, radius: f64) -> Backing {
        self.ws(radius).left(width)
            .ws(radius).forth(depth)
            .ws(radius).right(width)
            .ws(radius)
    }
}

path_state! {
    Forthed:
    path_funky! { cw(radius) -> Lefting = Corner(radius, 1, -radius, radius) }
    path_funky! { ws(radius) -> Righting = Corner(radius, 0, radius, radius) }

    fn frame(self, width: f64, depth: f64, radius: f64) -> Forthing {
        self.ws(radius).right(width)
            .ws(radius).back(depth)
            .ws(radius).left(width)
            .ws(radius)
    }
}

path_state! {
    Lefted:
    path_funky! { cw(radius) -> Backing = Corner(radius, 1, -radius, -radius) }
    path_funky! { ws(radius) -> Forthing = Corner(radius, 0, -radius, radius) }

    fn close(mut self) -> Path {
        self.cuts.push(Close());
        ensure_closed(&self.cuts);
        Path { cuts: self.cuts }
    }
}

path_state! {
    Righted:
    path_funky! { cw(radius) -> Forthing = Corner(radius, 1, radius, radius) }
    path_funky! { ws(radius) -> Backing = Corner(radius, 0, radius, -radius) }

    // inner cut, in opposite direction
    fn frame(self, width: f64, depth: f64, radius: f64) -> Righting {
        self.cw(radius).forth(depth)
            .cw(radius).left(width)
            .cw(radius).back(depth)
            .cw(radius)
    }
}
