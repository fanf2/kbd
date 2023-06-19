unix 69 keyboard layout
=======================

A proper unix keyboard layout must have escape next to 1 and control
next to A.

Unfortunately, this displaces backquote from its usual position next
to 1. But a proper unix keyboard should cover the entire ascii
repertoire, 94 printing characters on 47 keys, plus space.

This requirement can be handled by moving delete down a row so it is
above return, and putting backslash and backquote where delete was.

(Aside: the delete key emits the delete character, ascii 127, and the
return key emits the carriage return character, ascii 13. That is why
I don't call them backspace and enter.)

These changes produce a layout similar to a Sun Type 7, Happy Hacking,
Tsangan, and True Fox keyboards.

Personally, I prefer compact keyboards so I don't have to reach too
far for the mouse, but I can't do without arrow keys. So a 65% size
(16 x 5 key units) is ideal.

If you apply the unix layout requirements to a typical 68-key 65%
layout, you get a 69-key layout. I call it unix 69, because that was
also the year unix started.

    ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
    │esc│1! │2@ │3# │4$ │5% │6^ │7& │8* │9( │0) │-_ │=+ │\| │`~ │ f1│
    ├───┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴───┼───┤
    │ tab │ q │ w │ e │ r │ t │ y │ u │ i │ o │ p │[{ │]} │ del │ f2│
    ├─────┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴─────┼───┤
    │ ctrl │ a │ s │ d │ f │ g │ h │ j │ k │ l │;: │'" │ return │ f3│
    ├──────┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴────┬───┼───┤
    │ shift  │ z │ x │ c │ v │ b │ n │ m │,< │.> │/? │ shft │ ↑ │ f4│
    ├────┬───┴┬──┴─┬─┴───┴───┴───┴───┴───┴──┬┴──┬┴──┬┴──┬───┼───┼───┤
    │fn  │alt │meta│                        │ M-│ C-│ fn│ ← │ ↓ │ → │
    └────┴────┴────┴────────────────────────┴───┴───┴───┴───┴───┴───┘

I have arranged the bottom row modifiers for Emacs: there are left and
right meta keys and a right ctrl key for one-handed navigation. Meta
is what the USB HID spec calls the "GUI" key. Like unix workstations
made by Apple and Sun, the meta keys are either side of the space bar.

There are left and right fn keys for things that don't have dedicated
keys, e.g. fn+arrows for page up/down, home, end. The rightmost column
has user-programmable function keys, for things like media control or
window management.


unix 69 vs ansi 65%
-------------------

ANSI 65% keyboards have caps lock where ctrl should be.

They have an oversized backslash and lack a good place for backquote.


unix 69 vs true fox
-------------------

Unix 69 is similar to Matt3o's Whitefox / Nightfox "True Fox" layout,
with a 16 key top row.

On the bottom row, True Fox has two modifers and a gap between space
and arrows, whereas Unix 69 has three modifiers and no gap. Both
bottom rows are common in 65% keyboards.

True Fox has caps lock where ctrl should be.


unix 69 vs hhkb
---------------

The happy hacking keyboard is OK for a 60% unix layout. However it
lacks a left fn key, and lacks space for full-size arrow keys, so I
prefer a 65% layout.
