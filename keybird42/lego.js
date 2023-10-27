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

// space between beams
let beam_clearance = 0.2; // mm

// instead of one lego_stud between hole centres at the end of each beam
let beam_spacing = beam_radius * 2 + beam_clearance; // mm

// line between hole centres is 45 degrees
let beam_corner = Math.sqrt(beam_spacing * beam_spacing / 2);

function roundrect(c, x, y, w, h, r) {
    c.beginPath();
    c.roundRect(x, y, w, h, r);
    c.stroke();
}

function circle(c, x, y, r) {
    roundrect(c, x - r, y - r, r * 2, r * 2, r);
}

// x and y are centre of hole at one end
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

    let keeb_h = main_height * key_unit;
    let keeb_w = total_width * key_unit;

    let beam_len = 12 * lego_stud;
    let beam_h = beam_len;
    let beam_w = 4 * beam_len + 3 * beam_spacing;

    let box_h = beam_h + 2 * beam_corner;
    let box_w = beam_w + 2 * beam_corner;

    let clear_h = (box_h - 2 * beam_radius - keeb_h) / 2;
    let clear_w = (box_w - 2 * beam_radius - keeb_w) / 2;

    console.log(`keeb_w ${keeb_w}`);
    console.log(`keeb_h ${keeb_h}`);
    console.log(`beam_w ${beam_w}`);
    console.log(`beam_h ${beam_h}`);
    console.log(`box_w ${box_w}`);
    console.log(`box_h ${box_h}`);
    console.log(`clear_w ${clear_w}`);
    console.log(`clear_h ${clear_h}`);

    let beam_y = (keeb_h - beam_h) / 2;
    let beam_x = (keeb_w - beam_w) / 2;
    let upper_beam = (keeb_h - box_h) / 2;
    let lower_beam = upper_beam + box_h;
    let left_beam = (keeb_w - box_w) / 2;
    let right_beam = left_beam + box_w;

    beam(c, left_beam, beam_y, 1, 13);
    beam(c, right_beam, beam_y, 1, 13);

    for (let i = 0; i < 4; i++) {
	beam(c, beam_x, upper_beam, 13, 1);
	beam(c, beam_x, lower_beam, 13, 1);
	beam_x += beam_len + beam_spacing;
    }
}
