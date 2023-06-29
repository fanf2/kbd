#!/usr/bin/perl

use warnings;
use strict;

my $uuid;
my %component;
while (<>) {
	if (m{[(]uuid (\S+)[)]}) {
		$uuid = $1;
	}
	if (m{^\s+[(]path\s+"/([0-9a-f-]+)"\s*$}) {
		$uuid = $1;
	}
	if (m{^\s*[(]property\s+"Reference"\s+"SW[0-9?]+"\s+[(]id\s+0[)]
	      \s+[(]at\s+([0-9.]+)\s+([0-9.]+)\s+0[)][)]\s*$}x) {
		my $group = $1/25.4 - 2.2;
		my $track = $2 * 2/25.4 - 2.1;
		my $sw = sprintf "SW%d%d", int $track, int $group;
		s{SW[0-9?]+}{$sw};
		$component{$uuid} = $sw;
	}
	if (m{^\s*[(]property\s+"Reference"\s+"D[0-9?]+"\s+[(]id\s+0[)]
		      \s+[(]at\s+([0-9.]+)\s+([0-9.]+)\s+0[)][)]\s*$}x) {
		my $group = $1/25.4 - 2.5;
		my $track = $2 * 2/25.4 - 2.1;
		my $d = sprintf "D%d%d", int $track, int $group;
		s{D[0-9?]+}{$d};
		$component{$uuid} = $d;
	}
	if (m{^\s+[(]reference\s+"[A-Z0-9?]+"[)]
	      \s+[(]unit\s+1[)]\s+[(]value\s+"(SW_Push|DIODE)"[)]}x) {
		s{"[A-Z0-9?]+"}{"$component{$uuid}"};
	}
	print;
}
