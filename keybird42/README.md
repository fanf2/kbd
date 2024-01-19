keybird42
=========

http://www.keyboard-layout-editor.com/#/gists/dae8374b0ce94d88869aaf67bffb43e0

The main niggle about keybird69 is the lack of gap between delete &
return, and the function column. Sculpted keycaps go some way to
mitigating it, but not completely.

I played around with layouts that have a separated arrow cluster and
function columns (like a reduced 1800 layout), but they make it harder
to use the arrow keys with the thumb on a modifier.

So keybird42 has the following features:

  * unix / hhkb / tsangan main block, i.e.
      - split backspace, with backslash and backquote taking its place
      - escape above tab, left of 1
      - control below tab, left of A
      - delete above return
      - 1.75u right shift with fn key to its right

  * modified tsangan bottom row
      - 1.25 1.25 1.5 7 1.5 1.25 1.25
      - better symmetry
      - reasonable space bar compatibility
      - leftmost and rightmost modifiers have equal sizes
          + more keycap options

  * compared to usual 6.25 bottom row, tsangan has
      - left meta key slightly further right
          + better ergonomics for M-x
          + more like apple keyboard
      - right meta key further right
          + easier to reach with fingers on arrow keys

  * modified arrow and nav cluster to the right
      - like tenkeyless board
      - arrow cluster moved 0.5u upwards
          + easier to reach modifiers with thumb
      - nav cluster moved 0.25u downwards
          + better vertical symmetry
          + equal gaps between clusters

  * function keys moved to left
      - function-rowless
      - two clusters of 6 mirroring the nav and arrow clusters
      - vaguely PC AT reto feel, but more symmetry

The result is a board with 84 keys and some lovely symmetries,
and better modifier + arrow key ergonomics than usual.

I called it keybird42 because:

  * 42 cm wide PCB
  * 21 keys wide (42 / 2)
  * 84 keys total (42 * 2)
  * 5 keys deep (fnord)
  * 23 key unit wide case (fnord)
  * 6.666 key unit deep case (devilish)


window placement
----------------

I intend to use the left hand function clusters to move windows into
the places I like on my 4K display. The most useful positions for me
are:

   * 4 columns, quarters
   * 3 columns, thirds
   * 3 columns, 1/4 1/2 1/4
   * 2 halves side-by-side
   * 1/3 and 2/3 side-by-side

These fit into the 12 function keys fairly nicely, thus:

        +---+---+---+
        |1  |2  |3+4|
        |  4|  4|  4|
        +---+---+---+
        |1+2|3  |4  |
        |  4|  4|  4|
        +---+---+---+

        +---+---+---+
        |1+2|2+3|2+3|
        |  3|  4|  3|
        +---+---+---+
        |1  |2  |3  |
        |  3|  3|  3|
        +---+---+---+

It might be useful to augment these with top-half (CTRL) and
bottom-half (SHIFT) variants.


other functions
---------------

The right function cluster has room for:

  * non-full-screen maximize
  * application windows
  * mission control
  * prev/next desktop (PG UP, PG DN)
  * screenshot (PRNT SCRN)
