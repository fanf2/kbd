// https://en.m.wikipedia.org/wiki/Moss%27s_egg
// https://web.archive.org/web/20200618202007/...
// ...https://www.dynamat.oriw.eu/upload_pdf/20121022_154322__0.pdf

const abs = Math.abs
const r2 = Math.sqrt(2);
const π = Math.PI;
const cos = Math.cos;
const atan2 = Math.atan2;

// scale positions but not line thickness or font size
const scale = 200;

let NX = 1.5;
let NY = 0.75;
let SX = 0.5;
let SY = 0.5;

function draw() {
    let c = canvas.getContext("2d")
    c.save();
    c.clearRect(0,0, canvas.width, canvas.height);
    c.translate(canvas.width/2, canvas.height/2);

    c.font = 'lighter 20px sans-serif';

    function style(w, s, f) {
	c.lineWidth = w;
	c.strokeStyle = s;
	c.fillStyle = f;
    }

    function print(x, y, msg) {
	c.fillText(msg, x * scale, y * scale);
    }

    function line(x1, y1, x2, y2) {
	c.beginPath();
	c.moveTo(x1 * scale, y1 * scale);
	c.lineTo(x2 * scale, y2 * scale);
	c.stroke();
    }

    function raw_arc(r, a, b) {
	c.beginPath();
	c.arc(0,0, r * scale, a, b);
	c.fill();
	c.stroke();
    }

    function arc(x, y, r, a, b, s) {
	c.save();
	c.translate(x * scale, y * scale);

	style(1, "#0000", s);
	raw_arc(0.05, -180,+180);

	print(0.1, -0.1, `x=${x}`.slice(0,7));
	print(0.1, 0000, `y=${y}`.slice(0,7));
	print(0.1, +0.1, `r=${r}`.slice(0,7));

	style(1, s, "#0000");
	raw_arc(r, -180,+180);

	style(5, s, "#0000");
	raw_arc(r, a,b);

	c.restore();
    }

    function eggend(x, y, r, g, b) {
	line(-11*x,-10*y, +10*x,+11*y);
	line(+11*x,-10*y, -10*x,+11*y);
	let ee = x < 0 ? π : 0;
	let ww = x < 0 ? 0 : π;
	let ne = atan2(y,+x);
	let nw = atan2(y,-x);
	let s = abs(x) + 1
	let n = s - x/cos(ne);
	arc(-x,0, s, ee, ne, r);
	arc(0,+y, n, ne, nw, g);
	arc(+x,0, s, nw, ww, b);
    }

    // axes
    line(-10,0,+10,0);
    line(0,-10,0,+10);

    eggend(+SX, +SY, "#c00", "#0c0", "#00c");
    eggend(-NX, -NY, "#0cc", "#c0c", "#cc0");

    c.restore();
}

function main() {
    draw();
}

function movement(ev) {
    if (ev.buttons == 0)
	return;

    let x = (ev.x - canvas.width/2) / scale;
    let y = (ev.y - canvas.height/2) / scale;

    let doit = function(){};

    if (y < 0) {
	if (abs(x) < abs(y)) {
	    NY = abs(y);
	    doit = draw;
	}
	if (abs(x) > abs(y)) {
	    NX = abs(x);
	    doit = draw;
	}
    }
    if (y > 0) {
	if (abs(x) < abs(y)) {
	    SY = abs(y);
	    doit = draw;
	}
	if (abs(x) > abs(y)) {
	    SX = abs(x);
	    doit = draw;
	}
    }

    doit();
}
