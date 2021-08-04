#![allow(dead_code)]

use anyhow::*;
use svg;

// we are mostly working in inches, except for the holes
const MM_IN: f64 = 25.4;

const KERF: f64 = 0.01;

const SWU: f64 = 0.75;

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
enum Cut {
    Goto(f64, f64),
    Back(f64),
    Forth(f64),
    Left(f64),
    Right(f64),
    Clockwise(f64),
    Widdershins(f64),
    Circle(f64),
}
use Cut::*;

fn ensure_closed(cuts: &Vec<Cut>) {
    let mut start_x = 0.0;
    let mut start_y = 0.0;
    let mut x = 0.0;
    let mut y = 0.0;
    for cut in cuts {
        match *cut {
            Goto(new_x, new_y) => {
                assert_eq!(start_x, x);
                assert_eq!(start_y, y);
                x = new_x;
                y = new_y;
                start_x = x;
                start_y = y;
            }
            Back(depth) => y -= depth,
            Forth(depth) => y += depth,
            Left(width) => x -= width,
            Right(width) => x += width,
            Clockwise(_) => (),
            Widdershins(_) => (),
            Circle(_) => (),
        }
    }
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

macro_rules! path_fn {
    {$name:ident = $cons:ident($arg:ident) -> $state:ident} => {
        fn $name(mut self, $arg: f64) -> $state {
            self.cuts.push($cons($arg));
            $state { cuts: self.cuts }
        }
    }
}

macro_rules! path_closed {
    () => {
        fn close(self) -> Completed {
            ensure_closed(&self.cuts);
            Completed { cuts: self.cuts }
        }
    };
}

path_state! {
    Path:

    fn new(x: f64, y: f64) -> Moved {
        Moved { cuts: vec![Goto(x, y)] }
    }
}

path_state! {
    Completed:

    fn goto(mut self, x: f64, y: f64) -> Moved {
        self.cuts.push(Goto(x,y));
        Moved { cuts: self.cuts }
    }

    fn done(self) -> Path {
        Path { cuts: self.cuts }
    }
}

path_state! {
    Moved:

    path_fn! { hole = Circle(diameter) -> Completed }

    // first corner must be top left
    path_fn! { ws = Widdershins(radius) -> Forthing }

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

path_state! { Backing:  path_fn! { back =  Back(depth) ->  Backed } }
path_state! { Forthing: path_fn! { forth = Forth(depth) -> Forthed } }

path_state! {
    Lefting:
    path_fn! { left =  Left(width) ->  Lefted }

    // into the inside
    fn portal(self, long: f64, short: f64, depth: f64, radius: f64) -> Righted {
        self.left(long).ws(radius).forth(depth).ws(radius).right(short)
    }
}
path_state! {
    Righting:
    path_fn! { right = Right(width) -> Righted }

    // back to the outside
    fn portal(self, long: f64, short: f64, depth: f64, radius: f64) -> Lefted {
        self.right(short).ws(radius).back(depth).ws(radius).left(long)
    }
}

path_state! {
    Backed:
    path_fn! { cw = Clockwise(radius) -> Righting }
    path_fn! { ws = Widdershins(radius) -> Lefting }
    path_closed!();
}

path_state! {
    Forthed:
    path_fn! { cw = Clockwise(radius) -> Lefting }
    path_fn! { ws = Widdershins(radius) -> Righting }
    path_closed!();
}

path_state! {
    Lefted:
    path_fn! { cw = Clockwise(radius) -> Backing }
    path_fn! { ws = Widdershins(radius) -> Forthing }
    path_closed!();
}

path_state! {
    Righted:
    path_fn! { cw = Clockwise(radius) -> Forthing }
    path_fn! { ws = Widdershins(radius) -> Backing }
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

fn main() {
    let path = Path::new(1.0, 1.0).rect(1.0, 2.0, 0.1).done();
    println!("{:#?}", path);
}
