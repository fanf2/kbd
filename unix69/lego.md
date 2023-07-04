lego technic beam sandwich
==========================

Originally inspired by James Munns, who [uses Lego for mounting
PCBs][bitshiftmask1], including [at least one keyboard][bitshiftmask2].

[bitshiftmask1]: https://twitter.com/bitshiftmask/status/1590395981686001664
[bitshiftmask2]: https://twitter.com/bitshiftmask/status/1376170525224022018

The first idea was to make a keyswitch plate from FR4 (i.e. a PCB with
appropriate cutouts) mounted on Lego bricks which form the enclosure,
somewhat like https://kbdcraft.store/products/adam

This was too difficult to make slender, largely because the distance
from the switch plate to the studs is about 8mm, less than the 5mm +
3.5mm needed for the switches and USB socket. But an FR4 base plate is
more adaptable with the possibility of cutouts, so I changed to a
sandwich design instead.

I failed to make the case for my HHKBeeb because it was toto hard to
find somewhere that could cut acrylic to my spec. Lego technic beams
are easier to obtain, albeit less flexible.

So the idea is to make an FR4 sandwich case, with lego technic beams
enclosing the sides between the switch plate and base plate.


lego dimensions
---------------

  * 1x1 brick is 8x8 mm (same as my HHKBeeb's surround)

  * plate height 3.2 mm
  * brick height 9.6 mm
  * stud height 1.7 mm
  * stud diameter 4.8 mm

  * clip diameter 3.2 mm (same as holes in studs)
      - might be useful with M3 bolts

  * technic hole diameter 4.8 mm
  * technic beam height 8 mm (along length of holes)
  * technic beam width 7.2 mm (diameter of end curve)


fasteners
---------

Two options:

  * M3 rivet nuts and bolts. 5mm outer diameter of rivet nut will
    press fit very firmly into a technic hole. I will use this
    since I have the bits left over from HHTBeeb.

  * M2 standoffs and bolts. M2 hex nut face-to-face distance is 4mm,
    corner-to-corner is 4.5mm, easily fits into technic hole. Needs to
    rely on friction against the plates to hold the beam in place.


nominal board dimensions
------------------------

16 keys * 19.05 mm = 304.8 mm

5 keys * 19.05 mm = 95.25 mm

38.1 x 11.9 studs => 3 x 13m beam wide, 1 x 13m beam deep

PCB dimension tolerance 0.2 mm


### component clearance

  - 5 mm switches + pcb
  - 1.9 mm hotswap socket
  - 2.1 mm RP2040-Tiny

  - max 7.1 mm

  - 8 mm technic beam

  - 1 mm clearance under sockets
  - 3 mm clearance under PCB


RP2040-Tiny USB adapter
-----------------------

outer dimensions 18 x 18 mm
  * corner radius 1 mm
  * board 1.6 mm thick

mounting holes
  * diameter 2 mm
  * centre to edge of board 2 mm

### components

based on web site image, 220 px == 18 mm

  * FPC connector
      - 1 mm thick
      - 6.5 mm wide
      - ??? 4.9 mm flex lead

  * buttons
      - 2.5 mm thick

  * USB socket
      - 7.5 mm deep
      - 9 mm wide

  * thickness step from 2.5 mm to 5 mm
      - 12.25 mm to USB edge of board
      - 5.75 mm to FPC edge of board

### limits on position

  * 2.5 mm hotswap to nominal edge

  * adapter on top of base plate
      - FPC connector under PCB
      - 15.5 mm nominal edge to USB edge

  * adaptor flush with base
      - FPC connector under sockets
      - PCB cutout for buttons
      - 9.75 mm nominal edge to USB edge


rectangular enclosure
---------------------

could not make space to mount the USB adapter nicely


angled enclosure
----------------

rectangular round the front, gentle enlargement at the back


front beams

  * whole studs, 38 * 8 = 304 mm
  * narrow gaps, 303.2 mm
  * tight, 302.4 mm

distance between end holes

  * whole stud, 8 mm
  * narrow gap, 7.6 mm
  * tight, 7.2 mm

isoceles corner triangle

  * h = 7.6 mm
  * b = `sqrt( 7.6 * 7.6 / 2 )`
  * b = 5.4 mm

internal distance between side beams

  * 303.2 + 5.4 * 2 - 7.2
  * 306.8 mm
      - 1 mm clearance either side of 304.8 mm nominal

internal distance between front and back beams

  * 12 * 8 + 5.4 * 2 - 7.2
  * 99.6 mm
      - 95.25 mm nominal plus 4.35 mm
      - 0.35 mm clearance at front, 4 mm space at back

angle rear beams so that space from nominal rear to enclosure rear is:

  * 2 mm FPC under PCB
  * 16 mm rest of USB adapter


stabilizer cutouts
------------------

cherry data sheet says

0.94 in between stab keycap mounts = 23.876 mm

0.166 in between mount and outer edge of cutout = 4.216 mm

0.262 in cutout width = 6.65 mm

width between outer edges of cutouts = 32.31 mm

space between switch cutout and stab cutout = 2.515 mm


ai03 uses 7 mm width, centred on keycap mounts

width between outer edges of cutouts = 30.876 mm

space between switch cutout and stab cutout = 1.438 mm


swill uses 6.75 mm cutout width

space between switch cutout and stab cutout = 1.525 mm

width between outer edges of cutouts = 30.55


for now let's use 7 x 14 mm stab cutouts,
aligned with and 1.5 mm from the switch cutout
(need to check wrt actual stab dimensions)
