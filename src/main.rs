#![allow(dead_code)]

use anyhow::*;
use svg;

// we are mostly working in inches, except for the holes
const MM_IN: f64 = 25.4;

const KERF: f64 = 0.01; // inch

const SWU: f64 = 0.75; // inch

const BLACK: f64 = 0.5 * SWU;

const BEIGE_NEAR: f64 = 0.75 * SWU;
const BEIGE_SIDE: f64 = 1.0 * SWU;
const BEIGE_FAR: f64 = 1.25 * SWU;

// for switches the kerf is larger than the tolerance
const SWITCH_HOLE: f64 = 14.0 / MM_IN - KERF;

// use the kerf to provide the right fit
const RIVET_HOLE: f64 = 5.0 / MM_IN;
const SCREW_HOLE: f64 = 3.0 / MM_IN;

#[derive(Clone, Copy, Debug, PartialEq)]
struct Pos {
    x: f64,
    y: f64,
}

#[derive(Clone, Copy, Debug, PartialEq)]
struct Bounds {
    min: Pos,
    max: Pos,
}

fn min(a: f64, b: f64) -> f64 {
    if a <= b {
        a
    } else {
        b
    }
}

fn max(a: f64, b: f64) -> f64 {
    if a >= b {
        a
    } else {
        b
    }
}

fn bounds(bbox: Bounds, pos: Pos) -> Bounds {
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
    Corner(f64, f64, f64),
    Close(),
    Circle(f64),
}
use Cut::*;

type SvgCircle = svg::node::element::Circle;
type SvgGroup = svg::node::element::Group;
type SvgPath = svg::node::element::Path;
type PathData = svg::node::element::path::Data;

type SvgStyle<'a> = &'a [(&'a str, svg::node::Value)];

fn to_svg(cuts: &Vec<Cut>) -> SvgGroup {
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

            (Goto(Pos { x, y }), Corner(r, _, _)) => p = p.move_to((x + r, y)),

            (Back(depth), Corner(nr, _, _)) => {
                p = p.line_by((0, -(depth - pr - nr)))
            }

            (Forth(depth), Corner(nr, _, _)) => {
                p = p.line_by((0, depth - pr - nr))
            }

            (Left(depth), Corner(nr, _, _)) => {
                p = p.line_by((-(depth - pr - nr), 0))
            }

            (Right(depth), Corner(nr, _, _)) => {
                p = p.line_by((depth - pr - nr, 0))
            }

            (Corner(r, x, y), _) => {
                p = p.elliptical_arc_by((r, r, 0, 0, 0, x, y));
                pr = r;
            }

            _ => unimplemented!(),
        }
    }
    unreachable!()
}

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

fn ensure_closed(cuts: &Vec<Cut>) -> Bounds {
    let mut start = None;
    let mut cur = Pos { x: 0.0, y: 0.0 };
    let mut bbox = Bounds { min: cur, max: cur };
    for cut in cuts {
        match *cut {
            Close() => {
                assert_eq!(start, Some(cur));
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
            Corner(_, _, _) => (),
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
        fn close(mut self) -> Completed {
            self.cuts.push(Close());
            ensure_closed(&self.cuts);
            Completed { cuts: self.cuts }
        }
    };
}

path_state! {
    Path:

    fn new(x: f64, y: f64) -> Moved {
        Moved { cuts: vec![Goto(Pos{x, y})] }
    }
}

path_state! {
    Completed:

    fn goto(mut self, x: f64, y: f64) -> Moved {
        self.cuts.push(Goto(Pos{x,y}));
        Moved { cuts: self.cuts }
    }

    fn done(self) -> Path {
        Path { cuts: self.cuts }
    }
}

path_state! {
    Moved:

    fn hole(mut self, diameter: f64) -> Completed {
        self.cuts.push(Circle(diameter));
        self.cuts.push(Close());
        Completed { cuts: self.cuts }
    }

    // first corner must be top left
    path_funky! { ws(radius) -> Forthing = Corner(radius, -radius, radius) }

    // around the outside omitting the back
    fn frame(self, width: f64, depth: f64, radius: f64) -> Lefting {
        self.ws(radius)
        .forth(depth)
        .ws(radius)
        .right(width)
        .ws(radius)
        .back(depth)
        .ws(radius)
    }

    fn rect(self, width: f64, depth: f64, radius: f64) -> Completed {
        self.frame(width, depth, radius)
        .left(width)
        .close()
    }
}

path_state! { Backing:  path_fn! { back(depth)  -> Backed  = Back  } }
path_state! { Forthing: path_fn! { forth(depth) -> Forthed = Forth } }

path_state! {
    Lefting:
    path_fn! { left(width) -> Lefted = Left }

    // into the inside
    fn portal(self, long: f64, short: f64, depth: f64, radius: f64) -> Righted {
        self.left(long).ws(radius).forth(depth).ws(radius).right(short)
    }
}
path_state! {
    Righting:
    path_fn! { right(width) -> Righted = Right }

    // back to the outside
    fn portal(self, long: f64, short: f64, depth: f64, radius: f64) -> Lefted {
        self.right(short).ws(radius).back(depth).ws(radius).left(long)
    }
}

path_state! {
    Backed:
    path_funky! { cw(radius) -> Righting = Corner(radius, radius, -radius) }
    path_funky! { ws(radius) -> Lefting = Corner(radius, -radius, -radius) }
    path_closed!();
}

path_state! {
    Forthed:
    path_funky! { cw(radius) -> Lefting = Corner(radius, -radius, radius) }
    path_funky! { ws(radius) -> Righting = Corner(radius, radius, radius) }
    path_closed!();
}

path_state! {
    Lefted:
    path_funky! { cw(radius) -> Backing = Corner(radius, -radius, -radius) }
    path_funky! { ws(radius) -> Forthing = Corner(radius, -radius, radius) }
    path_closed!();
}

path_state! {
    Righted:
    path_funky! { cw(radius) -> Forthing = Corner(radius, radius, radius) }
    path_funky! { ws(radius) -> Backing = Corner(radius, radius, -radius) }
    path_closed!();

    // inner cut, in opposite direction
    fn frame(self, width: f64, depth: f64, radius: f64) -> Righting {
        self.cw(radius)
            .forth(depth)
            .cw(radius)
            .left(width)
            .cw(radius)
            .back(depth)
            .cw(radius)
    }
}

fn main() -> Result<()> {
    let path = Path::new(1.0, 1.0).rect(1.0, 2.0, 0.1).done();
    save_svg("keybow/test.svg", &path, SWU)?;
    Ok(())
}
