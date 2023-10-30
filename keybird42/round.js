// all units mm

const key_unit = 19; // metricated
const mx_width = 14;
const stem_width = 10; // guess
const cap_width = 18;
const cap_height = 8;
const top_width = 12;

const plate_gap = (key_unit - mx_width) / 2;
const stem_gap = (key_unit - stem_width) / 2;
const cap_gap = (key_unit - cap_width) / 2;
const top_gap = (key_unit - top_width) / 2;

// switch dimensions, from data sheet
// boundary between upper and lower is top of plate
// boundary between lower and pins is top of pcb
const mx_height = 11.6;
const mx_lower = 5.0;
const mx_upper = mx_height - mx_lower;
const mx_pins = 3.3;
const plate_thick = 1.5; // 0.06 in
const cap_skirt = (0.46 - 0.43) * 25.4;
const mx_thick = mx_height - cap_skirt;

// daughterboard
const udb_width = 9;
const udb_thick = 1.6;
const usb_width = 7.3;
const usb_thick = 3.26;
const usb_hang = 1.3;

// pcba needs to be slender enough not to affect overall thickness
// pcb should be >= 1.2 mm (kailh socket depth)
// components are less than 2mm thick
const pcb_thick = 1.2;
const pcba_clearance = 0.5;
const pcba_thick = mx_pins + pcba_clearance;
const pcba_components = mx_pins - pcb_thick;

// enclosure
const case_thick = 15.0;
const frame_thick = 2.5;
const outer_radius = case_thick / 2;
const inner_radius = outer_radius - frame_thick;

console.assert(pcba_thick + mx_thick <= case_thick,
	       "case is too thin",
	       {mx_pins, mx_thick, case_thick});

const keys = 5;
const arrow_gap = 0.25 * key_unit;

function roundrect(c, x, y, w, h, r) {
    c.beginPath();
    c.roundRect(x, y, w, h, r);
    c.fill();
    c.stroke();
}

function drawkey(c, x, y) {
    c.beginPath();
    c.moveTo(x + plate_gap, y);
    c.lineTo(x + plate_gap, y + mx_lower);
    c.lineTo(x + key_unit - plate_gap, y + mx_lower);
    c.lineTo(x + key_unit - plate_gap, y);
    c.lineTo(x + key_unit - stem_gap, y - mx_upper);
    c.lineTo(x + stem_gap, y - mx_upper);
    c.closePath();
    y -= mx_upper - cap_skirt;
    c.moveTo(x + cap_gap, y);
    c.lineTo(x + key_unit - cap_gap, y);
    c.lineTo(x + key_unit - top_gap, y - cap_height);
    c.lineTo(x + top_gap, y - cap_height);
    c.closePath();
    c.fill();
    c.stroke();
}

function layer(c, x, y, w, h) {
    roundrect(c, x, y, w, h, 0);
    return h;
}

function beam(c, x, y, w, r) {
    roundrect(c, x - r, y - r, w + r*2, r*2, r);
}

function circle(c, x, y, r) {
    roundrect(c, x - r, y - r, r * 2, r * 2, r);
}

function main() {
    let x = 0;
    let y = 0;
    let c = canvas.getContext("2d")
    c.strokeStyle = "#000";
    c.fillStyle = "#fff";
    c.lineWidth = 0.1;
    c.transform(20, 0, 0, 20, 400, 400);

    const keyblock = keys * key_unit;
    const width = keyblock + arrow_gap * 2;
    const plate_width = keyblock + arrow_gap;
    const pcb_width = plate_width - plate_gap;
    const pin_width = 5;
    const keepout = (key_unit - pin_width) / 2;
    const component_width = plate_width - keepout - plate_gap;

    y = outer_radius;
    y -= pcba_clearance;
    circle(c, keepout, y, 1.0);
    c.fillStyle = "#ccc";
    y += layer(c, keepout, y, component_width, -pcba_components);
    c.fillStyle = "#080";
    y += layer(c, plate_gap, y, pcb_width, -pcb_thick);
    y -= mx_lower;
    layer(c, 0, y, plate_width, plate_thick);
    c.fillStyle = "#0000";
    drawkey(c, 0, y);
    for (x = 1; x < keys; x++) {
	drawkey(c, arrow_gap + x * key_unit, y);
    }

    c.fillStyle = "#080";
    roundrect(c, width, 12, -udb_width, udb_thick, 0);
    c.fillStyle = "#ccc";
    roundrect(c, width + usb_hang, 12,
	      -usb_width, -usb_thick, 0);

    c.strokeStyle = "#000";
    c.fillStyle = "#0000";
    beam(c, 0, 0, width, outer_radius);
    beam(c, 0, 0, width, inner_radius);

    const degree = Math.PI / 180;
    const theta = 5.5 * degree;
    const cos = Math.cos(theta);
    const sin = Math.sin(theta);

    x = -outer_radius * sin;
    y = +outer_radius * cos;
    circle(c, x, y, 1.0);
    circle(c, 0, outer_radius, 1.0);
    c.beginPath();
    c.moveTo(x, y);
    x += width * cos;
    y += width * sin;
    c.lineTo(x, y);
    c.lineTo(width, outer_radius);
    c.stroke();
    console.log({x,y});
}
