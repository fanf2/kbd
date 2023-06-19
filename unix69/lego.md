Lego keyboard case
==================

This idea is inspired by James Munns, who [uses Lego for mounting
PCBs][bitshiftmask1], including [at least one keyboard][bitshiftmask2].

[bitshiftmask1]: https://twitter.com/bitshiftmask/status/1590395981686001664
[bitshiftmask2]: https://twitter.com/bitshiftmask/status/1376170525224022018

The idea is to make a keyswitch plate from FR4
(i.e. a PCB with appropriate cutouts)
mounted on Lego bricks which form the enclosure.

A somewhat different design: https://kbdcraft.store/products/adam


lego dimensions
---------------

  * 1x1 brick is 8x8 mm (same as my hhkb's surround)

  * plate height 3.2 mm
  * brick height 9.6 mm
  * stud height 1.7 mm

  * stud diameter 4.8 mm
  * clip diameter 3.2 mm (same as holes in studs)


width
-----

16 keys * 19.05 mm = 304.8 mm = 38.1 studs

PCB needs to be slightly less wide than 16x the key spacing.

width including surround = 40 studs = 320 mm


depth
-----

5 keys * 19.05 mm = 95.25 mm = 11.9 studs

14 stud plates are unobtanium so use 16 stud plates

surround: 1 stud left, right, front; 3 stud rear


height
------

keyswitch plate is mounted on lego studs

PCB is 5 mm below plate (Cherry MX dimensions)

hotswap sockets need 2 mm

clearance = brick - stud = 9.6 mm  - 1.7 mm = 7.9 mm, ok


USB C socket is 3.5 mm thick x 8.5mm wide

5 mm + 3.5 mm = 8.5 mm, oops

does **not** fit within clearance - remove part of bottom plate?

brick + plate - stud = 9.6 mm + 3.2 mm - 1.7 mm = 11.1 mm, ok

USB plug clearance is 6.5mm x 12.5 mm

6.5/2 + 3.5/2 is 5 mm beyond the socket side of the PCB

5 mm + 5 mm = 10 mm, ok

no extra clearance needed on the other side of the PCB


### alternative 1

use a mid-mount USB socket, extends 2 mm below PCB, same as hotswap sockets

plug then extends 5 mm - 1.5 mm = 3.5 mm

still needs cut-out in bottom plate


### alternative 2

the KBDcraft Adam puts the USB socket _above_ the PCB
and sticking out from the board (it cannot fit between switches)


### alternative 3

or use a USB daughterboard https://unified-daughterboard.github.io/

old JST connector is 2.9 mm (_just_ fits)

pico-EZmate connector is 1.4 mm

best solution for fitting daughterboard is probably a 3d-printed brick
