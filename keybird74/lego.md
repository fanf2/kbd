lego technic beam sandwich, 74 key edition
==========================================

This is a successor to the keybird 69 key edition, with an extra column
of macro keys, and gaps between the main key block / arrows / macros.

http://www.keyboard-layout-editor.com/#/gists/dce374022378b1c54a5d802cb4affe9e

The RP2040 will be on the PCB insted of using a dev board.

Switches soldered in
  * no space for kailh hotswap sockets
  * could use mill-max tho


width of keys without gaps
--------------------------

17 * 19 = 323 mm

19 mm key spacing to avoid mixing metric and imperial


width of lego technic beams
---------------------------

328 mm = 41 studs

with side beams, 43 studs

  * 15 + 13 + 15 = 43

  * no kitty-corner half stud offsets at the corners

remove 2 * 0.4 mm to narrow gaps between beams

add 2 * 0.4 mm because side beams are 7.2 mm wide


space at edge
-------------

switch cutout and body 14 mm wide

(slightly more depth for catches)

  * 19 - 14 = 5 mm key surround counting both sides

  * no space for kailh socket (it sticks out past the switch body)

  * must allow for five pin holes (probably not an issue when there is
    enough space for the switch bodies - 1 mm clearance between
    fixture hole and edge of body)


gap sizes
---------

328 - 323 + 5 = 10 mm

0.5u macro gap = 9.5 mm

keep 0.5 mm for combined clearance (lol a bit tight)

or

8 mm macro gap (one lego stud)

1 mm clearance each side

gap around arrows is half the macro gap


depth of keys
-------------

main block 5 * 19 = 95 mm

add 4 mm arrow gap

remove 2 mm key surround at front of PCB

and 2 mm at rear


depth of lego technic beams
---------------------------

96 mm = 12 studs

with rear beams, 13 studs

remove 0.4 mm to narrow gap between front and side beams

add 0.4 mm because rear beams are 7.2 mm wide


indented front
==============

A rectangular enclosure tight around the keyblock is all very well,
except that it isn't tight around the front, except for the arrow
keys. But we don't have to be rectangular!

Let's indent the front so that it is also tight along the space bar,
with a bulge around the arrows.

A bulge just on the right would put a wrist rest at an angle if is is
shoved up against the keyboard, so maybe put another (empty) bulge on
the left.

  * gap is now the gap around the arrows
  * macro gap is twice arrow gap


clearance
---------

overhang = 2 mm

  * keycap overhang of 2 mm gives us 0.5 mm clearance between surround
    and switch body

  * actual overhang is less because keycaps are 18 mm wide


gap size
--------

aiming for roughly 8 mm

  * let's see how it works out


width between sides
-------------------

width = 17 * 19 + 2 * gap - 2 * overhang

width = 319 + 2 * gap


width of arrow bulge
--------------------

bulge = 4 * 19 + gap - 2 * overhang

bulge = 72 + gap

  * 9 stud beam is too short, must use 11 studs, 88 mm


indented beam ends
------------------

hypotenuse = 7.6 mm

  * beam diameter + 0.4 mm clearance

indent = gap

hole2hole = 8 - overlap

  * whole studs because reduced beam diameter is accounted for by the
    overlap (e.g. consider indent = 0)

hole2hole^2 + indent^2 = hypotenuse^2

hole2hole = sqrt(hypotenuse^2 - indent^2)

hole2hole = sqrt(57.76 - gap^2)

overlap = hypotenuse - hole2hole

overlap = 8 - sqrt(57.76 - gap^2)

  * example
      * gap = 4 mm
      * overlap = 1.54 mm


width of indent
---------------

  * indent is too wide for one beam, so let's calculate each half

width / 2 <= beams <= 7.6 + width / 2

  * beam diameter + 0.4 mm clearance again

  * front beams must not extend past width including side beams

159.5 + gap <= beams/2 <= 167.1 + gap

159.5 <= beams/2 - gap <= 167.1

beams/2 = outer + inner - overlap

outer = 11 studs = 88 mm

71.5 <= inner - overlap - gap <= 79.1

overlap + gap < 8

  * we know gap is about 4 and overlap will be less than that

inner = 10 studs = 80 mm

AWKWARD


front beam layout
-----------------

  * what if we make the indent 2 x 11 stud beams
  * and the left bulge a 9 stud beam

3 * 11 + 9 = 42 studs = 336 mm

beams = 336 - 2 * overlap - 0.4 mm

  * 0.4 mm clearance between indent beams

beams = 336 - 16 - 0.4 + 2 * sqrt(57.76 - gap^2)

beams = 319.6 + 2 * sqrt(57.76 - gap^2)
