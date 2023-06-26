function circle(c, x, y, r) {
    c.roundRect(x - r, y - r, r * 2, r * 2, r);
}

function beam(c, x, y, width, height) {
    // convert width and height from studs to ldu
    let w = width * 20 - 2;
    let h = height * 20 - 2;
    c.save();
    c.beginPath();
    c.roundRect(x - w / 2, y - h / 2, w, h, 9);
    for (let a = 0; a < width; a++) {
	for (let b = 0; b < height; b++) {
	    let xx = x - width * 20 / 2 + a * 20;
	    let yy = y - height * 20 / 2 + b * 20;
	    circle(c, xx + 10, yy + 10, 8);
	}
    }
    c.stroke();
    c.restore();
}

function main() {
    let c = canvas.getContext("2d")
    c.reset();
    c.strokeStyle="black";
    c.transform(2, 0, 0, 2, canvas.width/2, canvas.height/2);
    beam(c, +120, -132, 9, 1);
    beam(c, -120, -132, 9, 1);
    beam(c, +299, -132, 9, 1);
    beam(c, -299, -132, 9, 1);
    beam(c, +394, 0, 1, 13);
    beam(c, -394, 0, 1, 13);
    beam(c, +259, +132, 13, 1);
    beam(c, -259, +132, 13, 1);
    beam(c, 0, +132, 13, 1);
    // pcb
    let pcb_width = 381;
    let pcb_depth = 119;
    c.strokeRect(-pcb_width, -pcb_depth, pcb_width * 2, pcb_depth * 2);
    let plate_width = 403;
    let plate_depth = 141;
    let socket_width = 24;
    let socket_depth = 24;
    let socket_overhang = 6;
    let socket_recess = 5;
    c.strokeRect(-socket_width/2, -plate_depth + socket_recess,
		 socket_width, socket_depth);
    c.save();
    c.beginPath();
    c.moveTo(-36, -pcb_depth);
    c.lineTo(-18, -plate_depth + socket_overhang + socket_recess);
    c.lineTo(+18, -plate_depth + socket_overhang + socket_recess);
    c.lineTo(+36, -pcb_depth);
    c.stroke();
    c.restore();
}
