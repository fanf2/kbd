"use strict";

const bmp = [
    "                   ",
    " O O O O O O O O O ",
    "  O     O O     O  ",
    " O   O   O   O   O ",
    "    O O     O O    ",
    " O   O       O   O ",
    "  O     O O     O  ",
    " O O     O     O O ",
    "  O O         O    ",
    " O O O O O O O   O ",
    "  O O O O          ",
    " O O O O O       O ",
    "  O O O O          ",
    "   O O O O       O ",
    "    O O O O        ",
    "     O O O O     O ",
    "      O O O O      ",
    "       O O O O   O ",
    "        O   O O    ",
    "       O   O   O O ",
    "  O O O O O O   O  ",
    "                 O ",
    "                   ",
];

const txt = [
    "BRITISH",
    "BROADCASTING",
    "CORPORATION",
    "MICROCOMPUTER",
    "SYSTEM",
];

const radius = 16;
const space = 24;
const horz = space;
const vert = space;

const textx = bmp[0].length * horz;
const owlx = textx - horz/2;

const viewx = textx * 3;
const viewy = bmp.length * vert - vert;

const texth = viewy / txt.length;
const texty = texth - vert;

const svgns = 'http://www.w3.org/2000/svg';

function balls() {
    const balls = document.getElementById('balls');

    function ball(cx, cy, r) {
	const elem = document.createElementNS(svgns, 'circle');
	elem.setAttributeNS(null, 'cx', cx);
	elem.setAttributeNS(null, 'cy', cy);
	elem.setAttributeNS(null, 'r', r);
	balls.appendChild(elem);
    }

    for (let row = 0; bmp[row]; row++) {
	for (let col = 0; bmp[row][col]; col++) {
	    const x = col * horz;
	    const y = row * vert;
	    if (bmp[row][col] === 'O')
		ball(x,y,radius);
	}
    }
}

function owl_gooey() {
    svg.setAttributeNS(null, 'viewBox', `0 0 ${viewx} ${viewy}`);
    balls();

    for (let i = 0; i < txt.length; i++) {
	const elem = document.createElementNS(svgns, 'text');
	elem.setAttributeNS(null, 'x', textx);
	elem.setAttributeNS(null, 'y', i * texth + texty);
	elem.setAttributeNS(null, 'font-size', texth);
	elem.appendChild(document.createTextNode(txt[i]));
	legend.appendChild(elem);
    }
}

function owl_render() {
    svg.setAttributeNS(null, 'viewBox', `0 0 ${owlx} ${viewy}`);
    balls();

    // convert balls to svg image
    const svgxml = svg.parentElement.innerHTML;
    img.setAttribute("src", "data:image/svg+xml;utf8," + svgxml);

    // render image as bitmap
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);

    // convert balls to png image
    img.setAttribute("src", canvas.toDataURL());
}
