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

const RECESS_LEFT: f64 = 0.75 * SWU;
const RECESS_RIGHT: f64 = 0.75 * SWU;

// use the kerf to provide the right fit
const NUT_HOLE: f64 = 5.0 / MM_IN;
const SCREW_HOLE: f64 = 3.0 / MM_IN;

// for switches the kerf is larger than the tolerance
const SWITCH_HOLE: f64 = 14.0 / MM_IN - KERF;

const COUNT_WIDTH: u8 = 4;
const COUNT_DEPTH: u8 = 4;

const PCB_WIDTH: f64 = (COUNT_WIDTH as f64) * SWU;
const PCB_DEPTH: f64 = (COUNT_DEPTH as f64) * SWU;

const PCB_LEFT: f64 = OUT_SIDE + INNER;
const PCB_FAR: f64 = OUT_FAR + INNER;

const PCB_GAP: f64 = BLUNT;

const IN_RIGHT: f64 = OUT_SIDE + PCB_WIDTH + 2.0 * INNER;
const IN_NEAR: f64 = OUT_FAR + PCB_DEPTH + 2.0 * INNER;

const WIDTH: f64 = (OUT_SIDE + INNER) * 2.0 + PCB_WIDTH;
const DEPTH: f64 = OUT_FAR + OUT_NEAR + INNER * 2.0 + PCB_DEPTH;

struct Path {
    data: svg::node::element::path::Data,
}

impl Path {
    fn new() -> Path {
        Path { data: svg::node::element::path::Data::new() }
    }

    fn close(self) -> Path {
        Path { data: self.data.close() }
    }

    fn outer(self) -> Path {
        Path {
            data: self
                .data
                .move_to((CORNER, 0.0))
                .elliptical_arc_by((CORNER, CORNER, 0, 0, 0, -CORNER, CORNER))
                .line_to((0.0, DEPTH - CORNER))
                .elliptical_arc_by((CORNER, CORNER, 0, 0, 0, CORNER, CORNER))
                .line_to((WIDTH - CORNER, DEPTH))
                .elliptical_arc_by((CORNER, CORNER, 0, 0, 0, CORNER, -CORNER))
                .line_to((WIDTH, CORNER))
                .elliptical_arc_by((CORNER, CORNER, 0, 0, 0, -CORNER, -CORNER)),
        }
    }

    fn surround_inner(self) -> Path {
        Path {
            data: self
                .data
                .move_to((OUT_SIDE + BLUNT, OUT_FAR))
                .elliptical_arc_by((BLUNT, BLUNT, 0, 0, 0, -BLUNT, BLUNT))
                .line_to((OUT_SIDE, IN_NEAR - BLUNT))
                .elliptical_arc_by((BLUNT, BLUNT, 0, 0, 0, BLUNT, BLUNT))
                .line_to((IN_RIGHT - BLUNT, IN_NEAR))
                .elliptical_arc_by((BLUNT, BLUNT, 0, 0, 0, BLUNT, -BLUNT))
                .line_to((IN_RIGHT, OUT_FAR + BLUNT))
                .elliptical_arc_by((BLUNT, BLUNT, 0, 0, 0, -BLUNT, -BLUNT))
                .close(),
        }
    }

    fn surround_outer(self) -> Path {
        Path {
            data: self
                .data
                .move_to((OUT_SIDE, OUT_FAR))
                .line_to((OUT_SIDE, IN_NEAR))
                .line_to((IN_RIGHT, IN_NEAR))
                .line_to((IN_RIGHT, OUT_FAR))
                .close(),
        }
    }

    fn inner(self) -> Path {
        Path {
            data: self
                .data
                .move_to((PCB_LEFT, PCB_FAR))
                .line_to((PCB_LEFT, PCB_FAR + PCB_DEPTH))
                .line_to((PCB_LEFT + PCB_WIDTH, PCB_FAR + PCB_DEPTH))
                .line_to((PCB_LEFT + PCB_WIDTH, PCB_FAR))
                .close(),
        }
    }

    fn switch_hole(self, x: f64, y: f64, w: f64) -> Path {
        let left = PCB_LEFT + (x + w / 2.0) * SWU - SWITCH_HOLE / 2.0;
        let far = PCB_FAR + (y + 0.5) * SWU - SWITCH_HOLE / 2.0;
        let right = left + SWITCH_HOLE;
        let near = far + SWITCH_HOLE;
        Path {
            data: self
                .data
                .move_to((left, far))
                .line_to((left, near))
                .line_to((right, near))
                .line_to((right, far))
                .close(),
        }
    }

    fn cut(self) -> svg::node::element::Path {
        svg::node::element::Path::new()
            .set("fill", "none")
            .set("stroke", "black")
            .set("stroke-width", KERF)
            .set("d", self.data)
    }
}

fn main() -> Result<()> {
    let mut path = Path::new();
    for x in 0..COUNT_WIDTH {
        for y in 0..COUNT_DEPTH {
            path = path.switch_hole(x as f64, y as f64, 1.0);
        }
    }
    path = path.inner().surround_outer().outer().close();

    let size = (-SWU, -SWU, WIDTH + SWU * 2.0, DEPTH + SWU * 2.0);

    let document = svg::Document::new()
        .set("width", format!("{}in", size.2))
        .set("height", format!("{}in", size.3))
        .set("viewBox", size)
        .add(path.cut());

    svg::save("keybow/keybow.svg", &document)?;

    Ok(())
}
