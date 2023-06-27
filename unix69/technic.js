let lego_unit = 0.4; // mm
let key_unit = 19.05; // mm
let key_ldu = key_unit / lego_unit;

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

function stab_hole(c, x, y) {
    let stab_width = 18;
    let stab_depth = 40;
    c.strokeRect(x - stab_width / 2, y - stab_depth / 2,
		 stab_width, stab_depth);
}

function switch_hole(c, x, y, u) {
    let hole = 35; // ldu
    if (u > 1) {
	c.save();
	c.setLineDash([1,2]);
    }
    let width = (u - 1) * key_ldu + hole;
    let cx = (x - 8 + u/2) * key_ldu;
    let cy = (y - 2) * key_ldu;
    c.strokeRect(cx - width / 2, cy - hole / 2,
		 width, hole);
    if (u > 1) {
	c.restore();
	switch_hole(c, x + u/2 - 1/2, y, 1)
	if (u > 6) {
	    stab_hole(c, cx - 125, cy);
	    stab_hole(c, cx + 125, cy);
	} else if (u > 2) {
	    stab_hole(c, cx - 30, cy);
	    stab_hole(c, cx + 30, cy);
	}
    }
}

function main() {
    let c = canvas.getContext("2d")
    c.reset();
    c.strokeStyle = "black";
    c.lineWidth = 0.5;
    c.transform(2, 0, 0, 2, canvas.width/2, canvas.height/2);

    let stud = 20; // ldu
    let beam_x = 394;
    let beam_y = 132;

    beam(c, +4 * stud, -beam_y, 5, 1);
    beam(c, -4 * stud, -beam_y, 5, 1);
    beam(c, +13 * stud - 1, -beam_y, 13, 1);
    beam(c, -13 * stud + 1, -beam_y, 13, 1);
    // beam(c, -11 * stud + 1, -beam_y, 9, 1);
    // beam(c, -19 * stud + 1, -beam_y, 1, 1);
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

    for (let i = 0; i < 15; i++) {
	switch_hole(c, i, 0, 1);
    }
    switch_hole(c, 15, 0, 1);

    for (let i = 0; i < 12; i++) {
	switch_hole(c, i + 1.5, 1, 1);
    }
    switch_hole(c, 15, 1, 1);

    for (let i = 0; i < 11; i++) {
	switch_hole(c, i + 1.75, 2, 1);
    }
    switch_hole(c, 15, 2, 1);

    for (let i = 0; i < 10; i++) {
	switch_hole(c, i + 2.25, 3, 1);
    }
    switch_hole(c, 14, 3, 1);
    switch_hole(c, 15, 3, 1);

    for (let i = 0; i < 6; i++) {
	switch_hole(c, i + 10, 4, 1);
    }

    switch_hole(c, 0, 1, 1.5);
    switch_hole(c, 0, 2, 1.75);
    switch_hole(c, 0, 3, 2.25);

    switch_hole(c, 13.5, 1, 1.5);
    switch_hole(c, 12.75, 2, 2.25);
    switch_hole(c, 12.25, 3, 1.75);

    for (let i = 0; i < 3; i++) {
	switch_hole(c, i * 1.25, 4, 1.25);
    }

    switch_hole(c, 3.75, 4, 6.25);

    let bolt_radius = 4;
    let nut_radius = 6;

    circle(c, +beam_x, +6 * stud, bolt_radius);
    circle(c, +beam_x, -6 * stud, bolt_radius);
    circle(c, -beam_x, +6 * stud, bolt_radius);
    circle(c, -beam_x, -6 * stud, bolt_radius);

    circle(c, +beam_x, +6 * stud, nut_radius);
    circle(c, +beam_x, -6 * stud, nut_radius);
    circle(c, -beam_x, +6 * stud, nut_radius);
    circle(c, -beam_x, -6 * stud, nut_radius);

    circle(c, +7 * stud - 1, +beam_y, bolt_radius);
    circle(c, -7 * stud + 1, +beam_y, bolt_radius);
    circle(c, +7 * stud - 1, -beam_y, bolt_radius);
    circle(c, -7 * stud + 1, -beam_y, bolt_radius);

    circle(c, +7 * stud - 1, +beam_y, nut_radius);
    circle(c, -7 * stud + 1, +beam_y, nut_radius);
    circle(c, +7 * stud - 1, -beam_y, nut_radius);
    circle(c, -7 * stud + 1, -beam_y, nut_radius);

    // circle(c, +15 * stud - 1, -beam_y, nut_radius);
    // circle(c, -15 * stud + 1, -beam_y, nut_radius);

    circle(c, +19 * stud - 1, +beam_y, nut_radius);
    circle(c, -19 * stud + 1, +beam_y, nut_radius);
    circle(c, +19 * stud - 1, -beam_y, nut_radius);
    circle(c, -19 * stud + 1, -beam_y, nut_radius);

    circle(c, +6 * stud, +beam_y, nut_radius);
    circle(c, -6 * stud, +beam_y, nut_radius);
    circle(c, +6 * stud, -beam_y, nut_radius);
    circle(c, -6 * stud, -beam_y, nut_radius);

    circle(c, +2 * stud, -beam_y, nut_radius);
    circle(c, -2 * stud, -beam_y, nut_radius);

    // rp2040-tiny
    let usb_square = 45;
    let socket_square = 24;
    c.strokeRect(-socket_square/2, -plate_depth,
		 socket_square, socket_square);

    roundrect(c, -usb_square/2, -plate_depth, usb_square, usb_square, 2);

    circle(c, -usb_square/2 + 5, -plate_depth + 5, 2.5);
    circle(c, +usb_square/2 - 5, -plate_depth + 5, 2.5);
    circle(c, -usb_square/2 + 5, -plate_depth + usb_square - 5, 2.5);
    circle(c, +usb_square/2 - 5, -plate_depth + usb_square - 5, 2.5);

    return;

    let plug_width = 36; // with extra clearance
    let socket_width = 24;
    let socket_depth = 30;
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

    let left_socket = -7 * key_unit/lego_unit;
    c.strokeRect(left_socket - socket_width/2, -pcb_depth - socket_overhang,
		 socket_width, socket_depth);

    c.setLineDash([1,2]);

    c.strokeRect(left_socket - plug_width / 2, -plate_depth,
		 plug_width, plate_depth - pcb_depth + socket_depth);

}
