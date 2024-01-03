// all units mm

const key_unit = 19; // metricated
const mx_width = 14;
const stem_width = 10; // guess
const cap_width = 18;
const cap_height = 8;
const top_width = 12;

const base_gap = (key_unit - mx_width) / 2;
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
const udb_width = 18;
const udb_thick = 1;
const usb_width = 7.3;
const usb_thick = 3.26;
const usb_hang = 1.0; // nominally 1.3mm
const button_thick = 2.5;
const button_width = 12;
const fpc_thick = 1;

const bolt_head = 6;
const bolt_shank = 3;
const bolt_thick = 12;
const nut_shank = 5;
const nut_flange = 8;
const nut_thick = 8.5;

const pcb_thick = 1.2; // kailh socket depth
const pcba_clearance = 0.5;
const pcba_thick = mx_pins - pcb_thick;

console.assert(pcba_thick > 2, // thickness of parts
	       "not enough space for components");

// enclosure
const layer_thin = plate_thick;
const layer_thick = 3;

const keys = 5;
const keyblock = keys * key_unit;

const case_front = 0.5 * key_unit;
const case_back = 1.0 * key_unit;
const case_wide = case_front - pcba_clearance;
const case_thick = layer_thin * 4 + layer_thick * 4;
const case_bot = layer_thin * 3 + layer_thick * 2;
const case_top = case_bot - case_thick;

const width = keyblock + case_front + case_back;

const pcb_width = keyblock;
const component_width = pcb_width - base_gap * 2;

const screw_hole = case_front / 2;

function roundrect(c, x, y, w, h, r) {
    c.beginPath();
    c.roundRect(x, y, w, h, r);
    c.fill();
    c.stroke();
}

function drawkey(c, x, y) {
    c.beginPath();
    c.moveTo(x + base_gap, y);
    c.lineTo(x + base_gap, y + mx_lower);
    c.lineTo(x + key_unit - base_gap, y + mx_lower);
    c.lineTo(x + key_unit - base_gap, y);
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

function layer(c, thin, thick, wide, h) {
    const y = layer_thin * thin + layer_thick * thick;
    if (wide) {
	roundrect(c, 0, y, width, h, 0);
    } else {
	roundrect(c, 0, y, case_wide, h, 0);
	roundrect(c, width, y, -case_wide, h, 0);
    }
    return h;
}

function nut_bolt(c, x) {
    roundrect(c, x - nut_flange / 2, case_bot, nut_flange, 1, 0);
    roundrect(c, x - nut_shank / 2, case_bot, nut_shank, -nut_thick, 0);
    roundrect(c, x - bolt_head / 2, case_top, bolt_head, -1, 0);
    roundrect(c, x - bolt_shank / 2, case_top, bolt_shank, bolt_thick, 0);
}

function main() {
    let x = 0;
    let y = 0;
    let c = canvas.getContext("2d")
    c.strokeStyle = "#000";
    c.fillStyle = "#fff";
    c.lineWidth = 0.1;
    c.transform(20, 0, 0, 20, 200, 400);

    for (x = 0; x < keys; x++) {
	drawkey(c, case_front + x * key_unit, 0);
    }

    c.fillStyle = "#080";
    roundrect(c, case_front, mx_lower, pcb_width, pcb_thick, 0);
    c.fillStyle = "#88c";
    roundrect(c, case_front + base_gap, mx_lower + pcb_thick,
	      component_width, pcba_thick, 0);
    c.fillStyle = "#ccf";
    roundrect(c, case_front + base_gap, mx_lower + pcb_thick + pcba_thick,
	      component_width, pcba_clearance, 0);

    const udb_x = width - usb_hang;
    const udb_y = case_bot - layer_thin - udb_thick;

    c.fillStyle = "#080";
    roundrect(c, udb_x, udb_y, -udb_width, udb_thick, 0);
    c.fillStyle = "#88c";
    roundrect(c, udb_x, udb_y, -usb_width, -usb_thick, 0);
    roundrect(c, udb_x - usb_width, udb_y,
	      -button_width + usb_width, -button_thick, 0);
    roundrect(c, udb_x - button_width, udb_y,
	      -udb_width + button_width, -fpc_thick, 0);

    c.fillStyle = "#8088";
    layer(c, 0, 0, true, layer_thin);
    layer(c, 1, 0, false, layer_thick);
    layer(c, 1, 1, false, layer_thin);
    layer(c, 2, 1, false, layer_thick);
    layer(c, 2, 2, true, layer_thin);
    layer(c, 0, -1, false, layer_thick);
    layer(c, -1, -1, false, layer_thin);
    layer(c, -1, -2, true, layer_thick);

    c.fillStyle = "#0008";
    nut_bolt(c, screw_hole);
    nut_bolt(c, width - screw_hole);
}
