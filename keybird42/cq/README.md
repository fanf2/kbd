CADquery / build123d model
==========================

This model of keybird42 is written in Python.

It uses [build123d][]. For development and visualization, I installed
a build of [CQ-editor][] that includes build123d and CadQuery. They
are both based on the same underlying CAD library, so they can coexist
happily while providing different higher-level programming interfaces.

The keycaps are [matt3o's OPK][OPK] (open programmatic keycap) which
is developed in Python using [CadQuery][]. The keybird model expects
you have run `git checkout https://github.com/cubiq/OPK` in this
directory, so it can import the keycap model.

[OPK]: https://github.com/cubiq/OPK
[build123d]: https://build123d.readthedocs.io/
[CadQuery]: https://cadquery.readthedocs.io/
[CQ-editor]: https://github.com/jdegenstein/jmwright-CQ-Editor
