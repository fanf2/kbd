// https://en.m.wikipedia.org/wiki/Moss%27s_egg
// https://web.archive.org/web/20200618202007/...
// ...https://www.dynamat.oriw.eu/upload_pdf/20121022_154322__0.pdf

const tan = Math.tan;
const tau = Math.PI * 2;
const degrees = tau/360;

function atan2(opp, adj) {
    return Math.atan2(opp, adj) / degrees;
}

const INCH = 25.4;
const KU = INCH * 3/4;

// scale positions but not line thickness or font size
let scale = 42;

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

    function paint() {
	c.stroke();
	c.fill();
	c.beginPath();
    }

    function spot(x, y, r) {
	c.roundRect(x * scale - r, y * -scale - r,
		    r * 2, r * 2, r);
	paint();
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

    /* https://enwp.org/Divided_differences */

    let x0 = control[0].x;
    let x1 = control[1].x;
    let x2 = control[2].x;
    let x3 = control[3].x;
    let x4 = control[4].x;

    let y0 = control[0].y;
    let y1 = control[1].y;
    let y2 = control[2].y;
    let y3 = control[3].y;
    let y4 = control[4].y;

    let y01 = (y1 - y0) / (x1 - x0);
    let y12 = (y2 - y1) / (x2 - x1);
    let y23 = (y3 - y2) / (x3 - x2);
    let y34 = (y4 - y3) / (x4 - x3);

    let y012 = (y12 - y01) / (x2 - x0);
    let y123 = (y23 - y12) / (x3 - x1);
    let y234 = (y34 - y23) / (x4 - x2);

    let y0123 = (y123 - y012) / (x3 - x0);
    let y1234 = (y234 - y123) / (x4 - x1);

    let y01234 = (y1234 - y0123) / (x4 - x0);

    /* https://enwp.org/Newton_polynomial */

    function newton(x) {
	let d0 = x - x0;
	let d1 = x - x1;
	let d2 = x - x2;
	let d3 = x - x3;
	let d4 = x - x4;
	return y0
	    + y01 * d0
	    + y012 * d0 * d1
	    + y0123 * d0 * d1 * d2
	    + y01234 * d0 * d1 * d2 * d3;
    }

    for (let x = x4; x >= x0; x -= 0.01) {
	line(x, newton(x) + 6);
    }
    paint();

    style(1, "#888", "#7ff3");
    for (let p of control) {
	spot(p.x, p.y + 6, 10);
    }

    let base_width = control[4].x - control[0].x;

    let height = (control[3].y + control[1].y) / 2;
    let mid_depth = height - control[2].y;

    let top_width = control[3].x - control[1].x;
    let top_depth = control[3].y - control[1].y;
    let angle = atan2(top_depth, top_width);

    style(1, "#888", "#88f");
    let info_line = 0;
    function print_info(msg1, msg2) {
	print(10, 12 - info_line, msg1);
	print(12, 12 - info_line, msg2);
	info_line += 1;
    }

    print_info("top width", `= ${top_width.toFixed(2)}`);
    print_info("depth", `= ${mid_depth.toFixed(2)}`);
    print_info("angle", `= ${angle.toFixed(2)}`);
    print_info("height", `= ${height.toFixed(2)}`);
    print_info("base width", `= ${base_width.toFixed(2)}`);

    for (let i = 0; i < control.length; i++) {
	print(-13, 12 - i, `x${i} = ${control[i].x.toFixed(2)}`)
	print(-11, 12 - i, `y${i} = ${control[i].y.toFixed(2)}`)
    }

    c.restore();
}

function main() {
    console.log(canvas.width = window.innerWidth);
    console.log(canvas.height = window.innerHeight);
    scale = canvas.width/33.33;
    draw();
}

function reposition(ev) {
    let x = (ev.pageX - canvas.width/2) / scale;
    let y = -(ev.pageY - canvas.height*2/3) / scale - 6;

    function dist(p) {
	return (x - p.x)**2 + (y - p.y)**2;
    }

    let nearest = null;
    let near = 1/0;
    for (let i = 0; i < control.length; i++) {
	let p = control[i];
	let d = dist(p);
	if (near > d && d < 1) {
	    nearest = i;
	    near = d;
	}
    }

    const d = 0.1;
    switch (nearest) {
    case(0):
	if (x > -19/2 &&
	    x+d < +control[1].x &&
	    x+d < -control[3].x)
	{
	    control[0].x = +x;
	    control[4].x = -x;
	    draw();
	}
	return;
    case(4):
	if (x < +19/2 &&
	    x-d > -control[1].x &&
	    x-d > +control[3].x)
	{
	    control[0].x = -x;
	    control[4].x = +x;
	    draw();
	}
	return;
    case(1):
    case(2):
    case(3):
	let i = nearest;
	if (control[i-1].x < x-d && d+x < control[i+1].x)
	{
	    control[i].x = x;
	    control[i].y = y;
	    draw();
	}
	return;
    }
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
