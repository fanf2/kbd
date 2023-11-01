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
      - vaguely AT reto feel, but more symmetry

The result is a board with 84 keys and some lovely symmetries,
and better modifier + arrow key ergonomics than usual.

I called it keybird42 because 42 is funnier than 84, and because the
symmetry is emphasized by talking about half the number of keys.


inspiration
-----------

  * displaced arrow cluster
      - https://geekhack.org/index.php?topic=121633.0

  * upper case horizontal screws
      - https://geekhack.org/index.php?topic=121696.0

  * drone vibration isolation mount
      - https://geekhack.org/index.php?topic=119899.0

  * XT TKL FRL with grommet mount
      - https://geekhack.org/index.php?topic=121658.0

  * upper case curved like keycap profile
      - https://geekhack.org/index.php?topic=117922.0
      - https://en.wikipedia.org/wiki/Apple_Extended_Keyboard

  * rounded front and rear
      - https://clickykeyboards.com/wp-content/uploads/2016/11/030.jpg


CadQuery / build123d model
--------------------------

This model of keybird42 is written in Python.

It uses [build123d][]. For development and visualization, I installed
a build of [CQ-editor][] that includes [build123d][] and [CadQuery][].
They are both based on the same underlying CAD library, so they can
coexist happily while providing different higher-level programming
interfaces.

The keycaps are based on [matt3o's OPK][OPK] (open programmatic keycap)
rewritten to use [build123d][] instead of [CadQuery][].

[OPK]: https://github.com/cubiq/OPK
[build123d]: https://build123d.readthedocs.io/
[CadQuery]: https://cadquery.readthedocs.io/
[CQ-editor]: https://github.com/jdegenstein/jmwright-CQ-Editor
