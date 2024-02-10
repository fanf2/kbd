// https://en.m.wikipedia.org/wiki/Moss%27s_egg
// https://web.archive.org/web/20200618202007/...
// ...https://www.dynamat.oriw.eu/upload_pdf/20121022_154322__0.pdf

const tan = Math.tan;
const tau = Math.PI * 2;
const deg = tau/360;

const INCH = 25.4;
const KU = INCH * 3/4;

let control = [
    {x: -9, y: 0},
    {x: -7, y: 8},
    {x: 00, y: 7},
    {x: +7, y: 8},
    {x: +9, y: 0}
];

function draw() {
    let c = canvas.getContext("2d")
    c.save();
    c.clearRect(0,0, canvas.width, canvas.height);
    c.translate(canvas.width/2, canvas.height*2/3);
    // scale positions but not line thickness or font size
    const scale = canvas.width/33.33;

    c.font = 'lighter 20px sans-serif';

    function style(w, s, f) {
	c.lineWidth = w;
	c.strokeStyle = s;
	c.fillStyle = f;
    }

    function print(x, y, msg) {
	c.fillText(msg, x * scale, y * -scale);
    }

    function move(x, y) {
	c.moveTo(x * scale, y * -scale);
    }

    function line(x, y) {
	c.lineTo(x * scale, y * -scale);
    }

    function curve(c1x, c1y, c2x, c2y, x3, y3) {
	c.bezierCurveTo(c1x * scale, c1y * -scale,
			c2x * scale, c2y * -scale,
			x3 * scale, y3 * -scale);
    }

    function draw(x1, y1, x2, y2) {
	c.beginPath();
	c.moveTo(x1 * scale, y1 * -scale);
	c.lineTo(x2 * scale, y2 * -scale);
	c.stroke();
    }

    function paint() {
	c.stroke();
	c.fill();
	c.beginPath();
    }

    function spot(x, y, r) {
	c.beginPath();
	c.roundRect(x * scale - r, y * -scale - r,
		    r * 2, r * 2, r);
	c.fill();
	c.stroke();
    }

    // plate
    style(1, "#888", "#0707");
    move(-19.05/2, -1.5);
    line(+19.05/2, -1.5);
    line(+19.05/2, 0);
    line(-19.05/2, 0);
    line(-19.05/2, -1.5);
    paint();

    // switch body
    style(1, "#888", "#3337");
    move(-14.00/2, -1.5);
    line(-14.00/2, 0);
    line(-15.60/2, 0);
    line(-15.60/2, 1);
    line(-7.5/2, 6);
    line(+7.5/2, 6);
    curve(6, 6, 6, 6,
	 +15.00/2, 1);
    line(+15.60/2, 1);
    line(+15.60/2, 0);
    line(+14.00/2, 0);
    line(+14.00/2, -1.5);
    paint();

    // top of stem
    style(1, "#888", "#f007");
    move(-6.0/2, 6.0);
    line(-5.5/2, 6.3);
    line(+5.5/2, 6.3);
    line(+6.0/2, 6.0);
    // + mount y axis
    move(-4.0/2, 6.3);
    line(-4.0/2, 6.3+3.6);
    line(+4.0/2, 6.3+3.6);
    line(+4.0/2, 6.3);
    // + mount x axis
    move(-1.1/2, 6.3);
    line(-1.1/2, 6.3+3.6);
    line(+1.1/2, 6.3+3.6);
    line(+1.1/2, 6.3);
    paint();

    // inside keycap
    style(1, "#888", "#ff73");

    move(-19.0/2, 6);
    line(-15.5/2, 6);
    line(-14.5/2, 9);
    line(-13.0/2, 10.3);

    line(-5.5/2, 10.3);
    line(-5.5/2, 6.3);
    line(-4.2/2, 6.3);
    line(-4.2/2, 10.3);
    line(+4.2/2, 10.3);
    line(+4.2/2, 6.3);
    line(+5.5/2, 6.3);
    line(+5.5/2, 10.3);

    line(+13.0/2, 10.3);
    line(+14.5/2, 9);
    line(+15.5/2, 6);
    line(+19.0/2, 6);
    paint();

    style(1, "#888", "#7ff3");
    for (let p of control) {
	spot(p.x, p.y + 6, 10);
    }

    c.restore();
}

function main() {
    console.log(canvas.width = window.innerWidth);
    console.log(canvas.height = window.innerHeight);
    draw();
}

function reposition(ev) {
    let x = (ev.pageX - scale) / scale;
    let y = (ev.pageY - scale) / scale;
}

function moused(ev) {
    if (ev.buttons != 0) {
	reposition(ev);
    }
}

function touched(ev) {
    if (ev.touches.length > 0) {
	reposition(ev.touches.item(0));
    }
}
