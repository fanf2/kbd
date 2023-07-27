let key_unit = 19; // mm, metricated
let key_body = 14; // mm
let stab_width = 7; // mm
let stab_depth = 16; // mm

// key cap outside key body
let overhang = (key_unit - key_body) / 2;

// centre to centre
let stab_2u = 24; // mm
let stab_6u = 100; // mm

let lego_stud = 8; // mm
let half_stud = lego_stud / 2;
let beam_shrinkage = 0.4; // mm
let beam_radius = lego_stud / 2 - beam_shrinkage;
let axle_radius = beam_radius - 2 * beam_shrinkage;

// adjustable parameters

// around arrows
let gap = 0.25 * key_unit;

// space between edge of key body and enclosure beam
let body_clearance = 1; // mm

// space bar needs more space
// this is the same as yiancar's hs60, i think
let stab_clearance = 2; // mm

// space between beams
let beam_clearance = 0.5; // mm

// how much to indent in front of the space bar
let stab_shift = gap + body_clearance - stab_clearance;

let beam_origin = overhang - body_clearance - beam_radius;

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
    let cx = (x + u / 2) * key_unit + gx;
    let cy = (y + 1 / 2) * key_unit + gy;
    let width = (u - 1) * key_unit + key_body;
    c.strokeRect(cx - width/2, cy - key_body/2, width, key_body);
    if (u > 1) {
	c.restore();
	c.strokeRect(cx - key_body/2, cy - key_body/2, key_body, key_body);
	if (u > 6) {
	    stabilizer(c, cx, cy, stab_6u);
	} else if (u > 2) {
	    stabilizer(c, cx, cy, stab_2u);
	}
    }
}

function switch_hole(c, x, y, u) {
    gappy_hole(c, x, y, u, 0, 0);
}

function main() {
    let c = canvas.getContext("2d")
    c.reset();
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

    for (let i = 0; i < 3; i++) {
	switch_hole(c, i * 1.25, 4, 1.25);
    }

    switch_hole(c, 3.75, 4, 6.25);

    for (let i = 0; i < 3; i++) {
	switch_hole(c, 10 + i, 4, 1);
    }

    for (let i = 0; i < 3; i++) {
	gappy_hole(c, 13 + i, 4, 1, gap, gap);
    }

    gappy_hole(c, 14, 3, 1, gap, gap);
    gappy_hole(c, 16, 4, 1, 2 * gap, gap);

    for (let i = 0; i < 4; i++) {
	gappy_hole(c, 15, i, 1, 2 * gap, 0);
	gappy_hole(c, 16, i, 1, 2 * gap, 0);
    }

    c.save();
    c.setLineDash([0.2, 0.2]);

    // outline of key block
    let kw = 17 * key_unit + 2 * gap;
    let kh = 5 * key_unit + gap;
    c.strokeRect(0, 0, kw, kh);

    // outline of pcb
    c.strokeRect(overhang, overhang, kw -2 * overhang, kh - 2 * overhang);

    c.restore();

    let bw = 0;
    bw += 4 * lego_stud + shift_beam(stab_shift);
    bw += 12 * lego_stud + shift_beam(0);
    bw += 12 * lego_stud + shift_beam(stab_shift);
    bw += 10 * lego_stud;

    let bo = (kw - bw) / 2;
    let bx = bo;
    let by = 5 * key_unit + gap - beam_origin;

    beam(c, bx, by, 5, 1);
    by -= stab_shift;
    bx += 4 * lego_stud + shift_beam(stab_shift);
    beam(c, bx, by, 13, 1);
    bx += 12 * lego_stud + shift_beam(0);
    beam(c, bx, by, 13, 1);
    by += stab_shift;
    bx += 12 * lego_stud + shift_beam(stab_shift);
    beam(c, bx, by, 11, 1);
    bx += 10 * lego_stud;

    bx -= beam_origin - bo;
    by -= shift_beam(beam_origin - bo);
    beam(c, bx, by, 1, -13);

    bx = beam_origin;
    beam(c, bx, by, 1, -13);

    by -= 12 * lego_stud;
    bx += shift_beam(by - beam_origin);
    let rx = kw - bx;
    by = beam_origin;
    beam(c, bx, by, 13, 1);
    bx += 12 * lego_stud + shift_beam(0);
    beam(c, bx, by, 13, 1);
    bx += 12 * lego_stud + shift_beam(0);
    beam(c, bx, by, 9, 1);

    bx = rx;
    beam(c, bx, by, -4, 1);
}
