"use strict";

const tau = Math.PI * 2;
const sin = Math.sin;
const cos = Math.cos;
const exp = Math.exp;
const sqrt = Math.sqrt;

function main() {
    let c = canvas.getContext("2d");
    c.translate(canvas.width/2, canvas.height/2);
    let scale = 1000;
    c.scale(scale, scale);
    c.rotate(tau*2/3);

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
	let ds = 4/scale; // integration step size
	let x = 0;
	let y = 0;
	for (let i = 0; i < 8/ds; i++) {
	    let s = i * ds;
	    let dx = cos(s*s) * ds;
	    let dy = sin(s*s) * ds;
	    if (fun(i, x, y, dx, dy)) {
		return;
	    }
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

    function limit(x, y) {
	return (length(x - lim_c, y - lim_c) < lim_r);
    }

    // adjust according to aesthetic preference
    function width(i) {
	return (25 / (i + 125));
    }

    style(0.01, "#008", "#0000");
    circle(0, 0, 1);

    style(0.01, "#800", "#0000");
    circle(+lim_c, +lim_c, lim_r);
    circle(-lim_c, -lim_c, lim_r);
    circle(+lim_c, +lim_c, 0.01);
    circle(-lim_c, -lim_c, 0.01);

    clothoid(function(i, x, y, dx, dy) {
	style(width(i) * 2, "#8888", "#0000");
	c.beginPath();
	c.moveTo(+x,    +y);
	c.lineTo(+x+dx, +y+dy);
	c.moveTo(-x,    -y);
	c.lineTo(-x-dx, -y-dy);
	c.stroke();
    });

    function outline(inner, mirror) {
	style(0.005, "#000", "#0000");
	c.beginPath();
	c.moveTo(0, width(0) * inner * mirror);
	clothoid(function(i, x, y, dx, dy) {
	    let w = inner * width(i) / length(dx, dy);
	    let xx = x - dy * w;
	    let yy = y + dx * w;
	    c.lineTo(mirror * xx, mirror * yy);
	    return (limit(xx, yy));
	});
	c.stroke();
    }

    for (let inner of [-1, +1]) {
	for (let mirror of [-1, +1]) {
	    outline(inner, mirror);
	}
    }

    // find out where inner curve meets the limit
    let xe = 0;
    let ye = 0;
    clothoid(function(i, x, y, dx, dy) {
	let w = width(i) / length(dx, dy);
	xe = x + dy * w;
	ye = y - dx * w;
	return (limit(xe, ye));
    });
    console.log(xe, ye);
}
