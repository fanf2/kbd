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

    c.strokeStyle = "#008";
    c.fillStyle = "#ffff";
    c.lineWidth = 0.01;
    circle(0, 0, 1);

    // https://enwp.org/Euler_spiral
    // x = ∫ cos(s²) ds
    // y = ∫ sin(s²) ds

    // eyeballed limit of curve as s → ∞
    const r = 1 - exp(-1);

    c.strokeStyle = "#800";
    c.fillStyle = "#800";
    circle(+r, +r, 0.25);
    circle(-r, -r, 0.25);

    let x = 0;
    let y = 0;
    let ds = 0.01;
    let lim = exp(1);

    for (let s = 0; s < lim; s += ds) {
	let dx = cos(s*s) * ds;
	let dy = sin(s*s) * ds;

	c.lineWidth = exp(-1) / (s + 1) - exp(-3);

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
    }
}
