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

const RECESS_LEFT: f64 = 0.75 * SWU;
const RECESS_RIGHT: f64 = 0.75 * SWU;

// use the kerf to provide the right fit
const NUT_HOLE: f64 = 5.0 / MM_IN;
const SCREW_HOLE: f64 = 3.0 / MM_IN;

// for switches the kerf is larger than the tolerance
const SWITCH_HOLE: f64 = 14.0 / MM_IN - KERF;

const SW_WIDTH: u8 = 4;
const SW_DEPTH: u8 = 4;

const SWIN_WIDTH: f64 = (SW_WIDTH as f64) * SWU;
const SWIN_DEPTH: f64 = (SW_DEPTH as f64) * SWU;

const IN_WIDTH: f64 = (OUT_SIDE + INNER) * 2.0 + SWIN_WIDTH;
const IN_DEPTH: f64 = OUT_FAR + OUT_NEAR + INNER * 2.0 + SWIN_DEPTH;

struct Path {
    data: svg::node::element::path::Data,
}

impl Path {
    fn new() -> Self {
        Path { data: svg::node::element::path::Data::new() }
    }

    fn outer(self) -> Self {
        unimplemented!()
    }

    fn switch_hole(self, x: f64, y: f64, w: f64) -> Path {
        let left = OUT_SIDE + INNER + (x + w / 2.0) * SWU - SWITCH_HOLE / 2.0;
        let far = OUT_FAR + INNER + (y + 0.5) * SWU - SWITCH_HOLE / 2.0;
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
    for x in 0..SW_WIDTH {
        for y in 0..SW_DEPTH {
            path = path.switch_hole(x as f64, y as f64, 1.0);
        }
    }

    let size = (-KERF, -KERF, IN_WIDTH + KERF, IN_DEPTH + KERF);

    let document = svg::Document::new()
        .set("width", format!("{}in", IN_WIDTH + KERF * 2.0))
        .set("height", format!("{}in", IN_DEPTH + KERF * 2.0))
        .set("viewBox", size)
        .add(path.cut());

    svg::save("keybow/keybow.svg", &document)?;

    Ok(())
}
