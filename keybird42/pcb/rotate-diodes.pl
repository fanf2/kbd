#!/usr/bin/perl

use warnings;
use strict;

my $diode;

while (<>) {
	if (m{footprint "Diode_SMD}) {
		$diode = 1;
	} elsif (m{footprint}) {
		undef $diode;
	}
	s{^(\s*[(]at [0-9.]+ [0-9.]+)[)]$}{$1 180)} if $diode;
	print;
}
