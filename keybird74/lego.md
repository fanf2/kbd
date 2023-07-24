lego technic beam sandwich, 74 key edition
==========================================

This is a successor to the keybird 69 key edition, with an extra column
of macro keys, and gaps between the main key block / arrows / macros.

http://www.keyboard-layout-editor.com/#/gists/dce374022378b1c54a5d802cb4affe9e

The RP2040 will be on the PCB insted of using a dev board.

Switches soldered in
  * no space for kailh hotswap sockets
  * could use mill-max tho

19 mm key spacing for easier kicad grids


width of keys without gaps
--------------------------

17 * 19 = 323 mm

0.5 u gap between main block and macros = 9.5 mm

0.25 u gap around arrows = 4.75 mm

key width = 332.5 mm


width of lego technic beams
---------------------------

328 mm = 41 studs

with side beams, 43 studs

  * 15 + 13 + 15 = 43

  * no half stud offsets at the corners

remove 2 * 0.4 mm to narrow gaps between beams

add 2 * 0.4 mm because side beams are 7.2 mm wide


space at edge
-------------

switch cutout 14 mm

(19 - 14) / 2 = 2.5 mm key surround either side

  * no space for kailh socket

  * must allow for five pin holes

332.5 - 5 = 327.5 mm

0.5 mm clearance, bit tight

space to edge of fixation pins is 3.5 mm

maybe take 3 mm either side

turn fixation holes into slots near edge of board?

332.5 - 2 * 3 = 326.5 mm


depth of keys
-------------

main block 5 * 19 = 95 mm

add 4 mm arrow gap

remove 2 mm key surround at front of PCB

  * 97
