"use strict";

const tau = Math.PI * 2;
const exp = Math.exp;
const sin = Math.sin;
const cos = Math.cos;
const atan2 = Math.atan2;
const sqrt = Math.sqrt;

function main() {
    let c = canvas.getContext("2d");
    c.translate(canvas.width/2, canvas.height/2);
    let scale = 1000;
    c.scale(scale, scale);
    //c.rotate(tau*2/3);

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

    style(0.005, "#800", "#0000");
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

    let points = [];
    let inner_end = 0;
    let outer_end = 0;
    clothoid(function(i, x, y, dx, dy) {
	let w = width(i) / length(dx, dy);
	let xi = x - dy * w;
	let yi = y + dx * w;
	let xo = x + dy * w;
	let yo = y - dx * w;
	points[i] = { xi, yi, xo, yo };
	let ilim = limit(xi, yi);
	let olim = limit(xo, yo);
	inner_end = ilim ? inner_end : i;
	outer_end = olim ? outer_end : i;
	return (ilim && olim);
    });

    let ei = points[inner_end];
    let eo = points[outer_end];
    let ao1 = atan2(-lim_c + eo.yo, -lim_c + eo.xo);
    let ai1 = atan2(-lim_c + ei.yi, -lim_c + ei.xi);
    let ao2 = atan2(+lim_c - eo.yo, +lim_c - eo.xo);
    let ai2 = atan2(+lim_c - ei.yi, +lim_c - ei.xi);

    style(0.01, "#0808", "#0000");
    c.beginPath();
    c.moveTo(+points[0].xo, +points[0].yo);
    for (let i = 1; i <= outer_end; i++) {
	c.lineTo(+points[i].xo, +points[i].yo);
    }
    c.arc(+lim_c, +lim_c, lim_r, ao1, ai1);
    for (let i = inner_end; i >= 0; i--) {
	c.lineTo(+points[i].xi, +points[i].yi);
    }
    for (let i = 0; i <= outer_end; i++) {
	c.lineTo(-points[i].xo, -points[i].yo);
    }
    c.arc(-lim_c, -lim_c, lim_r, ao2, ai2);
    for (let i = inner_end; i > 0; i--) {
	c.lineTo(-points[i].xi, -points[i].yi);
    }
    c.closePath();
    c.stroke();
}
