function mm(elem) {
    return +elem.value.replace("mm", "");
}

function round_rect(c, x, y, w, h, r, f) {
    console.log(`round_rect(${x},\t${y},\t${w},\t${h},\t${r},\t${f})`);

    c.save();
    c.beginPath();
    c.roundRect(x, y, w, h, r);
    c.fillStyle = f;
    c.fill();
    c.restore();
}

function mark_y(c, x, y) {
    c.save();
    c.font = "1px sans-serif";
    c.fillStyle = "#888";
    c.fillText(y, x + 0.1, y + 0.3);
    c.restore();

    c.save();
    c.beginPath();
    c.moveTo(-2, y);
    c.lineTo(x, y);
    c.lineWidth = 0.1;
    c.strokeStyle = "#ccc";
    c.stroke();
    c.restore();
}

function redraw() {
    let c = canvas.getContext("2d")
    c.save();
    c.clearRect(0, 0, canvas.width, canvas.height);

    let scale = 20;
    let translate = scale; // 1 mm
    c.transform(scale, 0, 0, scale, translate, translate);

    // switch

    let body_h = mm(body);
    let pins_h = mm(pins);

    let switch_x = 1;
    let switch_w = 14;
    let pins_w = 2;

    let max_y = body_h + pins_h;

    // boards

    let plate_h = mm(plate);
    let pcb_h = mm(pcb);
    let base_h = mm(base);

    let plate_w = 42;
    let pcb_y = body_h;

    // chip

    let chip_h = mm(chip);
    let chip_w = 4;
    let chip_y = pcb_y + pcb_h;
    let chip_x = switch_x + switch_w + 1;

    let chip_max = chip_y + chip_h;
    max_y = max_y > chip_max ? max_y : chip_max;

    let usb_sink = mm(sink);
    let socket_h = mm(socket);
    let plug_h = mm(plug);
    let socket_w = 9;
    let plug_w = 12.5;

    let socket_y = chip_y - usb_sink;
    let usb_y = socket_y + socket_h / 2;
    let plug_y = usb_y - plug_h / 2;

    let usb_x = chip_x + chip_w + 1 + plug_w / 2;
    let plug_x = usb_x - plug_w / 2;
    let socket_x = usb_x - socket_w / 2;

    let usb_max = socket_y + socket_h
    max_y = max_y > usb_max ? max_y : usb_max;

    // fasteners

    let rivnut_h = mm(rivnut);
    let nut_w = 5;
    let flange_h = mm(flange);
    let flange_w = 7;
    let nut_h = rivnut_h - flange_h;

    let nut_max = plate_h + nut_h - base_h;
    let base_y =  max_y > nut_max ? max_y : nut_max;
    let flange_y = base_y + base_h;
    let nut_y = flange_y - nut_h;

    let rivnut_x = plug_x + plug_w + flange_w / 2;
    let nut_x = rivnut_x - nut_w / 2;
    let flange_x = rivnut_x - flange_w / 2;

    // drawing

    round_rect(c, switch_x, 0, switch_w, body_h, 0, "#0008");
    for (let i = 1; i < 4; i++) {
	round_rect(c, switch_x + switch_w*i/4 - pins_w/2, body_h,
		   pins_w, pins_h, 0, "#0008");
    }

    round_rect(c, chip_x, chip_y, chip_w, chip_h, 0, "#0008");

    round_rect(c, plug_x, plug_y, plug_w, plug_h, plug_h / 2, "#8088");
    round_rect(c, socket_x, socket_y, socket_w, socket_h, socket_h / 2, "#8088");

    round_rect(c, nut_x, nut_y, nut_w, nut_h, 0, "#8808");
    round_rect(c, flange_x, flange_y, flange_w, flange_h, 0, "#8808");

    round_rect(c, 0, 0, plate_w, plate_h, 0, "#8f88");
    round_rect(c, 0, pcb_y, plate_w, pcb_h, 0, "#8f88");
    round_rect(c, 0, base_y, plate_w, base_h, 0, "#8f88");

    mark_y(c, 44, pcb_y);
    mark_y(c, 44, chip_y);
    mark_y(c, 46, socket_y);
    mark_y(c, 46, socket_y + socket_h);
    mark_y(c, 44, max_y);
    mark_y(c, 46, base_y);
    mark_y(c, 44, base_y + base_h);

    c.restore();
}
