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

const PCB_LEFT: f64 = OUT_SIDE + INNER;
const PCB_FAR: f64 = OUT_FAR + INNER;
const PCB_WIDTH: f64 = (COUNT_WIDTH as f64) * SWU;
const PCB_DEPTH: f64 = (COUNT_DEPTH as f64) * SWU;

const PCB_GAP: f64 = BLUNT;

const BOX_LEFT: f64 = PCB_LEFT - PCB_GAP;
const BOX_FAR: f64 = PCB_FAR - PCB_GAP;
const BOX_WIDTH: f64 = PCB_WIDTH + PCB_GAP * 2.0;
const BOX_DEPTH: f64 = PCB_DEPTH + PCB_GAP * 2.0;

const IN_WIDTH: f64 = PCB_WIDTH + 2.0 * INNER;
const IN_DEPTH: f64 = PCB_DEPTH + 2.0 * INNER;

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

    fn move_to(self, x: f64, y: f64) -> Path {
        Path { data: self.data.move_to((x, y)) }
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

    fn surround_holder(self) -> Path {
        self.move_to(OUT_SIDE, OUT_FAR).open_rect(IN_WIDTH, IN_DEPTH).close()
    }

    fn surround_outer(self) -> Path {
        self.move_to(OUT_SIDE, OUT_FAR)
            .rounded_rect(IN_WIDTH, IN_DEPTH, BLUNT)
            .close()
    }

    fn surround_inner(self) -> Path {
        self.move_to(PCB_LEFT, PCB_FAR).open_rect(PCB_WIDTH, PCB_DEPTH).close()
    }

    fn pcb_box(self) -> Path {
        self.open_rect(BOX_WIDTH, BOX_DEPTH)
    }

    fn switch_hole(self, x: f64, y: f64, w: f64) -> Path {
        self.move_to(
            PCB_LEFT + (x + w / 2.0) * SWU - SWITCH_HOLE / 2.0,
            PCB_FAR + (y + 0.5) * SWU - SWITCH_HOLE / 2.0,
        )
        .open_rect(SWITCH_HOLE, SWITCH_HOLE)
        .close()
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
    path = path.surround_inner().surround_outer().outer().close();

    let size = (-SWU, -SWU, WIDTH + SWU * 2.0, DEPTH + SWU * 2.0);

    let document = svg::Document::new()
        .set("width", format!("{}in", size.2))
        .set("height", format!("{}in", size.3))
        .set("viewBox", size)
        .add(path.cut());

    svg::save("keybow/keybow.svg", &document)?;

    Ok(())
}
