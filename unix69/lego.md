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

  * 1x1 brick is 8x8 mm (same as my hhkbeeb's surround)

  * plate height 3.2 mm
  * brick height 9.6 mm
  * stud height 1.7 mm

  * stud diameter 4.8 mm
  * technic hole diameter 4.8 mm
  * technic beam height 8 mm (along length of holes)
  * technic beam width 7.2 mm (diameter of end curve)
      - according to LeoCAD

  * clip diameter 3.2 mm (same as holes in studs)
      - might be useful with M3 bolts


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


technic case
============

use FR4 for base as well as switch plate

use technic beams as surround between base and plate

use M3 bolts and rivet nuts to hold it together

  * M3 rivet nuts fit into technic holes
  * (nicely snug in beams, very tight in bricks)


dimensions
----------

  * width 3 x 13 beam = 39 studs => 0.5 extra each end
  * depth 1 x 13 beam => also 0.5 extra each end

we do not need to round to lego stud units!

using lego draw units, 1 ldu = 0.4 mm, 20 ldu = 1 stud

LeoCAD says technic beam is 2 ldu less than 8mm wide

  * inter-beam gap is more generous than inter-brick gap

we'll measure +/- from the centre of the board


left / right
------------

x position of centre line of vertical beams is +/-

16/2 keys + 1/2 stud

8 * 19.05 mm + 4 mm

152.4 mm + 4 mm

391 ldu

includes 1 ldu (ish) inter-beam gap clearance for pcb


y position of centre of end holes of beams is

+/- 13 studs / 2 - 0.5 stud = 6 studs = 48 mm = 120 ldu


front / back
------------

y position of centre line of horizontal beams is +/-

5/2 keys + 1/2 stud

2.5 * 19.05 mm + 4 mm

47.625 + 4 mm

129 ldu (plus a fraction)

includes 1 ldu (ish) inter-beam gap clearance for pcb


x position of centre of end holes is

+/- 3 * 13 studs / 2 - 0.5 stud = 19 studs = 380 ldu

minus inter-beam gap (2 ldu) between each beam


corner geometry
---------------

the distance between the centre points of the ends of the beams
must be 1 stud = 8 mm = 20 ldu minus inter-beam gap (2 ldu)

  * x1 = 391
  * y1 = 120
  * x2 = 380
  * y2 = 129

  * x = 391 - 380 = 11
  * y = 129 - 120 = 9

  * `sqrt(11*11 + 9*9) = sqrt(121 + 81) = sqrt(202) = 14.2 ldu`
      * too small!

additional 4 ldu clearance around pcb

  * x1 = 391 + 4
  * y1 = 120
  * x2 = 380
  * y2 = 129 + 4

  * `sqrt(15*15 + 13*13) = sqrt(394) = 19.8 ldu`
      * 2.0 ldu = 0.8 mm gap front and back
      * 1.8 ldu = 0.7 mm gap at corners
      * clearance around pcb is 5 ldu = 2 mm each side

remove 2 ldu inter-beam gap (reduces horizontal PCB clearance)
and reduce vertical PCB clearance to match

  * x1 = 391 - 2 + 4
  * y1 = 120
  * x2 = 380 - 2
  * y2 = 129 - 2 + 4

  * `sqrt(15*15 + 11*11) = sqrt(346) = 18.6 ldu`
      * 0.0 ldu = 0.0 mm gap front and back
      * 0.6 ldu = 0.2 mm gap at corners
      * clearance around pcb is 3 ldu = 1.2 mm each side

or reduce inter-beam gap by 1 ldu (wrt nominal 20 ldu)

  * `sqrt(15*15 + 12*12) = sqrt(369) = 19.2 ldu`
      * 1.0 ldu = 0.4 mm gap front and back
      * 1.2 ldu = 0.5 mm gap at corners
      * clearance around pcb is 4 ldu = 1.6 mm each side

probably a sensible middle ground?
what is pcb drilling tolerance?


plate and base corners
----------------------

The bevel angle between the beam ends is not 45 degrees (because 15 <> 12)

but if it was 45 degrees, the distance (in the direction continuing
along the beam) from a beam end to the edge of the case is 4mm * sqrt(2)

distance from start of beam end curve to edge of case is 4mm + 4mm * sqrt(2)
which is 9.7 mm - might as well round up to 10mm.

because the beam end radius is slightly less than 4mm, a 10mm corner radius
cuts the corner slightly, in a nice way


USB-C clearance
---------------

centreline of connector is between esc and 1

7 keys +/- (12.5 mm / 2) = 7 * 19.05 mm +/- 6.25 mm

133.35 mm +/- 6.25 mm = 333 ldu +/- 16 ldu ish

distance from end of beam to plug is

  * 380 ldu (centre of last hole)
  * - 1 ldu (removed inter-beam gap)
  * + 10 ldu (half stud to end of beam)
  * - 333 ldu (centre of connector)
  * - 16 ldu (half of plug)

which is 40 ldu = 2 studs

plug is 32 ldu, 1.5 studs

so space for connector is

  * 1 stud beam (to form the enclosure's corner)
  * 1 stud clearance
  * 1.5 stud plug
  * 0.5 stud clearance
  * 35 stud rest of enclosure


fixings
-------

not every beam needs a screw through the switch plate

beams can be mostly held in place by press fitting with rivet nuts
through the base, or with a screw in the beam hole recess (if the
ultra thin super flat wafer head is not so thick it interferes with
the switch plate above)

the switch plate needs enough screw holes to mount it and for
rigidity; 8 is probably fine (my hhkbeeb has 6)
