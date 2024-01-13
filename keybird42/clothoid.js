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

    function twinline(x1, y1, x2, y2) {
	c.beginPath();
	c.moveTo(+x1, +y1);
	c.lineTo(+x2, +y2);
	c.moveTo(-x1, -y1);
	c.lineTo(-x2, -y2);
	c.stroke();
    }

    function length(x, y) {
	return (sqrt(x*x + y*y));
    }

    // https://enwp.org/Euler_spiral
    // x = ∫ cos(s²) ds
    // y = ∫ sin(s²) ds

    // integration step size
    const ds = 0.01;
    // eyeballed limit of curve as s → ∞
    const lim_c = 1 - exp(-1);
    // size of infill around limit
    const lim_r = 1/4;

    function outside(x, y) {
	return (length(lim_c - x, lim_c - y) > lim_r);
    }

    function width(s) {
	return (0.1 / (s + 0.5));
    }

    style(0.01, "#008", "#0000");
    circle(0, 0, 1);

    style(0.01, "#800", "#0000");
    circle(+lim_c, +lim_c, lim_r);
    circle(-lim_c, -lim_c, lim_r);

    let x = 0;
    let y = 0;
    let s = 0;
    let xi = 0;
    let yi = -width(0);
    let xo = 0;
    let yo = +width(0);

    while (outside(x, y)) {
	let dx = cos(s*s) * ds;
	let dy = sin(s*s) * ds;
	let dlen = length(dx, dy);

	let w = width(s);
	let nxi = x + w * dy / dlen;
	let nyi = y - w * dx / dlen;
	let nxo = x - w * dy / dlen;
	let nyo = y + w * dx / dlen;

	style(w * 2, "#8888", "#0000");
	twinline(x, y, x+dx, y+dy);

	style(0.005, "#000", "#0000");
	twinline(xi, yi, nxi, nyi);
	twinline(xo, yo, nxo, nyo);

	s += ds;
	x += dx;
	y += dy;
	xi = nxi;
	yi = nyi;
	xo = nxo;
	yo = nyo;
    }
}
