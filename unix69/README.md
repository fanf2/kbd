unix69 keyboard layout: nerdy and nice
======================================

A proper Unix keyboard layout must have escape next to 1 and control
next to A.

Unfortunately, this displaces backquote from its common position next
to 1. But a proper Unix keyboard should cover the entire ASCII
repertoire, 94 printing characters on 47 keys, plus space, in the main
block of keys.

This requirement can be handled by moving delete down a row so it is
above return, and putting backslash and backquote where delete was.

(Aside: the delete key emits the delete character, ASCII 127, and the
return key emits the carriage return character, ASCII 13. That is why
I don't call them backspace and enter.)

These changes produce a layout similar to the main key block of Sun
Type 7, Happy Hacking, Tsangan, and True Fox keyboards.

Personally, I prefer compact keyboards so I don't have to reach too
far for the mouse, but I can't do without arrow keys. So a 65% size
(5 rows, 16 keys wide) is ideal.

If you apply the Unix layout requirements to a typical 68-key 65%
layout, you get a 69-key layout. I call it unix69. (1969 was also
the year Unix started.)

    ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
    │esc│1! │2@ │3# │4$ │5% │6^ │7& │8* │9( │0) │-_ │=+ │\| │`~ │ m1│
    ├───┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴───┼───┤
    │ tab │ q │ w │ e │ r │ t │ y │ u │ i │ o │ p │[{ │]} │ del │ m2│
    ├─────┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴─────┼───┤
    │ ctrl │ a │ s │ d │ f │ g │ h │ j │ k │ l │;: │'" │ return │ m3│
    ├──────┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴────┬───┼───┤
    │ shift  │ z │ x │ c │ v │ b │ n │ m │,< │.> │/? │ shft │ ↑ │ m4│
    ├────┬───┴┬──┴─┬─┴───┴───┴───┴───┴───┴──┬┴──┬┴──┬┴──┬───┼───┼───┤
    │fn  │alt │meta│                        │ M-│ C-│ fn│ ← │ ↓ │ → │
    └────┴────┴────┴────────────────────────┴───┴───┴───┴───┴───┴───┘

I have arranged the bottom row modifiers for Emacs: there are left and
right meta keys and a right ctrl key for one-handed navigation. Meta
is what the USB HID spec calls the "GUI" key; it sometimes has a
diamond icon legend. Like the HHKB and Unix workstations made by Apple
and Sun, the meta keys are either side of the space bar.

There are left and right fn keys for things that don't have dedicated
keys, e.g. fn+arrows for page up/down, home, end. The rightmost column
has user-programmable macro keys, for things like media control or
window management.


unix69 vs ansi 65%
------------------

ANSI 65% keyboards have caps lock where ctrl should be.

They have an oversized backslash and lack a good place for backquote.

The right column is wasted on fixed-function keys.


unix69 vs true fox
------------------

Matt3o's Whitefox / Nightfox "True Fox" layout has the same top 2 rows
as unix69.

True Fox has caps lock where ctrl should be. Its right column is
wasted on fixed-function keys.

On the bottom row, True Fox has two modifers and a gap between space
and arrows, whereas unix69 has three modifiers and no gap. Both
bottom rows are common in 65% keyboards.


unix69 vs hhkb
---------------

The happy hacking keyboard is OK for a 60% Unix layout. However it
lacks a left fn key, and lacks space for full-size arrow keys, so I
prefer a 65% layout.

(The Tsangan layout is basically HHKB, plus two extra modifier keys so
the bottom row is full width.)
