let tau = Math.PI * 2;

let key_unit = 19.05; // mm
let key_body = 14; // mm
let stab_width = 7; // mm
// (0.484+0.004 - 0.26+0.004) * 25.4 == 5.9 mm
let stab_depth = 6; // mm
// (0.53+0.006) * 25.4 == 13.6 mm (take off stab_depth)
let stab_height = 8; // mm

let lego_stud = 8; // mm
let beam_shrinkage = 0.4; // mm
let beam_radius = lego_stud / 2 - beam_shrinkage;
let axle_radius = beam_radius - 2 * beam_shrinkage;

// Waveshare RP2040-Tiny daughterboard
let tdb_width = 18; // mm
let tdb_depth = 18; // mm
let tdb_radius = 1; // mm

// space between edge of board and edge of case
// USB space between socket and plug is nominally 1.3mm
let tdb_hang = 1.0;

// slight over-estimate
let usb_width = 9; // mm
let usb_depth = 7.3; // mm

//////// adjustable parameters

// around blocks, in key_units
let gap = 0.25;

// a little extra to make the pcb 420mm wide
let pcb_wing = 9/32; // key_unit

// positions of blocks, all in key_units
let main_width = 15;
let main_height = 5;
let side_width = 3;
let side_height = 2;
let outside_width = side_width + gap;
let keys_wide = main_width + outside_width * 2;

let left_x = 0;
let main_x = side_width + gap;
let right_x = main_x + main_width + gap;
let upper_y = gap;
let lower_y = upper_y + side_height + gap;
let below_y = upper_y + side_height + gap + side_height;

//////// lego enclosure

// space between beams
let beam_clearance = 0.2; // mm

// instead of one lego_stud between hole centres at the end of each beam
let beam_spacing = beam_radius * 2 + beam_clearance; // mm

// space between horizontal beams and pcb
let board_clearance = 0.8; // mm

//////// layered enclosure

let case_rear = 1.0 * key_unit;
let case_front = 0.5 * key_unit;
let case_side = (1 - gap) * key_unit;

let accent_h = 39; // mm
let accent_in = 2; // mm
let accent_w = 3.2; // 3 mm + clearance

let ellipse_indent = 1.5;
let ellipse_axis = 7.5 * key_unit;

let rivnut_r = 7 / 2;

let rivnut_x0 = 2;
let rivnut_x1 = 6;
let rivnut_x2 = 9.75;
let rivnut_y0 = 3.02;
let rivnut_y1 = 3.02;
let rivnut_y2 = 2.55;

// derived dimensions

let keys_h = main_height * key_unit;
let keys_w = keys_wide * key_unit;
let case_h = keys_h + case_front + case_rear;
let case_w = keys_w + case_side * 2;

let centre_x = keys_w / 2;
let centre_y = case_h / 2 - case_rear;

let ellipse_left = (main_x + ellipse_indent) * key_unit;
let ellipse_right = ellipse_left + (main_width - ellipse_indent * 2) * key_unit;

// don't clip ellipse
let clip_clearance = 2; // mm
let rect_rear = -case_rear -clip_clearance;
let rect_front = keys_h + case_front + clip_clearance;

function roundrect(c, x, y, w, h, r) {
    c.beginPath();
    c.roundRect(x, y, w, h, r);
    c.stroke();
}

function circle(c, x, y, r) {
    roundrect(c, x - r, y - r, r * 2, r * 2, r);
}

function rivnut(c, x, y) {
    for (let i = 0; i < 3; i++) {
	circle(c, x, y, rivnut_r - i);
    }
}

function rivnut_quad(c, x, y) {
    x *= key_unit;
    y *= key_unit;
    rivnut(c, centre_x - x, centre_y - y);
    rivnut(c, centre_x + x, centre_y - y);
    rivnut(c, centre_x - x, centre_y + y);
    rivnut(c, centre_x + x, centre_y + y);
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
    c.strokeRect(x - stab_width / 2, y - stab_height,
		 stab_width, stab_depth + stab_height);
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

function line_key_units(c, x, y) {
    c.lineTo(x * key_unit, y * key_unit);
}

function lego_beam_enclosure(c) {
    let keeb_h = main_height * key_unit;
    let keeb_w = keys_wide * key_unit;

    let beam_len = 12 * lego_stud;
    let beam_h = beam_len;
    let beam_w = 4 * beam_len + 3 * beam_spacing;

    let beam_y = (keeb_h - beam_h) / 2;
    let beam_x = (keeb_w - beam_w) / 2;
    let upper_beam = -beam_radius -board_clearance;
    let lower_beam = keeb_h - upper_beam;

    let corner_y = beam_y - upper_beam;
    let corner_x = Math.sqrt(beam_spacing ** 2 - corner_y ** 2);

    let left_beam = beam_x - corner_x

    for (let i = 0; i < 4; i++) {
	beam(c, beam_x, upper_beam, 13, 1);
	beam(c, beam_x, lower_beam, 13, 1);
	beam_x += beam_len + beam_spacing;
    }

    let right_beam = beam_x - beam_spacing + corner_x;

    beam(c, left_beam, beam_y, 1, 13);
    beam(c, right_beam, beam_y, 1, 13);
}

function ellipse_enclosure(c) {
    c.beginPath();
    c.moveTo(ellipse_left, keys_h + case_front);
    c.ellipse(ellipse_left, centre_y, ellipse_axis, case_h / 2,
	      0, tau * 1/4, tau * 3/4);
    c.lineTo(ellipse_right, -case_rear);
    c.ellipse(ellipse_right, centre_y, ellipse_axis, case_h / 2,
	      0, tau * 3/4, tau * 5/4);
    c.closePath();
}

function rectangle_enclosure(c) {
    c.beginPath();
    c.moveTo(-case_side, rect_rear);
    c.lineTo(keys_w + case_side, rect_rear);
    c.lineTo(keys_w + case_side, rect_front);
    c.lineTo(-case_side, rect_front);
    c.closePath();
}

function main() {
    let c = canvas.getContext("2d")
    c.transform(8, 0, 0, 8, 300, 300);

    // switch plate

    c.save();
    c.strokeStyle = "#00c";
    c.lineWidth = 0.2;

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
	    if (i == 1 || j == 1) {
		gappy_hole(c, i, j, 1, right_x, lower_y);
	    }
	}
    }

    c.restore();

    // outline of pcb

    c.save();
    c.strokeStyle = "#0c0";
    c.lineWidth = 0.4;

    c.beginPath();
    c.moveTo(outside_width * key_unit, 0);
    line_key_units(c, outside_width + main_width,
		   0);
    line_key_units(c, outside_width + main_width + gap,
		   upper_y);
    line_key_units(c, outside_width + main_width + outside_width,
		   upper_y);
    line_key_units(c, outside_width + main_width + outside_width + pcb_wing,
		   upper_y + pcb_wing);
    line_key_units(c, outside_width + main_width + outside_width + pcb_wing,
		   below_y - pcb_wing);
    line_key_units(c, outside_width + main_width + outside_width,
		   below_y);
    line_key_units(c, outside_width + main_width + gap * 2,
		   below_y);
    line_key_units(c, outside_width + main_width,
		   main_height);
    line_key_units(c, outside_width,
		   main_height);
    line_key_units(c, side_width - gap,
		   below_y);
    line_key_units(c, 0,
		   below_y);
    line_key_units(c, -pcb_wing,
		   below_y - pcb_wing);
    line_key_units(c, -pcb_wing,
		   upper_y + pcb_wing);
    line_key_units(c, 0,
		   upper_y);
    line_key_units(c, side_width,
		   upper_y);
    line_key_units(c, outside_width,
		   0);
    c.closePath();
    c.stroke();
    c.restore();

    // Waveshare RP2040-Tiny daughterboard

    c.save();
    c.strokeStyle = "#080";
    c.lineWidth = 0.2;

    roundrect(c, centre_x - tdb_width/2, -case_rear + tdb_hang,
	      tdb_width, tdb_depth, tdb_radius);
    roundrect(c, centre_x - usb_width/2, -case_rear + tdb_hang,
	      usb_width, usb_depth, 0);

    c.restore();

    // key blocks

    c.save();
    c.strokeStyle = "#088";
    c.lineWidth = 0.6;
    c.setLineDash([0.4, 0.4]);

    rect_key_units(c, left_x, upper_y, side_width, side_height);
    rect_key_units(c, left_x, lower_y, side_width, side_height);
    rect_key_units(c, right_x, upper_y, side_width, side_height);
    rect_key_units(c, right_x, lower_y, side_width, side_height);
    rect_key_units(c, main_x, 0, main_width, main_height);

    c.restore();

    // outline of enclosure

    c.save();
    c.strokeStyle = "#000";
    c.lineWidth = 0.2;

    c.save();
    rectangle_enclosure(c);
    c.clip();
    ellipse_enclosure(c);
    c.stroke();
    c.restore();

    c.save();
    ellipse_enclosure(c);
    c.clip();
    rectangle_enclosure(c);
    c.stroke();
    c.restore();

    // inside enclosure

    for (let x of [-1, +1]) {
	for (let y of [-1, +1]) {
	    c.beginPath();

	    let clear_y = centre_y + y;

	    c.moveTo(centre_x,
		     clear_y + y * key_unit * 2.75);
	    c.lineTo(centre_x + x * key_unit * (main_width / 2 - 1),
		     clear_y + y * key_unit * 2.75);
	    c.bezierCurveTo(centre_x + x * key_unit * (main_width / 2 + 1),
			    clear_y + y * key_unit * 2.75,
			    centre_x + x * key_unit * (main_width / 2 + 1),
			    clear_y + y * key_unit * 2.75,
			    centre_x + x * key_unit * (main_width / 2 + 2.2),
			    clear_y + y * key_unit * 2.25);
	    c.lineTo(centre_x + x * (case_w / 2 - case_side + 1),
		     clear_y + y * (key_unit * 2.25));
	    c.lineTo(centre_x + x * (case_w / 2 - accent_w - accent_in * 2),
		     clear_y + y * (accent_h - accent_in));
	    c.lineTo(centre_x + x * (case_w / 2 - accent_w - accent_in),
		     clear_y + y * (accent_h - accent_in));
	    c.lineTo(centre_x + x * (case_w / 2 - accent_w - accent_in),
		     clear_y + y * (accent_h));
	    c.lineTo(centre_x + x * (case_w / 2 - accent_in),
		     clear_y + y * (accent_h));
	    c.lineTo(centre_x + x * (case_w / 2 - accent_in),
		     clear_y + y * (accent_h - accent_in));
	    c.lineTo(centre_x + x * (case_w / 2 - 0),
		     clear_y + y * (accent_h - accent_in));

	    c.stroke();
	}
    }

    c.restore();

    // fasteners

    c.save();
    c.strokeStyle = "#a0a";
    c.lineWidth = 0.2;

    rivnut_quad(c, rivnut_x0, rivnut_y0);
    rivnut_quad(c, rivnut_x1, rivnut_y1);
    rivnut_quad(c, rivnut_x2, rivnut_y2);

    c.restore();
}
