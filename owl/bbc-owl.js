"use strict";

const bmp = [
    "                   ",
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

const gooey = 3;
const radius = 16;
const space = 24;
const horz = space;
const vert = space;

function owl() {
    const svg = document.getElementById('svg');
    const svgns = svg.getAttribute('xmlns');

    const textx = bmp[0].length * horz;
    const viewx = textx * 3;
    const viewy = bmp.length * vert - vert;
    const texty = viewy - vert;
    svg.setAttributeNS(null, 'viewBox', `0 0 ${viewx} ${viewy}`);

    const blur = document.getElementById('blur');
    blur.setAttributeNS(null, 'stdDeviation', gooey);

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

    const legend = document.getElementById('legend');
    const n = txt.length;
    for (let i = 1; i <= n; i++) {
	const elem = document.createElementNS(svgns, 'text');
	elem.setAttributeNS(null, 'x', textx);
	elem.setAttributeNS(null, 'y', i * texty / n);
	elem.setAttributeNS(null, 'font-size', texty / n);
	elem.appendChild(document.createTextNode(txt[i-1]));
	legend.appendChild(elem);
    }
}
