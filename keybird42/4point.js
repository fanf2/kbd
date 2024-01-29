// https://en.m.wikipedia.org/wiki/Moss%27s_egg
// https://web.archive.org/web/20200618202007/...
// ...https://www.dynamat.oriw.eu/upload_pdf/20121022_154322__0.pdf

function main() {
    const r2 = Math.sqrt(2);
    const degrees = Math.PI / 180;

    let c = canvas.getContext("2d")
    c.translate(canvas.width/2, canvas.height/2);

    // scale positions but not line thickness or font size
    const scale = 100;

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

    function raw_arc(x, y, r, a, b) {
	c.beginPath();
	c.arc(x * scale, y * scale, r * scale, a * degrees, b * degrees);
	c.fill();
	c.stroke();
    }

    function arc(x, y, r, a, b, s) {
	c.save();
	c.translate(x * scale, y * scale);
	c.rotate(a * degrees);

	style(1, "#0000", s);
	raw_arc(0, 0, 0.05, -180,+180);
	print(r + 0.1, 0, `r=${r}`.slice(0,7));

	style(1, s, "#0000");
	raw_arc(0,0, r, -180,+180);

	style(5, s, "#0000");
	raw_arc(0,0, r, 0,b-a);

	c.restore();
    }

    // axes
    line(-100,0,+100,0);
    line(0,-100,0,+100);

    arc(0,0, 1, 0,0, "#000");
    arc(0,0, 1+r2, -80,-80, "#000");

    arc(0,1, 2, 45,135, "#f00");

    arc(+1,0, 2+r2, 135,180, "#0c0");
    arc(-1,0, 2+r2, 0,45, "#080");

    arc(-1-r2,0, 2+2*r2, -45,0, "#008");
    arc(+1+r2,0, 2+2*r2, -180,-135, "#00c");

    arc(0,-1-r2, r2, -135,-45, "#880");
}
