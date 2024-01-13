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

    c.strokeStyle = "#008";
    c.lineWidth = 0.01;

    function circle(x, y, r) {
	c.beginPath();
	c.roundRect(x - r, y - r, 2*r, 2*r, r);
	c.stroke();
    }
    circle(0, 0, 1);

    c.strokeStyle = "#800";
    c.fillStyle = "#800";

    const r = 1 - exp(-1);
    console.log(r);

    circle(+r, +r, 0.25);
    circle(-r, -r, 0.25);

    // https://enwp.org/Euler_spiral
    // x = integral cos(s*s) ds
    // y = integral sin(s*s) ds

    let x = 0;
    let y = 0;
    let ds = 0.01;
    let lim = exp(1);

    for (let s = 0; s < lim; s += ds) {
	let dx = cos(s*s) * ds;
	let dy = sin(s*s) * ds;

	let f = exp(-1)
	c.lineWidth = f / (s + 1) - exp(-3)

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

    for (let s = lim; s < 100; s += ds) {
	let dx = cos(s*s) * ds;
	let dy = sin(s*s) * ds;
	x += dx;
	y += dy;
    }

    console.log(x, y);
}
