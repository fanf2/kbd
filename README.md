A keyboard like the BBC Micro, made from modern parts
=====================================================

It's the 40th anniversary of the BBC Micro this year. I am trying to
make a keyboard in a similar style, made from modern parts.

The Beeb's keyboard was what is now called a mechanical keyboard.
There's a very lively community of mechanical keyboard makers and
customizers, who have made it fairly easy to get a long way with
off-the-shelf parts.


The BBC Micro keyboard
----------------------

The Beeb's keyboard was mostly a standard [ECMA-23][] layout. The main
oddity from today's point of view is that it has a [bit-paired][]
punctuation layout.

In addition to the basic ECMA-23 keys (all black) the Beeb has some
colourful extras: red function keys and greenish brown arrow keys.

[ECMA-23]: https://en.wikipedia.org/wiki/ECMA-23
[bit-paired]: https://en.wikipedia.org/wiki/Bit-paired_keyboard

I have drawn the [BBC Model B][] and [BBC Master][] keyboard using the
online [Keyboard Layout Editor][] (KLE).

[Keyboard Layout Editor]: http://www.keyboard-layout-editor.com/

![BBC Micro keyboard layout](kle/bbc-model-b.png)

Modern keyboard sizes
---------------------

Key sizes are usually quoted as so many "u", as in units, which are
the size of one standard key. 1u is 0.75 inches.

There are a number of common form-factors:

  * Tenkeyless, aka TKL: Like a full-size keyboard without the number
    pad (which has more than 10 keys, shrug)

  * 60%: Just the main block of the keyboard; no function keys or
    arrow keys etc. The overall size is 15u x 5u, typically with 61
    keys.

  * 75%: Like a TKL but with the function and arrow keys smooshed
    together, so there's a single block of keys. The overall size is
    16u x 6u, typically with 84 keys.

The more we re-use one of these standard layouts, the easier it will
be to build (e.g. using off-the-shelf cases and PCBs) at the cost of
authenticity.


Adjusting the BBC Micro layout
------------------------------

The Beeb keyboard is slightly wider than a 75% board: CAPS LOCK and
SHIFT LOCK stick out 0.25u on the left, and DOWN sticks out 0.5u on
the right. It can be made to fit in a 75% case by using a BBC Master
arrow cluster, and by displacing the LOCK keys. To be usable with a
modern operating system, the keyboard also needs a few more modifier
keys.

My [BBC Master 75%][] layout is based on those ideas. However, fitting
in the 75% form factor isn't as useful as it might be: in typical 75%
case designs, there are PCB mounting holes mid-way between some of the
function keys, which are aligned with the number row below; but the
Beeb's function keys are offset by 0.5u so they clash with the
mounting holes.

A standard 75% ISO board could be given a Beebish appearance with just
some replacement keycaps, like my [Beeb 75% ISO][] layout.

I like small keyboards, so I have made a [Beeb 60% HHKB][] layout.
This has a jokey number row that goes 0-9 (like the BBC Micro function
keys) and is shifted towards the centre.

![Beeb HHKB layout](kle/beeb-60%25-hhkb.png)


Keycaps
-------


Fonts
-----

The BBC Micro keycaps were made by Comptec, who are now known as
[Signature Plastics][]. Their main style of legends is called "Gorton
Modified", named after Gorton engraving machines.

[Signature Plastics]: https://pimpmykeyboard.com/

There are a number of fonts made in the style of engraving machines.

The best I have found so far is [Routed Gothic][], which has a large
repertoir of characters, though some of them are not good matches for
Gorton Modified.

[Open Gorton][] has better matches for some character shapes; it
covers ASCII only.

There is another font called [Gorton Digital][], which is available as a
FontForge script not as built font files. Unfortunately the script
produced mangled output when I tried it, though some of the characters
are usable.

Also worth noting is [National Park][], whose repertoir is roughly
ISO 8859-1.

[Gorton Digital]: https://github.com/drdnar/GortonDigital
[National Park]: https://nationalparktypeface.com/
[Open Gorton]:  https://github.com/dakotafelder/open-gorton
[Routed Gothic]: https://webonastick.com/fonts/routed-gothic/

What I have found works best is a combination of Routed Gothic, Routed
Gothic Wide, and Open Gorton.


### Detailed notes on keycap fonts

CTRL, SHIFT, etc. are all Routed Gothic, except for ESCAPE which is
Routed Gothic Narrow.

Most of the letters and digits are Routed Gothic Wide. A few letters
are Routed Gothic (non-wide): R S B

J is problematic: Open Gorton has a more authentic glyph shape, but
its weights dont match Routed Gothic (regular is too loght; bold is
too heavy).

Zero is a Scandinavian capital slashed O and the correct 1 is found in
Routed Gothic's private use character codes.

3 is problematic. Again, Open Gorton has a more authentic shape
(rounded top instead of angular), but its numerals are too narrow.

For punctuation, #$%&@*^~,.;:<> come from Open Gorton; "(){}[]
from Routed Gothic Wide, and -=`'/|\?! from Routed Gothic.

For symmetry I used reversed prime and prime for `' and rotated them
slightly to make them more distinct. | is a broken bar, _ is an
em-dash, and - is an en-dash.

I upped the font size a lot for ,.;:^~*

The * on the BBC micro has 6 points; Open Gorton has 8 points, a bit
like the * on the BBC Master's numeric keypad (though I think Open
Gorton has shorter points). Gorton Digital has a fairly nice 5-point
asterisk which is a plausible alternative.



[BBC Model B]: http://www.keyboard-layout-editor.com/##@_backcolor=#333333&name=BBC%20Model%20B&author=Tony%20Finch%20(dot/@dotat.at);&@_x:2.5&c=#ff0000&t=#ffffff&a:7&f:5;&=%F0%9D%91%93%C3%B8&=%F0%9D%91%931&=%F0%9D%91%932&=%F0%9D%91%933&=%F0%9D%91%934&=%F0%9D%91%935&=%F0%9D%91%936&=%F0%9D%91%937&=%F0%9D%91%938&=%F0%9D%91%939&_c=#222222&f:2;&=BREAK;&@_x:0.25;&=ESCAPE&_a:5&f:6;&=!%0A1&_f:9&f2:6;&=%22%0A2&_f:6;&=#%0A3&=$%0A4&=%25%0A5&=/&%0A6&_f:9&f2:6;&=%E2%80%B2%0A7&_f:5&f2:6;&=(%0A8&=)%0A9&_a:7&f:9;&=%C3%98&_a:5&f:7;&=/=%0A%E2%80%93&_f:6;&=%E2%81%93%0A%E2%8C%83&_f:5;&=%7C%0A%5C&_c=#554422&a:7&f:9;&=%E2%86%90&=%E2%86%92;&@_x:0.25&c=#222222&f:3&w:1.5;&=TAB&_f:9;&=Q&=W&=E&=R&=T&=Y&=U&=I&=O&=P&=/@&_a:5&f:5;&=%7B%0A%5B&_f:7;&=%C2%A3%0A%E2%80%94&_c=#554422&a:7&f:9;&=%E2%86%91&=%E2%86%93;&@_c=#222222&a:5&f:3;&=CAPS%0ALOCK&_a:7;&=CTRL&_f:9;&=A&=S&=D&=F&=G&=H&=J&=K&=L&_a:5&f:8;&=+%0A/;&_fa@:6;;&=%E2%9C%BB%0A/:&_f:5;&=%7D%0A%5D&_a:7&f:3&w:2;&=RETURN;&@_a:5;&=SHIFT%0ALOCK&_a:7&w:1.5;&=SHIFT&_f:9;&=Z&=X&=C&=V&=B&=N&=M&_a:5&f:8&f2:9;&=%3C%0A,&=%3E%0A.&_f:6;&=?%0A//&_a:7&f:3&w:1.5;&=SHIFT&_f:2;&=DELETE&_c=#554422&f:3;&=COPY;&@_x:3.5&c=#222222&w:8;&=

[BBC Master]: http://www.keyboard-layout-editor.com/##@_backcolor=#333333&name=BBC%20Master&author=Tony%20Finch%20(dot/@dotat.at)&css=*%20%7B%20font-family/:%20%22Arial%22/;%20%7D;&@_x:1.75&c=#ff0000&t=#ffffff&a:7&f:5;&=%F0%9D%91%93%C3%B8&=%F0%9D%91%931&=%F0%9D%91%932&=%F0%9D%91%933&=%F0%9D%91%934&=%F0%9D%91%935&=%F0%9D%91%936&=%F0%9D%91%937&=%F0%9D%91%938&=%F0%9D%91%939&_x:1&c=#222222&f:2;&=BREAK&_x:1&c=#554422&f:9;&=%E2%86%91&_x:0.75&c=#222222;&=+&=%E2%80%93&=//&=%E2%9C%B3%EF%B8%8E;&@_x:0.25&f:2;&=ESCAPE&_a:5&f:6;&=!%0A1&_f:9&f2:6;&=%22%0A2&_f:6;&=#%0A3&=$%0A4&=%25%0A5&=/&%0A6&_f:9&f2:6;&=%E2%80%B2%0A7&_f:5&f2:6;&=(%0A8&=)%0A9&_a:7&f:9;&=%C3%98&_a:5&f:7;&=/=%0A%E2%80%93&_f:6;&=%E2%81%93%0A%E2%8C%83&_f:5;&=%7C%0A%5C&_c=#554422&a:7&f:9;&=%E2%86%90&=%E2%86%92&_x:0.25&c=#222222;&=7&=8&=9&=#;&@_x:0.25&f:3&w:1.5;&=TAB&_f:9;&=Q&=W&=E&=R&=T&=Y&=U&=I&=O&=P&=/@&_a:5&f:5;&=%7B%0A%5B&_f:7;&=%C2%A3%0A%E2%80%94&_c=#554422&a:7&f:9;&=%E2%86%93&_x:0.75&c=#222222;&=4&=5&=6&_f:2;&=DELETE;&@_a:5&f:3;&=CAPS%0ALOCK&_a:7;&=CTRL&_f:9;&=A&=S&=D&=F&=G&=H&=J&=K&=L&_a:5&f:8;&=+%0A/;&_fa@:6;;&=%E2%9C%BB%0A/:&_f:5;&=%7D%0A%5D&_a:7&f:3&w:2;&=RETURN&_x:0.5&f:9;&=1&=2&=3&=,;&@_a:5&f:3;&=SHIFT%0ALOCK&_a:7&w:1.5;&=SHIFT&_f:9;&=Z&=X&=C&=V&=B&=N&=M&_a:5&f:8&f2:9;&=%3C%0A,&=%3E%0A.&_f:6;&=?%0A//&_a:7&f:3&w:1.5;&=SHIFT&_f:2;&=DELETE&_c=#554422&f:3;&=COPY&_x:0.5&c=#222222&f:9;&=%C3%98&=.&_f:3&w:2;&=RETURN;&@_x:3.5&w:8;&=

[BBC Master 75%]: http://www.keyboard-layout-editor.com/##@_backcolor=#333333&name=BBC%20Master%2075%25&author=Tony%20Finch%20(dot/@dotat.at)&css=*%20%7B%20font-family/:%20%22Arial%22/;%20%7D;&@_x:1.5&c=#ff0000&t=#ffffff&a:7&f:5;&=%F0%9D%91%93%C3%B8&=%F0%9D%91%931&=%F0%9D%91%932&=%F0%9D%91%933&=%F0%9D%91%934&=%F0%9D%91%935&=%F0%9D%91%936&=%F0%9D%91%937&=%F0%9D%91%938&=%F0%9D%91%939&_x:1&c=#222222&f:2;&=BREAK&_x:1&c=#554422&f:9;&=%E2%86%91;&@_c=#222222&f:2;&=ESCAPE&_a:5&f:6;&=!%0A1&_f:9&f2:6;&=%22%0A2&_f:6;&=#%0A3&=$%0A4&=%25%0A5&=/&%0A6&_f:9&f2:6;&=%E2%80%B2%0A7&_f:5&f2:6;&=(%0A8&=)%0A9&_a:7&f:9;&=%C3%98&_a:5&f:7;&=/=%0A%E2%80%93&_f:6;&=%E2%81%93%0A%E2%8C%83&_f:5;&=%7C%0A%5C&_c=#554422&a:7&f:9;&=%E2%86%90&=%E2%86%92;&@_c=#222222&f:3&w:1.5;&=TAB&_f:9;&=Q&=W&=E&=R&=T&=Y&=U&=I&=O&=P&=/@&_a:5&f:5;&=%7B%0A%5B&_f:7;&=%C2%A3%0A%E2%80%94&_c=#554422&a:7&f:9;&=%E2%86%93;&@_x:0.25&c=#222222&f:3&w:1.5;&=CTRL&_f:9;&=A&=S&=D&=F&=G&=H&=J&=K&=L&_a:5&f:8;&=+%0A/;&_fa@:6;;&=%E2%9C%BB%0A/:&_f:5;&=%7D%0A%5D&_a:7&f:3&w:2;&=RETURN;&@_x:0.75&w:1.5;&=SHIFT&_f:9;&=Z&=X&=C&=V&=B&=N&=M&_a:5&f:8&f2:9;&=%3C%0A,&=%3E%0A.&_f:6;&=?%0A//&_a:7&f:3&w:1.5;&=SHIFT&=DEL&_c=#554422;&=COPY;&@_x:1.25;&=FN&=OWL&=ALT&_c=#222222&w:7;&=&_c=#554422;&=ALT&=OWL&=MENU

[Beeb 75% ISO]: http://www.keyboard-layout-editor.com/##@_backcolor=#333333&name=beeb%2075%25%20ISO&author=Tony%20Finch%20(dot/@dotat.at)&css=*%20%7B%20font-family/:%20%22Arial%22/;%20%7D;&@_x:2&c=#ff0000&t=#ffffff&a:7&f:4;&=%F0%9D%91%93%C3%B8&=%F0%9D%91%931&=%F0%9D%91%932&=%F0%9D%91%933&=%F0%9D%91%934&=%F0%9D%91%935&=%F0%9D%91%936&=%F0%9D%91%937&=%F0%9D%91%938&=%F0%9D%91%939&_x:1&c=#222222&f:2;&=BREAK;&@=ESCAPE&_a:5&f:6;&=!%0A1&_fa@:9;;&=%22%0A2&_f:6;&=#%0A3&_f:6;&=$%0A4&_f:6;&=%25%0A5&_f:6;&=/&%0A6&_f:9&f2:6;&=%E2%80%B2%0A7&_f:5&f2:6;&=(%0A8&=)%0A9&_f:6;&=%E2%80%94%0A%C3%98&_f:7;&=%E2%80%93%0A/=&_f:6;&=%E2%81%93%0A%E2%8C%83&_a:7&f:3&w:2;&=DELETE&_c=#554422&f:9;&=%E2%A4%92;&@_c=#222222&f:3&w:1.5;&=TAB&_f:9;&=Q&=W&=E&=R&=T&=Y&=U&=I&=O&=P&_a:5&f:7;&=%E2%80%B5%0A/@&_f:5;&=%7B%0A%5B&_x:0.25&t=#000000&a:7&f:3&w:1.25&h:2&w2:1.5&h2:1&x2:-0.25;&=&_c=#554422&t=#ffffff&f:9;&=%E2%86%9F;&@_c=#222222&f:3&w:1.75;&=CTRL&_f:9;&=A&=S&=D&=F&=G&=H&=J&=K&=L&_a:5&f:8;&=+%0A/;&_fa@:6;;&=%E2%9C%BB%0A/:&_f:5;&=%7D%0A%5D&_x:1.25&c=#554422&a:7&f:9;&=%E2%86%A1;&@_c=#222222&f:3&w:1.25;&=SHIFT&_a:5&f:5;&=%7C%0A%5C&_a:7&f:9;&=Z&=X&=C&=V&=B&=N&=M&_a:5&f:8&f2:9;&=%3C%0A,&=%3E%0A.&_f:6;&=?%0A//&_a:7&f:3&w:1.75;&=SHIFT&_c=#554422&f:9;&=%E2%86%91&=%E2%A4%93;&@_f:3&w:1.25;&=FN&_w:1.25;&=OWL&_w:1.25;&=ALT&_c=#222222&w:6.25;&=&_c=#554422;&=ALT&=OWL&=MENU&_f:9;&=%E2%86%90&=%E2%86%93&=%E2%86%92

[Beeb 60% HHKB]: http://www.keyboard-layout-editor.com/##@_backcolor=#333333&name=beeb%2060%25%20hhkb&author=Tony%20Finch%20(dot/@dotat.at)&css=*%20%7B%20font-family/:%20%22Arial%22/;%20%7D;&@_c=#222222&t=#ffffff&a:7&f:2;&=ESCAPE&_a:5&f:7;&=%E2%80%B5%0A/@&_c=#cc0000&f:6;&=%E2%80%94%0A%C3%98&=!%0A1&_f:9&f2:6;&=%22%0A2&_f:6;&=#%0A3&=$%0A4&=%25%0A5&=/&%0A6&_f:9&f2:6;&=%E2%80%B2%0A7&_f:5&f2:6;&=(%0A8&=)%0A9&_c=#222222&f:7;&=%E2%80%93%0A/=&_f:6;&=%E2%81%93%0A%E2%8C%83&_f:5;&=%7C%0A%5C;&@_a:7&f:3&w:1.5;&=TAB&_f:9;&=Q&=W&=E&=R&=T&=Y&=U&=I&=O&=P&_a:5&f:5;&=%7B%0A%5B&=%7D%0A%5D&_a:7&f:3&w:1.5;&=DEL;&@_w:1.75;&=CTRL&_f:9;&=A&=S&=D&=F&=G&=H&=J&=K&=L&_a:5&f:8;&=+%0A/;&_fa@:6;;&=%E2%9C%BB%0A/:&_a:7&f:3&w:2.25;&=RETURN;&@_w:2.25;&=SHIFT&_f:9;&=Z&=X&=C&=V&=B&=N&=M&_a:5&f:8&f2:9;&=%3C%0A,&=%3E%0A.&_f:6;&=?%0A//&_a:7&f:3&w:1.75;&=SHIFT&=FN;&@_x:0.25&c=#554422&w:1.25;&=HYPER&_w:1.25;&=SUPER&_w:1.25;&=META&_c=#222222&w:7;&=&_c=#554422&w:1.25;&=META&_w:1.25;&=SUPER&_w:1.25;&=HYPER
