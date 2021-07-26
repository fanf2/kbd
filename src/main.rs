use anyhow::*;
use svg;

// we are mostly working in inches, except for the holes
const MM_IN: f64 = 25.4;

const KERF: f64 = 0.01;

const SWU: f64 = 0.75;

const INNER: f64 = 0.5 * SWU;

const OUT_NEAR: f64 = 0.75 * SWU;
const OUT_SIDE: f64 = 1.0 * SWU;
const OUT_FAR: f64 = 1.25 * SWU;

const CORNER: f64 = 0.25 * SWU;
const BLUNT: f64 = (1.0 / 16.0) * SWU;

// clearance inside box
const PCB_GAP: f64 = BLUNT;

const RECESS_PCB_LEFT: f64 = 0.75 * SWU;
const RECESS_PCB_RIGHT: f64 = 0.75 * SWU;

// use the kerf to provide the right fit
const NUT_HOLE: f64 = 5.0 / MM_IN;
const SCREW_HOLE: f64 = 3.0 / MM_IN;

// for switches the kerf is larger than the tolerance
const SWITCH_HOLE: f64 = 14.0 / MM_IN - KERF;

const COUNT_WIDTH: u8 = 4;
const COUNT_DEPTH: u8 = 4;

const PCB_LEFT: f64 = OUT_SIDE + INNER;
const PCB_FAR: f64 = OUT_FAR + INNER;
const PCB_WIDTH: f64 = (COUNT_WIDTH as f64) * SWU;
const PCB_DEPTH: f64 = (COUNT_DEPTH as f64) * SWU;

const RECESS_LEFT: f64 = PCB_LEFT + RECESS_PCB_LEFT;
const RECESS_RIGHT: f64 = PCB_LEFT + PCB_WIDTH - RECESS_PCB_RIGHT;

const BOX_LEFT: f64 = PCB_LEFT - PCB_GAP;
const BOX_FAR: f64 = PCB_FAR - PCB_GAP;
const BOX_WIDTH: f64 = PCB_WIDTH + PCB_GAP * 2.0;
const BOX_DEPTH: f64 = PCB_DEPTH + PCB_GAP * 2.0;
const BOX_RIGHT: f64 = BOX_LEFT + BOX_WIDTH;
const BOX_NEAR: f64 = BOX_FAR + BOX_DEPTH;

const IN_WIDTH: f64 = PCB_WIDTH + 2.0 * INNER;
const IN_DEPTH: f64 = PCB_DEPTH + 2.0 * INNER;

const DRILL_FAR: f64 = (BOX_FAR + OUT_FAR) / 2.0;
const DRILL_NEAR: f64 = (BOX_NEAR + OUT_FAR + IN_DEPTH) / 2.0;
const DRILL_LEFT: f64 = (BOX_LEFT + OUT_SIDE) / 2.0;
const DRILL_RIGHT: f64 = (BOX_RIGHT + OUT_SIDE + IN_WIDTH) / 2.0;

const WIDTH: f64 = (OUT_SIDE + INNER) * 2.0 + PCB_WIDTH;
const DEPTH: f64 = OUT_FAR + OUT_NEAR + INNER * 2.0 + PCB_DEPTH;

#[derive(Clone)]
struct Path {
    data: svg::node::element::path::Data,
}

type Cut = svg::node::element::Element;

type Style<'a> = &'a [(&'a str, svg::node::Value)];

impl Path {
    fn new() -> Path {
        Path { data: svg::node::element::path::Data::new() }
    }

    fn close(self) -> Path {
        Path { data: self.data.close() }
    }

    fn move_to(self, x: f64, y: f64) -> Path {
        Path { data: self.data.move_to((x, y)) }
    }

    fn line_to(self, x: f64, y: f64) -> Path {
        Path { data: self.data.line_to((x, y)) }
    }

    fn open_rect(self, width: f64, depth: f64) -> Path {
        Path {
            data: self
                .data
                .line_by((0.0, depth))
                .line_by((width, 0.0))
                .line_by((0.0, -depth)),
        }
    }

    fn rounded_rect(self, width: f64, depth: f64, radius: f64) -> Path {
        Path {
            data: self
                .data
                .move_by((radius, 0.0))
                .elliptical_arc_by((radius, radius, 0, 0, 0, -radius, radius))
                .line_by((0.0, depth - radius * 2.0))
                .elliptical_arc_by((radius, radius, 0, 0, 0, radius, radius))
                .line_by((width - radius * 2.0, 0.0))
                .elliptical_arc_by((radius, radius, 0, 0, 0, radius, -radius))
                .line_by((0.0, -depth + radius * 2.0))
                .elliptical_arc_by((radius, radius, 0, 0, 0, -radius, -radius)),
        }
    }

    fn outer(self) -> Path {
        self.move_to(0.0, 0.0).rounded_rect(WIDTH, DEPTH, CORNER)
    }

    fn switch_hole(self, x: f64, y: f64, w: f64) -> Path {
        self.move_to(
            PCB_LEFT + (x + w / 2.0) * SWU - SWITCH_HOLE / 2.0,
            PCB_FAR + (y + 0.5) * SWU - SWITCH_HOLE / 2.0,
        )
        .open_rect(SWITCH_HOLE, SWITCH_HOLE)
        .close()
    }

    fn cut(self, style: Style) -> Cut {
        let mut path = svg::node::element::Path::new();
        for attr in style {
            path = path.set(attr.0, attr.1.clone());
        }
        path.set("d", self.data).into()
    }
}

fn hole(style: Style, cx: f64, cy: f64, d: f64) -> Cut {
    let mut hole = svg::node::element::Circle::new()
        .set("cx", cx)
        .set("cy", cy)
        .set("r", d / 2.0);
    for attr in style {
        hole = hole.set(attr.0, attr.1.clone());
    }
    hole.into()
}

fn drill(cut: Cut, style: Style, diameter: f64) -> Cut {
    svg::node::element::Group::new()
        .add(cut)
        .add(hole(style, DRILL_LEFT, DRILL_FAR, diameter))
        .add(hole(style, DRILL_LEFT, DRILL_NEAR, diameter))
        .add(hole(style, DRILL_RIGHT, DRILL_NEAR, diameter))
        .add(hole(style, DRILL_RIGHT, DRILL_FAR, diameter))
        .into()
}

fn outer(style: Style) -> Cut {
    Path::new()
        .outer()
        .move_to(OUT_SIDE, OUT_FAR)
        .open_rect(IN_WIDTH, IN_DEPTH)
        .close()
        .cut(style)
}

fn inner(style: Style) -> Cut {
    let path = Path::new()
        .move_to(OUT_SIDE, OUT_FAR)
        .rounded_rect(IN_WIDTH, IN_DEPTH, BLUNT)
        .close()
        .move_to(PCB_LEFT, PCB_FAR)
        .open_rect(PCB_WIDTH, PCB_DEPTH)
        .close()
        .cut(style);
    drill(path, style, SCREW_HOLE)
}

fn plate(style: Style, hole: f64) -> Cut {
    let mut path = Path::new();
    for x in 0..COUNT_WIDTH {
        for y in 0..COUNT_DEPTH {
            path = path.switch_hole(x as f64, y as f64, 1.0);
        }
    }
    let plate = path.outer().close().cut(style);
    drill(plate, style, hole)
}

fn closed_box(style: Style) -> Cut {
    let path = Path::new()
        .outer()
        .close()
        .move_to(BOX_LEFT, BOX_FAR)
        .open_rect(BOX_WIDTH, BOX_DEPTH)
        .close()
        .cut(style);
    drill(path, style, NUT_HOLE)
}

fn open_box(style: Style) -> Cut {
    let path = Path::new()
        .outer()
        .line_to(RECESS_RIGHT, 0.0)
        .line_to(RECESS_RIGHT, BOX_FAR)
        .line_to(BOX_RIGHT, BOX_FAR)
        .open_rect(-BOX_WIDTH, BOX_DEPTH) // reverse
        .line_to(RECESS_LEFT, BOX_FAR)
        .line_to(RECESS_LEFT, 0.0)
        .close()
        .cut(style);
    drill(path, style, NUT_HOLE)
}

fn base(style: Style) -> Cut {
    let path = Path::new()
        .outer()
        .line_to(RECESS_RIGHT, 0.0)
        .line_to(RECESS_RIGHT, PCB_FAR)
        .line_to(RECESS_LEFT, PCB_FAR)
        .line_to(RECESS_LEFT, 0.0)
        .close()
        .cut(style);
    drill(path, style, NUT_HOLE)
}

fn save(name: &str, cut: Cut) -> Result<()> {
    let size = (-SWU, -SWU, WIDTH + SWU * 2.0, DEPTH + SWU * 2.0);
    let document = svg::Document::new()
        .set("width", format!("{}in", size.2))
        .set("height", format!("{}in", size.3))
        .set("viewBox", size)
        .add(cut);
    svg::save(name, &document)?;
    Ok(())
}

fn main() -> Result<()> {
    let style = &[
        ("fill", "none".into()),
        ("stroke", "olive".into()),
        ("stroke-width", KERF.into()),
    ];

    let o = outer(style);
    let i = inner(style);
    let pn = plate(style, NUT_HOLE);
    let ps = plate(style, SCREW_HOLE);
    let c = closed_box(style);
    let r = open_box(style);
    let b = base(style);

    save("keybow/outer.svg", o.clone())?;
    save("keybow/inner.svg", i.clone())?;
    save("keybow/plate_nut.svg", pn.clone())?;
    save("keybow/plate_screw.svg", ps.clone())?;
    save("keybow/closed_box.svg", c.clone())?;
    save("keybow/open_box.svg", r.clone())?;
    save("keybow/base.svg", b.clone())?;

    let all = svg::node::element::Group::new()
        .add(o)
        .add(i)
        .add(ps)
        .add(c)
        .add(r)
        .add(b)
        .into();
    save("keybow/all.svg", all)?;

    Ok(())
}
