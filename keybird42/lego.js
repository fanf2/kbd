let key_unit = 19.05; // mm
let key_body = 14; // mm
let stab_width = 7; // mm
let stab_depth = 16; // mm

let lego_stud = 8; // mm
let beam_shrinkage = 0.4; // mm
let beam_radius = lego_stud / 2 - beam_shrinkage;
let axle_radius = beam_radius - 2 * beam_shrinkage;

// slight over-estimate
let usb_width = 12; // mm
let usb_depth = 8; // mm
let usb_gap = 3; // mm
let usb_recess = 2; // mm
let button_width = 5; // mm
let button_depth = 4; // mm

// package is 7mm, allow some space for pins
let rp2040_size = 8; // mm

// adjustable parameters

// around blocks, in key_units
let gap = 0.25;

// positions of blocks, all in key_units
let main_width = 15;
let main_height = 5;
let side_width = 3;
let side_height = 2;
let total_width = main_width + side_width * 2 + gap * 2;

let left_x = 0;
let main_x = side_width + gap;
let right_x = main_x + main_width + gap;
let upper_y = gap;
let lower_y = upper_y + side_height + gap;

// space between pcb and beams
let board_clearance = 0.5; // mm

// space between beams
let beam_clearance = 0.2; // mm

function shift_beam(a) {
    // a*a + b*b = hypot*hypot
    let hypot = beam_radius * 2 + beam_clearance;
    return (Math.sqrt(hypot * hypot - a * a));
}

function roundrect(c, x, y, w, h, r) {
    c.beginPath();
    c.roundRect(x, y, w, h, r);
    c.stroke();
}

function circle(c, x, y, r) {
    roundrect(c, x - r, y - r, r * 2, r * 2, r);
}

function beam(c, x, y, width, height) {
    // convert width and height from studs to mm
    let i = width < 0 ? -1 : +1;
    let j = height < 0 ? -1 : +1;
    let w = width * lego_stud - 2 * i * beam_shrinkage;
    let h = height * lego_stud - 2 * j * beam_shrinkage;
    roundrect(c, x - i * beam_radius, y - j * beam_radius, w, h, beam_radius);
    for (let a = 0; a != width; a += i) {
	for (let b = 0; b != height; b += j) {
	    let xx = x + a * lego_stud;
	    let yy = y + b * lego_stud;
	    circle(c, xx, yy, axle_radius);
	}
    }
}

function stab_half(c, x, y) {
    c.strokeRect(x - stab_width / 2, y - stab_depth / 2,
		 stab_width, stab_depth);
    // from cherry data sheet
    circle(c, x, y + 7, 1.5);
    circle(c, x, y + 7, 2.5);
    circle(c, x, y - 8.25, 2);
}

function stabilizer(c, x, y, w) {
    stab_half(c, x - w / 2, y);
    stab_half(c, x + w / 2, y);
}

function gappy_hole(c, x, y, u, gx, gy) {
    if (u > 1) {
	c.save();
	c.setLineDash([1,1]);
    }
    let cx = (x + u / 2 + gx) * key_unit;
    let cy = (y + 1 / 2 + gy) * key_unit;
    let width = (u - 1) * key_unit + key_body;
    c.strokeRect(cx - width/2, cy - key_body/2, width, key_body);
    if (u > 1) {
	c.restore();
	c.strokeRect(cx - key_body/2, cy - key_body/2, key_body, key_body);
	if (u > 2) {
	    stabilizer(c, cx, cy, key_unit * (u - 1));
	}
    }
}

function switch_hole(c, x, y, u) {
    gappy_hole(c, x, y, u, main_x, 0);
}

function rect_key_units(c, x, y, w, h) {
    c.strokeRect(x * key_unit, y * key_unit, w * key_unit, h * key_unit);
}

function main() {
    let c = canvas.getContext("2d")
    c.strokeStyle = "black";
    c.lineWidth = 0.2;
    c.transform(8, 0, 0, 8, 80, 80);

    for (let i = 0; i < 15; i++) {
	switch_hole(c, i, 0, 1);
    }

    for (let i = 0; i < 12; i++) {
	switch_hole(c, i + 1.5, 1, 1);
    }

    for (let i = 0; i < 11; i++) {
	switch_hole(c, i + 1.75, 2, 1);
    }

    for (let i = 0; i < 10; i++) {
	switch_hole(c, i + 2.25, 3, 1);
    }

    switch_hole(c, 0, 1, 1.5);
    switch_hole(c, 0, 2, 1.75);
    switch_hole(c, 0, 3, 2.25);

    switch_hole(c, 13.5, 1, 1.5);
    switch_hole(c, 12.75, 2, 2.25);
    switch_hole(c, 12.25, 3, 1.75);
    switch_hole(c, 14, 3, 1);

    switch_hole(c, 0, 4, 1.25);
    switch_hole(c, 1.25, 4, 1.25);
    switch_hole(c, 2.5, 4, 1.5);

    switch_hole(c, 4, 4, 7);

    switch_hole(c, 11, 4, 1.5);
    switch_hole(c, 12.5, 4, 1.25);
    switch_hole(c, 13.75, 4, 1.25);

    for (let i = 0; i < side_width; i++) {
	for (let j = 0; j < side_height; j++) {
	    gappy_hole(c, i, j, 1, left_x, upper_y);
	    gappy_hole(c, i, j, 1, left_x, lower_y);
	    gappy_hole(c, i, j, 1, right_x, upper_y);
	    gappy_hole(c, i, j, 1, right_x, lower_y);
	}
    }

    c.save();
    c.setLineDash([0.2, 0.2]);

    // outline of pcb
    rect_key_units(c, 0, 0, total_width, main_height);

    // key blocks
    rect_key_units(c, left_x, upper_y, side_width, side_height);
    rect_key_units(c, left_x, lower_y, side_width, side_height);
    rect_key_units(c, right_x, upper_y, side_width, side_height);
    rect_key_units(c, right_x, lower_y, side_width, side_height);
    rect_key_units(c, main_x, 0, main_width, main_height);

    c.restore();

    let kw = total_width * key_unit;
    let kh = main_height * key_unit;

    let bh = 12 * lego_stud;
    let bw = 0;
    bw += 12 * lego_stud + shift_beam(0);
    bw += 12 * lego_stud + shift_beam(0);
    bw += 12 * lego_stud + shift_beam(0);
    bw += 12 * lego_stud;

    let ox = (bw - kw) / 2;
    let oy = (bh - kh) / 2;
    let cy = board_clearance + beam_radius;

    let bx = -ox;
    let by = kh + cy;

    beam(c, bx, by, 13, 1);
    bx += 12 * lego_stud + shift_beam(0);
    beam(c, bx, by, 13, 1);
    bx += 12 * lego_stud + shift_beam(0);
    beam(c, bx, by, 13, 1);
    bx += 12 * lego_stud + shift_beam(0);
    beam(c, bx, by, 13, 1);
    bx += 12 * lego_stud;

    bx += shift_beam(by - kh + oy);
    by = kh - oy;
    beam(c, bx, by, 1, -13);
    by -= 12 * lego_stud;
    bx -= shift_beam(by + cy);
    by = -cy

    beam(c, bx, by, -13, 1);
    bx -= 12 * lego_stud + shift_beam(0);
    beam(c, bx, by, -13, 1);
    bx -= 12 * lego_stud + shift_beam(0);
    beam(c, bx, by, -13, 1);
    bx -= 12 * lego_stud + shift_beam(0);
    beam(c, bx, by, -13, 1);
    bx -= 12 * lego_stud;

    bx -= shift_beam(by + oy);
    by = -oy;
    beam(c, bx, by, 1, 13);
}
