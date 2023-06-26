function roundrect(c, x, y, w, h, r) {
    c.beginPath();
    c.roundRect(x, y, w, h, r);
    c.stroke();
}

function circle(c, x, y, r) {
    roundrect(c, x - r, y - r, r * 2, r * 2, r);
}

function beam(c, x, y, width, height) {
    // convert width and height from studs to ldu
    let w = width * 20 - 2;
    let h = height * 20 - 2;
    roundrect(c, x - w / 2, y - h / 2, w, h, 9);
    for (let a = 0; a < width; a++) {
	for (let b = 0; b < height; b++) {
	    let xx = x - width * 20 / 2 + a * 20;
	    let yy = y - height * 20 / 2 + b * 20;
	    circle(c, xx + 10, yy + 10, 8);
	}
    }
}

function main() {
    let c = canvas.getContext("2d")
    c.reset();
    c.strokeStyle = "black";
    c.lineWidth = 0.5;
    c.transform(2, 0, 0, 2, canvas.width/2, canvas.height/2);

    let stud = 20;
    let beam_x = 394;
    let beam_y = 132;

    beam(c, +6 * stud, -beam_y, 9, 1);
    beam(c, -6 * stud, -beam_y, 9, 1);
    beam(c, +15 * stud - 1, -beam_y, 9, 1);
    beam(c, -15 * stud + 1, -beam_y, 9, 1);
    beam(c, +13 * stud - 1, +beam_y, 13, 1);
    beam(c, -13 * stud + 1, +beam_y, 13, 1);
    beam(c, 0, +beam_y, 13, 1);
    beam(c, +beam_x, 0, 1, 13);
    beam(c, -beam_x, 0, 1, 13);

    let pcb_width = 381;
    let pcb_depth = 119;
    c.strokeRect(-pcb_width, -pcb_depth,
		 pcb_width * 2, pcb_depth * 2);

    let plate_width = 403;
    let plate_depth = 141;
    let plate_radius = 25;
    roundrect(c, -plate_width, -plate_depth,
	      plate_width * 2, plate_depth * 2, plate_radius);

    let socket_width = 24;
    let socket_depth = 24;
    let socket_overhang = 6;
    let socket_recess = 5;
    c.strokeRect(-socket_width/2, -plate_depth + socket_recess,
		 socket_width, socket_depth);

    c.beginPath();
    c.moveTo(-36, -pcb_depth);
    c.lineTo(-18, -plate_depth + socket_overhang + socket_recess);
    c.lineTo(+18, -plate_depth + socket_overhang + socket_recess);
    c.lineTo(+36, -pcb_depth);
    c.stroke();
}
