pcba notes
==========


flexible layout
---------------

### pi60 HSE

staggered hotswap sockets support both ANSI and Tsangan

incompatible with per-key RGB LEDs where alternative key positions
have sockets above and below

https://1upkeyboards.com/shop/controllers/1upkeyboards-pi60hse-60-pcb/

### planck hot-swap

another example of staggered sockets

https://drop.com/buy/planck-mechanical-keyboard


reduced height
--------------

  * 1.5 mm plate
  * 3.5 mm switch bodies
  * 1.5 mm pcb
  * 2.0 mm hotswap sockets
  * 1.5 mm base

total 10 mm

USB-C dimensions

  * 1.5 mm plug clearance
  * 3.5 mm USB-C socket
  * 1.5 mm PCB / plug clearance

mid-mount USB-C socket is flush with one surface of PCB

  * 1.5 mm plug clearance
  * 2.0 mm socket
  * 1.5 mm PCB / socket
  * 1.5 mm plug clearance

mid-mount socket might fit in the usual place between esc and 1 ?
or centred between 7 and 8 ?

(won't be compatible with standard cases)

USB plug positions:

(first two need a PCB extension)

  * top mount
      - 0.0 mm above
      - 1.5 mm plate / plug clearance
      - 3.5 mm switch bodies / socket
      - 1.5 mm pcb / plug clearance
      - 2.0 mm components / below
      - 1.5 mm base / below

  * upper mid-mount
      - 1.5 mm plate / above
      - 1.5 mm switch bodies / plug clearance
      - 2.0 mm switch bodies / socket
      - 1.5 mm pcb / socket
      - 1.5 mm components / plug clearance
      - 0.5 mm components / below
      - 1.5 mm base / below

  * lower mid-mount
      - 1.5 mm plate / above
      - 2.0 mm switch bodies / above
      - 1.5 mm switch bodies / plug clearance
      - 1.5 mm pcb / socket
      - 2.0 mm components / socket
      - 1.5 mm base / plug clearance
      - 0.0 mm below

  * bottom mount
      - 1.5 mm plate / above
      - 3.5 mm switch bodies / above
      - 1.5 mm pcb / plug clearance
      - 2.0 mm components / socket
      - 1.5 mm base / socket
      - 1.5 mm overhang / plug clearance

### Drop Alt

Upper mid-mount USB-C.

PCB is larger than usual with edge-mounted RGB LEDs
and extra projections for the USB sockets

https://drop.com/buy/drop-alt-pcba

The case is supposed to be 9mm thick; I guess they shaved some space
from the components and used a really thin baseplate

https://drop.com/buy/drop-alt-aluminum-case

### KBDcraft Adam

Top-mount USB-C

Sticks out on a finger of board into high-profile case surround.

https://kbdcraft.store/products/core64


diy controllers
---------------

matrix gpio pins:

  - 16 + 5 -> 21 pins
      * simple matrix needs lots of pins
      * fewest for 69 keys is 17 pins

  - 72 = 9 * 8 -> 17 pins
      * 16 key columns in pairs -> 8 matrix columns
      * max 9 keys per matrix column


### rp2040-tiny

https://www.waveshare.com/rp2040-tiny.htm
https://www.waveshare.com/wiki/RP2040-Tiny

separate controller and usb adaptor boards

controller dimensions 18 x 23.5 mm (same as a 1.25u keycap)

19 gpio pins

  * adaptor mounted on base
      - 1.5 mm plate / above
      - 1.5 mm switch bodies / above
      - 1.5 mm switch bodies / plug clearance
      - 0.5 mm switch bodies / socket
      - 1.5 mm keyboard pcb / socket
      - 1.5 mm socket
      - 1.5 mm adaptor pcb / plug clearance
      - 1.5 mm base / below

buttons behind socket conflict with keyboard pcb

best solution is probably an underplate

  * adaptor mounted on underplate
      - 1.5 mm plate / above
      - 3.5 mm switch bodies / above
      - 1.0 mm keyboard pcb / plug clearance
      - 0.5 mm keyboard pcb / socket
      - 3.0 mm components
      - 1.5 mm adaptor pcb / base / plug clearance
      - 1.5 mm underplate / below

adaptor dimensions 18 x 18 mm (same as a keycap)

mounting holes 2 mm, 1 mm from board edge

socket depth 7.8 mm

button depth 8.5 ... 12.2 mm

button width 1.1 ... 5.5 mm


### elite-pi

https://keeb.io/products/elite-pi-usb-c-pro-micro-replacement-rp2040

mid-mount usb socket

25 gpio pins

### 0xCB helios

https://keeb.supply/products/0xcb-helios

mid-mount usb socket

21 gpio pins


copper
------

how much does copper affect weight?

typically 1 oz / sq. ft.

key matrix N by M

base is roughly (N + 1) * (M + 1) * 0.75 * 0.75 / 12*12 sq. ft.

= (N+1) * (M+1) / 256

plate is base - cutouts

cutouts are roughly N * M * (14 / 12*25.4)^2

= N * M / 480

total is 4 * base - 2 * cutouts

= (N+1) * (M+1) / 64 - N * M / 240

for 65%

= 17 * 6 / 64 - 16 * 5 / 240 = 1.26 oz = 36 g

