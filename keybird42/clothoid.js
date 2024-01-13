"use strict";

const tau = Math.PI * 2;
const sin = Math.sin;
const cos = Math.cos;
const exp = Math.exp;
const sqrt = Math.sqrt;

function main() {
    let c = canvas.getContext("2d");
    c.translate(canvas.width/2, canvas.height/2);
    c.scale(1000, 1000);

    function style(w, s, f) {
	c.lineWidth = w;
	c.strokeStyle = s;
	c.fillStyle = f;
    }

    function circle(x, y, r) {
	c.beginPath();
	c.roundRect(x - r, y - r, 2*r, 2*r, r);
	c.fill();
	c.stroke();
    }

    // https://enwp.org/Euler_spiral
    // x = ∫ cos(s²) ds
    // y = ∫ sin(s²) ds

    function clothoid(fun) {
	let s = 0;
	let x = 0;
	let y = 0;
	for (;;) {
	    let ds = 0.01; // integration step size
	    let dx = cos(s*s) * ds;
	    let dy = sin(s*s) * ds;
	    if (fun(s, x, y, dx, dy)) {
		return;
	    }
	    s += ds;
	    x += dx;
	    y += dy;
	}
    }

    // eyeballed limit of curve as s → ∞
    const lim_c = 1 - exp(-1);
    // size of infill around limit
    const lim_r = 1/4;

    function length(x, y) {
	return (sqrt(x*x + y*y));
    }

    function inside(x, y) {
	return (length(lim_c - x, lim_c - y) < lim_r);
    }

    // adjust according to aesthetic preference
    function width(s) {
	return (0.1 / (s + 0.5));
    }

    style(0.01, "#008", "#0000");
    circle(0, 0, 1);

    style(0.01, "#800", "#0000");
    circle(+lim_c, +lim_c, lim_r);
    circle(-lim_c, -lim_c, lim_r);

    function inner(mirror) {
	style(0.005, "#000", "#0000");
	c.beginPath();
	c.moveTo(0, -width(0) * mirror);
	clothoid(function(s, x, y, dx, dy) {
	    let w = width(s) / length(dx, dy);
	    let xx = x + dy * w;
	    let yy = y - dx * w;
	    c.lineTo(mirror * xx, mirror * yy);
	    return (inside(xx, yy));
	});
	c.stroke();
    }

    function outer(mirror) {
	style(0.005, "#000", "#0000");
	c.beginPath();
	c.moveTo(0, +width(0) * mirror);
	clothoid(function(s, x, y, dx, dy) {
	    let w = width(s) / length(dx, dy);
	    let xx = x - dy * w;
	    let yy = y + dx * w;
	    c.lineTo(mirror * xx, mirror * yy);
	    return (inside(xx, yy));
	});
	c.stroke();
    }

    clothoid(function(s, x, y, dx, dy) {
	style(width(s) * 2, "#8888", "#0000");
	c.beginPath();
	c.moveTo(+x,    +y);
	c.lineTo(+x+dx, +y+dy);
	c.moveTo(-x,    -y);
	c.lineTo(-x-dx, -y-dy);
	c.stroke();
	return (inside(x, y));
    });

    outer(+1); inner(+1);
    outer(-1); inner(-1);
}
