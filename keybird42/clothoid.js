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

    function circle(x, y, r) {
	c.beginPath();
	c.roundRect(x - r, y - r, 2*r, 2*r, r);
	c.fill();
	c.stroke();
    }

    function style(w, s, f) {
	c.lineWidth = w;
	c.strokeStyle = s;
	c.fillStyle = f;
    }

    style(0.01, "#008", "#0000");
    circle(0, 0, 1);

    // https://enwp.org/Euler_spiral
    // x = ∫ cos(s²) ds
    // y = ∫ sin(s²) ds

    // eyeballed limit of curve as s → ∞
    const lim_c = 1 - exp(-1);
    // eyeballed infill around limit
    const lim_r = 1/4;

    function limit(x, y) {
	let rx = lim_c - x;
	let ry = lim_c - y;
	return (rx*rx + ry*ry < lim_r * lim_r);
    }

    style(0.01, "#800", "#0000");
    circle(+lim_c, +lim_c, lim_r);
    circle(-lim_c, -lim_c, lim_r);

    let x = 0;
    let y = 0;
    let s = 0;
    const ds = 0.01;

    while (!limit(x, y)) {
	let dx = cos(s*s) * ds;
	let dy = sin(s*s) * ds;

	style(exp(-1) / (s + 1) - 0.05,
	      "#8888", "#0000");

	c.beginPath();
	c.moveTo(+x, +y);
	c.lineTo(+x + dx, +y + dy);
	c.stroke();

	c.beginPath();
	c.moveTo(-x, -y);
	c.lineTo(-x - dx, -y - dy);
	c.stroke();

	x += dx;
	y += dy;
	s += ds;
    }
}
